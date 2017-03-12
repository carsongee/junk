#!/usr/bin/env python
"""
Generates a little start page.
"""
from __future__ import print_function
import io
from glob import glob
from os.path import dirname, expanduser, join, realpath
from random import randint

from jinja2 import Environment, FileSystemLoader

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


def main():
    """Main function."""
    context = dict()

    background_list = glob(WALLPAPER_DIR + '*.jpg')
    if background_list:
        context['background_img'] = background_list[
            randint(0, len(background_list) - 1)
        ]
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
    print('Starting')
    main()
    print('Ending')
