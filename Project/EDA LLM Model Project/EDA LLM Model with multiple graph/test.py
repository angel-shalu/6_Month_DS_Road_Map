import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import ollama
import os

# Function to Perform EDA and Generate Visualizations
def eda_analysis(file_path):
    df = pd.read_csv(file_path)
    
    # Fill missing values with median for numeric columns
    for col in df.select_dtypes(include=['number']).columns:
        df[col].fillna(df[col].median(), inplace=True)
    
    # Fill missing values with mode for categorical columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col].fillna(df[col].mode()[0], inplace=True)
    
    # Data Summary
    summary = df.describe(include='all').to_string()
    
    # Missing Values
    missing_values = df.isnull().sum().to_string()

    # Generate AI Insights
    insights = generate_ai_insights(summary)
    
    # Generate Data Visualizations and PDF
    plot_paths, pdf_path = generate_visualizations(df)
    
    report_text = (
        f"\n✅ Data Loaded Successfully!\n\n"
        f"📋 Summary:\n{summary}\n\n"
        f"🔍 Missing Values:\n{missing_values}\n\n"
        f"🧠 AI Insights:\n{insights}"
    )

    return report_text, plot_paths, pdf_path

# AI-Powered Insights using Mistral-7B (Ollama)
def generate_ai_insights(df_summary):
    prompt = f"Analyze the dataset summary and provide insights:\n\n{df_summary}"
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def generate_visualizations(df):
    plot_paths = []
    
    # Histograms for Numeric Columns
    for col in df.select_dtypes(include=['number']).columns:
        plt.figure(figsize=(6,4))
        sns.histplot(df[col], bins=30, kde=True, color="blue")
        plt.title(f"Distribution of {col}")
        path = f"{col}_distribution.png"
        plt.savefig(path)
        plot_paths.append(path)
        plt.close()

    # Box Plots for Numeric Columns
    for col in df.select_dtypes(include=['number']).columns:
        plt.figure(figsize=(6,4))
        sns.boxplot(y=df[col], color='orange')
        plt.title(f"Box Plot of {col}")
        path = f"{col}_boxplot.png"
        plt.savefig(path)
        plot_paths.append(path)
        plt.close()

    # Correlation Heatmap (only numeric columns)
    numeric_df = df.select_dtypes(include=['number'])
    if not numeric_df.empty:
        plt.figure(figsize=(8,5))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title("Correlation Heatmap")
        path = "correlation_heatmap.png"
        plt.savefig(path)
        plot_paths.append(path)
        plt.close()
        
    # Pair Plot (if not too many columns)
    if numeric_df.shape[1] <= 5:
        sns.pairplot(numeric_df)
        path = "pairplot.png"
        plt.savefig(path)
        plot_paths.append(path)
        plt.close()

    return plot_paths


    pdf.close()
    return plot_paths, pdf_path

# Gradio Interface
demo = gr.Interface(
    fn=eda_analysis,
    inputs=gr.File(type="filepath", label="📁 Upload CSV Dataset"),
    outputs=[
        gr.Textbox(label="📄 EDA Report"),
        gr.Gallery(label="📊 Data Visualizations", columns=2, height="auto"),
        gr.File(label="📥 Download Visual Report (PDF)")
    ],
    title="📊 LLM-Powered Exploratory Data Analysis (EDA)",
    description="Upload a CSV file to perform AI-powered exploratory data analysis with visualizations and PDF report export."
)

# Launch the Gradio App
demo.launch(share=True)
