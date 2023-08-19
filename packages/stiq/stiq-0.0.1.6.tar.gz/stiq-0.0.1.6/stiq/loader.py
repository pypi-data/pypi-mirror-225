# Copyright 2022 Thinh Vu @ GitHub

from .config import *

# LISTING COMPANIES
def listing_companies(lang='vi', columns=['ticker', 'comGroupCode', 'organName', 'organTypeCode', 'comTypeCode', 'icbCode'], headers=fiin_headers):
    url = f"https://core.fiintrade.vn/Master/GetListOrganization?language={lang}"
    response = requests.request("GET", url, headers=headers, data={}).json()
    df = json_normalize(response['items'])
    df = df[columns]
    return df

def listing_industries(lang='vi', columns=['icbName', 'icbNamePath', 'icbCode'], headers=fiin_headers):
    url = f"https://core.fiintrade.vn/Master/GetAllIcbIndustry?language={lang}"
    response = requests.request("GET", url, headers=headers, data={}).json()
    df = json_normalize(response['items'])
    df = df[columns]
    return df

def listing_companies_enhanced (lang='vi', columns=['ticker', 'comGroupCode', 'organName', 'organShortName', 'organTypeCode', 'comTypeCode', 'icbCode'], headers=fiin_headers):
    df_companies = listing_companies(lang, columns, headers=headers)
    df_industries = listing_industries(lang, columns=['icbName', 'icbNamePath', 'icbCode'], headers=headers)
    df = pd.merge(df_companies, df_industries, on='icbCode', how='left')
    df[['sector', 'industry', 'group', 'subgroup']] = df['icbNamePath'].str.split('/', expand=True)
    df = df[[c for c in df if c not in ['icbCode']] + ['icbCode']]
    return df


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

### Extract price & volume data
def hitorical_stock_price (symbol='ACB', resolution='1', from_date='2023-04-01', to_date='2023-07-12', headers=vnd_headers):
    from_timestamp = int(datetime.strptime(from_date, '%Y-%m-%d').timestamp())
    to_timestamp = int(datetime.strptime(to_date, '%Y-%m-%d').timestamp())
    url = f"https://dchart-api.vndirect.com.vn/dchart/history?resolution={resolution}&symbol={symbol}&from={from_timestamp}&to={to_timestamp}"
    response = requests.get(url, headers=headers).json()
    df = pd.DataFrame(response)
    df.drop(columns=['s'], inplace=True)
    df.rename(columns={'t': 'time', 'c': 'close', 'o': 'open', 'h': 'high', 'l': 'low', 'v': 'volume'}, inplace=True)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = df[['time', 'open', 'high', 'low', 'close', 'volume']]
    return df

def indices_price_board (index='VN100', headers=ssi_headers):
    payload = json.dumps({
        "operationName": "stockRealtimesByGroup",
        "variables": {
            "group": f"{index}"
        },
        "query": "query stockRealtimesByGroup($group: String) {\n  stockRealtimesByGroup(group: $group) {\n    stockNo\n    ceiling\n    floor\n    refPrice\n    stockSymbol\n    stockType\n    exchange\n    lastMatchedPrice\n    matchedPrice\n    matchedVolume\n    priceChange\n    priceChangePercent\n    highest\n    avgPrice\n    lowest\n    nmTotalTradedQty\n    best1Bid\n    best1BidVol\n    best2Bid\n    best2BidVol\n    best3Bid\n    best3BidVol\n    best4Bid\n    best4BidVol\n    best5Bid\n    best5BidVol\n    best6Bid\n    best6BidVol\n    best7Bid\n    best7BidVol\n    best8Bid\n    best8BidVol\n    best9Bid\n    best9BidVol\n    best10Bid\n    best10BidVol\n    best1Offer\n    best1OfferVol\n    best2Offer\n    best2OfferVol\n    best3Offer\n    best3OfferVol\n    best4Offer\n    best4OfferVol\n    best5Offer\n    best5OfferVol\n    best6Offer\n    best6OfferVol\n    best7Offer\n    best7OfferVol\n    best8Offer\n    best8OfferVol\n    best9Offer\n    best9OfferVol\n    best10Offer\n    best10OfferVol\n    buyForeignQtty\n    buyForeignValue\n    sellForeignQtty\n    sellForeignValue\n    caStatus\n    tradingStatus\n    remainForeignQtty\n    currentBidQty\n    currentOfferQty\n    session\n    tradingUnit\n    __typename\n  }\n}\n"
        })
    
    url = 'https://wgateway-iboard.ssi.com.vn/graphql'
    response = requests.request("POST", url, headers=headers, data=payload).json()
    df = json_normalize(response['data']['stockRealtimesByGroup'])
    df.rename(columns={'stockSymbol': 'ticker'}, inplace=True)
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

# a function to get the list of tickers from stock screening from url = "https://scanner.tradingview.com/vietnam/scan"
# payload = "{\"columns\":[\"name\",\"description\",\"logoid\",\"update_mode\",\"type\",\"typespecs\",\"close\",\"pricescale\",\"minmov\",\"fractional\",\"minmove2\",\"currency\",\"change\",\"volume\",\"volume_change\",\"market_cap_basic\",\"fundamental_currency_code\",\"Perf.1Y.MarketCap\",\"price_earnings_ttm\",\"earnings_per_share_diluted_ttm\",\"sector\",\"market\",\"dividends_yield_fy\",\"volume|1M\",\"average_volume_90d_calc\",\"average_volume_30d_calc\",\"average_volume_10d_calc\",\"SMA50\",\"SMA200\"],\"filter\":[{\"left\":\"sector\",\"operation\":\"in_range\",\"right\":[\"Finance\"]},{\"left\":\"price_book_fq\",\"operation\":\"eless\",\"right\":5},{\"left\":\"dividends_yield_fy\",\"operation\":\"greater\",\"right\":0},{\"left\":\"average_volume_90d_calc\",\"operation\":\"greater\",\"right\":10000},{\"left\":\"typespecs\",\"operation\":\"has_none_of\",\"right\":[\"etn\",\"etf\"]}],\"ignore_unknown_fields\":false,\"options\":{\"lang\":\"en\"},\"price_conversion\":{\"to_symbol\":true},\"range\":[0,100],\"sort\":{\"sortBy\":\"average_volume_90d_calc\",\"sortOrder\":\"asc\"},\"markets\":[\"vietnam\"]}"

