from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, ContentType

from datagrowth.datatypes import CollectionBase, DocumentCollectionMixin, DocumentBase, DocumentPostgres


class Collection(DocumentCollectionMixin, CollectionBase):

    community = GenericForeignKey(ct_field="community_type", fk_field="community_id")
    community_type = models.ForeignKey(ContentType, related_name="+", on_delete=models.PROTECT)
    community_id = models.PositiveIntegerField()

    def init_document(self, data, collection=None):
        Document = self.get_document_model()
        return Document(
            community=self.community,
            collection=collection,
            schema=self.schema,
            properties=data
        )


class Document(DocumentPostgres, DocumentBase):

    community = GenericForeignKey(ct_field="community_type", fk_field="community_id")
    community_type = models.ForeignKey(ContentType, related_name="+", on_delete=models.PROTECT)
    community_id = models.PositiveIntegerField()

    def to_search(self):
        content = " ".join(partial for partial in self.properties["content"] if partial)
        return {
            "_id": self.id,
            "title": self.properties["title"],
            "title_plain": self.properties["title"],
            "argument_score": float(self.properties.get("argument_score", 0.0001)),
            "url": self.properties["url"],
            "author": self.properties["author"],
            "source": self.properties["source"],
            "content": content,
            "content_plain": content
        }
