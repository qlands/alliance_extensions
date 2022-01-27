from alliance_cgcore.orm.alliance_cgcore import ExampleTable

from sqlalchemy.orm import configure_mappers
from formshare.models.schema import initialize_schema

configure_mappers()


def includeme(config):
    initialize_schema()
