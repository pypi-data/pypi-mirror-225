import pandas as pd
import yfinance as yf
from datetime import time, date, datetime, timedelta
import pytz, holidays
from pytz import timezone

import numpy as np
import math
import inspect

#import sys

#sys.path.append(r'\Users\jimhu\option_trader\src')    

from option_trader.consts import asset as at
from option_trader.settings import app_settings


from option_trader.utils.option_tool import delta_call
from option_trader.utils.option_tool import delta_put
from option_trader.utils.option_tool import theta_call
from option_trader.utils.option_tool import theta_put
from option_trader.utils.option_tool import gamma
from option_trader.utils.option_tool import vega

from option_trader.utils.option_tool import time_to_maturity_in_year

from option_trader.utils.calc_prob import calc_prob_higher_than
from option_trader.utils.calc_prob import calc_prob_lower_than
from option_trader.utils.calc_prob import calc_prob_between
from option_trader.utils.calc_prob import predicted_list

from option_trader.utils.data_getter_ib import IBClient
from option_trader.utils.data_getter_ib import IB_get_option_chain
from option_trader.utils.data_getter_ib import IB_get_option_leg_details

import option_trader.consts.strategy as st

from  option_trader.admin import position
from  option_trader.admin import option_summary
from  option_trader.admin import quote


import logging

import warnings

from pandas.errors import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

#logging.getLogger('yfinance').setLevel(logging.WARNING)

#logger = logging.getLogger(__name__)
            
from diskcache import Cache

cache = Cache()

def get_price_history(symbol, period='6mo', interval="1d"):     
    logger = logging.getLogger(__name__)    
    cache_key = symbol+'price_history'+period+interval
    if cache_key in cache:        
        try:
            return cache[cache_key]       
        except:
            pass

    q = get_ticker(symbol)

    try:        
        hist = q.history(period=period, interval=interval)
        cache.set(cache_key, hist, expire=300)
        return hist              
    except Exception as ex:
        logger.exception('q.history raise exception %s' % symbol)
        raise ex
    
def get_ticker(symbol):
    return yf.Ticker(symbol) 
          
def get_last_dividend(symbol):
    cache_key = symbol+'last_dividend'
    if cache_key in cache:
        return cache[cache_key]       

    stock = get_ticker(symbol)
    ed = stock.get_dividends()
    if len(ed) > 0:
        cache.set(cache_key, ed, expire=86400)           
        return ed[-1]
    else:
        return 0.0      

def afterHours(now = None):
    tz = pytz.timezone(app_settings.TIMEZONE)
    us_holidays = holidays.US()        
    if not now:
        now = datetime.now(tz)        
    openTime = time(hour = 9, minute = 30, second = 0)
    closeTime = time(hour = 16, minute = 0, second = 0)
    # If a holiday
    if now.strftime('%Y-%m-%d') in us_holidays:
        return True
    # If before 0930 or after 1600
    if (now.time() < openTime) or (now.time() > closeTime):
        return True
    # If it's a weekend
    if now.date().weekday() > 4:
        return True

    return False       
    
def get_next_earning_date(symbol):
    cache_key = symbol+'next_earning_dates'
    if cache_key in cache:
        return cache[cache_key]    
            
    stock = get_ticker(symbol)
    ed = stock.get_earnings_dates()
    if isinstance(ed, type(None)):
        return None
    
    if ed.empty == False:
        today = pd.Timestamp.now(ed.head(1).index.tz)
        et = ed[ed.index > today]
        if et.empty == False:
            cache.set(cache_key, et.index[-1], expire=86400)        
            return et.index[-1]
    return None
        
def get_earning_dates(symbol):
    
    cache_key = symbol+'earning_dates'
    
    if cache_key in cache:
        return cache[cache_key]    
        
    stock = get_ticker(symbol)

    earning_dates = stock.get_earnings_dates()

    cache.set(cache_key, earning_dates, expire=86400)
    
    return earning_dates     

def get_support_resistence_levels(symbol, data=pd.DataFrame()):

    def isSupport(df,i):
        support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
        return support

    def isResistance(df,i):
        resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
        return resistance

    if data.empty:
        df = get_price_history(symbol)
    else:
        df = data

    s =  np.mean(df['High'] - df['Low'])

    def isFarFromLevel(l):
        return np.sum([abs(l-x) < s  for x in levels]) == 0

    SUPPORT = 0
    RESISTANCE = 1
    levels = []
    for i in range(2,df.shape[0]-2):
        if isSupport(df,i):
            l = df['Low'][i]
            if isFarFromLevel(l):
                levels.append((i,l,SUPPORT))
        elif isResistance(df,i):
            l = df['High'][i]
            if isFarFromLevel(l):
                levels.append((i,l,RESISTANCE))        

    l = range( len(levels) - 1, -1, -1)
    support = None
    resistence = None

    for i in l:
        if levels[i][2] == SUPPORT and support == None:
            support = levels[i][1]
        if levels[i][2] == RESISTANCE and resistence == None:
            if support != None and levels[i][1] > support:
                resistence = levels[i][1]

    return support, resistence

def get_option_exp_date(symbol, min_days_to_expire=np.nan, max_days_to_expire=np.nan):

    cache_key =symbol+'exp_date'+str(min_days_to_expire)+str(max_days_to_expire)
    if cache_key in cache:
        return cache[cache_key]
    
    today = datetime.now(timezone(app_settings.TIMEZONE))

    q = get_ticker(symbol)    
    
    exp_date_list = q.options
    
    list_to_return = []

    for exp_date in exp_date_list:        
        days_to_expire = (pd.Timestamp(exp_date).tz_localize(timezone(app_settings.TIMEZONE))-today).days

        if days_to_expire <= 0:
            continue

        if math.isnan(min_days_to_expire) == False:
            if days_to_expire <= min_days_to_expire:
                continue
        
        if math.isnan(max_days_to_expire) == True:
            list_to_return.append(exp_date)            
        else:
            if days_to_expire <= max_days_to_expire:
                list_to_return.append(exp_date)

    cache.set(cache_key, list_to_return, expire=86400)    

    return list_to_return
    
def convert_yahoo_df(df):
    df.drop(['contractSymbol', 'lastTradeDate','change', 'currency', 'contractSize', 'inTheMoney', 'percentChange'], axis=1, inplace=True)
    df[quote.BID_SIZE] = df[quote.ASK_SIZE] = df[quote.OPEN] = df[quote.HIGH] = np.nan
    df[quote.LOW] = df[quote.CLOSE] = df[quote.DELTA] = df[quote.GAMMA] = np.nan
    df[quote.VEGA] = df[quote.THETA] = df[quote.SIGMA] = np.nan        
    return df

