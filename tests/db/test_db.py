from peewee import IntegerField

from src.base_model import BaseModel, db


class ModelTest(BaseModel):
    """Model for testing purposes
    """
    test_value = IntegerField()


def test_db():
    # I just wanted to test if the db is working
    db.create_tables([ModelTest])
    ModelTest.create(test_value=1).save()
    test_obj = ModelTest.select().where(ModelTest.test_value == 1).first()
    assert test_obj.test_value == 1
