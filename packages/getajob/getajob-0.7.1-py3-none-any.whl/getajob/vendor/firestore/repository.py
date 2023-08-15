import typing as t

from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.base_query import BaseQuery

from getajob.exceptions import EntityNotFound, MultipleEntitiesReturned

from .mock import MockFirestoreClient
from .client_factory import FirestoreClientFactory
from .helpers import get_list_of_parent_collections_from_dict, add_filters_to_query
from .models import (
    FirestoreDocument,
    FirestoreFilters,
    FirestoreOrderBy,
    FirestorePagination,
    FirestorePaginatedResponse,
)


class FirestoreDB:
    def __init__(
        self, client: Client | MockFirestoreClient = FirestoreClientFactory.get_client()
    ):
        self._client = client

    def disconnect(self):
        self._client.close()

    def _reset_mock(self):
        if isinstance(self._client, MockFirestoreClient):
            self._client.reset()

    def _get_collection_ref(self, parent_collections: dict, collection_name: str):
        collection_ref = self._client
        for parent, parent_id in parent_collections.items():
            collection_ref = collection_ref.collection(parent).document(parent_id)  # type: ignore
        return collection_ref.collection(collection_name)

    def _get_subcollection_ref(self, collection_name: str):
        return self._client.collection_group(collection_name)  # type: ignore

    def _verify_parent_exists(self, parent_collections: dict) -> bool | None:
        if not parent_collections:
            return None
        all_parent_collections = get_list_of_parent_collections_from_dict(
            parent_collections
        )
        for parent_collection in all_parent_collections:
            # This will raise an exception if the parent doesn't exist
            self.get(
                parent_collection.parents,
                parent_collection.collection,
                parent_collection.id,
            )
        return True

    def create(
        self,
        parent_collections: dict,
        collection_name: str,
        document_id: str,
        document_data: dict,
    ):
        self._verify_parent_exists(parent_collections)
        collection_ref = self._get_collection_ref(parent_collections, collection_name)
        doc_ref = collection_ref.document(document_id)
        doc_ref.set(document_data)
        return self.get(parent_collections, collection_name, doc_ref.id)

    def get(self, parent_collections: dict, collection_name: str, document_id: str):
        collection_ref = self._get_collection_ref(parent_collections, collection_name)
        doc_ref = collection_ref.document(document_id)
        doc = doc_ref.get()
        if not doc.exists:
            raise EntityNotFound(collection_name, document_id)
        return FirestoreDocument(id=doc.id, data=doc.to_dict() or {})

    def get_with_filters(
        self,
        parent_collections: dict,
        collection_name: str,
        document_id: str,
        filters: t.List[FirestoreFilters],
    ):
        self._verify_parent_exists(parent_collections)
        document = self.get(parent_collections, collection_name, document_id)
        for f in filters:
            if document.data.get(f.field) != f.value:
                raise EntityNotFound(collection_name, document_id)
        return document

    def update(
        self,
        parent_collections: dict,
        collection_name: str,
        document_id: str,
        document_data: dict,
    ):
        collection_ref = self._get_collection_ref(parent_collections, collection_name)
        doc_ref = collection_ref.document(document_id)
        doc_ref.set(document_data, merge=True)
        return self.get(parent_collections, collection_name, doc_ref.id)

    def delete(
        self, parent_collections: dict, collection_name: str, document_id: str
    ) -> bool:
        collection_ref = self._get_collection_ref(parent_collections, collection_name)
        doc_ref = collection_ref.document(document_id)
        collection_ref = self._get_collection_ref(parent_collections, collection_name)
        doc_ref = collection_ref.document(document_id)
        doc_ref.delete()
        return True

    def query(
        self,
        parent_collections: dict,
        collection_name: str,
        filters: t.Optional[t.List[FirestoreFilters]] = None,
        order_by: t.Optional[FirestoreOrderBy] = None,
        pagination: FirestorePagination = FirestorePagination(),
    ) -> FirestorePaginatedResponse:
        self._verify_parent_exists(parent_collections)
        query_reference = self._get_collection_ref(parent_collections, collection_name)
        return self.perform_query(
            query_reference=query_reference,  # type: ignore
            filters=filters,
            order_by=order_by,
            pagination=pagination,
        )

    def query_subcollection(
        self,
        collection_name: str,
        filters: t.Optional[t.List[FirestoreFilters]] = None,
        order_by: t.Optional[FirestoreOrderBy] = None,
        pagination: FirestorePagination = FirestorePagination(),
    ) -> FirestorePaginatedResponse:
        query_reference = self._get_subcollection_ref(collection_name)
        return self.perform_query(
            query_reference=query_reference,  # type: ignore
            filters=filters,
            order_by=order_by,
            pagination=pagination,
        )

    def get_all(
        self, parent_collections: dict, collection_name: str, items_to_get: list[str]
    ):
        self._verify_parent_exists(parent_collections)
        query_reference = self._get_collection_ref(parent_collections, collection_name)
        return query_reference.get

    def get_count_from_collection(
        self,
        parent_collections: dict,
        collection_name: str,
        filters: t.Optional[t.List[FirestoreFilters]] = None,
    ) -> int:
        self._verify_parent_exists(parent_collections)
        query_reference = self._get_collection_ref(parent_collections, collection_name)
        if filters:
            query_reference = add_filters_to_query(query_reference, filters)  # type: ignore
        return query_reference.count().get()[0][0].value  # type: ignore

    def get_count_from_subcollection(
        self,
        collection_name: str,
        filters: t.Optional[t.List[FirestoreFilters]] = None,
    ) -> int:
        query_reference = self._get_subcollection_ref(collection_name)
        if filters:
            query_reference = add_filters_to_query(query_reference, filters)
        return query_reference.count().get()[0][0].value  # type: ignore

    def perform_query(
        self,
        query_reference: BaseQuery,
        filters: t.Optional[t.List[FirestoreFilters]] = None,
        order_by: t.Optional[FirestoreOrderBy] = None,
        pagination: FirestorePagination = FirestorePagination(),
    ):
        # Apply filters, sort, and pagination
        if filters:
            query_reference = add_filters_to_query(query_reference, filters)
        if order_by:
            query_reference = query_reference.order_by(
                order_by.field, direction=order_by.direction
            )
        if pagination.start_after is not None:
            query_reference = query_reference.start_after(pagination.start_after)
        query_reference = query_reference.limit(pagination.limit)

        # Get the results
        result_stream = list(query_reference.stream())
        if len(result_stream) == 0:
            return FirestorePaginatedResponse(results=[], start_after=None)
        return FirestorePaginatedResponse(
            results=[
                FirestoreDocument(id=result.id, data=result.to_dict())  # type: ignore
                for result in result_stream
            ],
            start_after=result_stream[-1].to_dict(),
        )

    def get_one_by_attribute(
        self,
        parent_collections: dict,
        collection_name: str,
        attribute: str,
        value: str,
    ) -> FirestoreDocument:
        res = self.query(
            parent_collections=parent_collections,
            collection_name=collection_name,
            filters=[FirestoreFilters(field=attribute, operator="==", value=value)],
        )
        if len(res.results) == 1:
            return res.results[0]
        if len(res.results) > 1:
            raise MultipleEntitiesReturned(collection_name, value)
        raise EntityNotFound(collection_name, value)
