import pandas as pd
from pandas import json_normalize
import requests
import json

from datetime import datetime, timedelta
import time
from dateutil.relativedelta import relativedelta

# # from io import BytesIO
# from bs4 import BeautifulSoup

# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import plotly.express as px

# import os

today = datetime.today().strftime("%Y-%m-%d")

# ----------------------------------------------------------------------
# REQUESTS CONFIG

## Fireant token, this token has been generated from a Incognito session
fa_token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSIsImtpZCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4iLCJhdWQiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4vcmVzb3VyY2VzIiwiZXhwIjoxODg5NjIyNTMwLCJuYmYiOjE1ODk2MjI1MzAsImNsaWVudF9pZCI6ImZpcmVhbnQudHJhZGVzdGF0aW9uIiwic2NvcGUiOlsiYWNhZGVteS1yZWFkIiwiYWNhZGVteS13cml0ZSIsImFjY291bnRzLXJlYWQiLCJhY2NvdW50cy13cml0ZSIsImJsb2ctcmVhZCIsImNvbXBhbmllcy1yZWFkIiwiZmluYW5jZS1yZWFkIiwiaW5kaXZpZHVhbHMtcmVhZCIsImludmVzdG9wZWRpYS1yZWFkIiwib3JkZXJzLXJlYWQiLCJvcmRlcnMtd3JpdGUiLCJwb3N0cy1yZWFkIiwicG9zdHMtd3JpdGUiLCJzZWFyY2giLCJzeW1ib2xzLXJlYWQiLCJ1c2VyLWRhdGEtcmVhZCIsInVzZXItZGF0YS13cml0ZSIsInVzZXJzLXJlYWQiXSwianRpIjoiMjYxYTZhYWQ2MTQ5Njk1ZmJiYzcwODM5MjM0Njc1NWQifQ.dA5-HVzWv-BRfEiAd24uNBiBxASO-PAyWeWESovZm_hj4aXMAZA1-bWNZeXt88dqogo18AwpDQ-h6gefLPdZSFrG5umC1dVWaeYvUnGm62g4XS29fj6p01dhKNNqrsu5KrhnhdnKYVv9VdmbmqDfWR8wDgglk5cJFqalzq6dJWJInFQEPmUs9BW_Zs8tQDn-i5r4tYq2U8vCdqptXoM7YgPllXaPVDeccC9QNu2Xlp9WUvoROzoQXg25lFub1IYkTrM66gJ6t9fJRZToewCt495WNEOQFa_rwLCZ1QwzvL0iYkONHS_jZ0BOhBCdW9dWSawD6iF1SIQaFROvMDH1rg'

rv_cookie = r"JSESSIONID=5F6CFF24C14F528841B8DFE10C15FD6E; vdsc-liv=\u00219SAjbJTdrdVJMsrGJTT3LEhTmJvzwdZmJnfyYNQvKbwk52j3vTk2cdjZCnRcHJqnP0fvRfQ8TtQGig==; hideMarketChartCKName=0; allCustomGroupsCkName=ALL_DEFAULT_GROUP_ID%23%23%23%23%23%23%23%23CTD%3BDHG%3BDRC%3BFPT%3BHPG%3BHSG%3BKDC%3BMWG%3BNT2%3BPAC%3BPC1%3BPNJ%3BTAC%3BVCB%3BVDS%3BVGC%3BVJC%3BVNM%3B%23%23%23%23%23%23%23%23T%C3%B9y%20ch%E1%BB%8Dn; _ga=GA1.1.422839090.1692367193; rv_avraaaaaaaaaaaaaaaa_session_=GMMIGBCHCKBBCDHGIMFPNKEJFEBIIGCKJNNOLHNDNDGPOAIPMNBMFDPHMKNGKLCPGCKDFLKHPJGMJKBNJGJAAEBFBHAHBHGDNMHIDFMAICPGDHHCNNCDBCKOMIEHDHNL; _ga_D36ML1235R=GS1.1.1692367192.1.0.1692367200.0.0.0; RV9cd20160034=08557ab163ab20000275b1afd8ac0c84941fee6c1465959ac03e4ceb74a70e91726914493a761a4a08a1c1d8e3113000302e18ca2940b908e8274d3f97f4abe28d45ae17a9ee60b63b3799aa5ae4bb5cbe8885583676fe1177aa31dbffb4e951"

fa_headers = {
  'authority': 'restv2.fireant.vn',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9',
  'dnt': '1',
  'origin': 'https://fireant.vn',
  'sec-ch-ua': '"Google Chrome";v="114", "Chromium";v="114", "Not=A?Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

rv_headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Language': 'en-US,en;q=0.9',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'DNT': '1',
  'Origin': 'https://livedragon.vdsc.com.vn',
  'Referer': 'https://livedragon.vdsc.com.vn/general/intradayBoard.rv',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

tcbs_headers = {
  'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
  'DNT': '1',
  'Accept-language': 'vi',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37',
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Referer': 'https://tcinvest.tcbs.com.vn/',
  'sec-ch-ua-platform': '"Windows"'
}

fiin_headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.9',
  'Authorization': 'Bearer',
  'Connection': 'keep-alive',
  'DNT': '1',
  'Origin': 'https://fiintrade.vn',
  'Referer': 'https://fiintrade.vn/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37',
  'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}


# API request config for SSI API endpoints
ssi_headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'X-Fiin-Key': 'KEY',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Fiin-User-ID': 'ID',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'X-Fiin-Seed': 'SEED',
        'sec-ch-ua-platform': 'Windows',
        'Origin': 'https://iboard.ssi.com.vn',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://iboard.ssi.com.vn/',
        'Accept-Language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7'
        }

