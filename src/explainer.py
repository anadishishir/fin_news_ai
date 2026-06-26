import shap 
from src.logger import setup_logger 

logger = setup_logger("Explainer") 

class SentimentExplainer : 
    def __init__(self, model, tokenizer) : 
        self.explainer = shap.Explainer(model, tokenizer) 
        logger.info("SHAP Explainer initialized.") 

    def get_shap_values(self, text) : 
        try : 
            return self.explainer([text]) 
        except Exception as e : 
            logger.error(f"SHAP calculation failed: {e}") 
            return None 