import ujson
from cached_property import cached_property
from peewee import Field, PostgresqlDatabase


try:
    from playhouse.postgres_ext import Json, JsonLookup
except:
    Json = JsonLookup = None


class JSONField(Field):

    def __init__(self, dumps=None, loads=None, *args, **kwargs):
        self.dumps = dumps or ujson.dumps
        self.loads = loads or ujson.loads
        super(JSONField, self).__init__(*args, **kwargs)

    @cached_property
    def db_field(self):
        if Json and isinstance(self.get_database(), PostgresqlDatabase):
            return 'json'
        return 'text'

    def db_value(self, value):
        if self.db_field == 'text':
            return self.dumps(value)

        if not isinstance(value, Json):
            return Json(value, dumps=self.dumps)

        return value

    def coerce(self, value):
        if self.db_field == 'text':
            return self.loads(value)
        return value

    def __getitem__(self, value):
        return JsonLookup(self, [value])