# VNDirect Dchart header
vnd_headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.9',
  'Connection': 'keep-alive',
  'DNT': '1',
  'Origin': 'https://dchart.vndirect.com.vn',
  'Referer': 'https://dchart.vndirect.com.vn/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0',
  'sec-ch-ua': '"Edge";v="114", "Chromium";v="114", "Not=A?Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

# VNDirect trade.vndirect.com.vn header
vndt_headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.9',
  'Connection': 'keep-alive',
  'DNT': '1',
  'Origin': 'https://trade.vndirect.com.vn',
  'Referer': 'https://trade.vndirect.com.vn/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

entrade_headers = {
  'authority': 'services.entrade.com.vn',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9',
  'dnt': '1',
  'origin': 'https://banggia.dnse.com.vn',
  'referer': 'https://banggia.dnse.com.vn/',
  'sec-ch-ua': '"Edge";v="114", "Chromium";v="114", "Not=A?Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'cross-site',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0'
}

# TradingView API config
tdv_headers = {
  'authority': 'scanner.tradingview.com',
  'accept': 'application/json',
  'accept-language': 'en-US,en;q=0.9',
  'content-type': 'text/plain;charset=UTF-8',
  'dnt': '1',
  'origin': 'https://www.tradingview.com',
  'referer': 'https://www.tradingview.com/',
  'sec-ch-ua': '"Edge";v="114", "Chromium";v="114", "Not=A?Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0'
}

custom_cols = ['name','description', 'sector', 'currency', 'close', 'volume','high|1M', 'low|1M', 'average_volume_90d_calc', 'market_cap_basic']
overview_cols = ["name","description","logoid","currency","close","change","volume","volume_change","market_cap_basic","fundamental_currency_code","price_earnings_ttm","earnings_per_share_diluted_ttm","sector","market"]
performance_cols = ["name","description","logoid","currency","close","change","Perf.W","Perf.1M","Perf.3M","Perf.6M","Perf.YTD","Perf.Y","Perf.5Y","Perf.All","Volatility.W","Volatility.M"]
extended_hours_cols = ["name","description","logoid","currency","premarket_close","pricescale","premarket_change","premarket_gap","premarket_volume","close","change","gap","volume","volume_change","postmarket_close","postmarket_change","postmarket_volume"]
valuation_cols = ["name","description","logoid","market_cap_basic","fundamental_currency_code","price_earnings_ttm","price_earnings_growth_ttm","price_sales_current","price_book_fq","price_to_cash_f_operating_activities_ttm","price_free_cash_flow_ttm","price_to_cash_ratio","enterprise_value_current","enterprise_value_to_revenue_ttm","enterprise_value_to_ebit_ttm","enterprise_value_ebitda_ttm"]
dividend_cols = ["name","description","logoid","dps_common_stock_prim_issue_fy","fundamental_currency_code","dps_common_stock_prim_issue_fq","dividends_yield_current","dividends_yield","dividend_payout_ratio_ttm","dps_common_stock_prim_issue_yoy_growth_fy","continuous_dividend_payout","continuous_dividend_growth"]
profitablity_cols = ["name","description","logoid","gross_margin_ttm","operating_margin_ttm","pre_tax_margin_ttm","net_margin_ttm","free_cash_flow_margin_ttm","return_on_assets_fq","return_on_equity_fq","return_on_invested_capital_fq","research_and_dev_ratio_ttm","sell_gen_admin_exp_other_ratio_ttm"]
income_statement_cols = ["name","description","logoid","total_revenue_ttm","fundamental_currency_code","total_revenue_yoy_growth_ttm","gross_profit_ttm","oper_income_ttm","net_income_ttm","ebitda_ttm","earnings_per_share_diluted_ttm","earnings_per_share_diluted_yoy_growth_ttm"]
balancesheet_cols = ["name","description","logoid","total_assets_fq","fundamental_currency_code","total_current_assets_fq","cash_n_short_term_invest_fq","total_liabilities_fq","total_debt_fq","net_debt_fq","total_equity_fq","current_ratio_fq","quick_ratio_fq","debt_to_equity_fq","cash_n_short_term_invest_to_total_debt_fq"]
cashflow_cols = ["name","description","logoid","cash_f_operating_activities_ttm","fundamental_currency_code","cash_f_investing_activities_ttm","cash_f_financing_activities_ttm","free_cash_flow_ttm","capital_expenditures_ttm"]
oscillator_cols = ["name","description","logoid","Recommend.Other","RSI","Mom","AO","CCI20","Stoch.K","Stoch.D","MACD.macd","MACD.signal"]
trend_cols = ["name","description","logoid","Recommend.MA","close","pricescale","minmov","fractional","minmove2","currency","SMA20","SMA50","SMA200","BB.upper","BB.lower"]

all_cols = list(set(overview_cols + performance_cols + extended_hours_cols + valuation_cols + dividend_cols + profitablity_cols + income_statement_cols + balancesheet_cols + cashflow_cols + oscillator_cols + trend_cols))
