import os
import csv
import requests
import json
import traceback


class Extract:


    TO_JSON = lambda data: json.dumps(data).encode('utf-8')
    FROM_JSON = lambda data: json.loads(data.decode('utf-8'))


    def __init__(self) -> None:
        self
    
    def __str__(self) -> str:
        return str(self.__dict__)
    
    
    def downloadCSVFromURL(self,
            url: str,
            path: str,
            filename: str,
            overwrite: bool=False
            ):
        try:
            with requests.get(url) as response:
                if response.status_code == 200:
                    
                    if filename.find('.csv') == (-1):
                        path = os.path.join(path, f'{filename}.csv')
                    else:
                        path = os.path.join(path, f'{filename}')

                    content = response.content
                    if not os.path.exists(path) \
                            or (os.path.exists(path) and overwrite):
                        with open(path, 'wb') as file:
                            file.write(content)
                    
                    return True

            return False
        except Exception: #noqa
            return False

    @classmethod
    def getCSVFromURL(cls,
            url: str,
            method: str='GET'
            ):
        try:
            if method == 'GET':

                with requests.Session() as session:
                    download = session.get(url)
                    content = download.content.decode('utf-8')
                    csv_file = csv.reader(
                        content.splitlines(),
                        delimiter=','
                    )
                return list(csv_file)

            return False
        except Exception: #noqa
            return False
    
    @classmethod
    def readCSV(cls,
            filename,
            path: str='',
            header: bool=True
            ):
        try:
            path = path if path else os.getcwd()

            if filename.find('.csv') == (-1):
                path = os.path.join(path, f'{filename}.csv')
            else:
                path = os.path.join(path, f'{filename}')
            
            if os.path.exists(path):
                response = {}
                with open(path, 'r') as file:
                    csv_file = csv.reader(
                        file,
                        delimiter=','
                    )
                    for index, row in enumerate(csv_file):
                        response[index] = row
                if header:
                    response['header'] = response[0]
                    del(response[0])
                return response
            
            return False

        except Exception: #noqa
            return False

