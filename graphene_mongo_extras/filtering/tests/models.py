from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField,
    StringField,
    IntField,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    ListField,
    ReferenceField,
)


class PlaythruInfo(EmbeddedDocument):
    difficulty = StringField()
    continues = IntField()


class HighScore(Document):
    player = StringField()
    score = IntField()
    recorded = DateTimeField()
    info = EmbeddedDocumentField(PlaythruInfo)
    cheats = ListField(StringField(), choices=('99 lives', 'No damage',))


class Game(Document):
    name = StringField(required=True)
    publisher = StringField()
    desc = StringField(default="No description provided")
    scores = ListField(ReferenceField(HighScore))
    options = EmbeddedDocumentListField(PlaythruInfo)
    alt_options = ListField(EmbeddedDocumentField(PlaythruInfo))
    metacritic_score = IntField()
    opencritic_score = IntField()
