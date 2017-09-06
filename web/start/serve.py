from os.path import dirname, realpath

from flask import Flask, render_template
import requests

import generate


app = Flask(
    __name__,
    template_folder=dirname(realpath(__file__))
)


@app.route('/')
def start_page():
    """Run generate and serve html"""
    context = generate.make_context()
    return render_template('index.j2.html', **context)


@app.route('/style.css')
def style():
    context = dict()
    bing = 'https://www.bing.com'
    try:
        response = requests.get(
            bing + '/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'
        )
        context['background_img'] = bing + response.json()['images'][0]['url']
    except requests.RequestException:
        context['background_img'] = (
            'http://www.bing.com/az/hprichbg/rb/'
            'MeerkatAmuck_EN-US5734433814_1920x1080.jpg'
        )
    return (
        render_template('style.j2.css', **context),
        200,
        {'Content-Type': 'text/css; charset=utf-8'}
    )
