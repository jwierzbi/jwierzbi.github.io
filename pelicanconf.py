#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Jarosław Wierzbicki'
SITENAME = 'blog.laobo.dev'
# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'https://blog.laobo.dev'

PATH = 'content'
ARTICLE_PATHS = ['blog']
THEME = 'themes/minimal'

ARTICLE_URL = 'blog/{slug}.html'
ARTICLE_SAVE_AS = 'blog/{slug}.html'

TIMEZONE = 'Asia/Taipei'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('Facebook', 'https://www.facebook.com/jwierzbi'),
    ('Instagram', 'https://www.instagram.com/wierzbicki.jaroslaw/'),
    ('Twitter', 'https://twitter.com/j_wierzbicki'),
    ('Github', 'https://github.com/jwierzbi'),
    ('LinkedIn', 'https://www.linkedin.com/in/jaroslaw-wierzbicki-14845043'),
)

DEFAULT_PAGINATION = 10

# Static files to be coppied to root

STATIC_PATHS = [
    'extra/CNAME'
]

# Plugins

PLUGIN_PATHS = ['plugins']
PLUGINS = ['summary', 'rstfootnotes']

# Enable document-relative URLs when developing
RELATIVE_URLS = True
