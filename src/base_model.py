from peewee import Model, PostgresqlDatabase


db: PostgresqlDatabase = PostgresqlDatabase(database="postgres",user="postgres",password="root",host="localhost")


class BaseModel(Model):
    """All model classes have to inherit from this base class.
    """
    class Meta:
        """Set Database
        """
        database = db

    @classmethod
    def from_dict(cls, data: dict) -> 'BaseModel':
        """constructs a model object from a dictionary.

        :param data: the dictionary
        :return: an instance of the model
        """
        return cls.Schema().load(data)

    def to_dict(self) -> dict:
        """serializes the model object to a dictionary.

        :return: the dictionary
        """
        return self.Schema().dump(self)
