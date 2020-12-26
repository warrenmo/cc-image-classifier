import requests
from pathlib import Path

import numpy as np
import pandas as pd

import streamlit as st

from fastai.vision import download_images


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
        download_images()
    elif app_mode == 'Train the classifier':
        train_classifier()
    elif app_mode == 'Use/download the classifier':
        run_classifier()
    elif app_mode == 'Show the source code':
        instructions.empty()
        st.code(get_file_content_as_string('cc_image_classifier.py'))

    #classes, num_images_per_class = ui()

    #num_images_per_class = 500
    #page_size = min(500, num_images_per_class)
    #num_pages = ((num_images_per_class-1) // page_size) + 1

    #license = 'CC0'
    #params = {'q': None,
    #          'license': license,
    #          'page_size': page_size,
    #         }

    #queries = []
    #query_urls = get_urls(queries, num_pages, params)


def instructions():
    labels = {}
    with open('input_labels.txt', 'r') as infile:
        for i, line in enumerate(infile):
            if i % 2 == 0:
                key = line.strip('\n')
            else:
                labels[key] = line.strip('\n')


    st.markdown("### Pick the kinds of images you want to classify")
    classes = st.text_area(labels['classes'],
                value="dog\ncat\ngothic architecture").split('\n')
    st.write("Here's an example of valid input!")
    st.markdown("![classes_input_example](https://" \
                "raw.githubusercontent.com/warrenmo/" \
                "cc-image-classifier/master/class_input_example.jpg)")

    st.markdown('### Pick the number of photos per class')
    num_photos_per_class = st.number_input(labels['num_photos_per_class'],
                                           min_value=1,
                                           max_value=1000,
                                           value=200)
    return classes, num_photos_per_class


def download_images():
    labels = {}
    with open('input_labels.txt', 'r') as infile:
        for i, line in enumerate(infile):
            if i % 2 == 0:
                key = line.strip('\n')
            else:
                labels[key] = line.strip('\n')


    st.markdown("### What images do you want to classify?")
    classes = st.text_area('').split('\n')

    st.markdown('### How many photos per class?')
    num_photos_per_class = st.number_input('',
                                           min_value=1,
                                           max_value=1000,
                                           value=200)
    return classes, num_photos_per_class


def train_classifier():
    pass


def run_classifier():
    pass


def get_urls(queries, num_pages, params):
    query_urls = {}
    for q in queries:
        params['q'] = q
        urls = []

        for page in range(1, num_pages+1):
            params['page'] = page
            page_urls = _get_urls_one_q(q, params)
            urls.extend(page_urls)

        query_urls[q] = urls
    return query_urls


def _get_urls_one_q(q, params):
    params['q'] = q
    r = requests.get('https://api.creativecommons.engineering/v1/images',
                     params=params)
    params['q'] = None
    return [res['url'] for res in r.json()['results']]




if __name__ == "__main__":
    main()
