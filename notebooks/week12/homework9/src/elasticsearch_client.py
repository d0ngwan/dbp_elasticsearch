from elasticsearch import Elasticsearch, helpers
from src.configuration import Configuration


class ElasticsearchClient:
    def __init__(self):
        self.config = Configuration().get_config('elasticsearch')
        self.client = self.connect_to_elastic()

    def connect_to_elastic(self) -> Elasticsearch:
        client = Elasticsearch(
            f"{self.config['host']}:{self.config['port']}",
            ca_certs=self.config['ca_cert'],
            basic_auth=(self.config['username'], self.config['password']),
            request_timeout=120,
        )
        return client

    def create_index(self, index_name: str, mapping: dict) -> None:
        if not self.client.indices.exists(index=index_name):
            self.client.indices.create(index=index_name, mappings={"properties": mapping})

    def insert_one_document(self, index_name: str, body: dict, doc_id=None) -> None:
        response = self.client.index(index=index_name, id=doc_id, document=body)

    def get_document(self, index_name: str, doc_id: int) -> dict:
        response = self.client.get(index=index_name, id=doc_id)
        return response['_source']

    def update_document_by_id(self, index_name: str, doc_id: int, body: dict) -> None:
        response = self.client.update(index=index_name, id=doc_id, doc=body)

    def delete_index(self, index_name: str) -> None:
        self.client.options(ignore_status=[404]).indices.delete(index=index_name)

    def delete_document(self, index_name: str, doc_id: int) -> None:
        response = self.client.delete(index=index_name, id=doc_id)

    def search(self, query: dict, index_name: str) -> list:
        result = self.client.search(index=index_name, body=query)
        return result['hits']['hits']

    def count(self, index_name: str) -> int:
        self.client.indices.refresh(index=index_name)
        result = self.client.count(index=index_name)
        return result['count']

    def scan_index(self, index_name: str, query: dict, size: int, scroll='2m') -> list:
        response = helpers.scan(self.client, index=index_name, query=query,
                                size=size, scroll=scroll)
        for doc in response:
            yield doc['_source']

    def bulk_request(self, actions: list = None, chunk_size: int = 500):
        return helpers.bulk(self.client, actions, chunk_size=chunk_size,
                            raise_on_error=False)