def get_option_chain(symbol, 
                    otype,
                    max_strike_ratio=0.25,                    
                    exp_date_list = [], 
                    max_days_to_expire=np.nan,                     
                    max_bid_ask_spread=np.nan,
                    min_open_interest=np.nan): 
    
    import traceback

    logger = logging.getLogger(__name__)   

    if  otype not in [at.CALL, at.PUT]:
        logger.error('Invaid option type %s given' % otype)
        return pd.DataFrame()

    if len(exp_date_list) == 0:
        exp_date_list = get_option_exp_date(symbol, max_days_to_expire=max_days_to_expire)            

    if len(exp_date_list) == 0:
        logger.error('No exp date found')
        return pd.DataFrame()
                    
    all_chain = pd.DataFrame()

    today = datetime.now(timezone(app_settings.TIMEZONE)).date()

    stock_price = get_price_history(symbol, period='1d', interval='1d')['Close'][-1]

    for exp_date in exp_date_list:                   

        days_to_expire = (pd.Timestamp(exp_date).date()-today).days

        chain_cache_key =symbol+otype+'_chain'+exp_date
        if chain_cache_key in cache:
            chain = cache[chain_cache_key]
        else:
            chain = pd.DataFrame()

        #if isinstance(calls, pd.DataFrame) and isinstance(puts, pd.DataFrame):
        #    return calls, puts
        #
        # if afterHours() == False:
        #    ib = IBClient.get_client()
        #    if ib != None and ib.isconnected():
        #        calls, puts = IB_get_option_chain(symbol, exp_date, stock_price)
        #        if calls.shape[0] == 0 or puts.shape[0] == 0:
        #            logger.info('Cannot get option chain from IB, try Yahoo now')
        #        else:
        #            calls, puts = insert_option_quote_meta(calls, puts, exp_date)                  
        #            cache.set(call_chain_cache_key, calls, expire=300)                      
        #            cache.set(put_chain_cache_key, puts, expire=300) 
        #            insert_option_quote_meta(calls, puts, exp_date):    
        #            return [calls, puts]

        if chain.shape[0] == 0: # not in chache
            try:
                q = get_ticker(symbol)
                if otype == at.CALL:
                    chain = q.option_chain(exp_date).calls           
                else:
                    chain = q.option_chain(exp_date).puts       
                cache.set(chain_cache_key, chain, expire=300)                           
            except Exception as e:
                logger.error('%s %s option chain for %s not found' %(symbol, otype, exp_date))
                logger.exception(e)            
                continue

        if math.isnan(max_strike_ratio) != True:
            i =  chain.shape[0]
            chain = chain[(abs(chain[quote.STRIKE]-stock_price)/stock_price) < max_strike_ratio ]
            #print('%s %d -> %d %s filtered on strike ratio <= %.2f' % (get_option_chain.__name__, i, chain.shape[0], otype, max_strike_ratio))
            #logger.debug('%d -> %d %s filtered on strike ratio <= %.2f' % (i, chain.shape[0], otype, max_strike_ratio))

        chain = convert_yahoo_df(chain)      

        #chain[quote.PNL] = np.nan     
        #chain[quote.PROFIT] = np.nan      
        if afterHours():
            chain[quote.PRICE] = chain[quote.LAST_PRICE]             
        else:
            chain[quote.PRICE] = (chain[quote.BID] + chain[quote.ASK]) / 2         
                    
        chain[quote.BID_ASK_SPREAD] = (chain[quote.ASK] - chain[quote.BID])

        S = stock_price
        
        #predList = predicted_list(symbol, exp_date)

        chain[quote.SYMBOL]   = symbol
        chain[quote.EXP_DATE] = exp_date
        if otype == at.CALL:
            chain[quote.OTYPE] = at.CALL
            chain[quote.DELTA] = chain.apply(lambda x: delta_call(S, x[quote.STRIKE], time_to_maturity_in_year(today, pd.Timestamp(x[quote.EXP_DATE]).date())),axis=1)
            chain[quote.THETA] = chain.apply(lambda x: theta_call(S, x[quote.STRIKE], time_to_maturity_in_year(today, pd.Timestamp(x[quote.EXP_DATE]).date())),axis=1)
            #chain[quote.BREAKEVEN_LONG] = chain.apply(lambda x: x[quote.STRIKE] + x[quote.PRICE], axis=1)
            #chain[quote.BREAKEVEN_SHORT] = chain.apply(lambda x: x[quote.STRIKE] - x[quote.PRICE], axis=1)
            #chain[quote.WIN_PROB_LONG] = chain.apply(lambda x: calc_prob_higher_than(predList, x[quote.BREAKEVEN_LONG]), axis=1)
            #chain[quote.WIN_PROB_SHORT] = chain.apply(lambda x: calc_prob_lower_than(predList, x[quote.BREAKEVEN_SHORT]), axis=1)
            chain[quote.IN_MONEY] = chain.apply(lambda x: stock_price - x[quote.STRIKE] , axis=1)
        else:
            chain[quote.OTYPE] = at.PUT
            chain[quote.DELTA] = chain.apply(lambda x: delta_put(S, x[quote.STRIKE], time_to_maturity_in_year(today, pd.Timestamp(x[quote.EXP_DATE]).date())),axis=1)                 
            chain[quote.THETA] = chain.apply(lambda x: theta_put(S, x[quote.STRIKE], time_to_maturity_in_year(today, pd.Timestamp(x[quote.EXP_DATE]).date())),axis=1)
            #chain[quote.BREAKEVEN_LONG] = chain.apply(lambda x: x[quote.STRIKE] - x[quote.PRICE], axis=1)
            #chain[quote.BREAKEVEN_SHORT] = chain.apply(lambda x: x[quote.STRIKE] + x[quote.PRICE], axis=1)
            #chain[quote.WIN_PROB_LONG] = chain.apply(lambda x: calc_prob_lower_than(predList, x[quote.BREAKEVEN_LONG]), axis=1)
            #chain[quote.WIN_PROB_SHORT] = chain.apply(lambda x: calc_prob_higher_than(predList, x[quote.BREAKEVEN_SHORT]), axis=1)
            chain[quote.IN_MONEY] = chain.apply(lambda x: x[quote.STRIKE] - stock_price, axis=1)

        chain[quote.GAMMA] == chain.apply(lambda x: gamma(S, x[quote.STRIKE], time_to_maturity_in_year(today, pd.Timestamp(x[quote.EXP_DATE]).date())),axis=1)
        chain[quote.VEGA] = chain.apply(lambda x: vega(S, x[quote.STRIKE], time_to_maturity_in_year(today, pd.Timestamp(x[quote.EXP_DATE]).date())),axis=1)
        chain[quote.STOCK_PRICE] = stock_price
        chain[quote.DAYS_TO_EXPIRE] = days_to_expire

        all_chain = pd.concat([all_chain, chain])

    #if math.isnan(max_price) != True:
    #    i =  chain.shape[0]
    #    chain = chain[chain[quote.PRICE] <= max_price]
        #print('%s %d -> %d %s filtered on max price <= %.2f' % (get_option_chain.__name__, i, chain.shape[0], otype, max_price))
    #    logger.debug('%d -> %d %s filtered on max price <= %.2f' % (i, chain.shape[0], otype, max_price))

    chain = all_chain

    #if math.isnan(min_price) != True:
    #    i =  chain.shape[0]
    #    chain = chain[chain[quote.PRICE] >= min_price]
    #    #print('%s %d -> %d %s filtered out min price >= %.2f' % (get_option_chain.__name__, i, chain.shape[0], otype, min_price))
    #    logger.debug('%d -> %d %s filtered on min price >= %.2f' % (i, chain.shape[0], otype, min_price))

    if afterHours() == False:
        if math.isnan(max_bid_ask_spread) != True:
            i =  chain.shape[0]
            chain = chain[chain[quote.BID_ASK_SPREAD] <= max_bid_ask_spread]
            #print('%s %d -> %d %s filtered on bid/ask spread <= %.2f' % (get_option_chain.__name__, i, chain.shape[0], otype, max_bid_ask_spread))
            logger.debug('%d -> %d %s filtered on bid/ask spread <= %.2f' % (i, chain.shape[0], otype, max_bid_ask_spread))

        if math.isnan(min_open_interest) != True:
            i = chain.shape[0]
            chain = chain[chain[quote.OPEN_INTEREST] >= min_open_interest]
            #print('%s %d -> %d %s filtered on openInteretst >= %d' % (get_option_chain.__name__, i, chain.shape[0], otype, min_open_interest))
            logger.debug('%d -> %d %s filtered on openInteretst >= %d' % (i, chain.shape[0], otype, min_open_interest))

    return chain

def get_option_leg_IV_delta(symbol, exp_date, otype):
 
    logger = logging.getLogger(__name__)

    trade_date = datetime.now().astimezone(timezone(app_settings.TIMEZONE)).date()     
 
    stock_price = get_price_history(symbol, period='1d', interval='1d')['Close'][-1]
    q = get_ticker(symbol)

    if otype == at.CALL:
        opt = q.option_chain(exp_date).calls    
    else:
        opt = q.option_chain(exp_date).puts    

    leg = opt[opt[quote.STRIKE] >= stock_price]  

    if leg.shape[0] > 0:         
        iv =  round(leg[quote.IMPLIED_VOLATILITY].head(1).values[0],3)
        strike = leg[quote.STRIKE].head(1).values[0]
        T = time_to_maturity_in_year(trade_date, exp_date)        
        if T == 0:
            logger.error('T==0 trade date %s exp_date%s' % (str(trade_date), exp_date))
            delta = np.nan
        else:
            delta = delta_call(stock_price, strike, T)    
        return iv, delta
    else:
        return np.nan, np.nan

def get_option_leg_details(symbol, stock_price, exp_date, strike, otype):

    logger = logging.getLogger(__name__)   

    option_leg_key =symbol+'option_leg'+str(strike)+otype+exp_date
    #logger.info(option_leg_key)
    if option_leg_key in cache:
        return cache[option_leg_key]
    
    '''
    if afterHours() == False:    
        ib = IBClient.get_client()
        if ib != None:
            x = IB_get_option_leg_details(symbol, exp_date, strike, otype) 
            if x == None:
                logger.debug("Failed to get option quote from IB, try yahoo next")
            else:        
                cache.set(option_leg_key, x, expire=300)                            
                return x
    '''        
    trade_date = datetime.now().astimezone(timezone(app_settings.TIMEZONE)).date()

    q = get_ticker(symbol)

    if otype == at.CALL:
        cache_key =symbol+'call_chain'+exp_date               
        if cache_key in cache:
            calls = cache[cache_key]
        else:
            calls = q.option_chain(exp_date).calls         
            cache.set(cache_key, calls, expire=300)                 
        
        calls[quote.EXP_DATE] = exp_date
        leg = calls[calls[quote.STRIKE]==strike]             
        if leg.shape[0] == 0:
            logger.error('cannot find leg detail %s %s %.1f %s' % (symbol, exp_date, strike, otype))            
            return {}       
        leg = convert_yahoo_df(leg)           
        leg = leg.to_dict('records')[0]               
        leg[quote.DELTA] = delta_call(stock_price, 
                            strike, 
                            time_to_maturity_in_year(trade_date, exp_date))
 
    elif otype == at.PUT:
        cache_key =symbol+'put_chain'+exp_date          
        if cache_key in cache:
            puts = cache[cache_key]
        else:
            puts = q.option_chain(exp_date).puts        
            cache.set(cache_key, puts, expire=300) 

        puts[quote.EXP_DATE] = exp_date
        leg = puts[puts[quote.STRIKE]==strike]
        if leg.shape[0] == 0:
            logger.error('cannot find leg detail %s %s %.1f %s' % (symbol, exp_date, strike, otype))            
            return {}           
        leg = convert_yahoo_df(leg)   
        leg = leg.to_dict('records')[0]    
        leg[quote.DELTA] = delta_put(stock_price, 
                                strike, 
                                time_to_maturity_in_year(trade_date, exp_date))

    else:
        logger.error('invalie otype %s %s %.1f %s' % (symbol, exp_date, strike, otype))            
        return {}
    
    cache.set(option_leg_key, leg, expire=300)         

    return leg            
 
