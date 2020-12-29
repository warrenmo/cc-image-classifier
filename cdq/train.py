from pathlib import Path

import streamlit as st
from fastai.vision.all import *
#from fastai.vision.data import ImageDataLoaders

from .config import IMAGE_DIR
from .utils import preview_images


__all__ = ['train_image_classifier']


def train_image_classifier():
    class_paths = list(IMAGE_DIR.iterdir())
    classes = [cp.name for cp in class_paths]
    selected = st.multiselect(
        "Detected the following classes. Which would you like to classify?",
        classes, default=classes
        )
    if not selected:
        st.stop()
    press = st.button("Submit")
    if press:
        preview_images(classes)
        # TODO: let (advanced) users choose valid_pct, seed, batch size and
        #           transform options
        dls = ImageDataLoaders.from_folder(
            IMAGE_DIR, vocab=selected, valid_pct=0.2, seed=0,
            item_tfms=Resize(224)
            )

