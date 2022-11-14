from dynamorm import DynaModel
from marshmallow import fields
from typlesss.settings import DB_ENDPOINT, DB_TABLE
from datetime import date


class Documents(DynaModel):
    # Define properties
    class Table:
        resource_kwargs = {
            'endpoint_url': DB_ENDPOINT
        }
        name = DB_TABLE
        hash_key = 'number'
        read = 25
        write = 5

    # Define our data schema, each property here will become a property on instances of the Document
    class Schema:
        number = fields.String(required=True)
        date = fields.Date()
        type = fields.String()
