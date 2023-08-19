from abc import (
    abstractmethod,
)
from collections import (
    defaultdict,
)
from operator import (
    itemgetter,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Union,
)

from educommon.utils.conversion import (
    int_or_none,
)

from edu_rdm_integration.adapters.caches import (
    WebEduEntityCache,
    WebEduFunctionCacheStorage,
    WebEduRunnerCacheStorage,
)
from edu_rdm_integration.collect_data.calculated.base.consts import (
    LOOKUP_SEP,
)
from educommon.utils.conversion import (
    int_or_none,
)

from edu_rdm_integration.collect_data.base.mixins import (
    ReformatLogsMixin,
)


class BaseCollectingCalculatedExportedDataRunnerCacheStorage(WebEduRunnerCacheStorage):
    """
    Базовый кеш помощников ранеров функций сбора расчетных данных для интеграции с "Региональная витрина данных".
    """


class BaseCollectingCalculatedExportedDataFunctionCacheStorage(ReformatLogsMixin, WebEduFunctionCacheStorage):
    """
    Базовый кеш помощников функций сбора расчетных данных для интеграции с "Региональная витрина данных".
    """

    def __init__(self, raw_logs, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Необработанные логи как есть.
        self.raw_logs = raw_logs

        # Подготовленные логи в виде:
        # {
        #     'person.person': {
        #         48939: [(1, {'surname': 'Иванов', 'snils': '157-283-394 92'...}), (2, {...})],
        #         44281: [(2, {...}), (2, {...}), ...],
        #         12600: [(3, {...})],
        #     },
        #     'schoolchild.schoolchild': {
        #         ...
        #     },
        # }
        self.logs = defaultdict(lambda: defaultdict(list))

    def _prepare_logs(self):
        """
        Подготовка логов для дальнейшей работы.
        """
        self._reformat_logs()

    @staticmethod
    def _add_id_to_set(ids: set, object_id: Union[int, str, None]) -> None:
        """Добавление значения id во множество ids."""
        object_id = int_or_none(object_id)
        if object_id:
            ids.add(object_id)

    @abstractmethod
    def _collect_product_model_ids(self):
        """Собирает идентификаторы записей моделей продукта с упором на логи."""

    @abstractmethod
    def _prepare_caches(self):
        """Формирование кэшей."""

    def _prepare(self, *args, **kwargs):
        """Запускает формирование кэша помощника Функции."""
        self._prepare_logs()
        self._collect_product_model_ids()
        self._prepare_caches()


class WebEduEntityValueCache(WebEduEntityCache):
    """Расширение базового класс для возможности получать значения из QuerySet."""

    def __init__(self, *args, values, **kwargs):
        self._values = values
        self._filters = {}
        self._filtered_entity_cache = []
        self.is_filtered = False

        self.filter_functions = {
            'range': lambda r: lambda v: r[0] <= v <= r[1],
            'in': lambda r: lambda v: v in r,
            'eq': lambda r: lambda v: v == r
        }

        super().__init__(*args, **kwargs)

    def _prepare_entities(self):
        """
        Получение выборки объектов модели по указанными параметрам.
        """
        self._entities = self._actual_entities_queryset.filter(
            **self._additional_filter_params,
        )

        if self._only_fields:
            self._entities = self._entities.only(*self._only_fields)

        if self._values:
            self._entities = self._entities.values(*self._values)

        self._entities = self._entities.distinct()

    def filter(self, **kwargs):  # noqa: A003
        """
        Установка фильтра для выборки данных.

        При повторном применении фильтра, ранее установленные параметры сбрасываются.

        Пример использования:
        some_objects_list = cache.filter(
            id__range=(1,10), elements_id__in=[1,2,3]
        ).values_list('id')
        some_objects_list => [1,5,6]

        some_objects_list = cache.filter(
            id__range=(1,10), elements_id__in=[1,2,3]
        ).values_list('id', 'elements_id')
        some_objects_list => [(1,1), (5,2), (6,3)]
        """
        self._clear_filter()

        for attr, value_filter in kwargs.items():
            lookup_attr = attr.split(LOOKUP_SEP)
            if lookup_attr[-1] in self.filter_functions:
                attr = LOOKUP_SEP.join(lookup_attr[:-1])
                lookup_value = self.filter_functions.get(lookup_attr[-1])(value_filter)
            else:
                lookup_value = self.filter_functions.get('eq')(value_filter)

            self._filters[attr] = lookup_value

        return self

    def _filtered_entities(self, entities, filters):
        """Фильтрует сущности на основании применяемых фильтров."""
        self._filtered_entity_cache = []
        if filters:
            for entity in entities:
                if all(
                    func_filter(entity.get(attr)) for attr, func_filter in filters.items()
                ):
                    self._filtered_entity_cache.append(entity)
        else:
            self._filtered_entity_cache = entities

    def _get_filter(self) -> Dict[str, Callable[..., Any]]:
        """Возвращает наименование атрибута и фильтр по нему."""
        return self._filters

    def _clear_filter(self):
        """Сброс примененных фильтров и очистка кеша."""
        self.is_filtered = False
        self._filtered_entity_cache = []
        self._filters = {}

    def values_list(self, *args, **kwargs) -> Optional[List[Any]]:
        """
        Получение списка кортежей или значений согласно заданным параметрам фильтрации.

        Пример использования:
        some_objects_list = cache.filter(
            id__range=(1,10), elements_id__in=[1,2,3]
        )
        some_objects_list = some_objects_list.values_list('id', 'elements_id')
        some_objects_list => [(1,1), (5,2), (6,3)]
        """
        if not self.is_filtered:
            self._filtered_entities(self._entities, self._get_filter())
            self.is_filtered = True

        fields_getter = itemgetter(*args)

        return [fields_getter(entity) for entity in self._filtered_entity_cache]

    def exists(self) -> bool:
        """
        Проверка существования отфильтрованных данных.

        Кеширует результат фильтрации данных, для исключения повторного прохода.
        """
        if not self.is_filtered:
            self._filtered_entities(self._entities, self._get_filter())
            self.is_filtered = True

        return bool(self._filtered_entity_cache)
