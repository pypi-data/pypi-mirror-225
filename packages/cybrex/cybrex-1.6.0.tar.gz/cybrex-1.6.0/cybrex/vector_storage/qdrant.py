import uuid
from typing import List

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, Filter, FieldCondition, MatchValue, PointStruct, Range, VectorParams

from .base import BaseVectorStorage


class QdrantVectorStorage(BaseVectorStorage):
    def __init__(self, url, collection_name, embedding_function):
        self.db = QdrantClient(url=url)
        self.collection_name = collection_name
        self.embedding_function = embedding_function
        self.db.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        self.db.create_payload_index(
            collection_name=collection_name,
            field_name="document_id",
            field_schema="keyword",
        )

    def get_by_field_value(self, field, value) -> List[dict]:
        points, _ = self.db.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                should=[
                    FieldCondition(
                        key=field,
                        match=MatchValue(value=value)
                    ),
                ],
            ),
        )
        return [point.payload for point in points]

    def query(self, query_embedding, n_chunks: int, where: dict = None):
        query_filter = None
        if where:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key=k,  # Condition based on values of `rand_number` field.
                        range=Range(
                            gte=v,
                            lte=v
                        )
                    ) for k, v in where.items()
                ]
            )
        points = self.db.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            query_filter=query_filter,
            limit=n_chunks,
        )
        return [{**point.payload, 'score': point.score} for point in points]

    def upsert(self, chunks: List[dict]):
        embeddings = self.embedding_function([
            chunk['text']
            for chunk in chunks
        ])
        return self.db.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=str(uuid.uuid1()),
                    vector=embedding,
                    payload=chunk
                )
                for chunk, embedding in zip(chunks, embeddings)
            ]
        )
