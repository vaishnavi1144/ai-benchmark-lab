\# 🤖 AI Benchmark Lab — LLM Evaluation Platform



\## 🚀 Overview

AI Benchmark Lab is a multi-model evaluation system that compares Open-Source LLMs and Frontier LLMs using automated benchmarking, evaluation metrics, and analytics.



\## 🧠 Features

\- Compare OSS vs Frontier LLMs

\- LLM-as-judge evaluation system

\- Multi-metric scoring:

&#x20; - Helpfulness

&#x20; - Hallucination

&#x20; - Safety

&#x20; - Reasoning

&#x20; - Conciseness

\- Auto benchmark mode (batch testing)

\- Radar chart analytics

\- CSV + PDF export reports

\- Conversation memory tracking

\- Streamlit interactive UI



\## 🏗️ Architecture

UI (Streamlit)

→ LLM Layer (Groq API)

→ Evaluation Engine

→ Analytics Layer

→ Export System (CSV/PDF)



\## ⚙️ Setup



```bash

pip install -r requirements.txt

streamlit run ui/app.py

