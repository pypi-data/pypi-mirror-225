# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta as rd
from .api import quantim

class risk_data(quantim):
    def __init__(self, username, password, secretpool, env="pdn"):
        super().__init__(username, password, secretpool, env)

    def load_ports_alm_co(self, file_name, overwrite=False, sep='|'):
        '''
        Load portfolio file to s3.
        '''
        payload = pd.read_csv(file_name, sep=sep).to_dict(orient='records')
        data = {'bucket':'condor-sura-alm', 'file_name':'portfolios/co/'+file_name.split('/')[-1], 'payload':payload, 'sep':sep, 'overwrite':overwrite}
        try:
            resp = self.api_call('load_data_s3', method="post", data=data, verify=False)
        except:
            resp = {'success':False, 'message':'Check permissions!'}
        return resp

    def load_master_limits(self, file_name, overwrite=True, sep=';'):
        '''
        Load portfolio file to s3.
        '''
        payload = pd.read_csv(file_name, sep=sep).to_dict(orient='records')
        data = {'bucket':'condor-sura', 'file_name':'inputs/risk/static/'+file_name.split('/')[-1], 'payload':payload, 'sep':sep, 'overwrite':overwrite}
        try:
            resp = self.api_call('load_data_s3', method="post", data=data, verify=False)
        except:
            resp = {'success':False, 'message':'Check permissions!'}
        return resp

    def get_limits(self, portfolio):
        '''
        Get limits table.
        '''

        data = {'portfolio':portfolio.to_dict(orient="records")}
        resp = self.api_call('limits', method="post", data=data, verify=False)
        summ, detail = pd.DataFrame(resp['summ']), pd.DataFrame(resp['detail'])

        return port_date, summ, detail

    def get_portfolio(self, client_id=None, port_type=None, ref_date=None):
        '''
        Get portfolio
        
        '''
        data = {'client_id':client_id, 'port_type':port_type, 'ref_date':ref_date}
        resp = self.api_call('portfolio', method="post", data=data, verify=False)

        portfolio, port_dur, port_per_msg, limits = pd.DataFrame(resp['portfolio']), resp['port_dur'], resp['port_per_msg'], resp['limits']
        limits_summ =  pd.DataFrame(limits['summ'])
        return portfolio, port_dur, port_per_msg, limits_summ

    def get_cashflows(self, client_id=None, port_type=None):
        '''
        Get cashflows
        '''
        data = [{'key':'client_id', 'value':client_id}, {'key':'port_type', 'value':port_type}] if client_id is not None else None
        resp = self.api_call('port_cashflows', method="get", data=data, verify=False)
        port_cfs = pd.DataFrame(resp)
        return port_cfs

    def get_value_at_risk(self, bucket="condor-sura", prefix="output/fixed_income/co/var/", sep=',', ref_date=None):
        '''
        Get Value at Risk results and suport information.
        '''
        ref_date = (dt.datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - rd(days=1)).strftime("%Y%m%d") if ref_date is None else ref_date
        files = ["var", "bond_cf", "exp_cps", "bond_float", "exp_cca", "exp_fx", "exp_eq"] 

        try:
            dfs = {}
            for file_i in files: 
                dfs[file_i] = self.retrieve_s3_df(bucket, f'{prefix}{ref_date}/{file_i}_{ref_date}.csv', sep=sep)
                print(f'{file_i} ready!')
            dfs = dfs.values()
        except:
            print(f"Files not available for {ref_date}!")
            dfs = None
        return dfs