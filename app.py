import os
from time import sleep
from datetime import datetime, timedelta, timezone
import csv
import json
import requests
import traceback
import threading
from pprint import pprint

from dotenv import load_dotenv

from warehouse import custom_logging
from warehouse import DataWarehouse


load_dotenv('./setup/.env[MODEL]')


def DataProcesser(args: list=[], kwargs: dict={}):
    #warehouse = DataWarehouse(*args, **kwargs)
    return True


#[BUILD DATABASE]

class DatabaseETL():

    
    URLs = {
        "payments": 'https://docs.google.com/spreadsheets/d/1j_2LLIoJqO3B0eqMjhBFwWldFDiXWrcdxM7vArM0oQw/edit?usp=sharing',
        "plans": 'https://docs.google.com/spreadsheets/d/18DM7zBC0wZoyb3VIRgJ4l3lS8ty8OO0tJD2saQjYkA8/edit?usp=sharing'
    }
    APIs = {
        "customer": 'https://demo4461965.mockable.io/clientes'
    }
    ENDPOINTs = {
        "plan": "http://127.0.0.1:8000/financial/plan/",
        "customer": "http://127.0.0.1:8000/financial/customer/",
        "date": "http://127.0.0.1:8000/financial/date/",
        "payment": "http://127.0.0.1:8000/financial/payment/"
    }


    def __init__(self, logger) -> None:
        self.start = datetime.now()
        self.batch_start = self.start
        self.batch_size = 500
        self.batch_frequency = timedelta(days=1)
        self.batch_wait_time = 3600/100
        self.speed_start = self.start
        self.speed_size = 100
        self.speed_frequency = timedelta(hours=1)
        self.speed_wait_time = 60/10
        self.connector = self.setConnection()
        self.timeout = 30
        self.logger = logger


    #[CONNECT-WAREHOUSE]

    def setConnection(self):
        try:
            credentials = DataWarehouse.ENGINES.POSTGRES
            credentials['host'] = os.environ.get('DB_SQL_HOSTNAME')
            credentials['port'] = int(os.environ.get('DB_SQL_PORT'))
            credentials['user'] = os.environ.get('DB_SQL_USERNAME')
            credentials['password'] = os.environ.get('DB_SQL_PASSWORD')
            credentials['database'] = os.environ.get('DB_SQL_INITDB')
            connector = DataWarehouse.Connector.connectToRelationalDatabase(
                credentials
            )
            return connector
        except:
            cursor = connector.cursor()
            cursor.rollback()
            self.logger.debug(traceback.format_exc())

    
    #[PLANS]

    def extractPlans(self,
            url: str="",
            path: str="lake/raw",
            csv_file: str="planos.csv"
            ) -> dict:
        try:
            plans = DataWarehouse.Extract.readCSV(
                path=os.path.join(os.getcwd(), path),
                filename=csv_file
            )
            return plans
        except Exception: #noqa
            self.logger.debug(traceback.format_exc())
    
    def transformPlans(self, plans: dict, url: str="") -> list:
        try:
            if not plans:
                plans = self.extractCustomers(url=url)
            response = list()
            for key, value in plans.items():
                if key == 'header':
                    continue
                document = dict()
                for index in range(len(value)):
                    if value[index].isnumeric():
                        document[plans['header'][index].lower()] = float(value[index])
                    else:
                        document[plans['header'][index].lower()] = value[index].lower()
                response.append(document)
            return response
        except Exception: #noqa
            self.logger.debug(traceback.format_exc())
    
    def loadPlans(self, dataset, url: str=""):
        try:
            if not dataset:
                dataset = self.transformCustomers(url=url)
            for document in dataset:
                with requests.post(
                        self.ENDPOINTs.get('plan'),
                        json=document
                        ) as response:
                    if response.status_code == 200:
                        continue
                    else:
                        print(
                            response.status_code,
                            response.reason
                        )
        except Exception: #noqa
            self.logger.debug(traceback.format_exc())
    
    def getPlans(self, plan_id: int=None):
        try:
            if plan_id:
                response = json.loads(
                    requests.get(
                        f"{self.ENDPOINTs.get('plan')}{plan_id}/"
                    ).content.decode('utf-8')
                )
            else:
                response = json.loads(
                    requests.get(
                        self.ENDPOINTs.get('plan')
                    ).content.decode('utf-8')
                )
            return response
        except Exception: #noqa
            self.logger.debug(traceback.format_exc())

    def buildPlans(self) -> bool:
        try:
            plans = self.extractPlans()
            print(plans)
            payload = self.transformPlans(plans)
            self.loadPlans(dataset=payload)
            return True
        except Exception:
            self.logger.debug(traceback.format_exc())
            return False
    
    
    #[CUSTOMERS]

    def extractCustomers(self, url: str="") -> dict:
        try:
            if url:
                URL = url
            else:
                URL = self.APIs.get("customer")
            with requests.get(URL) as response:
                if response.status_code == 200:
                    customers = json.loads(
                        response.content.decode('utf-8')
                    )
            #return customers
            response = {}
            for index, customer in enumerate(customers):
                response[index+1] = customer
            return response
        except Exception: #noqa
            self.logger.debug(traceback.format_exc())
    
    def transformCustomers(self,
            customers,
            url: str=""
            ) -> list:
        try:
            if not customers:
                customers = self.extractCustomers(url=url)
            response = list()
            #for customer in customers:
            for key, customer in customers.items():
                customers[key]['id'] = customer.get('id') + 1
                response.append(customers[key])
            return response
        except Exception: #noqa
            self.logger.debug(traceback.format_exc())

    def loadCustomers(self, dataset, url: str="") -> None:
        try:
            if not dataset:
                dataset = self.transformCustomers(url=url)
            for document in dataset:
                with requests.post(
                        self.ENDPOINTs.get('customer'),
                        json=document
                        ) as response:
                    if response.status_code == 200:
                        continue
                    else:
                        print(
                            response.status_code,
                            response.reason
                        )
        except Exception: #noqa
            self.logger.debug(traceback.format_exc())
    
    def getCustomers(self, customer_id: int=None):
        try:
            if customer_id:
                response = json.loads(
                    requests.get(
                        f"{self.ENDPOINTs.get('customer')}{customer_id}/"
                    ).content.decode('utf-8')
                )
            else:
                response = json.loads(
                    requests.get(
                        self.ENDPOINTs.get('customer')
                    ).content.decode('utf-8')
                )
            return response
        except Exception: #noqa
            self.logger.debug(traceback.format_exc())
    
    def buildCustomers(self) -> bool:
        try:
            customers = self.extractCustomers()
            payload = self.transformCustomers(customers)
            self.loadCustomers(dataset=payload)
            return True
        except Exception:
            self.logger.debug(traceback.format_exc())
            return False


    #[DATES]

    def extractDates(self,
            url: str="",
            path: str="lake/raw",
            csv_file: str="pagamentos.csv"
            ) -> dict:
        try:
            dates = DataWarehouse.Extract.readCSV(
                path=os.path.join(os.getcwd(), path),
                filename=csv_file
            )
            distinct_dates = list(
                set([register[1] for _, register in dates.items()])
            )
            for data in distinct_dates:
                if len(data.split('/')) == 1:
                    distinct_dates.remove(data)
            dates = {}
            for index, date in enumerate(distinct_dates):
                dates[index] = date
            dates["header"] = "data_pagamento"
            return dates
        except Exception: #noqa
            self.logger.debug(traceback.format_exc())
    
    def transformDates(self, dates, url: str="") -> list:
        try:
            if not dates:
                dates = self.extractDates(url=url)
            
            for index, register in dates.items():
                if index == "header":
                    continue
                date_info = [int(value) for value in register.split('/')]
                dates[index] = [
                    index,
                    f"{date_info[2]}-{date_info[1]}-{date_info[0]}",
                    date_info[1],
                    date_info[-1]
                ]
            dates['header'] = ['id', 'data', 'mes', 'ano']

            response = list()
            for key, value in dates.items():
                if key == 'header':
                    continue
                document = dict()
                for index in range(len(value)):
                    if isinstance(value[index], int):
                        document[dates['header'][index].lower()] = int(value[index])
                    elif isinstance(value[index], float):
                        document[dates['header'][index].lower()] = float(value[index])
                    elif value[index].isnumeric():
                        document[dates['header'][index].lower()] = float(value[index])
                    else:
                        document[dates['header'][index].lower()] = value[index].lower()
                response.append(document)
            
            return response
        except Exception: #noqa
            self.logger.debug(traceback.format_exc())

    def loadDates(self, dataset, url: str="") -> None:
        try:
            if not dataset:
                dataset = self.transformDates(url=url)
            for document in dataset:
                with requests.post(
                        self.ENDPOINTs.get('date'),
                        json=document
                        ) as response:
                    if response.status_code == 200:
                        continue
                    else:
                        print(
                            response.status_code,
                            response.reason
                        )
        except Exception: #noqa
            self.logger.debug(traceback.format_exc())
    
    def getDates(self, date_id: int=None) -> list:
        try:
            if date_id:
                response = json.loads(
                    requests.get(
                        f"{self.ENDPOINTs.get('date')}{date_id}/"
                    ).content.decode('utf-8')
                )
            else:
                response = json.loads(
                    requests.get(
                        self.ENDPOINTs.get('date')
                    ).content.decode('utf-8')
                )
            return response
        except Exception: #noqa
            self.logger.debug(traceback.format_exc())
    
    def buildDates(self) -> bool:
        try:
            dates = self.extractDates()
            payload = self.transformDates(dates)
            self.loadDates(dataset=payload)
            return True
        except Exception:
            self.logger.debug(traceback.format_exc())
            return False


    #[PAYMENTS]

    def extractPayments(self,
            url: str="",
            path: str="lake/raw",
            csv_file: str="pagamentos.csv"
            ) -> dict:
        try:
            payments = DataWarehouse.Extract.readCSV(
                path=os.path.join(os.getcwd(), path),
                filename=csv_file
            )
            return payments
        except Exception: #noqa
            self.logger.debug(traceback.format_exc())
    
    def transformPayments(self, payments, url: str="") -> list:
        try:
            if not payments:
                payments = self.extractPayments(url=url)
            
            registers = [
                [key, value] for key, value in payments.items()
            ]

            customers = self.extractCustomers()
            for index, register in registers:
                if index == "header":
                    continue
                customer_id = int(register[0])
                for _, customer in customers.items():
                    if customer.get('id') == customer_id:
                        customer = customer
                payments[index][0] = dict(
                    nome=customer.get('nome'),
                    cidade=customer.get('cidade'),
                    estado=customer.get('estado'),
                    segmento=customer.get('segmento')
                )
            payments['header'][0] = ["nome", "cidade", "estado", "segmento"]
            
            for index, register in registers:
                if index == "header":
                    continue
                date_info = [int(value) for value in register[1].split('/')]
                payments[index][1] = dict(
                    data=f"{date_info[2]}-{date_info[1]}-{date_info[0]}",
                    mes=date_info[1],
                    ano=date_info[-1]
                )
            payments['header'][1] = ["data", "mes", "ano"]
            
            plans = self.extractPlans()
            for index, register in registers:
                if index == "header":
                    continue
                plan_id = int(register[3])
                for _, plan in plans.items():
                    if plan_id == int(plan[0]):
                        plan = plan[1]
                        break
                plan = plan.lower()
                payments[index][3] = dict(
                    plano=plan
                )
            payments['header'][3] = ['plano']

            response = list()
            for key, value in payments.items():
                if key == "header":
                    continue
                document = dict(
                    id=key,
                    customer=value[0],
                    date=value[1],
                    valor=float(value[2]),
                    plan=value[3],
                    qtde_meses_pagos=int(value[4])
                )
                response.append(document)
            return response

        except Exception: #noqa
            self.logger.debug(traceback.format_exc())

    def loadPayments(self, dataset, url: str="") -> None:
        try:
            if not dataset:
                dataset = self.transformPayments(url=url)
            for document in dataset:
                with requests.post(
                        self.ENDPOINTs.get('payment'),
                        json=document
                        ) as response:
                    if response.status_code == 200:
                        continue
                    else:
                        print(
                            response.status_code,
                            response.reason
                        )
        except Exception: #noqa
            self.logger.debug(traceback.format_exc())
    
    def getPayments(self, payment_id: int=None) -> list:
        try:
            if payment_id:
                response = json.loads(
                    requests.get(
                        f"{self.ENDPOINTs.get('payment')}{payment_id}/"
                    ).content.decode('utf-8')
                )
            else:
                response = json.loads(
                    requests.get(
                        self.ENDPOINTs.get('payment')
                    ).content.decode('utf-8')
                )
            return response
        except Exception: #noqa
            self.logger.debug(traceback.format_exc())
    
    def buildPayments(self) -> bool:
        try:
            payments = self.extractPayments()
            payload = self.transformPayments(payments)
            self.loadPayments(dataset=payload)
            return True
        except Exception:
            self.logger.debug(traceback.format_exc())
            return False
    

    #[PROCESS]

    def batchProcess(self):
        self.buildPlans()
        self.buildCustomers()
        self.buildDates()
        self.buildPayments()
    
    def speedProcess(self):
        pass
    
    
    #[SERVER]

    def batchDataProcessing(self):
        self.logger.debug('batch layer is running...')
        while True:
            try:
                delta_time = (datetime.now() - self.batch_start)
                if delta_time <= self.batch_frequency:
                    sleep(self.batch_wait_time)
                else:
                    self.batchProcess()
                    self.batch_start = datetime.now()
            except Exception: #noqa
                self.logger.debug(traceback.format_exc())
    
    def speedDataProcessing(self):
        self.logger.debug('speed layer is running...')
        while True:
            try:
                delta_time = datetime.now() - self.speed_start
                if delta_time <= self.speed_frequency:
                    sleep(self.speed_wait_time)
                else:
                    self.speedProcess()
                    self.speed_start = datetime.now()
                    pass
            except Exception: #noqa
                self.logger.debug(traceback.format_exc())



#[PARAMETERs]
args = []
kwargs = {}


logger = custom_logging.get_base_logger('app')
logger.info("Starting setup...")


etl = DatabaseETL(logger)


threads = []
threads.append(
    threading.Thread(
        target=etl.batchDataProcessing
    )
)
threads.append(
    threading.Thread(
        target=etl.speedDataProcessing
    )
)


for index in range(len(threads)):
    threads[index].start()

