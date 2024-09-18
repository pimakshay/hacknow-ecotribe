from typing import TypedDict, List

class InputState(TypedDict):
    image_path: str
    image_analysis_result: dict # name of the fruit or vegetable
    
    hyperspectral_analysis_result: dict # yes or no
    
    gas_detector_result: dict

    ripen_assessment_result: dict

    defect_assessment_result: dict

    quality_assessment_result: dict

    decision_support_result: dict

class OutputState(TypedDict):
    # image_path: str
    image_analysis_result: dict # name of the fruit or vegetable
    
    hyperspectral_analysis_result: dict # yes or no
    
    gas_detector_result: dict

    ripen_assessment_result: dict

    defect_assessment_result: dict

    quality_assessment_result: dict

    decision_support_result: dict
# class OutputState(TypedDict):
#     object_name: str # name of the fruit or vegetable
#     color: str # color of the fruit
#     surface_texture: str # texture of the surface: ToDo Type?
#     has_model_spot: str # yes or no
    
#     has_spoilage: str # yes or no
    
#     level_of_ethylene: str # ["excessive", "high", "normal"] # excessive means already ripened
#     level_of_CO2: str # ["excessive", "high", "normal"] # spike in CO2 indicates reduced shelf life
#     level_of_methane: str # if methane detected, fruit is spoiled
#     level_of_ammonia: str # Indicator: The presence of ammonia indicates significant spoilage and bacterial activity.
#     level_of_hydrogenSulfide: str
