==================================================
Serving compressed files from Google Cloud Storage
==================================================

:author: Jarosław Wierzbicki
:category: Web development
:date: 2020-01-14
:slug: serve-gzip-files-from-gcs
:lang: en
:tags: Google Cloud Storage, gzip, tips&tricks

Recently I’ve been looking into some ways to optimise the loading speed
of a website that I’m working on. One of the possible improvements suggested
by Chromium’s `Audit <https://developers.google.com/web/tools/lighthouse>`_ tool
was to `enable text  compression <https://web.dev/uses-text-compression>`_.
An obvious thing to do, one might say, but the question is not whether to do it
at all but rather how to do it.

Let’s start from the beginning though. The idea is simple. Instead of serving
plain text files like CSS and JavaScript to the browser, those files should be
sent compressed so that the browser, upon receiving them, can decompress them
to a plain text format. There is, of course, a CPU time cost to this approach
but in most cases the savings from the data transfer outweigh it by a large
margin [#]_. This is particularly true for mobile devices where the bandwidth
is often limited.

Many servers nowadays support compression (be that dynamic or static) and there
are plenty of resources describing how to enable it but for some reason I
couldn’t quickly find information on how exactly to do it for Google Cloud
Storage.

.. PELICAN_END_SUMMARY

Google Cloud Storage
====================

`Google Cloud Storage <https://cloud.google.com/storage/>`_ (GCS) by default
serves files uncompressed. There is however an option to enable
`gzip <https://en.wikipedia.org/wiki/Gzip>`_ compression for selected files.
There is a catch though. It’s only possible to use static compression which
means that the files need to be uploaded already compressed to the storage.
Some servers allow you to use dynamic compression which means that they will
compress files on the fly when the files are requested by a client but
unfortunately GCS, as I mentioned, doesn't do this.

So how to do it in GCS, you might ask. Turns out Google makes it extremely easy
to compress files upon uploading using their
`:gsutil <https://cloud.google.com/storage/docs/gsutil>`_ tool.

There are two ways to upload multiple files at a time to Google Cloud Storage
using the :code:`gsutil` command. The first is to use :code:`rsync` and the
other one is to use the :code:`cp` sub-command [#]_. Usually :code:`rsync`
is more convenient but in this case we need to use `cp` because the former
doesn’t support compressing files during the upload (well that’s not exactly
true, read further what the :code:`-j` option does and why it's not applicable
here).

Let's get to business. Using the :code:`cp` sub-command is really easy, e.g.:

.. code-block:: bash

    $ gsutil -m cp -z css,js,map [LOCAL_DIR] gs://[BUCKET]/[REMOTE_DIR]

Let’s break it down:

:code:`-m`
    This option tells the :code:`cp` sub-command to run in parallel. While this
    is not really needed here, it can greatly shorten the upload time so it's
    a good idea to use it.
:code:`-z [ext,...]`
    Causes all files with given extensions to be compressed before the upload
    and keeps them like that afterwards (this is how it differs from
    the :code:`-j` option which only compresses files for the duration
    of the upload process and decompresses them at the destination).

    Beyond compressing of the files, the command will also apply the required
    attributes to the stored files needed to properly serve them compressed
    [#]_. In our example, all CSS, JS and MAP files will be stored compressed
    (using gzip).
:code:`LOCAL_DIR`
    The directory path to the files we want to upload to Google Cloud Storage.
:code:`BUCKET`
    Name of the Google Cloud Storage bucket.
:code:`REMOTE_DIR`
    Remote directory in the bucket that the files will be copied to.

If you have public access configured to your bucket, you can test if the files
are served compressed by opening a link to one of them in your browser (if not,
then you'll need to find a way to do it in your particular case by yourself):

.. code-block:: text

    https://storage.googleapis.com/[BUCKET_NAME]/[FILE_PATH]

and checking (for example, by using the web browser's development tools) if the
response contains :code:`content-encoding: gzip` and
:code:`content-type: text/css` (for CSS) headers, e.g.:

.. image:: {attach}images/gcs_gzip_resp.png
   :alt: GCS response headers.

If it does, then all is working as intended and we're home. That’s it,
so simple, isn’t it?

Conclusion
==========

Gzip compression of static files can significantly speed up loading of your
website especially if it’s a fairly complex one with a lot of CSS and JS files.
Luckily, if you’re using Google Cloud Storage, there’s really very little work
needed to make it happen. Adding only one option to the :code:`gsutil` command
can make your website load noticeably faster. There’s really no argument not do
it. |winking-face|

.. |winking-face| unicode:: 0x1F609

Further Reading
===============

.. [#] `Can gzip Compression Really Improve Web Performance? <https://royal.pingdom.com/can-gzip-compression-really-improve-web-performance/>`_
.. [#] `Transcoding of gzip-compressed files <https://cloud.google.com/storage/docs/transcoding>`_
.. [#] `gsutil cp command documentation <https://cloud.google.com/storage/docs/gsutil/commands/cp>`_
