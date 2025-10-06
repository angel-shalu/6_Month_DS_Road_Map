import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import gradio as gr

# -----------------
# Utility functions
# -----------------
def strip_html(text):
    soup = BeautifulSoup(text, "xml")
    return soup.get_text()

def remove_between_square_brackets(text):
    return re.sub(r'\[[^]]*\]', '', text)

def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    text = re.sub('  ', '', text)
    return text

# -----------------
# Main processing
# -----------------
def process_xml(file_obj):
    try:
        tree = ET.parse(file_obj.name)
        root = tree.getroot()
        xml_string = ET.tostring(root, encoding='utf8').decode('utf8')

        cleaned_text = denoise_text(xml_string)
        return xml_string, cleaned_text
    except Exception as e:
        return "Error parsing XML", str(e)

# -----------------
# Gradio Interface
# -----------------
with gr.Blocks(title="XML Cleaner") as demo:
    gr.Markdown("# 📝 XML Scraper & Cleaner\nUpload an XML file to clean it and extract plain text.")

    xml_file = gr.File(label="Upload XML File", file_types=[".xml"])
    raw_xml = gr.Code(label="Raw XML Content", language="html")
    clean_text = gr.Textbox(label="Cleaned Text", lines=15)

    # ✅ Event binding stays inside the Blocks context
    xml_file.change(
        process_xml,
        inputs=xml_file,
        outputs=[raw_xml, clean_text]
    )

# Launch app
if __name__ == "__main__":
    demo.launch(debug=True)
