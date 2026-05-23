import streamlit as st
import sys
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.open_source_assistant import generate_response as open_ai
from core.frontier_assistant import generate_response as frontier_ai
from core.evaluator import evaluate_response


# ================= PAGE CONFIG =================
st.set_page_config(page_title="AI Benchmark Lab", layout="wide")

st.title("🤖 AI Benchmark Lab — Top 1% AI Evaluation Platform")
st.markdown("### 📊 Compare OSS vs Frontier LLMs with advanced evaluation & analytics")

# ================= SESSION STATE =================
if "history_oss" not in st.session_state:
    st.session_state.history_oss = []

if "history_frontier" not in st.session_state:
    st.session_state.history_frontier = []

if "oss_scores" not in st.session_state:
    st.session_state.oss_scores = []

if "frontier_scores" not in st.session_state:
    st.session_state.frontier_scores = []


# ================= INPUT =================
user_input = st.text_input("💬 Enter prompt")


# ================= BENCHMARK MODE =================
st.subheader("🧪 Auto Benchmark Mode")

test_prompts = [
    "What is AI?",
    "Explain gravity simply",
    "Write Python code to sort a list",
    "What is 2+2?",
    "Explain machine learning"
]

if st.button("Run Full Benchmark"):

    st.info("Running benchmark...")

    for i, prompt in enumerate(test_prompts):

        st.write(f"Testing {i+1}/{len(test_prompts)}: {prompt}")

        oss_response = open_ai(prompt, st.session_state.history_oss)
        frontier_response = frontier_ai(prompt, st.session_state.history_frontier)

        oss_score = evaluate_response(prompt, oss_response)
        frontier_score = evaluate_response(prompt, frontier_response)

        st.session_state.history_oss.append((prompt, oss_response))
        st.session_state.history_frontier.append((prompt, frontier_response))

        st.session_state.oss_scores.append(oss_score)
        st.session_state.frontier_scores.append(frontier_score)

    st.success("Benchmark Completed!")


# ================= SINGLE RUN =================
if st.button("Run Single Prompt") and user_input:

    oss_response = open_ai(user_input, st.session_state.history_oss)
    frontier_response = frontier_ai(user_input, st.session_state.history_frontier)

    oss_score = evaluate_response(user_input, oss_response)
    frontier_score = evaluate_response(user_input, frontier_response)

    st.session_state.history_oss.append((user_input, oss_response))
    st.session_state.history_frontier.append((user_input, frontier_response))

    st.session_state.oss_scores.append(oss_score)
    st.session_state.frontier_scores.append(frontier_score)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🟢 OSS Model")
        st.write(oss_response)

    with col2:
        st.subheader("🔵 Frontier Model")
        st.write(frontier_response)

    st.subheader("📊 Scores")
    st.write("OSS:", oss_score)
    st.write("Frontier:", frontier_score)

    # ================= RADAR CHART =================
    labels = ["Helpfulness", "Hallucination", "Safety", "Reasoning", "Conciseness"]

    oss_vals = [oss_score.get(l, 0) for l in labels]
    frontier_vals = [frontier_score.get(l, 0) for l in labels]

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()

    oss_vals += oss_vals[:1]
    frontier_vals += frontier_vals[:1]
    angles += angles[:1]

    fig = plt.figure(figsize=(6,6))
    ax = plt.subplot(111, polar=True)

    ax.plot(angles, oss_vals, label="OSS")
    ax.fill(angles, oss_vals, alpha=0.2)

    ax.plot(angles, frontier_vals, label="Frontier")
    ax.fill(angles, frontier_vals, alpha=0.2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    ax.set_title("LLM Performance Radar")
    ax.legend()

    st.pyplot(fig)


# ================= HISTORY =================
st.divider()
st.subheader("🗂 Conversation History")

tab1, tab2 = st.tabs(["OSS", "Frontier"])

with tab1:
    for q, a in st.session_state.history_oss:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**OSS:** {a}")
        st.divider()

with tab2:
    for q, a in st.session_state.history_frontier:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Frontier:** {a}")
        st.divider()


# ================= CSV EXPORT =================
st.divider()
st.subheader("📦 Export Results")

if st.button("Download CSV"):

    rows = []

    for i in range(len(st.session_state.history_oss)):
        rows.append({
            "prompt": st.session_state.history_oss[i][0],
            "oss_response": st.session_state.history_oss[i][1],
            "frontier_response": st.session_state.history_frontier[i][1],
            "oss_score": st.session_state.oss_scores[i],
            "frontier_score": st.session_state.frontier_scores[i]
        })

    df = pd.DataFrame(rows)

    file_name = f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(file_name, index=False)

    st.success(f"CSV saved: {file_name}")


# ================= PDF EXPORT =================
def generate_pdf(rows):
    file_name = "benchmark_report.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)

    y = 750
    c.setFont("Helvetica", 10)

    c.drawString(50, 800, "AI Benchmark Report")

    for r in rows[:20]:
        text = f"{r['prompt']} | OSS vs Frontier"
        c.drawString(50, y, text[:100])
        y -= 20

    c.save()
    return file_name


if st.button("Generate PDF Report"):

    rows = []

    for i in range(len(st.session_state.history_oss)):
        rows.append({
            "prompt": st.session_state.history_oss[i][0]
        })

    file = generate_pdf(rows)

    st.success(f"PDF Generated: {file}")