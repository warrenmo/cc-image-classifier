import json
import requests
from pathlib import Path

import numpy as np
import pandas as pd

import streamlit as st

from fastai.vision.utils import download_images


def main():
    instructions = st.markdown('# Test')

    st.sidebar.title("What to do next?")
    app_mode = st.sidebar.selectbox("",
        ["Show instructions", "Download images",
         "Train the classifier", "Use/download the classifier",
         "Show the source code"])
    if app_mode == 'Show instructions':
        st.sidebar.success('To continue select "Download images".')
    elif app_mode == 'Download images':
        instructions.empty()
        download_data()
    elif app_mode == 'Train the classifier':
        instructions.empty()
        train_classifier()
    elif app_mode == 'Use/download the classifier':
        instructions.empty()
        run_classifier()
    elif app_mode == 'Show the source code':
        instructions.empty()
        st.code(get_file_content_as_string('cc_image_classifier.py'))

    #queries = []
    #query_urls = get_urls(queries, num_pages, params)


def instructions():
    with open('input_labels.json', 'r') as j:
        labels = json.load(j)

    st.markdown("### Pick the kinds of images you want to classify")
    classes = st.text_area(
        labels['classes'],
        value="dog\ncat\ngothic architecture").split('\n')
    st.write("Here's an example of valid input!")
    st.markdown((
        "![classes_input_example](https://"
        "raw.githubusercontent.com/warrenmo/"
        "cc-image-classifier/master/class_input_example.jpg)"
        ))

    st.markdown('### Pick the number of photos per class')
    num_photos_per_class = st.number_input(
        labels['num_photos_per_class'],
        min_value=1,
        max_value=1000,
        value=200
        )
    return classes, num_photos_per_class


def download_data():
    # TODO: break up this overloaded function
    classes, num_images_per_class = [], 1
    st.markdown("# Download images")

    # TODO: handle empty lines
    classes = st.text_area(
        "What images do you want to classify?",
        value="dog\ncat\ngothic architecture"
        )
    classes = classes.split('\n')
    per_class = st.number_input(
        "How many images per class?",
        min_value=1,
        max_value=1000,
        value=200
        )
    press = st.button("Submit & Download")
    if press:
        # TODO: improve human readability of output
        st.text(f"{'Classes:':<28}{', '.join(classes):>40}")
        st.text(f"{'Number of images per class:':<28}{per_class:>40}")
        st.text((
            f"{'Total number of images:':<28}"
            f"{per_class*len(classes):>40}"
            ))

        page_size = min(500, per_class)
        num_pages = ((num_images_per_class-1) // page_size) + 1

        url_dict = _get_urls(classes, num_pages, page_size=page_size)
        _download_urls(url_dict)


def _get_urls(queries, num_pages, *, page_size, **kwargs):
    query_urls = {}
    for q in queries:
        urls = []
        for page in range(1, num_pages+1):
            page_urls = _get_urls_one_q(
                q, page=page, page_size=page_size, **kwargs
                )
            urls.extend(page_urls)
        query_urls[q] = urls
    return query_urls


def _get_urls_one_q(q, *, page, page_size, license='CC0'):
    params = {
        'q': q,
        'page': page,
        'page_size': page_size,
        'license': license
        }
    r = requests.get('https://api.creativecommons.engineering/v1/images',
                     params=params)
    return [res['url'] for res in r.json()['results']]


def _download_urls(url_dict, image_dir=Path('./cic_images')):
    image_dir = Path('./cic_images')
    image_dir.mkdir(exist_ok=True)
    for c, urls in url_dict.items():
        with st.spinner(f"Downloading images for: {c}"):
            download_images(image_dir/c.replace(' ', '_'), urls=urls)
        st.success(f"Success!")


def train_classifier():
    pass


def run_classifier():
    pass


if __name__ == "__main__":
    main()
