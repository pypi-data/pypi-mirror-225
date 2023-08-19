from collections import (
    defaultdict,
)
from datetime import (
    date,
    datetime,
    time,
    timedelta,
)
from typing import (
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Type,
)

from django.conf import (
    settings,
)
from django.db.models import (
    F,
    Max,
    Model,
)
from django.utils import (
    timezone,
)
from django.utils.datastructures import (
    OrderedSet,
)

from educommon import (
    logger,
)
from educommon.utils.date import (
    get_today_min_datetime,
)
from function_tools.managers import (
    RunnerManager,
)
from m3_db_utils.consts import (
    DEFAULT_ORDER_NUMBER,
)
from m3_db_utils.models import (
    ModelEnumValue,
)

from edu_rdm_integration.consts import (
    REGIONAL_DATA_MART_INTEGRATION_EXPORTING_DATA,
)
from edu_rdm_integration.models import (
    ExportingDataSubStage,
    ExportingDataSubStageStatus,
    RegionalDataMartEntityEnum,
)
from edu_rdm_integration.signals import (
    manager_created,
)
from edu_rdm_integration.storages import (
    RegionalDataMartEntityStorage,
)


class BaseExportEntitiesData:
    """Базовый класс экспорта сущностей РВД за указанных период."""

    def __init__(
        self,
        entities: Iterable[str],
        period_started_at=datetime.combine(date.today(), time.min),
        period_ended_at=datetime.combine(date.today(), time.min),
        **kwargs,
    ):
        # Если сущности не указаны, берется значение по умолчанию - все сущности:
        entities = entities if entities else RegionalDataMartEntityEnum.get_enum_data().keys()
        self.entities: List[ModelEnumValue] = [
            RegionalDataMartEntityEnum.get_model_enum_value(entity) for entity in entities
        ]

        self.period_started_at = period_started_at
        self.period_ended_at = period_ended_at

        # Классы менеджеров Функций, которые должны быть запущены для выгрузки данных
        self._exporting_data_managers: Set[Type[RunnerManager]] = set()

        # Результаты работы Функций выгрузки данных
        self._exporting_data_results = []

        # Идентификатор CollectDataCommandProgress для передачи сигналу manager_created
        self.command_id: Optional[int] = kwargs.get('command_id')

        self._configure_agent_client()

    def _configure_agent_client(self):
        """
        Конфигурирование клиента загрузчика данных в Витрину.

        #TODO Вынужденная мера, т.к. при запуске команды не производится проверка готовности конфигов приложений.
          # Нужно переработать механизм конфигурирования клиента загрузчика.
        """
        import uploader_client
        from uploader_client.contrib.rdm.interfaces.configurations import (
            RegionalDataMartUploaderConfig,
        )
        if settings.RDM_UPLOADER_CLIENT_ENABLE_REQUEST_EMULATION:
            uploader_client.set_config(
                RegionalDataMartUploaderConfig(
                    interface='uploader_client.contrib.rdm.interfaces.rest.OpenAPIInterfaceEmulation',
                    url=settings.RDM_UPLOADER_CLIENT_URL,
                    datamart_name=settings.RDM_UPLOADER_CLIENT_DATAMART_NAME,
                    timeout=1,
                    request_retries=1,
                )
            )
        else:
            uploader_client.set_config(
                RegionalDataMartUploaderConfig(
                    url=settings.RDM_UPLOADER_CLIENT_URL,
                    datamart_name=settings.RDM_UPLOADER_CLIENT_DATAMART_NAME,
                    timeout=settings.RDM_UPLOADER_CLIENT_REQUEST_TIMEOUT,
                    request_retries=settings.RDM_UPLOADER_CLIENT_REQUEST_RETRIES,
                )
            )

    def _fill_manager_entities_map(self, entity_storage: RegionalDataMartEntityStorage) -> None:
        """
        Заполнение словаря данных с классами менеджеров и их сущностями.
        """

    def _find_exporting_entities_data_managers(self):
        """
        Поиск менеджеров Функций выгрузки данных по сущностям РВД.
        """
        logger.info('find exporting entities data manager..')

        entity_storage = RegionalDataMartEntityStorage()
        entity_storage.prepare()

        exporting_entities_data_managers_map = entity_storage.prepare_entities_manager_map(
            tags={REGIONAL_DATA_MART_INTEGRATION_EXPORTING_DATA},
        )
        self._fill_manager_entities_map(entity_storage)

        entities = filter(lambda entity: entity.order_number != DEFAULT_ORDER_NUMBER, self.entities)

        for entity_enum in entities:
            manager_class = exporting_entities_data_managers_map.get(entity_enum.key)

            if manager_class:
                self._exporting_data_managers.add(manager_class)

        logger.info('finding exporting entities data manager finished.')

    def _export_entities_data(self, *args, **kwargs):
        """
        Выгрузка данных по указанным сущностям.
        """
        logger.info('start exporting entities data..')

        kwargs['period_started_at'] = self.period_started_at
        kwargs['period_ended_at'] = self.period_ended_at

        for manager_class in self._exporting_data_managers:
            manager = manager_class(*args, is_only_main_model=True, **kwargs)

            if self.command_id:
                # Подается сигнал, что менеджер создан:
                manager_created.send(sender=manager,
                                     command_id=self.command_id)

            manager.run()

            self._exporting_data_results.append(manager.result)

        logger.info('exporting entities data finished.')

    def export(self, *args, **kwargs):
        """
        Выполнение действий команды.
        """
        logger.info(
            f'start exporting data of entities - {", ".join([entity.key for entity in self.entities])}..'
        )

        self._find_exporting_entities_data_managers()
        self._export_entities_data(*args, **kwargs)

        logger.info('exporting entities data finished.')


