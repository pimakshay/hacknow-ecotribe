from langgraph.graph import StateGraph, END
from backend.utils.ecotribe_agents import EcoTribeAgent
from backend.utils.state import InputState, OutputState

class WorkflowManager:
    def __init__(self):
        self.agent = EcoTribeAgent()
        
    def create_workflow(self) -> StateGraph:
        # Initialize the graph
        workflow = StateGraph(input=InputState, output=OutputState)

        # Add nodes
        workflow.add_node("image_analysis", self.agent.image_analysis_node)
        workflow.add_node("hyperspectral_analysis", self.agent.hyperspectral_analysis_node)
        workflow.add_node("gas_detector_analysis", self.agent.gas_detector_analysis_node)
        workflow.add_node("ripen_assessment", self.agent.ripen_assessment_node)
        workflow.add_node("defect_assessment", self.agent.defect_assessment_node)
        workflow.add_node("quality_assessment", self.agent.quality_assessment_node)
        workflow.add_node("decision_support", self.agent.decision_support_node)

        # Set entry points (independent nodes)
        workflow.set_entry_point("image_analysis")
        workflow.set_entry_point("hyperspectral_analysis")
        workflow.set_entry_point("gas_detector_analysis")

        # Define edges
        workflow.add_edge("image_analysis", "defect_assessment")
        workflow.add_edge("hyperspectral_analysis", "defect_assessment")
        workflow.add_edge("hyperspectral_analysis", "ripen_assessment")
        workflow.add_edge("gas_detector_analysis", "ripen_assessment")
        workflow.add_edge("ripen_assessment", "quality_assessment")
        workflow.add_edge("defect_assessment", "quality_assessment")
        workflow.add_edge("quality_assessment", "decision_support")

        # Set the end point
        workflow.add_edge("decision_support", END)

        return workflow
    
    def returnGraph(self):
        return self.create_workflow().compile()

