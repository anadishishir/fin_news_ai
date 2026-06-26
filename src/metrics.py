import time 
import json 
import os 
from datetime import datetime 

METRICS_FILE = "logs/metrics.jsonl" 

class MetricsTracker : 
    @staticmethod 
    def log(stage, ticker, duration, status="success", error_msg=None) : 
        """Logs pipeline metrics to a file.""" 
        if not os.path.exists("logs") : 
            os.makedirs("logs") 
            
        data = { 
            "timestamp" : datetime.now().isoformat(), 
            "stage" : stage, 
            "ticker" : ticker, 
            "duration" : round(duration, 4), 
            "status" : status, 
            "error" : error_msg 
        } 
        
        with open(METRICS_FILE, "a") as f : 
            f.write(json.dumps(data) + "\n") 

def time_execution(stage) : 
    def decorator(func) : 
        def wrapper(*args, **kwargs) : 
            start = time.time() 
            ticker = kwargs.get('ticker') or (args[1] if len(args) > 1 else "N/A") 
            try : 
                result = func(*args, **kwargs) 
                MetricsTracker.log(stage, ticker, time.time() - start, "success") 
                return result 
            except Exception as e : 
                MetricsTracker.log(stage, ticker, time.time() - start, "failure", str(e)) 
                raise e 
        return wrapper 
    return decorator 