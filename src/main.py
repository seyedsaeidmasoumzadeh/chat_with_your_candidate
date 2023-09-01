from retrieval import DBQ
from llm import load_llm
import gradio as gr
import time
import os
import settings
from utils import print_box


class Agent:
    def __init__(self) -> None:
        self.llm = load_llm()

    def add_text(self, history, text):
        history = history + [(text, None)]
        return history, gr.update(value="", interactive=False)

    def bot(self, history):
        # I am bypassing the history and use the last question
        response = self.dbq.retrive(history[-1][0])
        history[-1][1] = ""
        for character in response["result"]:
            history[-1][1] += character
            time.sleep(0.01)
            yield history

    def process_uploaded_file(self, file, progress=gr.Progress()):
        progress(0.2, desc="Procsesing CV")
        self.dbq = DBQ(cv_path=file.name, llm=self.llm)
        return file.name


with gr.Blocks() as demo:
    agent = Agent()
    chatbot = gr.Chatbot([], elem_id="chatbot")
    with gr.Row():
        with gr.Column(scale=0.85):
            txt = gr.Textbox(
                show_label=False, placeholder="How can I help", container=False
            )
        with gr.Column(scale=0.15, min_width=0):
            file_output = gr.File()
            btn = gr.UploadButton(
                label="Click to Upload a CV 📁", type="file", file_types=["pdf"]
            )
            btn.upload(agent.process_uploaded_file, btn, file_output)

    txt_msg = txt.submit(
        agent.add_text, [chatbot, txt], [chatbot, txt], queue=False
    ).then(agent.bot, chatbot, chatbot)
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)
demo.queue().launch(server_name="0.0.0.0", share=False, height=750)
