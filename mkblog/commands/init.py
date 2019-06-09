# coding: utf-8

import io
import logging
import os

config_text = 'site_name: My Blog\n'
index_text = """# Welcome to MkBlogs

## Commands

* `mkblog init [dir-name]` - Create a new project.
* `mkblog serve` - Start the live-reloading blog server.
* `mkblog build` - Build the documentation site.
* `mkblog help` - Print this help message.

## Project layout

    mkblog.yml    # The configuration file.
    source/
        _posts/
            hello-world.md  # The documentation homepage.
        ...         # Other markdown pages, images and other files.
"""

log = logging.getLogger(__name__)


def init(output_dir):

    source_dir = os.path.join(output_dir, 'source')
    config_path = os.path.join(output_dir, 'mkblog.yml')
    posts_path = os.path.join(source_dir, '_posts')

    if os.path.exists(config_path):
        log.info('Project already exists.')
        return

    if not os.path.exists(output_dir):
        log.info('Creating project directory: %s', output_dir)
        os.mkdir(output_dir)

    log.info('Writing config file: %s', config_path)
    io.open(config_path, 'w', encoding='utf-8').write(config_text)

    if os.path.exists(posts_path):
        return

    log.info('Writing initial posts: %s', posts_path)
    if not os.path.exists(source_dir):
        os.mkdir(source_dir)
        os.mkdir(posts_path)
