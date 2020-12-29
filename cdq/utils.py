import requests
import streamlit as st


__all__ = ['app_mode_to_title', 'get_file_content_as_string']


def app_mode_to_title(app_mode):
    st.markdown(f"# {app_mode}")


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
