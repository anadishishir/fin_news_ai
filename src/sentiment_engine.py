import torch 
from transformers import AutoTokenizer, AutoModelForSequenceClassification 
import torch.nn.functional as F 
from src.logger import setup_logger 

logger = setup_logger("SentimentEngine") 

class SentimentEngine : 
    def __init__(self, model_name="ProsusAI/finbert") : 
        logger.info(f"Loading {model_name}...") 
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name) 
        logger.info("Model loaded successfully.") 

    def analyze(self, text) : 
        """Processes text and returns sentiment probabilities.""" 
        try : 
            # 1. Tokenize (Clean & Format Text For The Model) 
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512) 

            # 2. Inference (Feed To Model) 
            with torch.no_grad() : 
                outputs = self.model(**inputs) 

            # 3. Post - Processing (Softmax To Get Probabilities) 
            probs = F.softmax(outputs.logits, dim=-1) 

            # Labels : 0 -> Negative, 1 -> Neutral, 2 -> Positive 
            return { 
                "negative" : float(probs[0][0]), 
                "neutral" : float(probs[0][1]), 
                "positive" : float(probs[0][2]) 
            } 
        except Exception as e : 
            logger.error(f"Inference failed: {e}") 
            return None       