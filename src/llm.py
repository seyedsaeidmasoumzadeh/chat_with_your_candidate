"""Load LLMs"""

from langchain.llms import HuggingFaceEndpoint
from langchain.llms import OpenAI
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import settings
import openai
import os
from utils import get_bin_model


def load_llm():
    if settings.MODEL_TYPE == "local":
        filename = os.path.basename(settings.MODEL_URL_PATH)
        model_path = os.path.join(settings.MODEL_PATH, filename)
        get_bin_model(url_path=settings.MODEL_URL_PATH, model_path=model_path)

        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        llm = LlamaCpp(
            model_path=model_path,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_NEW_TOKENS,
            n_ctx=settings.CONTEXT_SIZE,
            callback_manager=callback_manager,
            verbose=True,
        )
    elif settings.MODEL_TYPE == "openai":
        openai.api_key = settings.OPENAI_API_KEY
        llm = OpenAI(
            max_tokens=settings.MAX_NEW_TOKENS, temperature=settings.TEMPERATURE
        )

    elif settings.MODEL_TYPE == "huggingface":
        llm = HuggingFaceEndpoint(
            endpoint_url=settings.HUGGING_FACE_API_URL,
            task="text2text-generation",
            huggingfacehub_api_token=settings.HUGGING_FACE_HUB_TOKEN,
            model_kwargs={
                "max_new_tokens": settings.MAX_NEW_TOKENS,
                "temperature": settings.TEMPERATURE,
            },
        )
    else:
        raise ValueError("model type value is required")

    return llm
