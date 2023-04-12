import inspect
import pkgutil
from types import ModuleType
from typing import Iterator

from src.base_model import BaseModel
from src.constants import tables
from tests.decorators import recreate_db_setup


class TestTables:
    """Test whether all classes that inherit from BaseModel
    are in src.constants.tables
    """

    SOURCE_PATH: list[str] = [".", "src"]

    def load_and_get_all_source_modules(self) -> Iterator[ModuleType]:
        # iterate over all modules in the src directory
        return (
            loader.find_module(module_name)
            for loader, module_name, _ in pkgutil.walk_packages(self.SOURCE_PATH)
        )

    def get_all_model_classes(self) -> Iterator[type]:
        # iterate over all stuff in all modules
        for module in self.load_and_get_all_source_modules():
            for _, obj in inspect.getmembers(module):
                # if the stuff is a class and inherits from BaseModel,
                # yield it
                if inspect.isclass(obj) and issubclass(obj, BaseModel):
                    yield obj

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_tables_complete(self):
        for model_class in self.get_all_model_classes():
            assert model_class in tables
