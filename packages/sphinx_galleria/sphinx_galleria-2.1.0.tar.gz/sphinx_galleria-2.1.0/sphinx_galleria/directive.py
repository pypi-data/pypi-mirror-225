#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Galleria directive
"""

import uuid
import json
from typing import Sequence

from docutils import nodes
from docutils.parsers.rst import Directive
import docutils.parsers.rst.directives as directives

from sphinx.writers.html import HTMLTranslator
from sphinx.writers.latex import LaTeXTranslator
from sphinx.writers.texinfo import TexinfoTranslator
from sphinx.writers.text import TextTranslator
from sphinx.writers.manpage import ManualPageTranslator
from sphinx.util.osutil import relative_uri
from sphinx.locale import _
from sphinx.addnodes import translatable


def length_or_percentage_or_unitless(argument: str):
    length_units = [
        'em', 'rem', 'ex',
        'px', 'pt',
        'in', 'cm', 'mm', 'pt', 'pc',
        'vh', 'vw',
        '%', ''
    ]
    return directives.get_measure(argument, length_units)


class galleria(nodes.General, nodes.Element, translatable):
    def preserve_original_messages(self) -> None:
        for image in self.get('images', []):
            if image.get('title'):
                image['rawtitle'] = image['title']
            if image.get('alt'):
                image['rawalt'] = image['alt']

    def extract_original_messages(self) -> Sequence[str]:
        messages = []
        for image in self.get('images', []):
            if image.get('rawalt'):
                messages.append(image['rawalt'])
            if image.get('rawtitle'):
                messages.append(image['rawtitle'])

        return messages

    def apply_translated_message(
            self, original_message: str,
            translated_message: str) -> None:
        for image in self.get('images', []):
            if image.get('rawtitle') == original_message:
                image['title'] = translated_message

            if image.get('rawalt') == original_message:
                image['alt'] = translated_message


def html_visit_galleria(self: HTMLTranslator, node: galleria) -> None:
    self.body.append(
        "<div id='%s' class='%s' style='width: %s; height: %s;'>" % (
            node['options']['galleria'],
            node['class'] + ' align-%s sphinxgalleria-core' %
            node['options']['align'],
            node['options']['width'],
            node['options']['height'],
        )
    )

    if len(node['images']) > 0:
        self.body.append("<figure><div class='row'>")
        self.body.append("<img src='%s' title='%s' alt='%s'>" % (
            node['images'][0]['uri'],
            node['images'][0]['title'],
            node['images'][0]['alt']
        ))
        self.body.append('</div></figure>')

    for img in node['images']:
        img['uri'] = relative_uri(
            self.builder.get_target_uri(self.builder.current_docname),
            img['uri']
        )
        img['thumb'] = relative_uri(
            self.builder.get_target_uri(self.builder.current_docname),
            img['thumb']
        )

    self.body.append(
        "</div><script type='module'>" +
        "import {SphinxGalleria} from './%s';\n" %
        relative_uri(
            self.builder.get_target_uri(self.builder.current_docname),
            '_static/sphinxgalleria/sphinxgalleria.mjs') +
        "new SphinxGalleria('%s', %s, %s).init();</script>" % (
            node['options']['galleria'],
            json.dumps(node['options']),
            json.dumps(node['images'])
        )
    )

    raise nodes.SkipNode


def latex_visit_galleria(self: LaTeXTranslator, node: galleria) -> None:
    for image in node['images']:
        self.body.append('[%s]' % image['alt'])
    raise nodes.SkipNode


def texinfo_visit_galleria(self: TexinfoTranslator, node: galleria) -> None:
    for image in node['images']:
        self.body.append('[%s]' % image['alt'])
    raise nodes.SkipNode


def text_visit_galleria(self: TextTranslator, node: galleria) -> None:
    for image in node['images']:
        self.body.append('[%s]' % image['alt'])
    raise nodes.SkipNode


def gemini_visit_galleria(self, node: galleria) -> None:
    for image in node['images']:
        self.body += '=> %s %s' % (image['uri'], image['alt'])
    raise nodes.SkipNode


def man_visit_galleria(self: ManualPageTranslator, node: galleria) -> None:
    if 'alt' in node.attributes:
        self.body.append('[%s]' % node['alt'])
    raise nodes.SkipNode


def align_choices(argument):
    return directives.choice(argument, ('left', 'right', 'center'))


class GalleriaDirective(Directive):

    has_content = False
    required_arguments = 1
    final_argument_whitespace = True

    option_spec = {
        'class': directives.class_option,
        'galleria': directives.unchanged,
        'alt': directives.unchanged,
        'title': directives.unchanged,
        'thumbsize': directives.unchanged,
        'timer': directives.nonnegative_int,
        'width': length_or_percentage_or_unitless,
        'height': length_or_percentage_or_unitless,
        'align': align_choices,
        'hide_title': directives.flag,
        'hide_alt': directives.flag,
        'no_transition': directives.flag,
    }

    def run(self):
        source = self.state_machine.document.settings._source
        env = self.state_machine.document.settings.env
        try:
            if source not in env.galleria_nodes:
                env.galleria_nodes[source] = {}

        except AttributeError:
            env.galleria_nodes = {}
            env.galleria_nodes[source] = {}

        galleria_name = self.options.get('galleria')
        galleria_name = galleria_name or str(uuid.uuid4()).replace('-', '')
        created = False

        if galleria_name in env.galleria_nodes[source]:
            node = env.galleria_nodes[source][galleria_name]

        else:
            node = galleria()
            node['class'] = 'galleria'
            node['options'] = {
                'galleria': 'galleria-' + galleria_name,
                'label_prev': _('Previous'),
                'label_next': _('Next'),
                'label_close': _('Close'),
                'label_thumbnail': _('Thumbnail, click to enlarge'),
            }
            node['images'] = []
            env.galleria_nodes[source][galleria_name] = node

            created = True

        if self.options.get('class'):
            node['class'] = ' '.join(self.options['class'])

        node['options']["width"] = self.options.get('width') or 'unset'
        node['options']["height"] = self.options.get('height') or 'unset'
        node['options']["align"] = self.options.get('align') or 'center'
        node['options']["no_transition"] = 'no_transition' in self.options

        node['options']["timer"] = self.options.get('timer')

        images_path = self.arguments
        for path in images_path:
            image = {}
            image["alt"] = self.options.get('alt')
            image["title"] = self.options.get('title')
            image["thumbsize"] = self.options.get('thumbsize') or '100x100'
            image["hide_alt"] = 'hide_alt' in self.options
            image["hide_title"] = 'hide_title' in self.options
            image['uri'] = path
            node['images'].append(image)

            image_node = nodes.image()
            image_node['alt'] = image['alt']
            image_node['uri'] = image['uri']
            image_node.parent = node
            node.children.append(image_node)

        if created:
            return [node]
        return []