def stock_screener_preset(columns_list=all_cols, size=200, country='vietnam', filter='"filter":[{"left":"typespecs","operation":"has_none_of","right":["etn","etf"]}]', sort_order = '"sort":{"sortBy":"market_cap_basic","sortOrder":"desc"}', headers=tdv_headers):
    range = f'"range":[0,{size}]'
    market = f'"markets":["{country}"]'
    columns = f'"columns":{str(columns_list)}'
    optional = '"ignore_unknown_fields":false, "options":{"lang":"en"},"price_conversion":{"to_symbol":true}'
    payload = '{' + ','.join([columns, filter, optional, range, sort_order, market]) + '}'
    payload = payload.replace("'", '"').replace('"', '\"')
    url = "https://scanner.tradingview.com/vietnam/scan"
    response = requests.request("POST", url, headers=headers, data=payload).json()
    print(f'Total results: {response["totalCount"]}')
    try:
        df = json_normalize(response['data'])
        df[['exchange', 'ticker']] = df['s'].str.split(':', expand=True)
        data_df = pd.DataFrame()
        for data in df['d']:
            row_df = pd.DataFrame(data).T
            data_df = pd.concat([data_df, row_df])
        columns_list = json.loads(payload)['columns']
        columns_list[columns_list.index('name')] = 'ticker'
        data_df.columns = columns_list
        df = df.merge(data_df, how='left', on='ticker')
        if 'logoid' in df.columns:
            df['logoid'] = 'https://s3-symbol-logo.tradingview.com/' + df['logoid'].astype(str) + '.svg'
        df.drop(columns=['s', 'd'], inplace=True)
        return df
    except:
        print('Error in get_screener_data function')

# TRADING CENTER
## Intraday data
def intraday_historical_data (ticker='VNM', date='2023-07-28', cookie=rv_cookie, headers=rv_headers):
    date = date[8:10] + '/' + date[5:7] + '/' + date[0:4]
    url = "https://livedragon.vdsc.com.vn/general/intradaySearch.rv"
    payload = F"stockCode={ticker}&boardDate={date}"
    headers['Cookie'] = cookie
    response = requests.request("POST", url, headers=headers, data=payload).json()
    df = json_normalize(response['list'])
    col_order = ['Code', 'FloorCode', 'TradeTime', 'RefPrice', 'CeiPrice', 'FlrPrice', 'BidPrice3', 'BidVol3', 'BidPrice2', 'BidVol2', 'BidPrice1', 'BidVol1', 'OfferPrice1', 'OfferVol1', 'OfferPrice2', 'OfferVol2', 'OfferPrice3', 'OfferVol3', 'MatchedPrice', 'MatchedVol', 'MatchedTotalVol', 'MatchedChange', 'HigPrice', 'LowPrice', 'AvgPrice', 'FBuyVol', 'FSellVol', 'AmPm']
    col_label = ['Mã CK', 'Sàn GD', 'Thời gian', 'Giá tham chiếu', 'Giá trần', 'Giá sàn', 'Giá mua 3', 'KL mua 3', 'Giá mua 2', 'KL mua 2', 'Giá mua 1', 'KL mua 1', 'Giá bán 1', 'KL bán 1', 'Giá bán 2', 'KL bán 2', 'Giá bán 3', 'KL bán 3', 'Giá khớp lệnh', 'KL khớp lệnh', 'Tổng KL khớp lệnh', '+/- khớp lệnh', 'Giá cao', 'Giá thấp', 'Giá TB', 'ĐTNN Mua', 'ĐTNN Bán', 'Buổi']
    col_dict = dict(zip(col_order, col_label))
    df = df.rename(columns=col_dict)[col_label]
    return df

def latest_intraday_data (symbol='CTG', limit=100000, headers=vndt_headers):
    url = f"https://api-finfo.vndirect.com.vn/v4/stock_intraday_latest?q=code:{symbol}&sort=time&size={limit}"
    response = requests.request("GET", url, headers=headers, data={}).json()
    df = json_normalize(response['data'])
    return df

def last_price_vol (symbol='CTG', limit=100000, headers=vndt_headers):
    df = latest_intraday_data (symbol, limit, headers)
    last_price_vol = pd.pivot_table(df, index=['last', 'side'], values='lastVol', aggfunc='sum')
    return last_price_vol


# NEWS & EVENTS

def ticker_events (symbol='TPB', page_size=15, page=0, headers=tcbs_headers):
    url = f"https://apipubaws.tcbs.com.vn/tcanalysis/v1/ticker/{symbol}/events-news?page={page}&size={page_size}"
    response = requests.request("GET", url, headers=headers, data={}).json()
    df = pd.DataFrame(response['listEventNews'])
    return df

def ticker_news (symbol='TCB', page_size=15, page=0, headers=tcbs_headers):
    url = f"https://apipubaws.tcbs.com.vn/tcanalysis/v1/ticker/{symbol}/activity-news?page={page}&size={page_size}"
    response = requests.request("GET", url, headers=headers, data={}).json()
    df = pd.DataFrame(response['listActivityNews'])
    df['ticker'] = symbol
    return df