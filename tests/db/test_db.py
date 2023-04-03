from uuid import UUID

import marshmallow as marsh
from peewee import IntegerField

from src.base_model import BaseModel, db


class ModelTest(BaseModel):
    """Model for testing purposes"""

    class Schema(BaseModel.Schema):
        """Schema for testing purposes"""

        test_value = marsh.fields.Integer(required=True)

        def _make(self, data: dict) -> "ModelTest":
            return ModelTest(**data)

    test_value = IntegerField()

    def __init__(self, test_value, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.test_value = test_value


class TestDB:
    """Test the database connection and the serialization/deserialization"""

    def setup_method(self):
        db.create_tables([ModelTest])

    def teardown_method(self):
        db.drop_tables([ModelTest])

    def test_db_connection_workflow(self):
        # I just wanted to test if the db is working
        ModelTest.create(test_value=1).save()
        test_obj = ModelTest.select().where(ModelTest.test_value == 1).first()
        assert test_obj.test_value == 1

    def test_serialization(self):
        # I just wanted to test if the serialization is working
        test_obj = ModelTest(test_value=1)
        assert test_obj.to_dict() == {"id": str(test_obj.id), "test_value": 1}

    def test_deserialization(self):
        # I just wanted to test if the deserialization is working
        test_obj = ModelTest.Schema().load({"test_value": 1})
        assert test_obj.test_value == 1
        assert isinstance(test_obj.id, UUID)
