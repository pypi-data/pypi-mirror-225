schema = "symbol TEXT,strategy TEXT, credit TEXT, status TEXT, exp_date TEXT,\
        spread REAL, open_price REAL,breakeven_l REAL, breakeven_h REAL,\
        max_profit REAL, max_loss REAL,pnl REAL, win_prob REAL, last_win_prob,\
        trade_date TEXT,earning_date TEXT,trade_stock_price REAL,\
        margin REAL,quantity REAL, last_quote_date,\
        last_stock_price REAL,exp_stock_price REAL,\
        last_price REAL,exp_price REAL,pl REAL,gain REAL,\
        stop_price REAL,stop_date TEXT,stop_reason TEXT,\
        order_id TEXT,uuid TEXT,legs_desc TEXT,\
        target_low, target_high,\
        primary key(uuid)"

SYMBOL           = 'symbol'
CREDIT           = 'credit'
STRATEGY         = 'strategy' 
SPREAD           = 'spread' 
EXP_DATE         = 'exp_date'
OPEN_PRICE       = 'open_price'
LAST_PRICE       = 'last_price'        
EXP_PRICE        = 'exp_price'
PL               = 'pl'
GAIN             = 'gain'  
BREAKEVEN_L      = 'breakeven_l'
BREAKEVEN_H      = 'breakeven_h'        
MAX_PROFIT       = 'max_profit'  
MAX_LOSS         = 'max_loss'
PNL              = 'pnl'         
WIN_PROB         = 'win_prob'
LAST_WIN_PROB    = 'last_win_prob'         
TRADE_DATE       = 'trade_date'           
LAST_QUOTE_DATE  = 'last_quote_date'

EARNING_DATE      = 'earning_date'        
TRADE_STOCK_PRICE = 'trade_stock_price'
LAST_STOCK_PRICE  = 'last_stock_price'
EXP_STOCK_PRICE   = 'exp_stock_price'        
             
MARGIN            = 'margin'        
QUANTITY          = 'quantity'
STATUS            = 'status'
STOP_PRICE        = 'stop_price'    
STOP_DATE         = 'stop_date'
STOP_REASON       = 'stop_reason'    
ORDER_ID          = 'order_id'
UUID              = 'uuid'              
LEGS              = 'legs_desc'

TARGET_LOW       = 'target_low'
TARGET_HIGH      = 'target_high'

##NNUALIZED_RETURN = 'annualized_return' 

class optionSummary():

    def __init__(self):
        return
        