#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Galleria image collector
"""

import os
import glob
import logging
from copy import copy
from typing import Set

from docutils import nodes
from sphinx.environment.collectors import EnvironmentCollector
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.util import FilenameUniqDict
from sphinx.locale import __

from sphinx_galleria.directive import galleria

logger = logging.getLogger(__name__)


class GalleriaCollector(EnvironmentCollector):
    """ Collect images for galleria """

    def clear_doc(
            self, app: Sphinx, env: BuildEnvironment, docname: str) -> None:

        if not hasattr(env, 'galleria'):
            env.galleria = FilenameUniqDict()

        if not hasattr(env, 'galleriathumbs'):
            env.galleriathumbs = FilenameUniqDict()

        env.galleria.purge_doc(docname)
        env.galleriathumbs.purge_doc(docname)

    def merge_other(
            self, app: Sphinx, env: BuildEnvironment,
            docnames: Set[str], other: BuildEnvironment) -> None:

        if not hasattr(env, 'galleria'):
            env.galleria = FilenameUniqDict()
        if not hasattr(other, 'galleria'):
            other.galleria = FilenameUniqDict()

        if not hasattr(env, 'galleriathumbs'):
            env.galleriathumbs = FilenameUniqDict()
        if not hasattr(other, 'galleriathumbs'):
            other.galleriathumbs = FilenameUniqDict()

        env.galleria.merge_other(docnames, other.galleria)
        env.galleriathumbs.merge_other(docnames, other.galleria)

    def process_doc(self, app: Sphinx, doctree: nodes.document) -> None:

        if not hasattr(app.env, 'galleria'):
            app.env.galleria = FilenameUniqDict()
        docname = app.env.docname

        for node in doctree.traverse(galleria):
            images = []
            for imageglob in node['images']:
                thumbsize = imageglob['thumbsize']
                size_array = []
                try:
                    for size in thumbsize.split('x'):
                        size_array.append(int(size))
                except ValueError:
                    logger.error(
                        __('thumbsize %s is invalid (use 100x120 format)'),
                        thumbsize)
                    raise

                del imageglob['thumbsize']
                glob_path = os.path.join(
                    os.path.dirname(node.source),
                    imageglob['uri']
                )

                for image_path in glob.glob(glob_path):
                    app.env.galleria.add_file(docname, image_path)

                    basename, ext = os.path.splitext(image_path)
                    thumb_path = basename + ".thumb-" + thumbsize + ext
                    thumb_path_cropped = basename + ".thumb-" + thumbsize
                    thumb_path_cropped += ext
                    if ext.lower() in ('.svg', '.svgz'):
                        thumb_path_cropped = image_path
                        thumb_path = image_path

                    jsonimage = copy(imageglob)
                    jsonimage['thumbsize'] = size_array
                    jsonimage['thumb'] = os.path.relpath(
                        thumb_path_cropped,
                        app.env.srcdir)
                    jsonimage['uri'] = os.path.relpath(
                        image_path,
                        app.env.srcdir
                    )
                    images.append(jsonimage)

                    app.env.dependencies[docname].add(image_path)
                    app.env.dependencies[docname].add(thumb_path_cropped)
                    if not os.access(
                        os.path.join(
                            app.srcdir,
                            image_path), os.R_OK):
                        logger.warning(
                            __('image file not readable %s'),
                            image_path)

                    app.env.galleria.add_file(docname, image_path)
                    app.env.galleriathumbs.add_file(docname, thumb_path)

            node['images'] = images
