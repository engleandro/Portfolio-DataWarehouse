

class Connector:
    
    @classmethod
    def connectToRelationalDatabase(cls, settings: dict):
        connector = settings['connector']
        credentials = dict(
            host=settings['host'],
            port=settings['port'],
            user=settings['user'],
            password=settings['password'],
            database=settings['database']
        )
        return connector(**credentials)
    
    @classmethod
    def querySelectFrom(cls, connector, query):
        cursor = connector.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
    @classmethod
    def queryInsertInto(cls, connector, query):
        try:
            cursor = connector.cursor()
            cursor.execute(query)
            return True
        except:
            cursor.rollback()
            return False


