import json
import base64
import os

from django.core.urlresolvers import reverse
from django.test import TestCase, LiveServerTestCase

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from easter_egg.models import split_image


class _HelperTestCase(TestCase):
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


class EasterEggTestCase(_HelperTestCase):
    url = reverse('index')

    def test_index_page_returns_200(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)

    def test_index_page_returns_json(self):
        r = self.client.get(self.url)
        self.assertEqual(
            r['Content-Type'],
            'application/json',
        )

    def test_index_page_returns_ten_pieces_in_a_list(self):
        r = self.client.get(self.url)
        response = json.loads(r.content)
        self.assertEqual(len(response), 10)

    def test_index_page_returns_split_up_image(self):
        r = self.client.get(self.url)
        response = json.loads(r.content)
        self.assertEqual(
            base64.b64decode(''.join(response)),
            self.content,
        )

    def test_test_page_returns_200(self):
        r = self.client.get(reverse('easter_egg_test'))
        self.assertEqual(r.status_code, 200)


class CoverageTestCase(TestCase):
    def test(self):
        from easter_egg import wsgi
        assert wsgi


class ImageSplitterTestCase(_HelperTestCase):
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
        self.assertEqual(
            base64.b64decode(image_content),
            self.content,
        )


class SleniumTestCase(_HelperTestCase, LiveServerTestCase):
    def setUp(self):
        super(SleniumTestCase, self).setUp()
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test(self):
        self.browser.get(self.live_server_url + reverse('easter_egg_test'))
        keys = ''.join([
            Keys.UP,
            Keys.UP,
            Keys.DOWN,
            Keys.DOWN,
            Keys.LEFT,
            Keys.RIGHT,
            Keys.LEFT,
            Keys.RIGHT,
            'b',
            'a',
        ])
        body = self.browser.find_element_by_tag_name('body')
        body.send_keys(keys)
        image_tag = self.browser.find_element_by_tag_name('img')
        assert image_tag
        image_data = image_tag.get_attribute('src')
        image_data = image_data[len('data:image/png;base64,'):]
        self.assertEqual(
            self.content,
            base64.b64decode(image_data),
        )
