from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

gpt_model = "gpt-4o"
API_KEY = ""

# ImageQuality model
class ImageQuality(BaseModel):
    # object_type: str # [Fruit, Vegetable]
    object_name: str # name of the fruit or vegetable
    color: str # color of the fruit
    surface_texture: str # texture of the surface: ToDo Type?
    has_model_spot: str # yes or no


# HyperspectralImageQuality model
class HyperspectralImageQuality(BaseModel):
    has_spoilage: str # yes or no

class GasDetection(BaseModel):
    """
    Key Insights:

        Freshness: Low levels of ethylene and carbon dioxide suggest the fruit is still fresh.
        Ripening: An increase in ethylene and CO₂ indicates ripening, but not spoilage.
        Spoilage: High levels of ammonia, methane, hydrogen sulfide, or certain VOCs are signs of spoilage.
    """
    level_of_ethylene: str # ["excessive", "high", "normal"] # excessive means already ripened
    level_of_CO2: str # ["excessive", "high", "normal"] # spike in CO2 indicates reduced shelf life
    level_of_methane: str # if methane detected, fruit is spoiled
    level_of_ammonia: str # Indicator: The presence of ammonia indicates significant spoilage and bacterial activity.
    level_of_hydrogenSulfide: str

class Agent1_ImageQuality:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful assistant."),
                ("human", "{input}")
            ])
        llm = ChatOpenAI(model=gpt_model,
                        temperature=0.0) #models.resnet50(pretrained=True)
        self.chain = self.prompt | llm

    def infer(self, image_path):
        output: ImageQuality = self.chain.invoke({"input": image_path})
        return output


class Agent2_HyperspectralImageQuality:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful assistant."),
                ("human", "{input}")
            ])
        llm = ChatOpenAI(model=gpt_model,
                        temperature=0.0) #models.resnet50(pretrained=True)
        self.chain = self.prompt | llm

    def infer(self, image_path):
        output: HyperspectralImageQuality = self.chain.invoke({"input": image_path})
        return output


class Agent3_GasDetector:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful assistant."),
                ("human", "{input}")
            ])
        llm = ChatOpenAI(model=gpt_model,
                        temperature=0.0) #models.resnet50(pretrained=True)
        self.chain = self.prompt | llm

    def infer(self, image_path):
        output: GasDetection = self.chain.invoke({"input": image_path})
        return output
    

def analyze_image_quality(image_path):
    model = Agent1_ImageQuality()
    return model.infer(image_path)

def analyze_hyperspectral_image_quality(image_path):
    model = Agent2_HyperspectralImageQuality()
    return model.infer()

def analyze_gas_detector(image_path):
    model = Agent3_GasDetector()
    return model.infer()