def pick_option_long( symbol, 
                      otype,                   
                      predictlist,
                      max_strike_ratio=0.25,          
                      min_pnl = 0.25,                                             
                      min_win_prob=0.2,
                      max_bid_ask_spread=np.nan,
                      min_open_interest=np.nan):

    logger = logging.getLogger(__name__)   

    if  otype not in [at.CALL, at.PUT]:
        logger.error('Invaid option type %s given' % otype)
        return pd.DataFrame()

    exp_date_list = predictlist['exp_date_list']

    chain = get_option_chain(symbol, 
                            otype,                         
                            exp_date_list= exp_date_list,                            
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)

    if chain.shape[0] == 0:
        return pd.DataFrame()

    single_df = pd.DataFrame()    

    stock_price = get_price_history(symbol, period='1d', interval='1d')['Close'][-1]

    for exp_date in exp_date_list:  
        target_low = predictlist[exp_date][quote.LOW]      
        target_high = predictlist[exp_date][quote.HIGH]                     
        if otype == at.CALL:              
            calls = chain[(chain[quote.STRIKE] < stock_price) & (chain[quote.EXP_DATE]==exp_date)] 
            calls.sort_values(by=[quote.STRIKE], ascending = False, inplace=True)
            for i, call in calls.iterrows():                           
                df = create_single_df(call, stock_price, target_high, target_low, credit=False)
                if df.at[0, option_summary.PNL] < min_pnl:
                    break              
                single_df = pd.concat([single_df, df])
        elif otype == at.PUT:               
            puts = chain[(chain[quote.STRIKE] > stock_price) & (chain[quote.EXP_DATE]==exp_date)]
            puts.sort_values(by=[quote.STRIKE], inplace=True)            
            for i, put in puts.iterrows():                         
                df = create_single_df(put, stock_price, target_high, target_low, credit=False)
                if df.at[0, option_summary.PNL] < min_pnl:
                    break                  
                single_df = pd.concat([single_df, df])

    if single_df.shape[0] == 0:
        return pd.DataFrame()
    
    win_prob_range = '[%.2f|%.2f]' % (single_df[option_summary.WIN_PROB].min(), single_df[option_summary.WIN_PROB].max())
    i = single_df.shape[0]
    single_df= single_df[single_df[option_summary.WIN_PROB] >= min_win_prob]
    #print('%s %d -> %d fillterd out by win prob >= %.2f' % (inspect.currentframe().f_code.co_name, i, spread_df.shape[0], min_win_prob))
    logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, single_df.shape[0], min_win_prob, win_prob_range))


    return single_df

def pick_option_short( symbol, 
                      otype,                   
                      predictlist,
                      min_pnl = 0.25,
                      min_price = 1.0,
                      max_strike_ratio=0.25,                             
                      min_win_prob=0.2,
                      max_bid_ask_spread=np.nan,
                      min_open_interest=np.nan):

    logger = logging.getLogger(__name__)   

    if  otype not in [at.CALL, at.PUT]:
        logger.error('Invaid option type %s given' % otype)
        return pd.DataFrame()

    exp_date_list = predictlist['exp_date_list']

    chain = get_option_chain(symbol, 
                            otype,                         
                            exp_date_list= exp_date_list,                            
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)

    if chain.shape[0] == 0:
        return pd.DataFrame()

    single_df = pd.DataFrame()    

    stock_price = get_price_history(symbol, period='1d', interval='1d')['Close'][-1]

    for exp_date in exp_date_list:  
        target_low = predictlist[exp_date][quote.LOW]      
        target_high = predictlist[exp_date][quote.HIGH]      
        if otype == at.CALL:              
            calls = chain[(chain[quote.STRIKE] > stock_price) & (chain[quote.EXP_DATE]==exp_date)]
            calls.sort_values(by=[quote.STRIKE], inplace=True)                
            for i, call in calls.iterrows():       
                df = create_single_df(call, stock_price, target_high, target_low, credit=True)
                if df.at[0, option_summary.PNL] < min_pnl:
                    break                  
                single_df = pd.concat([single_df, df])
        elif otype == at.PUT:                
            puts = chain[(chain[quote.STRIKE] < stock_price) & (chain[quote.EXP_DATE]==exp_date)]
            puts.sort_values(by=[quote.STRIKE], ascending = False, inplace=True)                
            for i, put in puts.iterrows():                   
                df = create_single_df(put, stock_price, target_high, target_low, credit=True)
                if df.at[0, option_summary.PNL] < min_pnl:
                    break                       
                single_df = pd.concat([single_df, df])

    if single_df.shape[0] == 0:
        return pd.DataFrame()
    
    open_price_range = '[%.2f|%.2f]' % (single_df[option_summary.OPEN_PRICE].min(), single_df[option_summary.OPEN_PRICE].max())
    i = single_df.shape[0]
    single_df= single_df[single_df[option_summary.OPEN_PRICE] >= min_price]
    logger.debug('%d -> %d reduced by open price >= %.2f %s' % (i, single_df.shape[0], min_price, open_price_range))

    win_prob_range = '[%.2f|%.2f]' % (single_df[option_summary.WIN_PROB].min(), single_df[option_summary.WIN_PROB].max())
    i = single_df.shape[0]
    single_df= single_df[single_df[option_summary.WIN_PROB] >= min_win_prob]
    logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, single_df.shape[0], min_win_prob, win_prob_range))

    return single_df

def pick_vertical_put_spreads( symbol,                          
                                predictlist,
                                credit=True,
                                max_spread = 10,
                                max_strike_ratio=0.25,
                                min_pnl=0.2,                                
                                min_win_prob=np.nan,
                                max_bid_ask_spread=np.nan,
                                min_open_interest=np.nan):

    logger = logging.getLogger(__name__)   

    exp_date_list = predictlist['exp_date_list']

    puts = get_option_chain(symbol, 
                            at.PUT,                         
                            exp_date_list= exp_date_list,                               
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)     
    
    spread_df = pd.DataFrame()        

    for exp_date in exp_date_list:

        target_low = predictlist[exp_date][quote.LOW]    

        target_high = predictlist[exp_date][quote.HIGH]    

        tputs = puts[ (puts[quote.STRIKE]  >= target_low ) &
                        (puts[quote.STRIKE]  <= target_high ) &
                        (puts[quote.EXP_DATE]==exp_date)]        

        if tputs.shape[0] == 0:
            continue

        if credit:    
            for i, sleg in tputs.iterrows():       
                tlputs = puts[(puts[quote.STRIKE]   <   sleg[quote.STRIKE]) &
                              (puts[quote.STRIKE]   >=  sleg[quote.STRIKE]-max_spread) &
                              (puts[quote.EXP_DATE] ==  exp_date)]  

                if tlputs.shape[0] == 0:
                    logger.debug('Cannot find long legs for %s %.2f' % (str(sleg[quote.EXP_DATE]), sleg[quote.STRIKE]))
                    continue            

                tlputs.sort_values(quote.STRIKE, ascending=False, inplace=True)                                     
                for j, lleg in tlputs.iterrows():                                             
                    df = create_spread_df(target_low, target_high, sleg, lleg, at.PUT) 
                    spread_df = pd.concat([spread_df, df])
        else:
            for i, lleg in tputs.iterrows():

                sputs = puts[(puts[quote.STRIKE]   <   lleg[quote.STRIKE]) &
                             (puts[quote.STRIKE]   >=  lleg[quote.STRIKE]-max_spread) &
                             (puts[quote.EXP_DATE] ==  exp_date)]                  
                if sputs.shape[0] == 0:
                    logger.debug('Cannot find short legs for %s %.2f' % (str(lleg[quote.EXP_DATE]), lleg[quote.STRIKE]))
                    continue                                           

                for j, sleg in sputs.iterrows(): 
                    df = create_spread_df(target_low, target_high, sleg, lleg, at.PUT, credit=False)                                                                             
                    spread_df = pd.concat([spread_df, df])

    if spread_df.shape[0] > 0:

        win_prob_range = '[%.2f|%.2f]' % (spread_df[option_summary.WIN_PROB].min(), spread_df[option_summary.WIN_PROB].max())
        i = spread_df.shape[0]
        spread_df= spread_df[spread_df[option_summary.WIN_PROB] >= min_win_prob]
        logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, spread_df.shape[0], min_win_prob, win_prob_range))

        pnl_range = '[%.2f|%.2f]' % (spread_df[option_summary.PNL].min(), spread_df[option_summary.PNL].max())
        i = spread_df.shape[0]
        spread_df= spread_df[spread_df[option_summary.WIN_PROB] >= min_pnl]
        logger.debug('%d -> %d reduced by pnl >= %.2f %s' % (i, spread_df.shape[0], min_pnl, pnl_range))

    return spread_df
 
