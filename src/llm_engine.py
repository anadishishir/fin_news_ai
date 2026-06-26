from src.utils import get_secrets 
import google.generativeai as genai 
from src.logger import setup_logger 

logger = setup_logger("LLMEngine") 

class LLMEngine : 
    def __init__(self) : 
        genai.configure(api_key=get_secrets("GEMINI_API_KEY"))  
        self.model = genai.GenerativeModel('gemini-3.5-flash') 

    def generate_insight(self, headline, sentiment_scores) : 
        """Combines quantitative data with LLM reasoning.""" 
        prompt = f""" 
        Analyze the following financial headline: "{headline}" 
        The quantitative sentiment analysis (FinBERT) returned these scores :  
        {sentiment_scores} 
        
        Provide a concise, 2-sentence financial analyst insight explaining why the market might react this way.
        """ 
        try : 
            response = self.model.generate_content(prompt) 
            return response.text 
        except Exception as e : 
            logger.error(f"Gemini API call failed: {e}") 
            return "Unable to generate insight at this time." 