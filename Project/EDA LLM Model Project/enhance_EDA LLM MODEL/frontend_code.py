import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ollama
import os

sns.set(style="whitegrid")  # Set seaborn theme

# Function to Generate AI Insights
def generate_ai_insights(df_summary):
    prompt = f"Analyze the dataset summary and provide insights:\n\n{df_summary}"
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Function to Generate Visualizations
def generate_visualizations(df):
    plot_paths = []

    for col in df.select_dtypes(include=['number']).columns:
        plt.figure(figsize=(6, 4))
        sns.histplot(df[col], bins=30, kde=True, color="royalblue")
        plt.title(f"Histogram of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        path = f"{col}_distribution.png"
        plt.savefig(path)
        plot_paths.append(path)
        plt.close()

    # Correlation Heatmap
    numeric_df = df.select_dtypes(include=['number'])
    if not numeric_df.empty:
        plt.figure(figsize=(8, 5))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title("Correlation Heatmap")
        path = "correlation_heatmap.png"
        plt.savefig(path)
        plot_paths.append(path)
        plt.close()

    return plot_paths

# Function to Perform EDA
def eda_analysis(file_path, show_plots=True):
    df = pd.read_csv(file_path)

    # Fill missing values
    for col in df.select_dtypes(include=['number']).columns:
        df[col].fillna(df[col].median(), inplace=True)
    for col in df.select_dtypes(include=['object']).columns:
        df[col].fillna(df[col].mode()[0], inplace=True)

    # Prepare sections
    head_preview = df.head().to_string()
    column_info = df.dtypes.to_string()
    summary = df.describe(include='all').to_string()
    missing_values = df.isnull().sum().to_string()
    insights = generate_ai_insights(summary)

    # Save AI Insights as downloadable report
    report_path = "ai_eda_report.txt"
    with open(report_path, "w") as f:
        f.write(insights)

    # Visualizations (optional)
    plot_paths = generate_visualizations(df) if show_plots else []

    # Output report text
    report_text = (
        f"✅ Data Loaded Successfully!\n\n"
        f"🔹 Preview of Data (Top 5 Rows):\n{head_preview}\n\n"
        f"🔹 Column Info:\n{column_info}\n\n"
        f"🔹 Summary Statistics:\n{summary}\n\n"
        f"🔹 Missing Values:\n{missing_values}\n\n"
        f"🤖 AI Insights:\n{insights}\n"
    )

    return report_text, plot_paths, report_path

# Gradio Interface
with gr.Blocks(title="LLM-Powered EDA Tool") as demo:
    gr.Markdown("## 📊 LLM-Powered Exploratory Data Analysis Tool")
    gr.Markdown("Upload a CSV file to explore your dataset with automatic summary statistics, visualizations, and AI-generated insights using Mistral via Ollama.")
    
    with gr.Row():
        file_input = gr.File(label="Upload CSV", type="filepath")
        plot_toggle = gr.Checkbox(label="Show Visualizations", value=True)
    
    with gr.Row():
        run_button = gr.Button("🔍 Analyze Dataset")
    
    report_output = gr.Textbox(label="📋 EDA Report", lines=25)
    gallery_output = gr.Gallery(label="📊 Visualizations", columns=2, height="auto")

    download_output = gr.File(label="📥 Download AI Report")

    def run_analysis(file, show_plots):
        return eda_analysis(file, show_plots)

    run_button.click(
        run_analysis,
        inputs=[file_input, plot_toggle],
        outputs=[report_output, gallery_output, download_output]
    )

demo.launch(share=True)