def pick_vertical_call_spreads(symbol,                          
                                predictlist,
                                credit=True,
                                max_spread = 10,
                                max_strike_ratio=0.25,
                                min_pnl=0.2,                                
                                min_win_prob=np.nan,
                                max_bid_ask_spread=np.nan,
                                min_open_interest=np.nan):

    logger = logging.getLogger(__name__)   

    spread_df = pd.DataFrame()

    exp_date_list = predictlist['exp_date_list']

    calls = get_option_chain(symbol, 
                            at.CALL,                         
                            exp_date_list= exp_date_list,                               
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)    
    
    stock_price = get_price_history(symbol, period='1d', interval='1d')['Close'][-1]

    for exp_date in exp_date_list:

        target_low = predictlist[exp_date][quote.LOW]    
        target_high = predictlist[exp_date][quote.HIGH]    

        tcalls = calls[ (calls[quote.STRIKE]  >= target_low ) &
                        (calls[quote.STRIKE]  <= target_high ) &
                        (calls[quote.EXP_DATE] == exp_date)]   
        
        if tcalls.shape[0] == 0:
            continue 
                
        if credit:                     
            tcalls.sort_values(quote.STRIKE,  ascending=False, inplace=True)        
            for i, sleg in tcalls.iterrows():   
                lcalls = calls[(calls[quote.STRIKE]   >   sleg[quote.STRIKE]) & 
                               (calls[quote.STRIKE]   <=  sleg[quote.STRIKE]+max_spread) &
                               (calls[quote.EXP_DATE] ==  sleg[quote.EXP_DATE])]

                if lcalls.shape[0] == 0:
                    logger.debug('Cannot find long legs for %s %.2f' % (str(sleg[quote.EXP_DATE]), sleg[quote.STRIKE]))
                    continue            
                lcalls.sort_values(quote.STRIKE, inplace=True)                            
                for j, lleg in lcalls.iterrows():
                    #print('long strike', lleg[quote.STRIKE])                                                       
                    df = create_spread_df(target_low, target_high, sleg, lleg, at.CALL)      
                    spread_df = pd.concat([spread_df, df])          
        else:                 
            for i, lleg in tcalls.iterrows():
                scalls = calls[ (calls[quote.STRIKE]   >   lleg[quote.STRIKE]) &
                                (calls[quote.STRIKE]   <=  lleg[quote.STRIKE]+max_spread) &
                                (calls[quote.EXP_DATE] ==  lleg[quote.EXP_DATE])]

                if scalls.shape[0] == 0:
                    logger.debug('Cannot find short legs for %s %.2f' % (str(lleg[quote.EXP_DATE]), lleg[quote.STRIKE]))
                    continue                                           

                for j, sleg in scalls.iterrows():                    
                    df = create_spread_df(target_low, target_high, sleg, lleg, at.CALL, credit=False)                                       
                    spread_df = pd.concat([spread_df, df])


    if spread_df.shape[0] > 0:

        win_prob_range = '[%.2f|%.2f]' % (spread_df[option_summary.WIN_PROB].min(), spread_df[option_summary.WIN_PROB].max())
        i = spread_df.shape[0]
        spread_df= spread_df[spread_df[option_summary.WIN_PROB] >= min_win_prob]
        logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, spread_df.shape[0], min_win_prob, win_prob_range))

        pnl_range = '[%.2f|%.2f]' % (spread_df[option_summary.PNL].min(), spread_df[option_summary.PNL].max())
        i = spread_df.shape[0]
        spread_df= spread_df[spread_df[option_summary.WIN_PROB] >= min_pnl]
        logger.debug('%d -> %d reduced by pnl >= %.2f %s' % (i, spread_df.shape[0], min_pnl, pnl_range))

    return spread_df

def pick_iron_condor(symbol,                                              
                    predictlist,
                    credit=True,                    
                    max_spread=10,
                    max_strike_ratio=0.25,                           
                    min_price=1.0,
                    min_pnl=0.2,                                
                    min_win_prob=np.nan,
                    max_bid_ask_spread=np.nan,
                    min_open_interest=np.nan):

    logger = logging.getLogger(__name__)   

    exp_date_list = predictlist['exp_date_list']

    put_chain = get_option_chain(symbol, 
                            at.PUT,                         
                            exp_date_list=exp_date_list,
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)

    call_chain = get_option_chain(symbol, 
                            at.CALL,                         
                            exp_date_list=exp_date_list,
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)


    iron_condor_df = pd.DataFrame()

    strategy = st.CREDIT_IRON_CONDOR if credit else st.DEBIT_IRON_CONDOR

    logger.debug('%s %s' %(symbol, strategy))

    for exp_date in exp_date_list:
        target_low = predictlist[exp_date][quote.LOW]      
        target_high = predictlist[exp_date][quote.HIGH]     
        target_mid = (target_low+target_high) / 2

        if credit:

            phs = put_chain[(put_chain[quote.STRIKE]   >= target_low ) &
                        (put_chain[quote.STRIKE]   <= target_mid) &
                        (put_chain[quote.PRICE]    >= min_price) &                        
                        (put_chain[quote.EXP_DATE] == exp_date)]    
        else:

            phs = put_chain[(put_chain[quote.STRIKE]   >= target_mid ) &
                        (put_chain[quote.STRIKE]   <= target_high) &
                        (put_chain[quote.PRICE]    >= min_price) &                        
                        (put_chain[quote.EXP_DATE] == exp_date)]            

        if phs.shape[0] == 0:
            continue    

        for i, ph in phs.iterrows():       
            pls = put_chain[(put_chain[quote.STRIKE]   <   ph[quote.STRIKE]) &
                            (put_chain[quote.STRIKE]   >=  ph[quote.STRIKE]-max_spread) &
                            (put_chain[quote.EXP_DATE] ==  exp_date)]  

            if pls.shape[0] == 0:
                continue

            for j, pl in pls.iterrows():    
                spread = ph[quote.STRIKE] - pl[quote.STRIKE]                                      
                if credit:
                    cls =  call_chain[(call_chain[quote.EXP_DATE] == exp_date)  &
                                      (call_chain[quote.STRIKE] > ph[quote.STRIKE])]  
                    for k, cl in cls.iterrows():
                        chs = call_chain[(call_chain[quote.EXP_DATE] == exp_date)  &
                                         (call_chain[quote.STRIKE] == cl[quote.STRIKE]+spread)]  

                        if chs.shape[0] == 0:
                            continue

                        for l, ch in chs.iterrows():
                            df = create_iron_condor_df(strategy, target_low, target_high, pl=pl, ph=ph, cl=cl, ch=ch)              
                            iron_condor_df = pd.concat([iron_condor_df, df])
                else:
                    chs =  call_chain[(call_chain[quote.EXP_DATE] == exp_date)  &
                                      (call_chain[quote.PRICE]    >= min_price) &                                            
                                      (call_chain[quote.STRIKE] < pl[quote.STRIKE])]  
                 
                    for k, ch in chs.iterrows():
                        cls = call_chain[(call_chain[quote.EXP_DATE] == exp_date)  &
                                         (call_chain[quote.STRIKE] == ch[quote.STRIKE]-spread)]  

                        if cls.shape[0] == 0:
                            continue

                        for l, cl in cls.iterrows():
                            df = create_iron_condor_df(strategy, target_low, target_high, pl=pl, ph=ph, cl=cl, ch=ch)              
                            iron_condor_df = pd.concat([iron_condor_df, df])

    if iron_condor_df.shape[0] == 0:
        return pd.DataFrame()
    
    open_price_range = '[%.2f|%.2f]' % (iron_condor_df[option_summary.OPEN_PRICE].min(), iron_condor_df[option_summary.OPEN_PRICE].max())
    i = iron_condor_df.shape[0]
    iron_condor_df = iron_condor_df[iron_condor_df[option_summary.OPEN_PRICE] >= min_price]
    logger.debug('%d -> %d reduced by open price >= %.2f %s' % (i, iron_condor_df.shape[0], min_price, open_price_range))

    win_prob_range = '[%.2f|%.2f]' % (iron_condor_df[option_summary.WIN_PROB].min(), iron_condor_df[option_summary.WIN_PROB].max())
    i = iron_condor_df.shape[0]
    iron_condor_df= iron_condor_df[iron_condor_df[option_summary.WIN_PROB] >= min_win_prob]
    logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, iron_condor_df.shape[0], min_win_prob, win_prob_range))

    pnl_range = '[%.2f|%.2f]' % (iron_condor_df[option_summary.PNL].min(), iron_condor_df[option_summary.PNL].max())
    i = iron_condor_df.shape[0]
    iron_condor_df= iron_condor_df[iron_condor_df[option_summary.WIN_PROB] >= min_pnl]
    logger.debug('%d -> %d reduced by pnl >= %.2f %s' % (i, iron_condor_df.shape[0], min_pnl, pnl_range))

    return iron_condor_df

