import logging 
from logging.handlers import RotatingFileHandler 
import os 

def setup_logger(name):
    if not os.path.exists("logs") : 
        os.makedirs("logs") 
        
    logger = logging.getLogger(name) 
    logger.setLevel(logging.INFO) 
    
    if not logger.handlers : 
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
        
        file_handler = RotatingFileHandler("logs/app.log", maxBytes=2000000, backupCount=3) 
        file_handler.setFormatter(formatter) 
        
        console_handler = logging.StreamHandler() 
        console_handler.setFormatter(formatter) 
        
        logger.addHandler(file_handler) 
        logger.addHandler(console_handler) 
    return logger 