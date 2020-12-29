from pathlib import Path

import streamlit as st
from fastai.vision.data import ImageDataLoaders

from .config import IMAGE_DIR


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
        dls = ImageDataLoaders.from_folder(
            IMAGE_DIR, vocab=selected, valid_pct=0.2
            )