def pick_call_butterfly(symbol,                         
                    predictlist, 
                    spread_list=[],
                    credit=True,
                    max_spread=10,
                    max_strike_ratio=0.25,                             
                    min_price = np.nan,
                    min_pnl=np.nan,                                
                    min_win_prob=np.nan,
                    max_bid_ask_spread=np.nan,
                    min_open_interest=np.nan):
    
    logger = logging.getLogger(__name__)   

    exp_date_list = predictlist['exp_date_list']

    chain = get_option_chain(symbol, 
                            at.CALL,                         
                            exp_date_list=exp_date_list,
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)

    
    butterfly_df = pd.DataFrame()

    strategy = st.CREDIT_CALL_BUTTERFLY if credit else st.DEBIT_CALL_BUTTERFLY

    for exp_date in exp_date_list:

        target_low = predictlist[exp_date][quote.LOW]    

        target_high = predictlist[exp_date][quote.HIGH]    

        target_price = (predictlist[exp_date][quote.HIGH]+predictlist[exp_date][quote.LOW])/2

        mall = chain[(abs(chain[quote.STRIKE]-target_price) < 2.5)]

        if mall.shape[0] == 0:
            continue

        mexp = mall[mall[quote.EXP_DATE]==exp_date]
        if mexp.shape[0] == 0:
            continue

        m = mexp.head(1).to_dict('records')[0]

        ls =  chain[(chain[quote.EXP_DATE] == exp_date) & (m[quote.STRIKE]- chain[quote.STRIKE] > 0) & (m[quote.STRIKE] - chain[quote.STRIKE] <= max_spread)]
        if ls.shape[0] == 0:
            continue  

        for i, l in ls.iterrows():                      
            spread = m[quote.STRIKE] - l[quote.STRIKE]            
            hs =  chain[(chain[quote.EXP_DATE] == exp_date)  & (chain[quote.STRIKE] - m[quote.STRIKE] == spread)]          
            if hs.shape[0] == 0:
                continue
            h = hs.head(1).to_dict('records')[0]     

            df = create_buttrfly_df(strategy, target_low, target_high, l=l, m=m, h=h)  
            butterfly_df = pd.concat([butterfly_df, df])

    if butterfly_df.shape[0] == 0:
        return pd.DataFrame()
    
    open_price_range = '[%.2f|%.2f]' % (butterfly_df[option_summary.OPEN_PRICE].min(), butterfly_df[option_summary.OPEN_PRICE].max())
    i = butterfly_df.shape[0]
    butterfly_df = butterfly_df[butterfly_df[option_summary.OPEN_PRICE] >= min_price]
    logger.debug('%d -> %d reduce by open price >= %.2f %s' % (i, butterfly_df.shape[0], min_price, open_price_range))

    win_prob_range = '[%.2f|%.2f]' % (butterfly_df[option_summary.WIN_PROB].min(), butterfly_df[option_summary.WIN_PROB].max())
    i = butterfly_df.shape[0]
    butterfly_df= butterfly_df[butterfly_df[option_summary.WIN_PROB] >= min_win_prob]
    logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, butterfly_df.shape[0], min_win_prob, win_prob_range))

    pnl_range = '[%.2f|%.2f]' % (butterfly_df[option_summary.PNL].min(), butterfly_df[option_summary.PNL].max())
    i = butterfly_df.shape[0]
    butterfly_df= butterfly_df[butterfly_df[option_summary.WIN_PROB] >= min_pnl]
    logger.debug('%d -> %d reduced by pnl >= %.2f %s' % (i, butterfly_df.shape[0], min_pnl, pnl_range))

    return butterfly_df

def pick_put_butterfly(symbol,                          
                    predictlist,
                    spread_list=[],
                    credit=True,
                    max_spread=10,
                    max_strike_ratio=0.25,
                    min_price = np.nan,                             
                    min_pnl=np.nan,                                
                    min_win_prob=np.nan,
                    max_bid_ask_spread=np.nan,
                    min_open_interest=np.nan):
    
    logger = logging.getLogger(__name__)   

    exp_date_list = predictlist['exp_date_list']

    chain = get_option_chain(symbol, 
                            at.PUT,                         
                            exp_date_list=exp_date_list,
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)
        

    butterfly_df = pd.DataFrame()

    strategy = st.CREDIT_PUT_BUTTERFLY if credit else st.DEBIT_PUT_BUTTERFLY

    for exp_date in exp_date_list:
        
        target_low = predictlist[exp_date][quote.LOW]    

        target_high = predictlist[exp_date][quote.HIGH]    

        target_price = (predictlist[exp_date][quote.HIGH]+predictlist[exp_date][quote.LOW])/2

        mall = chain[(abs(chain[quote.STRIKE]-target_price) < 2.5)]
        if mall.shape[0] == 0:
            continue    

        mexp = mall[mall[quote.EXP_DATE]==exp_date]
        if mexp.shape[0] == 0:
            continue
        m = mexp.head(1).to_dict('records')[0]        
        ls =  chain[(chain[quote.EXP_DATE] == exp_date) & (m[quote.STRIKE]- chain[quote.STRIKE] > 0) & (m[quote.STRIKE] - chain[quote.STRIKE] <= max_spread)]
        if ls.shape[0] == 0:
            continue  
        for i, l in ls.iterrows():                      
            spread = m[quote.STRIKE] - l[quote.STRIKE]              
            hs =  chain[(chain[quote.EXP_DATE] == exp_date)  & (chain[quote.STRIKE]-m[quote.STRIKE]==spread)]          
            if hs.shape[0] == 0:
                continue
            h = hs.head(1).to_dict('records')[0]                
            df = create_buttrfly_df(strategy, target_low, target_high, l=l, m=m, h=h)  
            butterfly_df = pd.concat([butterfly_df, df])

    if butterfly_df.shape[0] == 0:
        return pd.DataFrame()
    
    open_price_range = '[%.2f|%.2f]' % (butterfly_df[option_summary.OPEN_PRICE].min(), butterfly_df[option_summary.OPEN_PRICE].max())
    i = butterfly_df.shape[0]
    butterfly_df = butterfly_df[butterfly_df[option_summary.OPEN_PRICE] >= min_price]
    logger.debug('%d -> %d reduced by open price >= %.2f %s' % (i, butterfly_df.shape[0], min_price, open_price_range))

    win_prob_range = '[%.2f|%.2f]' % (butterfly_df[option_summary.WIN_PROB].min(), butterfly_df[option_summary.WIN_PROB].max())
    i = butterfly_df.shape[0]
    butterfly_df= butterfly_df[butterfly_df[option_summary.WIN_PROB] >= min_win_prob]
    logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, butterfly_df.shape[0], min_win_prob, win_prob_range))

    pnl_range = '[%.2f|%.2f]' % (butterfly_df[option_summary.PNL].min(), butterfly_df[option_summary.PNL].max())
    i = butterfly_df.shape[0]
    butterfly_df= butterfly_df[butterfly_df[option_summary.WIN_PROB] >= min_pnl]
    logger.debug('%d -> %d reduced by pnl >= %.2f %s' % (i, butterfly_df.shape[0], min_pnl, pnl_range))

    return butterfly_df

