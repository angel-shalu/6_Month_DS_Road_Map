import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ollama
import os
from matplotlib.backends.backend_pdf import PdfPages

# AI Insight Generator
def generate_ai_insights(df_summary):
    prompt = f"Analyze the dataset summary and provide insights:\n\n{df_summary}"
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Visualization Generator
def generate_visualizations(df):
    histograms = []
    boxplots = []
    others = []

    numeric_df = df.select_dtypes(include=['number'])
    pdf_path = "eda_visualizations.pdf"
    pdf_pages = PdfPages(pdf_path)

    # Histograms
    for col in numeric_df.columns:
        plt.figure(figsize=(6, 4))
        sns.histplot(df[col], bins=30, kde=True, color="skyblue")
        plt.title(f"Histogram - {col}", fontsize=14, fontweight='bold', loc='center')
        path = f"{col}_hist.png"
        plt.savefig(path)
        histograms.append(path)
        plt.close()

# Boxplots
    for col in numeric_df.columns:
        plt.figure(figsize=(6, 4))
        sns.boxplot(y=df[col], color="orange")
        plt.title(f"Box Plot - {col}", fontsize=14, fontweight='bold', loc='center')
        path = f"{col}_box.png"
        plt.savefig(path)
        boxplots.append(path)
        plt.close()

# Correlation Heatmap
    if not numeric_df.empty:
        plt.figure(figsize=(8, 5))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title("Correlation Heatmap", fontsize=14, fontweight='bold', loc='center')
        path = "correlation_heatmap.png"
        plt.savefig(path)
        others.append(path)
        plt.close()

# Pairplot
    if 2 <= numeric_df.shape[1] <= 5:
        pairplot = sns.pairplot(numeric_df)
        pairplot.fig.suptitle("Pair Plot", fontsize=14, fontweight='bold', ha='center')
        pairplot.fig.subplots_adjust(top=0.95)
        path = "pairplot.png"
        pairplot.savefig(path)
        others.append(path)
        plt.close()


    pdf_pages.close()
    return histograms, boxplots, others, pdf_path

# EDA Function
def eda_analysis(file_path):
    df = pd.read_csv(file_path)

    for col in df.select_dtypes(include=['number']).columns:
        df[col].fillna(df[col].median(), inplace=True)
    for col in df.select_dtypes(include=['object']).columns:
        df[col].fillna(df[col].mode()[0], inplace=True)

    summary = df.describe(include='all').to_string()
    missing = df.isnull().sum().to_string()
    insights = generate_ai_insights(summary)

    histograms, boxplots, other_graphs, pdf_path = generate_visualizations(df)

    report = f"""
✅ **Data Loaded Successfully**

📊 **Summary**:
{summary}

🚫 **Missing Values**:
{missing}

🤖 **AI Insights**:
{insights}
"""
    return report, histograms, boxplots, other_graphs, pdf_path

# Clear Function
def clear_outputs():
    return "", [], [], [], None

# Gradio Interface
with gr.Blocks(title="📈 Smart EDA Explorer with LLM Insights") as demo:
    gr.Markdown("""
    # 🔍 **Smart EDA Explorer**  
    ### 🤖 AI-Powered • 📊 Auto Visualizations • 📄 PDF Reports

    Upload any CSV dataset and get instant data insights with AI-powered analysis, summary stats, beautiful visualizations, and downloadable reports — all in one click!
    """)

    file_input = gr.File(type="filepath", label="📁 Upload CSV File")

    with gr.Row():
        submit_btn = gr.Button("✅ Submit")
        clear_btn = gr.Button("❌ Clear")

    with gr.Row():
        eda_output = gr.Textbox(label="📋 EDA Summary & AI Insights", lines=15, interactive=False)

    with gr.Row():
        hist_output = gr.Gallery(label="📈 Histogram Visualizations", columns=2, height="auto")
        box_output = gr.Gallery(label="📦 Box Plots", columns=2, height="auto")

    with gr.Row():
        others_output = gr.Gallery(label="🔗 Correlation & Pair Plot", columns=2, height="auto")
        pdf_download = gr.File(label="📄 Download PDF Report")

    submit_btn.click(
        fn=eda_analysis,
        inputs=file_input,
        outputs=[eda_output, hist_output, box_output, others_output, pdf_download]
    )

    clear_btn.click(
        fn=clear_outputs,
        inputs=[],
        outputs=[eda_output, hist_output, box_output, others_output, pdf_download]
    )

demo.launch(share=True)
