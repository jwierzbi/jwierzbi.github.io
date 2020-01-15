Title: Serving compressed files from Google Cloud Storage
Author: Jarosław Wierzbicki
Category: Web development
Date: 2020-01-14
Slug: serve-gzip-files-from-gcs
Lang: en
Tags: Google Cloud Storage, gzip, tips&tricks

Recently I’ve been looking into some ways to optimise the loading speed of a website that I’m working on. One of the possible improvements suggested by Chromium’s [Audit](https://developers.google.com/web/tools/lighthouse) tool was to [enable text  compression](https://web.dev/uses-text-compression). An obvious thing to do, one might say, but the question is not whether to do it at all but rather how to do it.

Let’s start from the beginning though. The idea is simple. Instead of serving plain text files like CSS and JavaScript to the browser, those files should be sent compressed so that the browser, upon receiving them, can decompress them to a plain text format. There is, of course, a CPU time cost to this approach but in most cases the savings from the data transfer outweigh it by a large margin.<sup>[1](#r1)</sup> This is particularly true for mobile devices where the bandwidth is often limited.

Many servers nowadays support compression (be that dynamic or static) and there are plenty of resources describing how to enable it but for some reason I couldn’t quickly find information on how exactly to do it for Google Cloud Storage.

<!-- PELICAN_END_SUMMARY -->

### Google Cloud Storage

[Google Cloud Storage](https://cloud.google.com/storage/) (GCS) by default serves files uncompressed. There is however an option to enable [gzip](https://en.wikipedia.org/wiki/Gzip) compression for selected files. There is a catch though. It’s only possible to use static compression which means that the files need to be uploaded already compressed to the storage. Some servers allow you to use dynamic compression which means that they will compress files on the fly when the files are requested by a client but unfortunately GCS, as I mentioned, doesn't do this.

So how to do it in GCS, you might ask. Turns out Google makes it extremely easy to compress files upon uploading using their [`gsutil`](https://cloud.google.com/storage/docs/gsutil) tool.

There are two ways to upload multiple files at a time to Google Cloud Storage using the `gsutil` command. The first is to use `rsync` and the other one is to use the `cp` sub-command.<sup>[2](#r2)</sup> Usually `rsync` is more convenient but in this case we need to use `cp` because the former doesn’t support compressing files during the upload (well that’s not exactly true, read further what the `-j` option does and why it's not applicable here).

Let's get to business. Using the `cp` sub-command is really easy, e.g.:

    :::bash
    $ gsutil -m cp -z css,js,map [LOCAL_DIR] gs://[BUCKET]/[REMOTE_DIR]

Let’s break it down:

<dl>
<dt><code>-m</code></dt>
<dd>This option tells the `cp` sub-command to run in parallel. While this is not really needed here, it can greatly shorten the upload time so it's a good idea to use it.</dd>

<dt><code>-z [ext,...]</code><dt>
<dd>Causes all files with given extensions to be compressed before the upload and keeps them like that afterwards (this is how it differs from the <code>-j</code> option which only compresses files for the duration of the upload process and decompresses them at the destination).<br>
Beyond compressing of the files, the command will also apply the required attributes to the stored files needed to properly serve them compressed.<sup><a href="#r3">3</a></sup><br>
In our example, all CSS, JS and MAP files will be stored compressed (using gzip).</dd>

<dt><code>LOCAL_DIR</code></dt>
<dd>The directory path to the files we want to upload to Google Cloud Storage.<dd>

<dt><code>BUCKET</code></dt>
<dd>Name of the Google Cloud Storage bucket.<dd>

<dt><code>REMOTE_DIR</code></dt>
<dd>Remote directory in the bucket that the files will be copied to.<dd>
</dl>

If you have public access configured to your bucket, you can test if the files are served compressed by opening a link to one of them in your browser (if not, then you'll need to find a way to do it in your particular case by yourself):

    :::text
    https://storage.googleapis.com/[BUCKET_NAME]/[FILE_PATH]

and checking (for example, by using the web browser's development tools) if the response contains `content-encoding: gzip` and `content-type: text/css` (for CSS) headers, e.g.:

![GCS Response Header with GZIP]({attach}images/gcs_gzip_resp.png)

If it does, then all is working as intended and we're home. That’s it, so simple, isn’t it?

### Conclusion

Gzip compression of static files can significantly speed up loading of your website especially if it’s a fairly complex one with a lot of CSS and JS files. Luckily, if you’re using Google Cloud Storage, there’s really very little work needed to make it happen. Adding only one option to the 'gsutil' command can make your website load noticeably faster. There’s really no argument not do it. ;)

### Further Reading

<a name="r1">[1]</a> [Can gzip Compression Really Improve Web Performance?](https://royal.pingdom.com/can-gzip-compression-really-improve-web-performance/)<br>
<a name="r2">[2]</a> [Transcoding of gzip-compressed files](https://cloud.google.com/storage/docs/transcoding)<br>
<a name="r3">[3]</a> [gsutil cp command documentation](https://cloud.google.com/storage/docs/gsutil/commands/cp)