def pick_iron_butterfly(symbol,      
                    predictlist,                    
                    spread_list=[],
                    credit=True,
                    max_spread=10,
                    max_strike_ratio=0.25,
                    min_price = np.nan,
                    min_pnl=np.nan,                                
                    min_win_prob=np.nan,
                    max_bid_ask_spread=np.nan,
                    min_open_interest=np.nan):

    logger = logging.getLogger(__name__)   

    exp_date_list = predictlist['exp_date_list']

    put_chain = get_option_chain(symbol, 
                            at.PUT,                         
                            exp_date_list=exp_date_list,
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)

    call_chain = get_option_chain(symbol, 
                            at.CALL,                         
                            exp_date_list=exp_date_list,
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)


    butterfly_df = pd.DataFrame()

    strategy = st.IRON_BUTTERFLY if credit else st.REVERSE_IRON_BUTTERFLY

    for exp_date in exp_date_list:

        target_low = predictlist[exp_date][quote.LOW]    

        target_high = predictlist[exp_date][quote.HIGH]    

        target_price = (predictlist[exp_date][quote.HIGH]+predictlist[exp_date][quote.LOW])/2

        pmall = put_chain[(abs(put_chain[quote.STRIKE]-target_price) < 2.5)]

        cmall = call_chain[(abs(call_chain[quote.STRIKE]-target_price) < 2.5)]

        if cmall.shape[0] == 0 or pmall.shape[0] == 0:
            continue    

        pmexp = pmall[pmall[quote.EXP_DATE]==exp_date]
        if pmexp.shape[0] == 0:
            continue

        m = pmexp.head(1).to_dict('records')[0]    

        cmexp = cmall[(cmall[quote.EXP_DATE]==exp_date) & (cmall[quote.STRIKE] == m[quote.STRIKE])]
        if cmexp.shape[0] == 0:
            continue

        iron = cmexp.head(1).to_dict('records')[0] 

        ls =  put_chain[(put_chain[quote.EXP_DATE] == exp_date) & (m[quote.STRIKE]- put_chain[quote.STRIKE] > 0) & (m[quote.STRIKE] - put_chain[quote.STRIKE] <= max_spread)]
        if ls.shape[0] == 0:
            continue  

        for i, l in ls.iterrows():               
            spread = m[quote.STRIKE] - l[quote.STRIKE]       
            hs =  call_chain[(call_chain[quote.EXP_DATE] == exp_date)  & (call_chain[quote.STRIKE] - m[quote.STRIKE] == spread)]          
            if hs.shape[0] == 0:
                continue
            h = hs.head(1).to_dict('records')[0] 
            df = create_buttrfly_df(strategy, target_low, target_high, l=l, m=m, h=h, iron=iron)              
            butterfly_df = pd.concat([butterfly_df, df])

    if butterfly_df.shape[0] == 0:
        return pd.DataFrame()
    
    open_price_range = '[%.2f|%.2f]' % (butterfly_df[option_summary.OPEN_PRICE].min(), butterfly_df[option_summary.OPEN_PRICE].max())
    i = butterfly_df.shape[0]
    butterfly_df = butterfly_df[butterfly_df[option_summary.OPEN_PRICE] >= min_price]
    logger.debug('%d -> %d reduced by open price >= %.2f %s' % (i, butterfly_df.shape[0], min_price, open_price_range))

    win_prob_range = '[%.2f|%.2f]' % (butterfly_df[option_summary.WIN_PROB].min(), butterfly_df[option_summary.WIN_PROB].max())
    i = butterfly_df.shape[0]
    butterfly_df= butterfly_df[butterfly_df[option_summary.WIN_PROB] >= min_win_prob]
    logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, butterfly_df.shape[0], min_win_prob, win_prob_range))

    pnl_range = '[%.2f|%.2f]' % (butterfly_df[option_summary.PNL].min(), butterfly_df[option_summary.PNL].max())
    i = butterfly_df.shape[0]
    butterfly_df= butterfly_df[butterfly_df[option_summary.WIN_PROB] >= min_pnl]
    logger.debug('%d -> %d reduced by pnl >= %.2f %s' % (i, butterfly_df.shape[0], min_pnl, pnl_range))

    return butterfly_df

def create_single_df(leg, stock_price, target_high, target_low, credit=True):

    dt = {}
    symbol      = leg[quote.SYMBOL]
    today       = datetime.now(timezone(app_settings.TIMEZONE))   
    price       = leg[quote.PRICE]    
    exp_date    = leg[quote.EXP_DATE]
    symbol      = leg[quote.SYMBOL]
    otype       = leg[quote.OTYPE]
    strike      = leg[quote.STRIKE]    
    margin      = stock_price if credit else 0.0
    predList    = predicted_list(symbol, exp_date)       

    if otype == at.CALL:
        dt[option_summary.STRATEGY] = [st.COVERED_CALL if credit else st.LONG_CALL]         
        if credit:
            max_profit = price
            max_loss = strike-target_low-price
            breakeven_h =  strike-price
            breakeven_l =  np.nan
            win_prob  = calc_prob_lower_than(predList, breakeven_h) 
        else:
            max_profit = target_high-strike-price
            max_loss = price
            breakeven_l =  strike+price
            breakeven_h =  np.nan
            win_prob  = calc_prob_higher_than(predList, breakeven_l)
    else:
        dt[option_summary.STRATEGY] = [st.SHORT_PUT if credit else st.LONG_PUT]        
        pnl = stock_price if credit else np.nan
        if credit:
            max_profit = price
            max_loss = target_high-strike-price            
            breakeven_l =  strike-price
            breakeven_h =  np.nan
            win_prob = calc_prob_higher_than(predList, breakeven_l)
        else:
            max_profit = strike-target_low-price
            max_loss = price            
            breakeven_h =  strike-price
            breakeven_l =  np.nan
            win_prob = calc_prob_lower_than(predList, breakeven_h)

    pnl = max_profit / max_loss

    dt[option_summary.SYMBOL]            = [symbol]
    dt[option_summary.EXP_DATE]          = [exp_date]
    dt[option_summary.OPEN_PRICE]        = [price]
    dt[option_summary.PNL]               = [pnl]
    dt[option_summary.WIN_PROB]          = [win_prob]
    dt[option_summary.MAX_LOSS]          = [max_loss]
    dt[option_summary.MAX_PROFIT]        = [max_profit]
    dt[option_summary.MARGIN]            = [margin]
    dt[option_summary.BREAKEVEN_H]       = [breakeven_h]
    dt[option_summary.BREAKEVEN_L]       = [breakeven_l]
    dt[option_summary.TRADE_DATE]        = [today]
    dt[option_summary.TRADE_STOCK_PRICE] = [stock_price]
    dt[option_summary.SPREAD]            = [np.nan]

    dt[option_summary.TARGET_HIGH]       = [target_high]
    dt[option_summary.TARGET_LOW]        = [target_low]       

    leg[position.SCALE]                 = 1
    leg[position.OPEN_ACTION] = at.SELL_TO_OPEN if credit else at.BUY_TO_OPEN    

    dt[option_summary.LEGS] = [[leg]]

    df = pd.DataFrame.from_dict(dt)

    return df

def create_spread_df(target_low, target_high, sleg, lleg, otype, credit=True):

    logger = logging.getLogger(__name__)   

    dt = {}

    symbol   = sleg[quote.SYMBOL]
    exp_date = sleg[quote.EXP_DATE]
    spread = abs(sleg[quote.STRIKE]-lleg[quote.STRIKE])
    price =  abs(sleg[quote.PRICE]-lleg[quote.PRICE])
    if price == spread:
        price = abs( ((sleg[quote.BID]+sleg[quote.ASK])/2) - ((lleg[quote.BID]+lleg[quote.ASK])/2))

    max_profit = price if credit else spread-price
    max_loss = (spread - price) if credit else price
    today = datetime.now(timezone(app_settings.TIMEZONE))
    stock_price = get_price_history(symbol, period='1d', interval='1d')['Close'][-1]
    if max_loss == 0:
        logger.info('noway')
        pass
    pnl = 999 if max_loss == 0 else max_profit / max_loss
    margin = spread if credit else 0.0
    predList    = predicted_list(symbol, exp_date)    

    if otype == at.CALL:
        dt[option_summary.STRATEGY] = [st.CREDIT_CALL_SPREAD if credit else st.DEBIT_CALL_SPREAD]      
        if credit:
            breakeven_h =sleg[quote.STRIKE]+price
            breakeven_l = np.nan
            win_prob = calc_prob_lower_than(predList, breakeven_h)                        
        else:
            breakeven_l =lleg[quote.STRIKE]+price 
            breakeven_h = np.nan
            win_prob = calc_prob_higher_than(predList, breakeven_l)               
    else:
        dt[option_summary.STRATEGY] = [st.CREDIT_PUT_SPREAD if credit else st.DEBIT_PUT_SPREAD]        
        if credit:
            breakeven_l =sleg[quote.STRIKE]-price
            breakeven_h = np.nan
            win_prob = calc_prob_higher_than(predList, breakeven_l)                   
        else:
            breakeven_h =lleg[quote.STRIKE]-price 
            breakeven_l = np.nan
            win_prob = calc_prob_lower_than(predList, breakeven_h)     

    dt[option_summary.SYMBOL]            = [symbol]
    dt[option_summary.EXP_DATE]          = [exp_date]
    dt[option_summary.SPREAD]            = [spread]         
    dt[option_summary.LAST_PRICE]        = [price]
    dt[option_summary.OPEN_PRICE]        = [price]   
    dt[option_summary.MAX_LOSS]          = [max_loss]
    dt[option_summary.MAX_PROFIT]        = [max_profit]
    dt[option_summary.MARGIN]            = [margin]
    dt[option_summary.PNL]               = [pnl]
    dt[option_summary.BREAKEVEN_H]       = [breakeven_h]
    dt[option_summary.BREAKEVEN_L]       = [breakeven_l]
    dt[option_summary.WIN_PROB]          = [win_prob] 
    dt[option_summary.TRADE_DATE]        = [today] 
    dt[option_summary.TRADE_STOCK_PRICE] = [stock_price]
    dt[option_summary.TARGET_HIGH]       = [target_high]
    dt[option_summary.TARGET_LOW]        = [target_low]    

    sleg[position.OPEN_ACTION] = at.SELL_TO_OPEN
    lleg[position.OPEN_ACTION] = at.BUY_TO_OPEN
    sleg[position.SCALE] = 1
    lleg[position.SCALE] = 1
    sleg[position.SYMBOL] = lleg[position.SYMBOL] = symbol
    sleg[position.EXP_DATE] = lleg[position.EXP_DATE] = exp_date
 

    dt[option_summary.LEGS] = [[sleg, lleg]]

    df = pd.DataFrame.from_dict(dt)
    return df

