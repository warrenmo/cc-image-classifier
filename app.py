import json
import streamlit as st

from cdq import (
    DownloadImages, run_classifier, train_image_classifier,
    app_mode_to_title, get_file_content_as_string
)


def main():
    instructions = st.markdown(get_file_content_as_string('instructions.md'))

    st.sidebar.title("What to do next?")
    app_mode = st.sidebar.selectbox("",
        ["Show instructions", "Download images",
         "Train the classifier", "Use/download the classifier",
         "Show the source code"])
    if app_mode == 'Show instructions':
        st.sidebar.success('To continue select "Download images".')
    elif app_mode == 'Download images':
        instructions.empty()
        app_mode_to_title(app_mode)
        DownloadImages().download()
    elif app_mode == 'Train the classifier':
        instructions.empty()
        app_mode_to_title(app_mode)
        train_image_classifier()
    elif app_mode == 'Use/download the classifier':
        instructions.empty()
        app_mode_to_title(app_mode)
        run_classifier()
    elif app_mode == 'Show the source code':
        instructions.empty()
        app_mode_to_title(app_mode)
        st.code(get_file_content_as_string('app.py'))


if __name__ == "__main__":
    main()
