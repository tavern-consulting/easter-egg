import base64
import os

from django.core.urlresolvers import reverse
from django.test import TestCase

import requests

from easter_egg.models import split_image


class EasterEggTestCase(TestCase):
    def test_index_page_returns_200(self):
        url = reverse('index')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)


class CoverageTestCase(TestCase):
    def test(self):
        from easter_egg import wsgi
        assert wsgi


class ImageSplitterTestCase(TestCase):
    path_to_image = '/tmp/google_logo.png'

    def setUp(self):
        if os.path.isfile(self.path_to_image):
            with open(self.path_to_image) as f:
                self.content = f.read()
            return

        self.content = requests.get(
            'https://www.google.com/images/srpr/logo11w.png',
        ).content

        with open(self.path_to_image, 'w') as f:
            f.write(self.content)

    def test_N_is_1_returns_image(self):
        image_content = split_image(self.path_to_image, 1, 1)
        self.assertEqual(
            base64.b64decode(image_content),
            self.content,
        )

    def test_N_is_2_returns_half_image(self):
        image_content = ''.join([
            split_image(self.path_to_image, 1, 2),
            split_image(self.path_to_image, 2, 2),
        ])
        self.assertEqual(
            base64.b64decode(image_content),
            self.content,
        )

    def test_N_is_3(self):
        image_content = ''.join([
            split_image(self.path_to_image, 1, 3),
            split_image(self.path_to_image, 2, 3),
            split_image(self.path_to_image, 3, 3),
        ])
        self.assertEqual(
            base64.b64decode(image_content),
            self.content,
        )

    def test_N_is_1337(self):
        image_content = ''.join([
            split_image(self.path_to_image, i, 1337)
            for i in range(1, 1338)
        ])
        with open('a.png', 'w') as f:
            f.write(base64.b64decode(image_content))
        self.assertEqual(
            base64.b64decode(image_content),
            self.content,
        )
