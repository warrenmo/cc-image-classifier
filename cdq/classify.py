from pathlib import Path

import streamlit as st
from fastai.vision.all import *

from .config import IMAGE_DIR
from .utils import preview_images


__all__ = ['train_image_classifier', 'classify_images']


def train_image_classifier():
    # TODO: time to break up this overloaded function as well
    class_paths = list(IMAGE_DIR.iterdir())
    classes = [cp.name for cp in class_paths if cp.name != 'MODELS']
    selected = st.multiselect(
        "Detected the following classes. Which would you like to classify?",
        classes, default=classes
        )
    if not selected:
        st.stop()
    press = st.button("Submit")
    if press:
        preview_images(selected)
        # TODO: let (advanced) users choose valid_pct, seed, batch size and
        #           transform options
        dls = ImageDataLoaders.from_folder(
            IMAGE_DIR, vocab=selected, valid_pct=0.2, seed=0,
            item_tfms=Resize(224)
            )
        learn = cnn_learner(dls, resnet34, metrics=error_rate)
        learn.model_dir = 'MODELS'
        # TODO: allow users to specify how long to train
        # TODO: give users update similar to that in the terminal from fastai
        # TODO: allow users to train more if unsatisfactory performance after 1
        # round of fine_tune()
        with st.spinner("Training the classifier..."):
            learn.fine_tune(1)

        # TODO: give users performance stats
        st.success("Training: Complete!")

        with st.spinner("Saving the classifier..."):
            # TODO: smarter naming scheme
            model_name = '-'.join(classes)
            learn.save(model_name)
        st.success(f"Model saved at '{learn.path/learn.model_dir/model_name}'")


def classify_images():
    # TODO: time to break up this overloaded function as well
    model_paths = list((IMAGE_DIR/'MODELS').iterdir())
    models = [p.name.split('.')[0] for p in model_paths]
    model_name = st.selectbox(
        "Detected the following classifiers. Which would you like to use?",
        models,
        )
    if not model_name:
        st.stop()
    press = st.button("Continue")
    if press:
        with st.spinner("Loading the classifier..."):
            selected = model_name.split('-')
            dls = ImageDataLoaders.from_folder(
                IMAGE_DIR, vocab=selected, valid_pct=0.2, seed=0,
                item_tfms=Resize(224)
                )
            learn = cnn_learner(dls, resnet34, metrics=error_rate)
            learn.model_dir = 'MODELS'
            learn.load(model_name)
        st.success("Loading: Complete!")

        # TODO: should be able to upload multiple images
        image = st.file_uploader("Upload an image:", type=['png', 'jpg'])
        st.write(type(image))
        st.write(image)
        st.write(bool(image))
        if not image:
            st.stop()
        pred = learn.predict(image.read())
        st.write(f"Prediction:\t{pred[0]}")
        image.seek(0)
