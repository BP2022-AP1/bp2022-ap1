from uuid import UUID

import pytest

from src.implementor.models import Run


class TestImplementorModelsRun:
    """Test the run table and the serialization/deserialization"""

    @pytest.fixture
    def run_as_dict(self):
        """Run as dict with all fields set."""
        return {}

    def test_create(self, run_as_dict):
        """Test that a run can be created."""
        run = Run.create(**run_as_dict)
        assert Run.select().where(Run.id == run.id).first() == run

    def test_serialization(self, run_as_dict):
        """Test that a run can be serialized."""
        run = Run.create()
        assert run.to_dict() == {"id": str(run.id), **run_as_dict}

    def test_deserialization(self, run_as_dict):
        """Test that a run can be deserialized."""
        run = Run.Schema().load(run_as_dict)
        assert isinstance(run, Run)
        assert isinstance(run.id, UUID)
