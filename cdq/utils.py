import requests
import streamlit as st


__all__ = ['get_file_content_as_string']


@st.cache(show_spinner=False)
def get_file_content_as_string(path):
    """
    Code copied & then modified from:
    https://github.com/streamlit/demo-self-driving/blob/master/streamlit_app.py#L200
    """
    url = (
        'https://raw.githubusercontent.com/warrenmo/cdq/main/' + path
        )
    text = requests.get(url).text
    return text
