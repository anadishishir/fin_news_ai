import os 
from dotenv import load_dotenv 

load_dotenv() 

def get_secrets(key_name) : 
    val = os.getenv(key_name) 
    
    if not val : 
        raise ValueError(f"CRITICAL : Enviroment Variable Is Not Set !!!") 
    
    return val  