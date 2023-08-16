import sys

sys.path.append(r'/Users/jimhu/option_trader/src')

from option_trader.jobs import core
from option_trader.admin.site import site
from option_trader.consts import strategy 

import logging


DEFAULT_SITE_STRATEGY = [strategy.CREDIT_PUT_SPREAD, strategy.CREDIT_IRON_CONDOR]


class refresh_monitorlist():
    def __init__(self, site_name):     
        self.site_name = site_name
        self.logger = logging.getLogger(__name__)        
        return
    
    def execute(self):
        with site(self.site_name) as mysite:
            mysite.refresh_site_monitor_list()     

        return
    
class publish_watchlist_report():
    def __init__(self, site_name):     
        self.site_name = site_name
        self.logger = logging.getLogger(__name__)        
        return
    
    def execute(self):
        with site(self.site_name) as mysite:
            mysite.publish_watchlist_report()     

        return
        
if __name__ == '__main__':
    
    from logging.handlers import RotatingFileHandler
    
    from option_trader.settings import app_settings    

    FORMAT = '%(asctime)s-%(levelname)s (%(message)s) %(filename)s-%(lineno)s-%(funcName)s'
        
    ch = logging.StreamHandler()    
    #ch.setFormatter(formatter)

    import os

    if os.path.exists(app_settings.LOG_ROOT_DIR) == False:        
        os.mkdir(app_settings.LOG_ROOT_DIR)

    import datetime    
    daily_log_path = app_settings.LOG_ROOT_DIR+'\\my_log-'+datetime.date.today().strftime("%Y-%m-%d")+'.log'
    fh = RotatingFileHandler(daily_log_path)
    #fh.setFormatter(formatter)

    logging.basicConfig(
                level=logging.INFO,
                format=FORMAT,
                handlers=[ch, fh]
            )

    logger = logging.getLogger(__name__)

    # Filter paramiko.transport debug and info from basic logging configuration
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARN)

    logging.getLogger('yfinance').setLevel(logging.WARN)

    logger.debug('processing single')

    t =  refresh_monitorlist('mysite')

    t.execute()
