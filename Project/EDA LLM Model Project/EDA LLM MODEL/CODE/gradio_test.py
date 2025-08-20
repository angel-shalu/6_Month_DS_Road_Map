# import gradio as gr
# def greet(name, intensity):
#     return "Hello, " + name + "!" * int(intensity)

# demo = gr.Interface(
#     fn=greet,
#     inputs=["text", "slider"],
#     outputs=["text"],
# )
# demo.launch(share=True)



import gradio as gr

# Function to test
def greet(name, intensity):
    return "Hello, " + (name + "! ") * int(intensity)

# Create Interface
demo = gr.Interface(
    fn=greet,
    inputs=[
        gr.Textbox(label="Enter your name"),
        gr.Slider(minimum=1, maximum=5, step=1, value=1, label="Intensity")
    ],
    outputs=gr.Textbox(label="Output")
)

# Launch the app
demo.launch(share=True)


