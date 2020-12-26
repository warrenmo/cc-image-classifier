import requests
from pathlib import Path

import numpy as np
import pandas as pd

import streamlit as st

from fastai.vision import download_images


def main():
    instructions = st.markdown('# Test')

    classes, num_images_per_class = ui()

    num_images_per_class = 500
    page_size = min(500, num_images_per_class)
    num_pages = ((num_images_per_class-1) // page_size) + 1

    license = 'CC0'
    params = {'q': None,
              'license': license,
              'page_size': page_size,
             }

    queries = []
    #query_urls = get_urls(queries, num_pages, params)


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


def ui():
    labels = {}
    with open('input_labels.txt', 'r') as infile:
        for i, line in enumerate(infile):
            if i % 2 == 0:
                key = line.strip('\n')
            else:
                labels[key] = line.strip('\n')


    st.markdown('### Pick the kinds of images you want to classify')
    classes = st.text_area(labels['classes']).split('\n')

    st.markdown('### Pick the number of photos per class')
    num_photos_per_class = st.number_input(labels['num_photos_per_class'],
                                           min_value=1,
                                           max_value=1000,
                                           value=200)
    return classes, num_photos_per_class


if __name__ == "__main__":
    main()
