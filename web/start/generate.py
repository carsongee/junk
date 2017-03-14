#!/usr/bin/env python
"""
Generates a little start page.
"""
from glob import glob
import io
from os.path import dirname, expanduser, join, realpath
from random import randint

from jinja2 import Environment, FileSystemLoader
import requests
import yaml

PATH = dirname(realpath(__file__))
TEMPLATES = (
    ('index.j2.html', 'index.html'),
    ('style.j2.css', 'style.css'),
)
WALLPAPER_DIR = expanduser('~/Pictures/Wallpapers/')


def render(template, context):
    """Renders a jinja template file"""
    jinja_env = Environment(loader=FileSystemLoader(PATH))
    return jinja_env.get_template(template).render(context)


def rando(list_like):
    """
    Returns a random item from the list_like object.
    """
    return list_like[randint(0, len(list_like) - 1)]


def main():
    """Main function."""
    context = dict()
    data = yaml.load(io.open(join(PATH, 'data.yml'), 'r', encoding='UTF-8'))
    context['greeting'] = rando(data['greetings'])
    context['fixed_links'] = data['fixed_links']
    try:
        context['quote'] = rando(requests.get(
            'https://gist.githubusercontent.com/dmakk767/'
            '9375ff01aff76f1788aead1df9a66338/raw/'
            '491f8c2e91b7d3b8f1c8230e32d9c9bc1a1adfa6/Quotes.json%2520'
        ).json())
    except requests.RequestException:
        pass

    background_list = glob(WALLPAPER_DIR + '*.jpg')
    if background_list:
        context['background_img'] = rando(background_list)
    for src, dst in TEMPLATES:
        with io.open(
                join(PATH, dst),
                'w',
                encoding='UTF-8'
        ) as file_descriptor:
            file_descriptor.write(
                render(src, context)
            )

if __name__ == '__main__':
    main()
