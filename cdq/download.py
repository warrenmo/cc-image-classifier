import requests
from pathlib import Path

import streamlit as st
from fastai.vision.utils import download_images, verify_images

from .config import IMAGE_DIR


__all__ = ['DownloadImages']


class DownloadImages:
    """
    TODO: class doc
    """
    def __init__(self, license='CC0', image_dir=IMAGE_DIR):
        self.classes = []
        self.nipc = 1   # num images per class
        self.num_pages = 1
        self.page_size = 20
        self.license = license
        self.url_dict = {}

        self.image_dir = image_dir
        self.image_dir.mkdir(parents=True, exist_ok=True)

    def download(self):
        self._get_classes()
        self._get_nipc()

        press = st.button("Submit & Download")
        if press:
            self._show_classes_nipc()
            self._get_ps_np()
            self._get_urls()
            self._download_urls()
            self._verify_downloads()

    def _get_classes(self):
        raw_text = st.text_area(
            "Specify the images you wish to classify:",
            value="dog\ncat\ngothic architecture"
            )
        self.classes = [c for c in raw_text.split('\n') if c.strip()]
        if len(self.classes) < 2:
            st.error("At least 2 classes must be given.")
            st.stop()

    def _get_nipc(self):
        self.nipc = st.number_input(
            "Specify the number of images per class:",
            min_value=1,
            max_value=1000,
            value=200
            )
        # TODO: check to see if 50 images is enough
        # TODO: min # of images recommended varies with # of classes
        if self.nipc < 50:
            st.warning((
                "Warning: expect unreliable performance "
                "with fewer than 50 images per class"
                ))

    def _show_classes_nipc(self):
        # TODO: improve human readability of output
        st.text(f"{'Classes:':<28}{', '.join(self.classes):>40}")
        st.text(f"{'Number of images per class:':<28}{self.nipc:>40}")
        st.text((
            f"{'Total number of images:':<28}"
            f"{self.nipc*len(self.classes):>40}"
            ))

    def _get_ps_np(self):
        self.page_size = min(500, self.nipc)
        self.num_pages = ((self.nipc-1) // self.page_size) + 1

    def _get_urls(self):
        for c in self.classes:
            urls = []
            for page in range(1, self.num_pages+1):
                page_urls = self._get_urls_one_c(
                    c, page=page, page_size=self.page_size,
                    license=self.license
                    )
                urls.extend(page_urls)
            self.url_dict[c] = urls

    @staticmethod
    def _get_urls_one_c(q, *, page, page_size, license):
        params = {
            'q': q,
            'page': page,
            'page_size': page_size,
            'license': license
            }
        r = requests.get(
            'https://api.creativecommons.engineering/v1/images',
            params=params
            )
        return [res['url'] for res in r.json()['results']]

    def _download_urls(self):
        for c, urls in self.url_dict.items():
            with st.spinner(f"Downloading '{c}' images..."):
                download_images(
                    self.image_dir/c.replace(' ', '_'), urls=urls
                    )
            st.success(f"Images of '{c}' downloaded successfully!")

    def _verify_downloads(self):
        st.spinner('Verifying the images...')
        fails = self._get_fails(self.url_dict, image_dir=self.image_dir)
        self._delete_fails(fails)

    @staticmethod
    def _get_fails(url_dict, *, image_dir):
        if not image_dir.exists():
            st.exception(
                FileNotFoundError(f"No such directory: {image_dir.absolute()}")
                )
        fails = {
            c: verify_images(Path.iterdir(image_dir/c)) for c in url_dict.keys()
            }
        return fails

    @staticmethod
    def _delete_fails(fails):
        """
        TODO: give users more info/control on which images to be deleted.
        """
        if sum(len(f) for f in fails.values()) == 0:
            st.success("No images failed to open :sunglasses:")
        else:
            for c, f in fails.items():
                if len(f) == 0:
                    continue
                f.map(Path.unlink)
                st.success(
                    f"Deleted {len(f)} images for class {c} that failed to open."
                    )

