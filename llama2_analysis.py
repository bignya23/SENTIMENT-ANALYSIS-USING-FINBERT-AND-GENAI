from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
from dotenv import load_dotenv
import os

load_dotenv()

def load_llama2_model():
    model_name = "meta-llama/Llama-2-7b-chat-hf"
    hf_token = os.getenv("hf_token")  # Replace with your actual token

    # Load tokenizer and model with the token, using CUDA if available
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hf_token)
    
    # Ensure the model uses GPU (CUDA) if available, with automatic device mapping
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        use_auth_token=hf_token, 
        device_map="auto",  # Automatically use GPU if available
        torch_dtype=torch.float16  # Use half-precision for faster inference
    )

    return model, tokenizer


def generate_summary_and_insights(headlines_df, model, tokenizer):
    # Concatenate all the headlines into one input string
    headlines_text = ". ".join(headlines_df['Headline'].tolist())

    # Determine the device: Use GPU if available, otherwise CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Set up a pipeline for text generation using the LLaMA 2 model
    text_generation = pipeline(
        "text-generation", 
        model=model, 
        tokenizer=tokenizer, 
        device=device  # Specify the device (GPU/CPU)
    )

    # Create a prompt for summarizing and generating insights on investment
    prompt = (f"Summarize the following headlines and provide investment insights, along with sentiment analysis: {headlines_text}. "
              "Also provide suggestions on whether it's a good time to invest in this company.")

    # Generate the summary and insights using the model
    summary_and_insights = text_generation(
        prompt,
        max_length=1024,
        do_sample=True,
        truncation=True  # Enable truncation
    )[0]['generated_text']

    return summary_and_insights
