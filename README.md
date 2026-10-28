# Culinary & Supply Intelligence Sentinel 🍲🤖

An end-to-end AI/ML pipeline designed for the food catering industry. It automatically ingests real-time supply chain updates, classifies risk/opportunity vectors using zero-shot NLP, and generates actionable operational advisory reports via high-speed LLM inference.

## 🏗 System Architecture

1. **Data Ingestion (`ingest.py`)**: Structured data pipeline using Pandas.
2. **ML Classification (`classifier.py`)**: Local zero-shot classification using Hugging Face (`distilbart-mnli-12-3`).
3. **LLM Advisory Engine (`advisor.py`)**: High-speed operational advisory generation powered by Groq API (`openai/gpt-oss-20b`).

## 🚀 Key Features

- **Cost-Optimized Architecture**: Runs 100% free using local Hugging Face transformer models combined with Groq free-tier LLM API.
- **Zero-Shot Domain Mapping**: Categorizes unstructured industry updates into `Financial Cost Spike`, `Customer Demand Shift`, or `Regulatory & Safety Warning` without fine-tuning.
- **Automated Executive Output**: Converts categorized operational signals into 3 high-impact, actionable business decisions.

## 🛠 Tech Stack

- **Language:** Python 3.11
- **Data Engineering:** Pandas
- **Machine Learning:** Hugging Face Transformers, PyTorch
- **Generative AI:** Groq API (LLM Inference)

## 🚦 Quickstart

```bash
# 1. Clone Repository
git clone [https://github.com/deepika_data_ai/food-sentinel.git](https://github.com/deepika_data_ai/food-sentinel.git)
cd food-sentinel

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Set API Key & Run
export GROQ_API_KEY="your_groq_api_key_here"
python3 main.py