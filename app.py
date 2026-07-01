import streamlit as st 
import streamlit.components.v1 as components 
import shap 
from src.data_loader import FinancialDataFetcher 
from src.sentiment_engine import SentimentEngine  
from src.explainer import SentimentExplainer 
from src.llm_engine import LLMEngine 
from src.logger import setup_logger 
import pandas as pd 
import os 
from src.metrics import MetricsTracker 

# 1. SetUp Logging 
logger = setup_logger("AppController") 
logger.info("--- Dashboard Session Started ---") 

# 2. Resource Caching 
@st.cache_resource 
def load_systems() : 
    logger.info("Initializing system engines...") 
    try : 
        sent_engine = SentimentEngine() 

        return { 
            "data": FinancialDataFetcher(), 
            "sentiment": sent_engine, 
            "explainer": SentimentExplainer( 
                sent_engine.model, 
                sent_engine.tokenizer 
            ), 
            "llm": LLMEngine() 
        } 

    except Exception as e : 
        logger.critical(f"Failed to initialize systems: {e}", exc_info=True) 
        raise 
# 3. Data Caching 
@st.cache_data(ttl=3600) 
def get_news(ticker) : 
    logger.info(f"Fetching fresh data for ticker: {ticker}") 
    return systems["data"].fetch_company_news(ticker) 

# Initialize 
systems = load_systems() 

st.set_page_config(page_title="FinAI Pro", layout="wide") 
st.title("📊 FinAI Professional Dashboard") 

with st.sidebar : 
    st.subheader("System Health Monitor") 
    if os.path.exists("logs/metrics.jsonl") : 
        df = pd.read_json("logs/metrics.jsonl",lines = True) 
        st.metric("Total Operations", len(df)) 
        st.write("Latency by Stage (seconds) :") 
        st.line_chart(df.groupby("stage")["duration"].mean()) 
    else : 
        st.info("No metrics collected yet.") 

ticker = st.text_input("Enter Ticker Symbol (e.g., AAPL):").upper() 
  
if st.button("Analyze Market") : 
    if not ticker : 
        st.warning("Please enter a ticker.") 
    else : 
        logger.info(f"User request: Analysis for {ticker}") 
        try : 
            with st.spinner("Processing market intelligence...") : 
                # Data Pipeline 
                news_df = get_news(ticker) 
                
                if news_df.empty : 
                    logger.warning(f"No news data found for {ticker}") 
                    st.error("No news available for this ticker.") 
                else : 
                    headline = news_df.iloc[0]['headline'] 
                    logger.info(f"Headline retrived : {headline[:30]}...")

                # Sentiment Analysis 
                scores = systems["sentiment"].analyze(headline) 
                st.write(f"**Sentiment Scores:** {scores}")     

                # SHAP Explanation 
                if st.checkbox("Show Explanation (SHAP)") : 
                        logger.info("Generating SHAP breakdown") 
                        shap_values = systems["explainer"].get_shap_values(headline) 
                        fig = shap.plots.text(shap_values[0], display=False) 
                        components.html(fig, height=300, scrolling=True) 
                
                # LLM Insight 
                logger.info("Generating LLM analyst insight") 
                insight = systems["llm"].generate_insight(headline, scores) 
                st.subheader("AI Analyst Insight") 
                st.info(insight) 
                    
        except Exception as e : 
            logger.error(f"Pipeline failure for {ticker}: {e}", exc_info=True) 
            st.error("An internal system error occurred. Please check the logs.") 

logger.info("--- Dashboard Session Finished ---") 