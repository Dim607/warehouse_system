from flask import Flask
from pymongo.database import Database 
from pymongo.collection import Collection


class CustomFlask(Flask):
    db: Database
    admin_collection: Collection
    unit_collection: Collection
    employee_collection: Collection
    supervisor_collection: Collection
    admin_collection: Collection
    product_collection: Collection

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

