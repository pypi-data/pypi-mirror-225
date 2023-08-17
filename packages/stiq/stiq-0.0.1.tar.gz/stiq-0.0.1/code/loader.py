# Copyright 2022 Thinh Vu @ GitHub

from .config import *

# INDICES
### Get latest info of all indices
def latest_indices (lang='vi', size=99999):
  url = f"https://market.fiintrade.vn/MarketInDepth/GetLatestIndices?language={lang}&pageSize={str(size)}&status=1"
  response = requests.request("GET", url, headers=fiin_headers, data={}).json()
  df = json_normalize(response['items'])
  df['comGroupCode'] = df['comGroupCode'].str.replace('Index', '')
  df = df.drop(columns=['indexId'])
  df = df.rename(columns={'comGroupCode': 'code'})
  return df

### Get the index value, P/E and P/B by date
def indices_valuation (code='VNINDEX', time_range='SixMonths', lang='vi', headers=fiin_headers):
  url = f"https://market.fiintrade.vn/MarketInDepth/GetValuationSeriesV2?language={lang}&Code={code}&TimeRange={time_range}"
  response = requests.request("GET", url, headers=headers, data={}).json()
  df = json_normalize(response['items'])
  df = df.rename(columns={'value': 'points', 'r21': 'P/E', 'r25': 'P/B'})
  df['tradingDate'] = pd.to_datetime(df['tradingDate'])
  df = df[['code', 'tradingDate', 'points', 'P/E', 'P/B']]
  df = df.rename(columns={'tradingDate': 'date', 'code': 'ticker'})
  return df

## BIG BOYS TRADING
def foreign_trading (code='STOCK_HNX,STOCK_UPCOM,STOCK_HOSE,ETF_HOSE,IFC_HOSE', sort='tradingDate', size=500, headers=vndt_headers):
  url = f"https://finfo-api.vndirect.com.vn/v4/foreigns?q=code:{code}&sort={sort}&size={size}"
  response = requests.request("GET", url, headers=headers, data={}).json()
  df = json_normalize(response['data'])
  if 'floor' in df.columns:
    df = df.rename(columns={'floor': 'exchange'})
  return df

def proprietary_trading (code='HNX,VNINDEX,UPCOM', date='2023-02-09', sort='date:desc', size=600, headers=vndt_headers):
  url = f"https://finfo-api.vndirect.com.vn/v4/proprietary_trading?q=code:{code}~date:gte:{date}&sort={sort}&size={size}"
  response = requests.request("GET", url, headers=headers, data={}).json()
  df = json_normalize(response['data'])
  if 'floor' in df.columns:
    df = df.rename(columns={'floor': 'exchange'})
  return df


# TICKER TECHNIAL ANALYSIS

## price quote
def ticker_historical_quote(symbol, start_date, end_date, authen_bearer=fa_token, headers=fa_headers): ## Get the comprehensive ticker's quotes data from FireAnt
    headers['authorization'] = f'{authen_bearer}'
    url = f"https://restv2.fireant.vn/symbols/{symbol}/historical-quotes?startDate={start_date}&endDate={end_date}&offset=0&limit=90"
    response = requests.request("GET", url, headers=headers).json()
    df = json_normalize(response)
    df['date'] = pd.to_datetime(df['date'])
    df = df.rename(columns={'symbol': 'ticker'})
    df = df[['ticker'] + [col for col in df.columns if col != 'ticker']]
    return df


# FUNDAMENTAL ANALYSIS

def company_financial_report (symbol='TCB', type='incomeStatement', year=2023, quarter=2, limit=6, value_display='M', unique_name= False, headers=fa_headers, authen_bearer=fa_token):
    if type == 'balanceSheet':
        type = 1
    elif type == 'incomeStatement':
        type = 2
    elif type == 'directCashflow':
        type = 3
    elif type == 'indirectCashflow':
        type = 4
    if value_display == 'M':
        value_display = 1000000
    elif value_display == 'B':
        value_display = 1000000000
    else:
        value_display = 1
    headers['authorization'] = f'{authen_bearer}'
    url = f"https://restv2.fireant.vn/symbols/{symbol}/full-financial-reports?type={type}&year={year}&quarter={quarter}&limit={limit}"
    response = requests.request("GET", url, headers=headers, data={}).json()
    df = json_normalize(response)
    df['unique_name'] = df['id'].astype(str) + ' | ' + df['name']
    hierarchy = df['id'].to_list()
    value_df_list = []
    for i in range(len(df['values'])):
        value_df = pd.DataFrame(df['values'][i])
        value_df['value'] = value_df['value']/value_display
        df1 = value_df.T
        df1.columns = df1.iloc[0]
        df1['name'] = df['name'][i]
        df1['id'] = df['id'][i]
        df1['unique_name'] = df1['id'].astype(str) + ' | ' + df1['name']
        df1.drop(index=['year', 'quarter', 'period'], inplace=True)
        df1 = df1[['name'] + [col for col in df1.columns if col != 'name']]
        value_df_list.append(df1)
        df1.drop(columns=['id'], inplace=True)
    df2 = pd.concat(value_df_list)
    df2.reset_index(drop=True, inplace=True)
    df2.index.name = None
    final_df = df[['id', 'unique_name']].merge(df2, how='left', on='unique_name')
    if unique_name == True:
        final_df.drop(columns=['name'], inplace=True)
    elif unique_name == False:
        final_df.drop(columns=['unique_name'], inplace=True)
    return final_df


# STOCK SCREENING

def stock_screening_insights (params, size=50, id=None, drop_lang='vi', headers=tcbs_headers):
    url = "https://apipubaws.tcbs.com.vn/ligo/v1/watchlist/preview"
    filters = []
    for key, value in params.items():
        if isinstance(value, tuple):
            min_value, max_value = value
            filters.append({
                "key": key,
                "operator": ">=",
                "value": min_value
            })
            filters.append({
                "key": key,
                "operator": "<=",
                "value": max_value
            })
        else:
            filters.append({
                "key": key,
                "value": value,
                "operator": "="
            })
    payload = json.dumps({
        "tcbsID": id,
        "filters": filters,
        "size": params.get("size", size)
    })
    response = requests.request("POST", url, headers=headers, data=payload).json()
    df = json_normalize(response['searchData']['pageContent'])
    df = df[df.columns.drop(list(df.filter(regex=f'\.{drop_lang}$')))]
    df = df.dropna(axis=1, how='all')
    return df
