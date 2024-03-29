# -*- coding: utf-8 -*-
import logging
import shutil
import tempfile

from mkdocs.commands.serve import _livereload, _static_server
from mkblog.commands.build import build
from mkblog.config import load_config

log = logging.getLogger(__name__)


def serve(config_file=None, dev_addr=None, strict=None, theme=None,
          theme_dir=None, livereload='livereload'):
    """
    Start the MkDocs development server

    By default it will serve the documentation on http://localhost:8000/ and
    it will rebuild the documentation and refresh the page automatically
    whenever a file is edited.
    """

    # Create a temporary build directory, and set some options to serve it
    # PY2 returns a byte string by default. The Unicode prefix ensures a Unicode
    # string is returned. And it makes MkDocs temp dirs easier to identify.
    site_dir = tempfile.mkdtemp(prefix='mkdocs_')

    def builder():
        log.info("Building documentation...")
        config = load_config(
            config_file=config_file,
            dev_addr=dev_addr,
            strict=strict,
            theme=theme,
            theme_dir=theme_dir,
            site_dir=site_dir
        )
        # Override a few config settings after validation
        config['site_url'] = 'http://{0}/'.format(config['dev_addr'])

        live_server = livereload in ['dirty', 'livereload']
        dirty = livereload == 'dirty'
        build(config, live_server=live_server, dirty=dirty)
        return config

    try:
        # Perform the initial build
        config = builder()

        host, port = config['dev_addr']

        if livereload in ['livereload', 'dirty']:
            _livereload(host, port, config, builder, site_dir)
        else:
            _static_server(host, port, site_dir)
    finally:
        shutil.rmtree(site_dir)
