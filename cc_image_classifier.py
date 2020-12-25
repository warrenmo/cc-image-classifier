import requests
from pathlib import Path

import numpy as np
import pandas as pd

#import streamlit as st

from fastai.vision import download_images


def main():
    #instructions = st.markdown('# Test')

    num_images_per_class = 500
    page_size = min(500, num_images_per_class)
    num_pages = ((num_images_per_class-1) // page_size) + 1

    license = 'CC0'
    params = {'q': None,
              'license': license,
              'page_size': page_size,
             }

    queries = []
    query_urls = get_urls(queries, num_pages, params)


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
