#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create image galleries
"""
import os

from typing import Dict, Any
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.util.osutil import ensuredir, copyfile
from PIL import Image

from sphinx_galleria import directive
from sphinx_galleria import collector

import pkg_resources
__version__ = pkg_resources.get_distribution(__package__).version
__version_info__ = tuple(int(v) for v in __version__.split('.'))

def copy_images_files(app: Sphinx, env: BuildEnvironment) -> None:

    if hasattr(env, 'galleria') and env.galleria:
        for source in env.galleria:
            relpath = os.path.relpath(source, env.srcdir)
            dest = os.path.join(app.outdir, relpath)
            ensuredir(os.path.dirname(dest))
            copyfile(source, dest)

    if hasattr(env, 'galleriathumbs') and env.galleriathumbs:
        for thumb in env.galleriathumbs:
            relpath = os.path.relpath(thumb, env.srcdir)
            dest = os.path.join(app.outdir, relpath)
            basename, ext = os.path.splitext(dest)

            if ext.lower() in ('.svg', '.svgz'):
                continue

            thumbsize = basename.split('-')[-1].split('x')
            thumbsize = [int(size) for size in thumbsize]
            original = '.'.join(basename.split('.')[:-1]) + ext
            dest = basename + ext
            ensuredir(os.path.dirname(dest))

            with Image.open(original) as im:
                if im.size[0]/im.size[1] > thumbsize[0]/thumbsize[1]:
                    out = im.resize((
                        thumbsize[0],
                        thumbsize[1]
                    ), box=(
                        (im.size[0]-thumbsize[1]*im.size[0]/thumbsize[0])//2,
                        0,
                        (im.size[0]+thumbsize[1]*im.size[0]/thumbsize[0])//2,
                        im.size[1]
                    ))
                else:
                    out = im.resize((
                        thumbsize[0],
                        thumbsize[1]
                    ), box=(
                        0,
                        (im.size[1]-thumbsize[0]*im.size[1]/thumbsize[0])//2,
                        im.size[0],
                        (im.size[1]+thumbsize[0]*im.size[1]/thumbsize[0])//2,
                    ))

                if ext.lower() in ("jpg", "jpeg"):
                    out.save(dest, "JPEG", quality=90)
                else:
                    out.save(dest)


def install_static_files(app: Sphinx, env: BuildEnvironment) -> None:
    path = os.path.join(
        app.builder.outdir,
        '_static',
        'sphinxgalleria'
    )
    source = os.path.join(
        os.path.dirname(__file__),
        'static',
        'sphinxgalleria',
    )

    statics = []
    for dirpath, dirs, files in os.walk(source):
        source_path = os.path.relpath(dirpath, source)
        for static in files:
            statics.append(os.path.join(source_path, static))

    for static in statics:
        static_path = os.path.join(path, static)
        source_path = os.path.join(source, static)
        if not os.path.exists(os.path.dirname(static_path)):
            ensuredir(os.path.dirname(static_path))

        copyfile(source_path, static_path)

        if static.endswith('.css'):
            app.add_css_file(os.path.join('sphinxgalleria', static))


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_node(
        directive.galleria,
        html=(directive.html_visit_galleria, None),
        epub=(directive.html_visit_galleria, None),
        latex=(directive.latex_visit_galleria, None),
        texinfo=(directive.texinfo_visit_galleria, None),
        text=(directive.text_visit_galleria, None),
        man=(directive.man_visit_galleria, None),
        gemini=(directive.gemini_visit_galleria, None),
    )
    app.add_directive('galleria', directive.GalleriaDirective)
    app.add_env_collector(collector.GalleriaCollector)
    app.connect('env-updated', install_static_files)
    app.connect('env-updated', copy_images_files)

    locale_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'locale'
    )
    app.add_message_catalog('sphinx', locale_path)
    return {'version': __version__}
