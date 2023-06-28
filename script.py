import gradio as gr
import requests
import json

params = {
    "activate": True,
    "max_returned": 3,
    "score_cutoff": 0.55,
    "database_host": "localhost:5000"
}

references_used = []

def get_context(query,url,retmax=1,minscore=0):
    headers = {'Content-Type': 'application/json'}
    data = {'query': query, 'retmax':retmax, 'minscore':minscore,'include_score':True}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        print('Request failed with status code:', response.status_code)
        return {}

def input_modifier(string):
    """
    This function is applied to your text inputs before
    they are fed into the model.
    """
    if not params['activate']:
        return string
    #fetch and apply the context
    ret = get_context(string, params['database_host'], params['max_returned'], 0)
    if len(ret['context']) == 0:
        #no context found.
        return string
    context = "The following is a set of snippets that may or may not be relevant to the below. They may be incorrectly formatted.\n\n"+ ret['context']
    references_used = ret['references']
    assert len(references_used) > 0
    return context + string

def output_modifier(string):
    """
    This function is applied to the model outputs.
    """
    if not params['activate']:
        return string
    else:
        if len(references_used) > 0:
            #return the references and reset the tracker
            fstring = string + "\n\n" + "\n".join(references_used)
            references_used = []
            return fstring
        else:
            return string + "\n\n" + "No relevant references found."

def ui():
    activate = gr.Checkbox(value=params['activate'], label='Activate citation fetching')
    max_returned = gr.Slider(1, 15, value=params['max_returned'], step=1, label="Maximum number of citations to return. Setting this value too high may lead to lost context!")
    score_cutoff = gr.Slider(0, 1, value=params['score_cutoff'], step=0.01, label="Minimum similarity to return citations. Set to higher values to be more stringent.")
    database_host = gr.Textbox(value="", placeholder="localhost:5000", label="", info='To use this textbox activate the checkbox above')
    
    activate.change(lambda x: params.update({"activate": x}), activate, None)
    max_returned.change(lambda x: params.update({"max_returned": x}), max_returned, None)
    score_cutoff.change(lambda x: params.update({"score_cutoff": x}), score_cutoff, None)
    database_host.change(lambda x: params.update({"database_host": x}), database_host, None)