def create_buttrfly_df(strategy, target_low, target_high, l={}, m={}, h={}, iron={}):
  
    logger = logging.getLogger(__name__)   

    dt = {}

    symbol          = m[quote.SYMBOL]
    spread          = m[quote.STRIKE]-l[quote.STRIKE]
    exp_date        = m[quote.EXP_DATE]
    days_to_expire  = m[quote.DAYS_TO_EXPIRE]  
    stock_price     = get_price_history(symbol, period='1d', interval='1d')['Close'][-1]
    today           = datetime.now(timezone(app_settings.TIMEZONE))
    if strategy == st.REVERSE_IRON_BUTTERFLY or strategy == st.IRON_BUTTERFLY:        
        price       = abs(l[quote.PRICE] + h[quote.PRICE] - m[quote.PRICE] - iron[quote.PRICE])               
    else:
        price       = abs(l[quote.PRICE] + h[quote.PRICE] - 2 * m[quote.PRICE])

    predList        = predicted_list(symbol, exp_date)   
    #dt[optionSummary.DAYS_TO_EXPIRE] = days_to_expire 
    m[position.SYMBOL]   = l[position.SYMBOL]   = h[position.SYMBOL] = symbol
    m[position.EXP_DATE] = l[position.EXP_DATE] = h[position.EXP_DATE] = exp_date

    if strategy == st.DEBIT_CALL_BUTTERFLY:
        margin = 0.0
        max_loss = price
        max_profit = spread-price
        breakeven_l = l[quote.STRIKE] + price    
        breakeven_h = h[quote.STRIKE] - price
        win_prob = calc_prob_between(predList, breakeven_l, breakeven_h)     
        l[position.OPEN_ACTION] = at.BUY_TO_OPEN
        m[position.OPEN_ACTION] = at.SELL_TO_OPEN
        h[position.OPEN_ACTION] = at.BUY_TO_OPEN
        l[position.SCALE] = 1
        m[position.SCALE] = 2
        h[position.SCALE] = 1
        legs =  [l, m, h]

    elif strategy == st.CREDIT_CALL_BUTTERFLY:
        max_profit = price
        max_loss = spread-price       
        margin = spread
        breakeven_h = h[quote.STRIKE] - price
        breakeven_l = l[quote.STRIKE] + price   
        win_prob = 100-calc_prob_between(predList, breakeven_l, breakeven_h)     
        
        l[position.OPEN_ACTION] = at.SELL_TO_OPEN
        m[position.OPEN_ACTION] = at.BUY_TO_OPEN
        h[position.OPEN_ACTION] = at.SELL_TO_OPEN
        l[position.SCALE] = 1
        m[position.SCALE] = 2
        h[position.SCALE] = 1

        legs = [l, m, h]
    elif strategy == st.CREDIT_PUT_BUTTERFLY: 
        max_profit = price
        max_loss = spread-price       
        margin = spread
        breakeven_h = h[quote.STRIKE] - price
        breakeven_l = l[quote.STRIKE] + price    
        win_prob = calc_prob_between(predList, breakeven_l, breakeven_h)     
               
        l[position.OPEN_ACTION] = at.SELL_TO_OPEN
        m[position.OPEN_ACTION] = at.BUY_TO_OPEN
        h[position.OPEN_ACTION] = at.SELL_TO_OPEN
        l[position.SCALE] = 1
        m[position.SCALE] = 2
        h[position.SCALE] = 1        
        legs =[l, m, h]

    elif strategy == st.DEBIT_PUT_BUTTERFLY: 
        max_loss = price
        max_profit = spread-price       
        margin = 0.0
        breakeven_h = h[quote.STRIKE] - price
        breakeven_l = l[quote.STRIKE] + price    
        win_prob = 100-calc_prob_between(predList, breakeven_l, breakeven_h)   

        l[position.OPEN_ACTION] = at.BUY_TO_OPEN
        m[position.OPEN_ACTION] = at.SELL_TO_OPEN
        h[position.OPEN_ACTION] = at.BUY_TO_OPEN
        l[position.SCALE] = 1
        m[position.SCALE] = 2
        h[position.SCALE] = 1

        legs = [l,m,h]

    elif strategy == st.REVERSE_IRON_BUTTERFLY:
        max_loss = price
        max_profit = spread-price       
        margin = 0.0
        breakeven_h = h[quote.STRIKE] - price
        breakeven_l = l[quote.STRIKE] + price    
        win_prob = 100-calc_prob_between(predList, breakeven_l, breakeven_h)  


        l[position.OPEN_ACTION] = at.SELL_TO_OPEN
        m[position.OPEN_ACTION] = at.BUY_TO_OPEN        
        iron[position.OPEN_ACTION] =at.BUY_TO_OPEN
        h[position.OPEN_ACTION] = at.SELL_TO_OPEN
        l[position.SCALE] = 1
        m[position.SCALE] = 1
        iron[position.SCALE] = 1        
        h[position.SCALE] = 1

        legs = [l, m, iron, h]

    elif strategy  == st.IRON_BUTTERFLY:
        max_loss = spread-price
        max_profit = price       
        margin = spread
        breakeven_h = h[quote.STRIKE] - price
        breakeven_l = l[quote.STRIKE] + price    

        win_prob = calc_prob_between(predList, breakeven_l, breakeven_h)             

        l[position.OPEN_ACTION] = at.BUY_TO_OPEN
        m[position.OPEN_ACTION] = at.SELL_TO_OPEN
        iron[position.OPEN_ACTION] = at.SELL_TO_OPEN
        h[position.OPEN_ACTION] = at.BUY_TO_OPEN
        
        l[position.SCALE] = 1
        m[position.SCALE] = 1
        iron[position.SCALE] = 1        
        h[position.SCALE] = 1

        legs = [l, m, iron, h]
    else:
        logger.error("Unknown strategy %s" % strategy)
        return pd.DataFrame()

    pnl = np.nan if max_loss == 0 else max_profit / max_loss
                                   
    dt[option_summary.SYMBOL]            = [symbol]
    dt[option_summary.STRATEGY]          = [strategy]
    dt[option_summary.SPREAD]            = [spread]
    dt[option_summary.EXP_DATE]          = [exp_date]
    dt[option_summary.LAST_PRICE]        = [price]
    dt[option_summary.OPEN_PRICE]        = [price]   

    dt[option_summary.MAX_PROFIT]        = [max_profit]
    dt[option_summary.MAX_LOSS]          = [max_loss]
    dt[option_summary.MARGIN]            = [margin]    
    dt[option_summary.PNL]               = [pnl]
    dt[option_summary.BREAKEVEN_H]       = [breakeven_h]
    dt[option_summary.BREAKEVEN_L]       = [breakeven_l]    
    dt[option_summary.WIN_PROB]          = [win_prob]   
    dt[option_summary.TRADE_DATE]        = [today] 
    dt[option_summary.TRADE_STOCK_PRICE] = [stock_price]
    dt[option_summary.TARGET_HIGH]       = [target_high]
    dt[option_summary.TARGET_LOW]        = [target_low]    

    dt[option_summary.LEGS] = [legs]
    df = pd.DataFrame.from_dict(dt)
    return df

