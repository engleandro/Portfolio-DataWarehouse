from warehouse.settings import Settings
from warehouse.enum import Enum
from warehouse.connector import Connector
from warehouse.extract import Extract
from warehouse.transform import Transform
from warehouse.load import Load


class DataWarehouse(Settings):

    Enum = Enum
    Connector = Connector
    Extract = Extract
    Transform = Transform
    Load = Load

