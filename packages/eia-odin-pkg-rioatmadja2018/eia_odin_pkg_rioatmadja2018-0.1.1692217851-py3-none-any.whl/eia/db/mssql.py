#!/usr/bin/env python3 
import pymssql 
import boto3 
import json
import os 
import pandas as pd

class OdinDBMSSQL(object): 

    def __init__(self, region_name: str = 'us-east-1'):
        
        self.secrets = boto3.client(service_name='secretsmanager',
                                    region_name=region_name, 
                                    aws_access_key_id=os.environ["DEV-KEY"],
                                    aws_secret_access_key=os.environ["DEV-VAL"]
                                   )
        self.user, self.password, self.server, self.db = list(json.loads(self.secrets.get_secret_value(SecretId='mssql_db_analysis').get('SecretString')).values())
        
        self.con: 'MSSQL' = pymssql.connect(user=self.user, password=self.password, server=self.server, database=self.db)
        self.con.autocommit(True)
        self.cursor = self.con.cursor() 


    def get_store_reviews(self, lat: float, lon: float) -> 'DataFrame':

        try: 
            return pd.read_sql(f"SELECT * FROM GetStoreReviews({lat}, {lon})", con=self.con)

        except ConnectionError as e:
            raise ConnectionError(f"[ ERROR ] Unable to retrieve store location at the following loc: ({lat},{lon})") from e 

            
    def get_live_gasprices(self, state: str) -> 'DataFrame':
        """
        Description: 
            - Helper function to return today's gasoline prices based on the given state
              and call the custom T-SQL gasoline prices GetTodayLiveGasPrices
        Params: 
            - @state: give a valid US State 
        
        """
        try: 
            return pd.read_sql(f"SELECT * FROM GetTodayLiveGasPrices('{state}') ORDER BY timestamp ASC", con=self.con)

        except ConnectionError as e:
            raise ConnectionError(f"[ ERROR ] Unable to query the following state {state}") from e 


    def get_avg_price(self, station_name: str , state:str) -> 'DataFrame':

        try: 
            return pd.read_sql(f"SELECT g.gas_station, g.state, CAST(g.avg_price AS MONEY ) FROM GetGasolineAvgPrice( '{station_name}', '{state}') g",con=self.con)
        
        except ConnectionError as e:
            raise ConnectionError(f"[ ERROR ] Unable to retrieve gas_station average price for the given region {state_name}") from e 

    def get_gas_station_reviews(self, state_name: str) -> 'DataFrame': 

        try:

            return pd.read_sql(f"SELECT * FROM GetGasStationReviews('{state_name}')", con=self.con)
        
        except ConnectionError as e:
            raise ConnectionError(f"[ ERROR ] Unable to retrieve reviews for the given region '{state_name}' ") from e 






















        