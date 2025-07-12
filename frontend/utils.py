import plotly.graph_objects as go

def create_gauge(value, title, max_value=100):
    return go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, max_value]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, max_value/3], 'color': "green"},
                    {'range': [max_value/3, 2*max_value/3], 'color': "orange"},
                    {'range': [2*max_value/3, max_value], 'color': "red"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': value}}))

def create_ripness_level_gauge(value, title, max_value=100):
    # Mapping of string values to numerical ranges
    value_mapping = {
        'full-spoiled': 100,
        'partially-spoiled': 75,
        'fully-ripen': 50,
        'partially-ripen': 25,
        'fresh': 0
    }
    
    # Get the numerical value from the mapping, default to 0 if not found
    num_value = value_mapping.get(value, 0)
    
    return go.Figure(go.Indicator(
        mode = "gauge+number",
        value = num_value,
        title = {'text': title+"\Lower the better"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, max_value]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, max_value/3], 'color': "green"},
                    {'range': [max_value/3, 2*max_value/3], 'color': "orange"},
                    {'range': [2*max_value/3, max_value], 'color': "red"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': num_value}}))

def create_quality_level_gauge(value: str, title: str, max_value=100):
    #["Extra Class", "Class I", "Class II", "Class III", "Below Standard"]
    # Mapping of string values to numerical ranges
    value_mapping = {
        'Extra Class': 100,
        'Class I': 75,
        'Class II': 50,
        'Class III': 25,
        'Below Standard': 0
    }
    
    # Get the numerical value from the mapping, default to 0 if not found
    num_value = value_mapping.get(value, 0)
    
    return go.Figure(go.Indicator(
        mode = "gauge+number",
        value = num_value,
        title = {'text': title+"\nHigher the better"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, max_value]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, max_value/3], 'color': "red"},
                    {'range': [max_value/3, 2*max_value/3], 'color': "orange"},
                    {'range': [2*max_value/3, max_value], 'color': "green"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': num_value}}))

# Example result data:
example_result_data = {'image_analysis_result': {'object_name': 'apple',
  'color': 'red',
  'surface_texture': 'smooth',
  'has_mould_spot': 'no',
  'shape': 'normal'},
 'hyperspectral_analysis_result': {'has_spoilage': 'no',
  'description': 'The fruit appears to be fresh and ripe.'},
 'gas_detector_result': {'level_of_ethylene': 'normal',
  'level_of_CO2': 'normal',
  'level_of_methane': 'not_detected',
  'level_of_ammonia': 'not_detected',
  'level_of_hydrogen_sulfide': 'not_detected'},
 'ripen_assessment_result': {'has_ripend': 'yes',
  'state': 'fully-ripen',
  'description': 'The fruit appears to be fully ripened based on the hyperspectral imaging results and normal levels of ethylene and CO2 detected by the gas sensors.'},
 'defect_assessment_result': {'has_defect': 'no',
  'state': [],
  'description': 'The fruit appears to be fresh and ripe with no visible defects.'},
 'quality_assessment_result': {'quality_standard': 'Extra Class',
  'description': 'The fruit is considered Extra Class as it is fully ripened, free from defects, and in excellent condition for immediate consumption.'},
 'decision_support_result': {'discount': 0,
  'shelf_life': '7-10 days',
  'recommendation': 'Premium quality fruit. No discount needed. Display prominently. Shelf life: 7-10 days'}}
