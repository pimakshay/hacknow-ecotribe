import os, sys
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
from utils import create_ripness_level_gauge, create_quality_level_gauge

# set system path
CURR_DIR = os.path.dirname('__file__')
ROOT_DIR=os.path.join('../')
sys.path.append(ROOT_DIR)

from backend.utils.workflow_manager import WorkflowManager
graph = WorkflowManager().returnGraph()

def main():
    sidebar = st.sidebar

    # set 'wide' as the default page layout
    st.set_page_config(layout="wide")
    sidebar.title("Parameters")

    # set the title without using bold font and by using white and make it left aligned
    st.markdown("<h2 style='text-align: left; center;'>EcoTribe</h2>", unsafe_allow_html=True)


    # Step 1: Upload the image
    uploaded_file = sidebar.file_uploader("Choose an image file", type=["jpg", "png", "jpeg"])
    
    # print the filepath of uploaded_file
    
    if uploaded_file is not None:
        # Create three columns
        col1, col2 = st.columns(2)
        # Add a title on top of each separation line, describing the content of each column
        with col1:
            st.markdown("<h3 style='text-align: center;'>Uploaded Image</h3>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h3 style='text-align: center;'>Fruit Quality Assessment</h3>", unsafe_allow_html=True)


        # add thin separation line in streamlit for each column
        col1.markdown("---")
        col2.markdown("---")
        with col1:
            # Display the uploaded image on the left side
            st.image(Image.open(uploaded_file), use_column_width=True)

        with col2:
            st.markdown("""
            <style>
            [data-testid="column"] {
                overflow: auto;
                height: 70vh;
            }
            </style>
            """, unsafe_allow_html=True)
            upload_dir = "uploaded_files"
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            file_path = os.path.join(upload_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            # st.write("File path:", file_path)
            run_pipeline_button = sidebar.button("Run Pipeline")
            if run_pipeline_button:
                result_data = graph.invoke({"image_path": file_path})


                # Decision Support Summary
                st.header("Decision Support Summary")
                decision = result_data['decision_support_result']
                st.info(f"**Recommendation:** {decision['recommendation']}")
                st.write(f"**Shelf Life:** {decision['shelf_life']}")
                st.write(f"**Discount:** {decision['discount'] if decision['discount'] else 'N/A'}")

                # Quality Assessment Overview
                st.subheader("Quality Assessment Overview")
                quality = result_data['quality_assessment_result']
                st.warning(f"**Quality Standard:** {quality['quality_standard']}")
                st.write(quality['description'])

                # Detailed Analysis Section
                st.header("Visual Analysis")
                vis_tab_names = ["Ripen Assessment", "Quality Assessment"]
                vis_tabs = st.tabs(vis_tab_names)
                
                with vis_tabs[0]:
                    st.plotly_chart(create_ripness_level_gauge(result_data['ripen_assessment_result']['state'], "Ripeness Level"), use_container_width=True)
                
                with vis_tabs[1]:
                    st.plotly_chart(create_quality_level_gauge(result_data['quality_assessment_result']['quality_standard'], "Quality Level"), use_container_width=True)


                # Detailed Analysis Section
                st.header("Detailed Analysis")
                tab_names = ["Image Analysis", "Hyperspectral Analysis", "Gas Detector", "Ripen Assessment", "Defect Assessment"]
                tabs = st.tabs(tab_names)

                with tabs[0]:
                    st.write(result_data['image_analysis_result'])

                with tabs[1]:
                    st.write(result_data['hyperspectral_analysis_result'])

                with tabs[2]:
                    gas_data = result_data['gas_detector_result']
                    for gas, level in gas_data.items():
                        st.write(f"**{gas.replace('_', ' ').title()}:** {level}")

                with tabs[3]:
                    st.write(result_data['ripen_assessment_result'])

                with tabs[4]:
                    defect_data = result_data['defect_assessment_result']
                    st.write(f"**Defects Detected:** {', '.join(defect_data['state'])}")
                    st.write(defect_data['description'])

if __name__ == "__main__":
    main()