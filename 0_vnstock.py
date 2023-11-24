import streamlit as st 

import api_vstock as vs
import pandas as pd
from pathlib import Path

@st.cache_data
def get_stock_lst():
    ### Wrapper only for caching
    df = vs.get_stock_symbol_lst()
    df['combined'] = df['ticker'] + ' - ' + df['organName']
    return df


# Function to create a download button for a file
def create_download_button(filename):
    with open(filename, "rb") as file:
        btn = st.download_button(
            label=f"Download {filename.name}",
            data=file,
            file_name=filename.name,
            mime='application/vnd.ms-excel'
        )


st.set_page_config(
    page_title="VN Stock",
    page_icon="https://api.dicebear.com/5.x/bottts-neutral/svg?seed=gptLAb"#,
    #menu_items={"About": "GPT Lab is a user-friendly app that allows anyone to interact with and create their own AI Assistants powered by OpenAI's GPT language model. Our goal is to make AI accessible and easy to use for everyone, so you can focus on designing your Assistant without worrying about the underlying infrastructure.", "Get help": None, "Report a Bug": None}
)

st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)
df = get_stock_lst()

st.session_state['stock_selection_lst'] = [] 


with st.sidebar:
    with st.form('Selection'):
        txtselect = st.multiselect(label='Select Stock',options=df['combined'])
        submitted_button = st.form_submit_button()







if submitted_button:
    st.session_state['stock_selection_lst'] = [ i[:3] for i in txtselect]
    # Display a loading message or a progress bar
    with st.spinner('Generating files... This may take up to a minute.'):
        file_lst = vs.generate_download_excel_files(st.session_state['stock_selection_lst'],Path.cwd() / 'output',True)  # Call the file generation function
    # After generating files, display a container with download buttons for each file
    with st.container():
        st.write("Files generated successfully! Click below to download:")
        for file_path in file_lst:
            create_download_button(file_path)







