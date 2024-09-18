from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

class LLMManager:
    def __init__(self):
        self.llm = AzureChatOpenAI(
                    api_key="b36879e47f2d42109a3d54edb22f78c3",
                    azure_endpoint="https://ecotribe.openai.azure.com/openai/deployments/Chat/chat/completions?api-version=2024-02-15-preview",
                    api_version="2024-02-15-preview",
                    model="gpt-4o",
                    temperature=0,
                    max_tokens=None
                )

    def invoke(self, prompt: ChatPromptTemplate, **kwargs) -> str:
        messages = prompt.format_messages(**kwargs)
        response = self.llm.invoke(messages)
        return response.content