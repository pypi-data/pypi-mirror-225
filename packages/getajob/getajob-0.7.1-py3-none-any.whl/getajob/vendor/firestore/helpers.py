import typing as t
from google.cloud.firestore_v1.base_query import BaseQuery

from .models import FirestoreFilters, ParentAndCollection


def add_filters_to_query(query_reference: BaseQuery, filters: t.List[FirestoreFilters]):
    for _filter in filters:
        if _filter.operator == "like":
            query_reference = query_reference.where(
                _filter.field, ">=", _filter.value
            ).where(_filter.field, "<=", _filter.value + "\uf8ff")
        else:
            query_reference = query_reference.where(
                _filter.field, _filter.operator, _filter.value
            )
    return query_reference


def get_list_of_parent_collections_from_dict(
    input_dict: dict,
) -> t.List[ParentAndCollection]:
    output_list = []
    parent_dict: t.Dict[str, str] = {}
    for key in input_dict:
        parent_dict_copy = parent_dict.copy()
        output_list.append(
            ParentAndCollection(
                parents=parent_dict_copy, collection=key, id=input_dict[key]
            )
        )
        parent_dict[key] = input_dict[key]
    return output_list
