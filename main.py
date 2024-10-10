import os
from dotenv import load_dotenv
import news_fetcher
import sentiment_analysis
import llama2_analysis
import torch
from fundamental_basic import get_all_stock_info as get_basic_info
from fundamental_adv import get_all_stock_info as get_advanced_info

# Load environment variables from .env file
load_dotenv()

# Fetch API key from .env file
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def main(company_name, symbol):
    # Fetch the top headlines for the company
    print(f"Fetching top news headlines for {company_name}...")
    headlines_df = news_fetcher.get_news(company_name, NEWS_API_KEY)
    
    if headlines_df is None or headlines_df.empty:
        print("No news found.")
        return

    # Fetch basic stock info
    print(f"\nFetching basic stock info for {symbol}...")
    basic_info_df = get_basic_info(symbol)
    print(basic_info_df)

    # Fetch advanced stock info
    print(f"\nFetching advanced stock info for {symbol}...")
    advanced_info = get_advanced_info(symbol)
    for key, value in advanced_info.items():
        print(f"{key}: {value}")

    # Load FinBERT model for sentiment analysis (with CUDA if available)
    print("Loading FinBERT model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    sentiment_pipeline = sentiment_analysis.load_finbert_model(device=device)

    # Analyze sentiment of the headlines
    print("Analyzing sentiment of news headlines...")
    headlines_with_sentiment = sentiment_analysis.analyze_sentiment(headlines_df, sentiment_pipeline)

    # Display top headlines with sentiment
    print("\nTop 10 News Headlines with Sentiment:")
    print(headlines_with_sentiment)

    # Load Llama 2 model for summarization and insights
    print("Loading Llama 2 model for summarization and insights...")
    llama_model, llama_tokenizer = llama2_analysis.load_llama2_model(device)

    # Use CUDA if available for the Llama model
    if torch.cuda.is_available():
        llama_model = llama_model.to("cuda")
        print("Llama 2 model is using CUDA.")
    else:
        print("CUDA not available. Llama 2 model is using CPU.")

    # Generate summary and insights using Llama 2
    print("Generating summary and insights using Llama 2...")
    llama_summary_and_insights = llama2_analysis.generate_summary_and_insights(headlines_df, llama_model, llama_tokenizer)

    # Display summary and insights
    print("\nSummary and Insights:")
    print(llama_summary_and_insights)

if __name__ == "__main__":
    company_name = input("Enter the company name: ")
    symbol = input("Enter the stock symbol: ")
    main(company_name, symbol)
