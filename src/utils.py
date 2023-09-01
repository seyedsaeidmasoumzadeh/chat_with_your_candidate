from langchain.document_loaders import PyPDFLoader
from langchain import LLMChain
import requests


def cv_loader(cv_path):
    loader = PyPDFLoader(cv_path)
    contexts = loader.load()
    context = "\n".join([context.page_content for context in contexts])
    return context


def generator(llm, prompt_template, context):
    llm_chain = LLMChain(prompt=prompt_template, llm=llm)
    compleation = llm_chain.run(context)
    return compleation


def get_bin_model(url_path, model_path):
    response = requests.get(url_path, stream=True)
    if response.status_code == 200:
        with open(model_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        raise requests.exceptions.HTTPError


def print_box(input_string):
    length = len(input_string)
    border = "+" + "-" * (length + 2) + "+"
    content = "| " + input_string + " |"

    print(border)
    print(content)
    print(border)