class BaseExportLatestEntitiesData(BaseExportEntitiesData):
    """Базовый класс выгрузки сущностей с момента последней успешной выгрузки."""

    def __init__(
        self,
        entities: Iterable[str],
        period_started_at=datetime.combine(date.today(), time.min),
        period_ended_at=datetime.combine(date.today(), time.min),
        **kwargs,
    ):
        super().__init__(entities, period_started_at, period_ended_at, **kwargs)

        self._exporting_data_managers: Set[Type[RunnerManager]] = OrderedSet()

        # Словарь данных с классами менеджеров и их сущностями
        self._manager_entities_map: Dict[Type[object], List[str]] = defaultdict(set)

        self.async_task = self._get_async_task()
        self.task_id = kwargs.get('task_id')

    def _get_async_task(self) -> Model:
        """Возвращает модель асинхронной задачи."""
        raise NotImplementedError

    def _set_description_to_async_task(self, exported_entities: Iterable[str]) -> None:
        """Добавляет в описание асинхронной задачи список выгруженных сущностей."""
        if exported_entities and self.task_id:
            self.async_task.objects.filter(
                task_id=self.task_id,
            ).update(
                description=F('description') + f': {", ".join(exported_entities)}',
            )

    def _fill_manager_entities_map(self, entity_storage: RegionalDataMartEntityStorage) -> None:
        """
        Заполнение словаря данных с классами менеджеров и их сущностями.
        """
        self._manager_entities_map = entity_storage.prepare_manager_entities_map(
            tags={REGIONAL_DATA_MART_INTEGRATION_EXPORTING_DATA},
        )

    def _get_last_finished_entity_export(self) -> Dict[str, datetime]:
        """
        Возвращает словарь с uuid менеджера и датой последнего успешного экспорта по указанным сущностям.
        """
        manager_to_last_date = ExportingDataSubStage.objects.annotate(
            max_period_ended_at=Max('stage__period_ended_at'),
        ).values(
            'stage__manager_id', 'max_period_ended_at',
        ).annotate(
            manager_id=F('stage__manager_id'),
            date_end=F('max_period_ended_at'),
        ).filter(
            status_id=ExportingDataSubStageStatus.FINISHED.key,
            manager_id__in=[m.uuid for m in self._exporting_data_managers],
        ).values('manager_id', 'date_end')

        return {str(m['manager_id']): m['date_end'] for m in manager_to_last_date}

    def _export_entities_data(self, *args, **kwargs) -> None:
        """
        Запуск Функций по для экспорта данных.
        """
        logger.info('export entities data..')

        # Массив с выгружаемыми сущностями для поля "Описание" в асинхронной задаче
        exported_entities = []

        last_finished_entity_export = self._get_last_finished_entity_export()

        for manager_class in self._exporting_data_managers:
            kwargs['period_started_at'] = (
                    last_finished_entity_export.get(manager_class.uuid)
                    or get_today_min_datetime()
            )
            kwargs['period_ended_at'] = timezone.now()

            if kwargs['period_started_at'] > kwargs['period_ended_at']:
                kwargs['period_started_at'] = kwargs['period_ended_at'] - timedelta(
                    seconds=settings.RDM_TRANSFER_TASK_TIMEDELTA
                )

            manager = manager_class(*args, **kwargs)

            if self.command_id:
                # Подается сигнал, что менеджер создан:
                manager_created.send(sender=manager,
                                     command_id=self.command_id)

            manager.run()

            self._exporting_data_results.append(manager.result)

            # Если сущность была выгружена, то добавим ее в список exported_entities
            if manager.result.entities and self.task_id:
                exported_entities.extend(self._manager_entities_map.get(manager_class))

        self._set_description_to_async_task(exported_entities)

        logger.info('collecting entities data finished.')


class ExportEntitiesData(BaseExportEntitiesData):
    """Экспорт сущностей РВД за указанных период."""
