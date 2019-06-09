# -*- coding: utf-8 -*-

import os
import logging
from mkdocs.commands import build as mkdocs_build
from mkdocs import utils
from mkdocs.structure.files import File, Files, _filter_paths, _sort_files
from mkdocs.structure.nav import get_navigation

log = logging.getLogger(__name__)
log.addFilter(mkdocs_build.DuplicateFilter())
log.addFilter(utils.warning_filter)


def get_files(config):
    """ Walk the `source_dir` and return a Files collection. """
    files = []
    exclude = ['.*', '/templates']

    for source_dir, dirnames, filenames in os.walk(config['source_dir'], followlinks=True):
        relative_dir = os.path.relpath(source_dir, config['source_dir'])
        for dirname in list(dirnames):
            path = os.path.normpath(os.path.join(relative_dir, dirname))
            # Skip any excluded directories
            if _filter_paths(basename=dirname, path=path, is_dir=True, exclude=exclude):
                dirnames.remove(dirname)
        dirnames.sort()
        
        for filename in _sort_files(filenames):
            path = os.path.normpath(os.path.join(relative_dir, filename))
            # Skip any excluded files
            if _filter_paths(basename=filename, path=path, is_dir=False, exclude=exclude):
                continue
            # Skip README.md is an index file also exists in dir
            if filename.lower() == 'readme.md' and 'index.md' in filenames:
                continue
            files.append(File(path, config['source_dir'], config['site_dir'], config['use_directory_urls']))

    return Files(files)


def build(config, live_server=False, dirty=False):
    """ Perform a full site build. """
    from time import time
    start = time()

    # Run `config` plugin events.
    config = config['plugins'].run_event('config', config)

    # Run `pre_build` plugin events.
    config['plugins'].run_event('pre_build', config)

    if not dirty:
        log.info("Cleaning site directory")
        utils.clean_directory(config['site_dir'])
    else:  # pragma: no cover
        # Warn user about problems that may occur with --dirty option
        log.warning("A 'dirty' build is being performed, this will likely lead to inaccurate navigation and other"
                    " links within your site. This option is designed for site development purposes only.")

    if not live_server:  # pragma: no cover
        log.info("Building site to directory: %s", config['site_dir'])
        if dirty and mkdocs_build.site_directory_contains_stale_files(config['site_dir']):
            log.info("The directory contains stale files. Use --clean to remove them.")

    # First gather all data from all files/pages to ensure all data is consistent across all pages.

    files = mkdocs_build.get_files(config)
    env = config['theme'].get_env()
    files.add_files_from_theme(env, config)

    # Run `files` plugin events.
    files = config['plugins'].run_event('files', files, config=config)

    nav = get_navigation(files, config)

    # Run `nav` plugin events.
    nav = config['plugins'].run_event('nav', nav, config=config, files=files)

    log.debug("Reading markdown pages.")
    for file in files.documentation_pages():
        log.debug("Reading: " + file.src_path)
        mkdocs_build._populate_page(file.page, config, files, dirty)

    # Run `env` plugin events.
    env = config['plugins'].run_event(
        'env', env, config=config, files=files
    )

    # Start writing files to site_dir now that all data is gathered. Note that order matters. Files
    # with lower precedence get written first so that files with higher precedence can overwrite them.

    for f in files:
        print(f.page)

    log.debug("Copying static assets.")
    files.copy_static_files(dirty=dirty)

    for template in config['theme'].static_templates:
        mkdocs_build._build_theme_template(template, env, files, config, nav)

    for template in config['extra_templates']:
        mkdocs_build._build_extra_template(template, files, config, nav)

    log.debug("Building markdown pages.")
    for file in files.documentation_pages():
        mkdocs_build._build_page(file.page, config, files, nav, env, dirty)

    # Run `post_build` plugin events.
    config['plugins'].run_event('post_build', config)

    if config['strict'] and utils.warning_filter.count:
        raise SystemExit('\nExited with {} warnings in strict mode.'.format(utils.warning_filter.count))

    log.info('site built in %.2f seconds', time() - start)
