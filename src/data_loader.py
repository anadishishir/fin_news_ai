import finnhub 
import pandas as pd 
from datetime import datetime, timedelta 
from src.logger import setup_logger  
from src.utils import get_secrets 
from src.metrics import time_execution 

logger = setup_logger("DataLoader") 

class FinancialDataFetcher : 
    # Initialize The Official Client 
    def __init__(self) : 
        self.api_key = get_secrets("FINHUB_API_KEY") 
        self.client = finnhub.Client(api_key = self.api_key) 
    
    @time_execution(stage="fetch_data") 
    def fetch_company_news(self, ticker) : 
        """Fetches news for the last 3 days.""" 
        try : 
            logger.info(f"Fetching news for {ticker}") 

            # Define Date Range 
            to_date = datetime.now() 
            from_date = to_date - timedelta(days=3) 

            # FinHub Requires String Format  YYYY-MM-DD 
            news = self.client.company_news(
                ticker, 
                _from=from_date.strftime('%Y-%m-%d'), 
                to=to_date.strftime('%Y-%m-%d')
            ) 
            
            if not news : 
                logger.warning(f"No news found for {ticker}") 
                return pd.DataFrame() 
            
            # Convert To DataFrame For Easy Processing 
            df = pd.DataFrame(news)
            logger.info(f"Successfully retrieved {len(df)} news items for {ticker}")
            return df
            
        except Exception as e : 
            logger.error(f"Error fetching Finnhub news: {e}") 
            return pd.DataFrame() 