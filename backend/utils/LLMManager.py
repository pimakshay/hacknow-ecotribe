import os

from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL")


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

class LLMManager:
    def __init__(self):
        api_key = API_KEY
        model_name = GEMINI_MODEL_NAME
        temperature = 0.0
        verbose = True

        # Create an OpenAI object.
        self.llm = ChatGoogleGenerativeAI(model=model_name, 
                                google_api_key=api_key, 
                                temperature=temperature, 
                                verbose=verbose)

    def invoke(self, prompt: ChatPromptTemplate, **kwargs) -> str:
        messages = prompt.format_messages(**kwargs)
        response = self.llm.invoke(messages)
        return response.content