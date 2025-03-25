from alliance_mediacheck.orm.alliance_mediacheck import ExampleTable

from sqlalchemy.orm import configure_mappers
from formshare.models.schema import initialize_schema

configure_mappers()


def includeme(config):
    initialize_schema()
