from backend.utils.image_tools import analyze_image_quality, analyze_hyperspectral_image_quality, analyze_gas_detector
from backend.utils.state import OutputState
from backend.utils.LLMManager import LLMManager
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

import base64
from io import BytesIO

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class EcoTribeAgent:
    def __init__(self, API_KEY):
        self.llm_manager = LLMManager(api_key=API_KEY)

    def image_analysis_node(self, state: OutputState) -> OutputState:
        """Parse user question and identify image qualities."""
        image_path = state['image_path']
        image_base64 = image_to_base64(image_path)
        prompt = ChatPromptTemplate.from_messages([
            ("system", '''You are an expert at detecting the type of fruits, and their qualities from an input image. These qualities include color, and surface texture. You also identify if there is any mould, and if the fruit is defective.
        The input images can include images of fresh, semi-ripen, fully-ripen, or rotten fruits.
        Your task is to return a json object with following keys:
        {{
        object_name: str, # name of the fruit
        color: str, # color of the fruit
        surface_texture: str, # texture of the surface: ["smooth", "rough", "fuzzy", "wrinkled", "bumpy", "waxy", "spiky", "dimpled"] 
        has_mould_spot: str, # yes or no
        shape: str # options: ["normal", "distorted", "swollen", "shriveled"]}}
     
     These information would help the user to identify if the fruit is fresh, partially-ripen, fully-ripen, partially-rotten, or fully-roten.
     '''),
    ("human", "Please analyze this fruit image and return JSON object as mentioned in the instructions."),
    ("human", f"![fruit_image](data:image/jpeg;base64,{image_base64})")
])

        output_parser = JsonOutputParser()
        prompt = prompt.format()
        response = self.llm_manager.invoke(prompt.format(), response_format={"type": "json_object"})
        parsed_response = output_parser.parse(response.content)
        return {"image_analysis_result": parsed_response}

    def hyperspectral_analysis_node(self, state: OutputState) -> OutputState:
        image_path = state['image_path']
        image_base64 = image_to_base64(image_path)
        prompt = ChatPromptTemplate.from_messages([
            ("system", '''Imagine yourself as a hyperspectral imaging detector which can identify if a fruit is spoiled or not by understanding inner state of the food.
             Due to unavailability of hyoerspectral imaging sensors, you will be given an image as input.
        Your task is to return a json object with following keys:
        {{
        "has_spoilage": "yes or no",  // Indicate if the fruit has spoilage internally or externally.  
        "description": "string"  // If spoilage is present, describe the type and extent of spoilage.
}}
     
     These information would help the user to identify if the fruit is fresh, partially-ripen, fully-ripen, partially-rotten, or fully-roten.
     '''),
    ("human", "Please analyze this fruit image and return JSON object as mentioned in the instructions."),
    ("human", f"![fruit_image](data:image/jpeg;base64,{image_base64})")
])

        output_parser = JsonOutputParser()
        prompt = prompt.format()
        response = self.llm_manager.invoke(prompt.format(), response_format={"type": "json_object"})
        parsed_response = output_parser.parse(response.content)
        return {"hyperspectral_analysis_result": parsed_response}

    def gas_detector_analysis_node(self, state) -> OutputState:
        image_path = state['image_path']
        image_base64 = image_to_base64(image_path)
        prompt = ChatPromptTemplate.from_messages([
            ("system", '''Imagine yourself as a gas detector which can identify if a fruit is releasing any gases which can indicate if it is fresh, ripen or rotten.
             Due to unavailability of gas detector sensors, you will be given an image as input, and your job is to guess which gases might have been released.
        Your task is to return a json object with following keys:
        {{
        level_of_ethylene: str # options: ["excessive", "high", "normal", "not_detected"]. Excessive means already ripened
        level_of_CO2: str # options: ["excessive", "high", "normal", "not_detected"]. Spike in CO2 indicates reduced shelf life
        level_of_methane: str # options: ["excessive", "high", "normal", "not_detected"]. If methane detected, fruit is spoiled
        level_of_ammonia: str # option: ["excessive", "high", "normal", "not_detected"]. The presence of ammonia indicates significant spoilage and bacterial activity.
        level_of_hydrogenSulfide: str # option: ["excessive", "high", "normal", "not_detected"]
             }}
     
     Be creative with the responses as these information would help the user to identify if the fruit is fresh, partially-ripen, fully-ripen, partially-rotten, or fully-roten.
     '''),
    ("human", "Please analyze this fruit image and return JSON object as mentioned in the instructions."),
    ("human", f"![fruit_image](data:image/jpeg;base64,{image_base64})")
])

        output_parser = JsonOutputParser()
        prompt = prompt.format()
        response = self.llm_manager.invoke(prompt.format(), response_format={"type": "json_object"})
        parsed_response = output_parser.parse(response.content)
        return {"gas_detector_result": parsed_response}

    def ripen_assessment_node(self, state: OutputState) -> OutputState:
        # Assess ripeness based on image, hyperspectral, and gas detector data
        combined_response = {
            "data": {
                "hyperspectral_imaging_results": state['hyperspectral_analysis_result'],
                "gas_detection_results": state['gas_detector_result'],
            }
        }
        prompt = ChatPromptTemplate.from_messages([
            ("system", '''You are an expert at identifying if the fruit is fresh, partially ripen, fully ripen, partially spoiled, or full spoiled from the data coming from hyperspectral imaging and gas detector sensors.
             Below is the data in json format with two keys, "hyperspectral_imaging_results" and "gas_detection_results": 
        {combined_response}
     
        Your task is to return a json object with following keys:
        {{
            "has_ripend": str, # yes or no
            "state": str, # options: ["fresh", "partially-ripen", "fully-ripen", "partially-spoiled", "full-spoiled"]
            "description": str, # describe the identified state of the fruit
        }}
     '''),
    ("human", "Please analyze sensor data and return JSON object as mentioned in the instructions."),
])
        output_parser = JsonOutputParser()
        prompt = prompt.format()
        response = self.llm_manager.invoke(prompt.format(combined_response=combined_response), response_format={"type": "json_object"})
        parsed_response = output_parser.parse(response.content)
        return {"ripen_assessment": parsed_response}

    def defect_assessment_node(self, state: OutputState) -> OutputState:
        # Assess defects based on image data
        combined_response = {
            "data": {
                "image_analysis_result": state["image_analysis_result"],
                "hyperspectral_imaging_results": state['hyperspectral_analysis_result']
            }
        }
        prompt = ChatPromptTemplate.from_messages([
            ("system", '''You are an expert at identifying if the fruit is defective from the data coming from image analysis and hyperspectral imaging sensors.
             Below is the data in json format with two keys, "image_analysis_result" and "hyperspectral_imaging_results": 
        {combined_response}
     
        Your task is to return a json object with following keys:
        {{
            "has_defect": str, # yes or no
            "state": List[str], # options: ["bruising", "rot", "sunburn", "skin-cracking", "scarring", "shriveling", "mold"]
            "description": str, # describe the identified state of the fruit
        }}
     '''),
    ("human", "Please analyze image analysis and hyperspectral imaging sensor data and return JSON object as mentioned in the instructions."),
])
        output_parser = JsonOutputParser()
        prompt = prompt.format()
        response = self.llm_manager.invoke(prompt.format(combined_response=combined_response), response_format={"type": "json_object"})
        parsed_response = output_parser.parse(response.content)
        return {"defect_assessment": parsed_response}

    def quality_assessment_node(state: OutputState) -> OutputState:
        # Assess overall quality based on ripeness and defect assessments
        state['quality_assessment'] = {
            "result": "Quality assessed",
            "data": {
                "ripeness": state['ripen_assessment'],
                "defects": state['defect_assessment']
            }
        }
        return state

    def decision_support_node(state: OutputState) -> OutputState:
        # Make a decision based on quality assessment
        state['decision'] = "Decision made based on quality assessment"
        return state

    def decision_node(state):
        analysis_result = state['analysis_result']
        if "score" in analysis_result and int(analysis_result.split(":")[1].strip()) > 5:
            return "high_quality"
        else:
            return "low_quality"
