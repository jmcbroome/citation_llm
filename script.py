import gradio as gr
import requests

params = {
    "activate": True,
    "max_returned": 3,
    "score_cutoff": 0.55,
    "database_host": "localhost:5000"
}

def input_modifier(string):
    """
    This function is applied to your text inputs before
    they are fed into the model.
    """
    if not params['activate']:
        return string

def output_modifier(string):
    """
    This function is applied to the model outputs.
    """
    if not params['activate']:
        return string

def ui():
    activate = gr.Checkbox(value=params['activate'], label='Activate citation fetching')
    max_returned = gr.Slider(1, 15, value=params['max_returned'], step=1, label="Maximum number of citations to return. Setting this value too high may lead to lost context!")
    score_cutoff = gr.Slider(0, 1, value=params['score_cutoff'], step=0.01, label="Minimum similarity to return citations. Set to higher values to be more stringent.")
    database_host = gr.Textbox(value="", placeholder="localhost:5000", label="", info='To use this textbox activate the checkbox above')
    
    activate.change(lambda x: params.update({"activate": x}), activate, None)
    max_returned.change(lambda x: params.update({"max_returned": x}), max_returned, None)
    score_cutoff.change(lambda x: params.update({"score_cutoff": x}), score_cutoff, None)
    database_host.change(lambda x: params.update({"database_host": x}), database_host, None)