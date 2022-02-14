from psycopg2 import connect as connector_postgres


class Settings:
    
    class ENGINES:

        POSTGRES = dict(
            connector=connector_postgres,
            host='localhost',
            port=5432,
            user='postgres',
            password=None,
            database=None
        )

