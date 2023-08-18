sphinx_galleria
###############

Create image galleries with Sphinx. No external JS
dependency.

Install
~~~~~~~

If you're using a virtualenv, just:

.. code:: bash

   pip install sphinx-galleria

.. important::

   Your webserver must deliver .mjs file with correct
   content type (`application/javascript`).

Using
~~~~~

Add `'sphinx_galleria'` in the list of extensions in
your `source.conf` file.

Just use the galleria directive like this:

.. code:: rst

   .. galleria:: imagefile1 imagefile2  images*.jpg
      :galleria: (optional) Name of gallery - node level
      :alt: (optional) A long description - image level
      :title: (optional) Title of image - image level
      :thumbsize: (optional) Image size (defaults to "100x100") - image level
      :width: Width of image (in pixel or percentage or with unit, default auto) - node level
      :height: (optional) Height of image (in pixel or with unit) - node level
      :align: Align to 'right', 'left' or 'center' (default to center) - node level
      :hide_title: Flag - hide title under image (not in dialog) - image level
      :hide_alt: Flag - hide alternative text under image - image level
      :no_transition: Flag - avoid transition effect - node level
      :timer: (optional) Go to next image each timer seconds
      :class: (optional) HTML class for gallery - node level

Image level options are same for all images defined by
the directive. If you need separated descriptions and
titles, just use the directive several times with the
same galleria name. In this case, node level options
must be defined only once.

Thumbnail size is in "WIDTHxHEIGHT" format, resulting
image keeps ratio. Be careful with tumbnail size, the
browser loads all thumbnails of a gallery when loading
the page. It can take some time with really big galleries.

The first image of a gallery is displayed if javascript
is not available on the browser.

Licensing
~~~~~~~~~

sphinx-galleria is under EUPL-1.2.