def create_iron_condor_df(strategy, target_low, target_high, pl=None, ph=None, cl=None, ch=None):
    
    logger = logging.getLogger(__name__)   

    dt = {}

    symbol = pl[quote.SYMBOL]

    if strategy not in [st.CREDIT_IRON_CONDOR, st.DEBIT_IRON_CONDOR]:
        logger.error('Unsupported strategy %s' % strategy)
        return pd.DataFrame()
    
    if abs(ph[quote.STRIKE]-pl[quote.STRIKE]) != abs(ch[quote.STRIKE]-cl[quote.STRIKE]):
        logger.error('Put spread %.2f Call spread %.2f not the same' % (abs(ph[quote.STRIKE]-pl[quote.STRIKE]), abs(ch[quote.STRIKE]-cl[quote.STRIKE])))
        return pd.DataFrame()
    
    credit = True if strategy == st.CREDIT_IRON_CONDOR else False

    dt[option_summary.STRATEGY] = [strategy]
    dt[option_summary.TRADE_DATE] = datetime.now(timezone(app_settings.TIMEZONE))
    dt[option_summary.TRADE_STOCK_PRICE] = get_price_history(symbol, period='1d', interval='1d')['Close'][-1]

    spread = abs(ph[quote.STRIKE]-pl[quote.STRIKE])
    price = abs(ph[quote.PRICE]-pl[quote.PRICE]) + abs(ch[quote.PRICE]-cl[quote.PRICE])
    max_loss = spread-price if credit else price-spread 
    max_profit = price if credit else (2* spread) - price 
    margin = spread-price if credit else 0.0
    exp_date   = ph[quote.EXP_DATE]
    breakeven_l = ph[quote.STRIKE] - price if credit else ph[quote.STRIKE] + max_loss
    breakeven_h = cl[quote.STRIKE] + price if credit else cl[quote.STRIKE] - max_loss
    days_to_expire = ph[quote.DAYS_TO_EXPIRE]
    dt[option_summary.EXP_DATE]    = [exp_date]
    dt[option_summary.SYMBOL]      = [symbol]
    dt[option_summary.SPREAD]      = [spread]
    dt[option_summary.OPEN_PRICE]  = [price]    
    dt[option_summary.LAST_PRICE]  = [price]
    dt[option_summary.EXP_DATE]    = [exp_date]
    dt[option_summary.MAX_PROFIT]  = [max_profit]
    dt[option_summary.MAX_LOSS]    = [max_loss]
    dt[option_summary.MARGIN]      = [margin]    
    dt[option_summary.PNL]         = [np.nan] if max_loss == 0 else [max_profit / max_loss]
    dt[option_summary.BREAKEVEN_H] = [breakeven_h]
    dt[option_summary.BREAKEVEN_L] = [breakeven_l]
    dt[option_summary.TARGET_HIGH] = [target_high]
    dt[option_summary.TARGET_LOW]  = [target_low]       

    predList = predicted_list(symbol, exp_date) 

    win_prob = calc_prob_between(predList, breakeven_l, breakeven_h)
    
    if credit == False:
        win_prob = 100 - win_prob

    dt[option_summary.WIN_PROB]  = [win_prob]   

    ph[position.SYMBOL] = pl[position.SYMBOL] = ch[position.SYMBOL] = cl[position.SYMBOL] = symbol
    ph[position.EXP_DATE] = pl[position.EXP_DATE] = ch[position.EXP_DATE] = cl[position.EXP_DATE] = exp_date
    ph[position.SCALE] = pl[position.SCALE] = ch[position.SCALE] = cl[position.SCALE] = 1

    ph[position.OPEN_ACTION] = at.SELL_TO_OPEN if credit else at.BUY_TO_OPEN
    pl[position.OPEN_ACTION] = at.BUY_TO_OPEN if credit else at.SELL_TO_OPEN
    ch[position.OPEN_ACTION] = at.BUY_TO_OPEN if credit else at.SELL_TO_OPEN
    cl[position.OPEN_ACTION] = at.SELL_TO_OPEN if credit else at.BUY_TO_OPEN


    dt[option_summary.LEGS] = [[ph, pl, ch, cl]]

    df = pd.DataFrame.from_dict(dt)

    return df

def open_one_leg_strategy( symbol, exp_date, otype, strike, credit):                

    logger = logging.getLogger(__name__)   

    stock_price = get_price_history(symbol, period='1d', interval='1d')['Close'][-1]

    from  option_trader.utils.predictor  import predict_price_range

    predictlist = predict_price_range(symbol, target_prob=app_settings.TARGET_PROB, target_date_list=[exp_date])

    chain = get_option_chain(symbol, otype, exp_date_list= [exp_date])     

    leg = chain[chain[quote.STRIKE] == strike ] 

    if leg.shape[0] == 0:
        return pd.DataFrame()

    target_low = predictlist[exp_date][quote.LOW]    

    target_high = predictlist[exp_date][quote.HIGH]    

    df = create_single_df(leg, stock_price, target_high, target_low, credit=credit)
            
    return df

def open_vertical_spread_strategy( symbol,exp_date,otype,s_strike,l_strike):                 

    logger = logging.getLogger(__name__)   

    from  option_trader.utils.predictor  import predict_price_range
    predictlist = predict_price_range(symbol, target_prob=app_settings.TARGET_PROB, target_date_list=[exp_date])

    chain = get_option_chain(symbol, otype, exp_date_list= [exp_date])     

    sleg = chain[chain[quote.STRIKE] == s_strike ] 

    lleg = chain[chain[quote.STRIKE] == l_strike ]

    if sleg.shape[0] == 0 or lleg.shape[0] == 0:
        return pd.DataFrame()

    target_low = predictlist[exp_date][quote.LOW]    

    target_high = predictlist[exp_date][quote.HIGH]    

    df = create_spread_df(target_low, target_high, sleg, lleg, otype) 
            
    return df

def open_iron_condor_strategy( strategy, symbol, exp_date, ps_strike,pl_strike,cs_strike, cl_strike):                 

    logger = logging.getLogger(__name__)   

    if strategy not in [st.CREDIT_IRON_CONDOR, st.DEBIT_IRON_CONDOR]:
        logger.error('Strategy %s not exoected in open_iron_condor call' % strategy)
        return pd.DataFrame()

    from  option_trader.utils.predictor  import predict_price_range    
    predictlist = predict_price_range(symbol, target_prob=app_settings.TARGET_PROB, target_date_list=[exp_date])

    put_chain = get_option_chain(symbol, at.PUT, exp_date_list= [exp_date])     

    call_chain = get_option_chain(symbol, at.CALL, exp_date_list= [exp_date])   

    ps_leg = put_chain[put_chain[quote.STRIKE] == ps_strike ] 

    pl_leg = put_chain[put_chain[quote.STRIKE] == pl_strike ] 

    cs_leg = call_chain[call_chain[quote.STRIKE] == cs_strike ] 

    cl_leg = call_chain[call_chain[quote.STRIKE] == cl_strike ] 

    target_low = predictlist[exp_date][quote.LOW]    

    target_high = predictlist[exp_date][quote.HIGH]    

    if strategy == st.CREDIT_IRON_CONDOR:
        df = create_iron_condor_df(strategy, target_low, target_high, pl=pl_leg, ph=ps_leg, cl=cs_leg, ch=cl_leg)
    else:
        df = create_iron_condor_df(strategy, target_low, target_high, pl=ps_leg, ph=pl_leg, cl=cl_leg, ch=cs_leg)

    return df


if __name__ == '__main__':

    #import sys
    import numpy as np

    #sys.path.append(r'\Users\jimhu\option_trader\src')
    from option_trader.consts import asset as at
    from option_trader.utils.data_getter import get_option_chain
    from option_trader.utils.data_getter import get_price_history
    from option_trader.utils.data_getter import pick_call_butterfly

    import warnings
    warnings.filterwarnings("ignore")

    import logging
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    from option_trader.settings.log_config import LOGGING
    #LOGGING['loggers']['']['level'] = 'DEBUG'
    #logging.config.dictConfig(LOGGING)

    symbol = 'MSFT'

    get_next_earning_date(symbol)

    exit(0)
    target_price =get_price_history(symbol)['Close'].iloc[-1]

    df =  pick_vertical_put_spreads(  symbol,                          
                                target_price,
                                credit=True,
                                exp_date_list=[],
                                spread_list=[],
                                min_price=np.nan,
                                max_spread = 10,
                                max_strike_ratio=0.25,
                                min_pnl=np.nan,                                
                                min_win_prob=np.nan,
                                max_bid_ask_spread=np.nan,
                                max_days_to_expire=np.nan, 
                                min_open_interest=np.nan)
    

    print(df)

    exit(0)

    print(get_option_exp_date(symbol))

    exit(0)
    current_price = get_price_history(symbol, period='1d', interval='1d')['Close'][-1]

    iv, delta = get_option_leg_IV_delta(symbol, datetime.strptime('2023-06-09','%Y-%m-%d').date(), datetime.strptime('2023-06-16','%Y-%m-%d').date(), current_price, at.CALL)
    print(iv)
    print(delta)
    #print(get_option_leg_IV(symbol, '2023-06-16', 300, at.PUT))

    exit(0)

    current_price =get_price_history(symbol)['Close'].iloc[-1]

    target_upper_price =  current_price + 5

    target_lower_price = current_price - 5


    cic = pick_iron_condor(symbol,                          
                            target_upper_price,
                            target_lower_price,
                            credit=False,
                            min_price= 0,
                            max_spread = 10,
                            exp_date_list=[],
                            spread_list=[],
                            min_pnl=0.0,
                            min_win_prob=50,
                            min_annualized_return=0,
                            max_bid_ask_spread=10,
                            max_days_to_expire=90, 
                            min_open_interest=100)

    def dump_chain(chain):
        print('----------')    
        print(chain[[quote.DAYS_TO_EXPIRE, quote.SPREAD, quote.PRICE, quote.MAX_PROFIT, quote.MARGIN, quote.MAX_LOSS, quote.PNL, quote.WIN_PROB, quote.BREAKEVEN_L, quote.BREAKEVEN_H, quote.ANNUALIZED_RETURN, quote.P1_ST, quote.P1_SK, quote.P1_LK, quote.P2_ST, quote.P2_SK, quote.P2_LK]])


    if cic.shape[0] > 0:
        dump_chain(cic)