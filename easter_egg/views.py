import json
from tempfile import NamedTemporaryFile

import requests

from django.http import HttpResponse
from django.shortcuts import render_to_response

from easter_egg.models import split_image


def index(request):
    content = requests.get(
        'https://www.google.com/images/srpr/logo11w.png',
    ).content
    with NamedTemporaryFile('rw+b') as f:
        f.write(content)
        f.seek(0)
        f.flush()
        data = [
            split_image(f.name, i, 10)
            for i in range(1, 11)
        ]
    return HttpResponse(
        json.dumps(data),
        content_type='application/json',
    )


def test(request):
    return render_to_response('test.html', {})
