import json
import streamlit as st

from cdq import (
    DownloadImages, run_classifier, train_classifier,
    get_file_content_as_string
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
        DownloadImages().download()
    elif app_mode == 'Train the classifier':
        instructions.empty()
        train_classifier()
    elif app_mode == 'Use/download the classifier':
        instructions.empty()
        run_classifier()
    elif app_mode == 'Show the source code':
        instructions.empty()
        st.code(get_file_content_as_string('cc_image_classifier.py'))


def instructions():
    #with open('input_labels.json', 'r') as j:
    #    labels = json.load(j)

    #st.markdown("### Pick the kinds of images you want to classify")
    #classes = st.text_area(
    #    labels['classes'],
    #    value="dog\ncat\ngothic architecture").split('\n')
    #st.write("Here's an example of valid input!")
    #st.markdown((
    #    "![classes_input_example](https://"
    #    "raw.githubusercontent.com/warrenmo/"
    #    "cc-image-classifier/master/class_input_example.jpg)"
    #    ))

    #st.markdown('### Pick the number of photos per class')
    #num_photos_per_class = st.number_input(
    #    labels['num_photos_per_class'],
    #    min_value=1,
    #    max_value=1000,
    #    value=200
    #    )
    #return classes, num_photos_per_class
    #
    pass


if __name__ == "__main__":
    main()
