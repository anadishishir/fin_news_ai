🚀 FinAI: Intelligent Market Sentiment Pipeline 
FinAI is a modular, fintech-grade news analysis pipeline that leverages advanced LLMs and sentiment engines to extract actionable insights from market news. 

🏗️ Architecture 
FinAI follows a decoupled, service-oriented architecture : 

Controller (app.py): A Streamlit-based UI for real-time interaction. 

Service Layer (src/): Independent modules for data fetching, sentiment analysis, LLM reasoning, and SHAP-based model explanations. 

Observability (src/metrics.py): Built-in instrumentation to track latency and API performance. 

Configuration: Decoupled security via .env management. 

🚀 Key Features 
Defensive Pipeline: Robust error handling ensures the app doesn't crash on bad data or API timeouts. 

Performance Observability: Real-time system health dashboard (latency tracking per stage). 

Modular Design: Swap components (e.g., switch LLM providers) without touching core logic. 

Dockerized: Deployable in any environment with consistent dependency management. 

⚙️ Quick Start 
1. Environment Setup 
Create a .env file in the root directory : 

Plaintext 
FINNHUB_API_KEY=your_key_here 
GEMINI_API_KEY=your_key_here 
2. Run with Docker 
Bash 
# Build the image 
docker build -t fin-news-ai . 

# Run the container 
docker run -p 8501:8501 fin-news-ai 
3. Run Locally (WSL/Linux) 
Bash 
pip install -r requirements.txt 
streamlit run app.py 
📊 Monitoring 
The app tracks all pipeline stages. Open the System Health Monitor sidebar to view : 

Total Operations: Count of successful/failed analyses. 

Latency by Stage: Performance benchmarks for Data Fetching, Sentiment Analysis, and LLM Reasoning. 