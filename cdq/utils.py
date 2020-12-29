import requests
from PIL import Image
import streamlit as st


from .config import IMAGE_DIR


__all__ = [
    'app_mode_to_title', 'get_file_content_as_string', 'preview_images',
    ]


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


def preview_images(classes, n=3, image_dir=IMAGE_DIR):
    # TODO: random preview?
    st.markdown("### Image preview")
    for c in classes:
        paths = (image_dir/c).iterdir()
        st.markdown(f"**{c}:**")
        cols = st.beta_columns(n)
        for i in range(n):
            cols[i].image(
                Image.open(next(paths)), caption='', use_column_width=True
                )
