from datetime import datetime
from uuid import UUID

import marshmallow as marsh
from peewee import IntegerField

from src.base_model import BaseModel, SerializableBaseModel, db
from tests.decorators import recreate_db_setup


class ModelTest(SerializableBaseModel):
    """Model for testing purposes"""

    test_value = IntegerField()

    def __init__(self, test_value, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.test_value = test_value

    def to_dict(self):
        data = super().to_dict()
        return {"test_value": self.test_value, **data}


class TestDB:
    """Test the database connection and the serialization/deserialization"""

    @recreate_db_setup
    def setup_method(self):
        db.create_tables([ModelTest])

    def teardown_method(self):
        db.drop_tables([ModelTest])

    def test_db_connection_workflow(self):
        # I just wanted to test if the db is working
        ModelTest(test_value=1).save()
        test_obj = ModelTest.select().where(ModelTest.test_value == 1).first()
        assert test_obj.test_value == 1

    def test_serialization(self):
        # I just wanted to test if the serialization is working
        test_obj = ModelTest(test_value=1)
        assert {
            "id": str(test_obj.id),
            "updated_at": str(test_obj.updated_at),
            "created_at": str(test_obj.created_at),
            "test_value": 1,
        }.items() == test_obj.to_dict().items()

    def test_created_at(self):
        start_datetime = datetime.now()
        test_obj = ModelTest(test_value=1)
        end_datetime = datetime.now()
        created_at = test_obj.created_at
        assert start_datetime <= created_at <= end_datetime

    def test_updated_at(self):
        start_datetime = datetime.now()
        test_obj = ModelTest(test_value=1)
        mid_datetime = datetime.now()
        test_obj.save()
        end_datetime = datetime.now()
        created_at = test_obj.created_at
        updated_at = test_obj.updated_at
        assert (
            start_datetime <= created_at <= mid_datetime <= updated_at <= end_datetime
        )
