import os
import pandas as pd
from dotenv import load_dotenv
from transformers import pipeline
from groq import Groq

# Automatically load environment variables from the local .env file
load_dotenv()

print("Step 1: Ingesting Masala Boulevard Supply Chain Data...")
data = [
    {
        "id": 1, 
        "text": "Wholesale prices for imported Guntur red chillies, tamarind, and tomatoes increased by 16% this week due to UK import clearance delays."
    },
    {
        "id": 2, 
        "text": "Weekend demand for family catering trays, idli/dosa batter packs, and samosa platters increased by 30% across Greater Manchester."
    },
    {
        "id": 3, 
        "text": "UK Food Standards Agency update: Enhanced hot-holding temperature logs and batch allergen labelling required for pre-packaged takeaway curries."
    }
]
df = pd.DataFrame(data)

print("Step 2: ML Zero-Shot Classification...")
classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-3")
candidate_labels = ["Financial Cost Spike", "Customer Demand Shift", "Regulatory & Safety Warning"]

categories = []
for item in df['text']:
    prediction = classifier(item, candidate_labels)
    categories.append(prediction['labels'][0])

df['ml_category'] = categories

print("Step 3: Generating Executive Advice for Masala Boulevard via Groq...")

formatted_input = ""
for idx, row in df.iterrows():
    formatted_input += f"- [{row['ml_category']}] {row['text']}\n"

prompt = f"""
You are the Chief Operations Advisor for 'Masala Boulevard', a South Indian food catering business based in Greater Manchester.
Analyze these ML-classified market signals and provide 3 concrete, operational recommendations for the business owner:

{formatted_input}
"""

# The Groq client automatically picks up the API key loaded by load_dotenv()
client = Groq()
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="openai/gpt-oss-20b",
)

advice = chat_completion.choices[0].message.content

print("\n================== MASALA BOULEVARD INTELLIGENCE REPORT ==================")
print(advice)
print("=========================================================================\n")

# Save intelligence report to a CSV log
df['advisory_report'] = advice
df.to_csv("masala_boulevard_intelligence_log.csv", index=False)
print("Saved live log to masala_boulevard_intelligence_log.csv!")