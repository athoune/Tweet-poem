#!/usr/bin/env python
# -*- coding: utf8 -*-

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

setup(name='Tweet-poem',
	version='0.2',
	license='GPL-3',
	description='Poems from tweeter',
	author='Mathieu Lecarme',
	author_email='mathieu@garambrogne.net',
	url='http://github.com/athoune/Tweet-poem',
	packages=['tweetpoem'],
	package_dir={'': 'src/'},
	scripts=['bin/tweetpoem'],
	install_requires=["tweepy"]#, "tornado"],
)
