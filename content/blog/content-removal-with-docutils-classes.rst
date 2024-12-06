==================================================
Conditional content removal using Docutils classes
==================================================

:author: Jarosław Wierzbicki
:category: Documentation
:date: 2021-06-07
:modified: 2024-12-06
:slug: content-removal-with-docutils-classes
:lang: en
:tags: Docutils, documentation, reStructuredText, reST
:description: Are you writing reStructuredText (reST) documents and don't know \
              how to conditionally exclude content? Look at this description \
              of the Docutils class directive.

Some time ago I had a problem where I had to exclude parts of one of my
documents based on a build-time condition. I wanted to maintain one document but
produce two versions: one that contained internal details of a product and one
that didn't.

Nowadays I use reStructuredText_ (reST) and Docutils_ for writing my documents
so naturally, I started Googling how to do it with the help of those tools.
After some research, I found an out-of-the-box solution (unsurprisingly because
we all have similar problems |winking-face|). It may surprise you if you haven't
looked into this problem before.

.. |winking-face| unicode:: 0x1F609
.. _Docutils: https://docutils.sourceforge.io
.. _reStructuredText: https://docutils.sourceforge.io/rst.html

.. PELICAN_END_SUMMARY

The *class* directive
=====================

As the title reveals, the solution is the Docutils' *class* directive. But
before we get to the main point let us explore what it can do and how it works
first. This will make the next (main) step more clear.

The class directive allows adding a class attribute to document nodes. For
example, this can be useful for applying styles when generating HTML output.

The class attribute can be applied in 2 ways:

* to a `structural element`_, e.g. a section
* to a `body element`_ (simple or compound), e.g. a paragraph

.. _`structural element`: https://docutils.sourceforge.io/docs/ref/doctree.html#id205
.. _`body element`: https://docutils.sourceforge.io/docs/ref/doctree.html#id209

.. _listing-01:

For example, we might want to add a :code:`subsection` class to a subsection
of a document, :code:`paragraph` and :code:`emphasised` classes to a paragraph
(we can apply more than one) and a :code:`compound-body` to a list.

.. code-block:: rst
   :hl_lines: 7 12 16

    Title
    =====

    Subtitle
    --------

    .. class:: subsection

    Section is a structural element
    """""""""""""""""""""""""""""""

    .. class:: paragraph emphasised

    A paragraph is a simple body element.

    .. class:: list

    - Bullet list,
    - is a compound body element.

The above document will be converted to a document tree that will look something
like the below:

.. code-block:: xml
   :hl_lines: 6 9 11

    <document>
        <title>
            Title
        <subtitle>
            Subtitle
        <section classes="subsection">
            <title>
                Section is a structural element
            <paragraph classes="paragraph emphasised">
                A paragraph is a simple body element.
            <bullet_list classes="list">
                <list_item>
                    <paragraph>
                        Bullet list,
                <list_item>
                    <paragraph>
                        is a compound body element.

.. class:: message

    .. class:: message-body

        The above output is a so-called `pseudo-XML`_. It’s a format used
        in Docutils for presenting a document tree in a easy-to-understand
        way. Note that for simplicity some of the node attributes were
        removed.

.. _`pseudo-XML`: https://docutils.sourceforge.io/docs/ref/doctree.html#pseudo-xml

As you can see some elements in the tree were assigned a :code:`classes`
attribute. Those are the same elements that we preceded with the class
directives. The general rule is that the directive is applied to a whole node
following the directive, so:

* Class applied to a structural node applies to the whole node, e.g. to the
  whole section.
* Class applied to a simple body element applies only to that element, e.g.
  to a paragraph.
* Class applied to a compound body element applies to the whole element but not
  to its children, e.g. to the top element of a list but not the list elements.

You might wonder what's going to happen when we apply a class to more than one
body element? Do we have to prepend every element with a class directive? If we
follow the previous example then yes but there's a better way:

.. code-block:: rst
   :hl_lines: 10

    Title
    =====

    Subtitle
    --------

    Section is a structural element
    """""""""""""""""""""""""""""""

    .. class:: a-block

        A paragraph is a simple body element.

        - Bullet list
        - is a compound body element.

The above example will give a document tree with the below structure:

.. code-block:: xml
   :hl_lines: 9 11

    <document>
        <title>
            Title
        <subtitle>
            Subtitle
        <section>
            <title>
                Section is a structural element
            <paragraph classes="a-block">
                A paragraph is a simple body element.
            <bullet_list classes="a-block">
                <list_item>
                    <paragraph>
                        Bullet list
                <list_item>
                    <paragraph>
                        is a compound body element.

Notice how the indented block was placed directly in the subsection and the
class :code:`a-block` was applied to each of the indented elements. This works
with the body elements only. If we try to do it for any of the structural
elements it won't work, i.e. sections can't be in the class' indented block.

Class directives can also be nested:

.. code-block:: rst
   :hl_lines: 10 14 18 22

    Title
    =====

    Subtitle
    --------

    Section is a structural element
    """""""""""""""""""""""""""""""

    .. class:: level-0

        Paragraph at level 0.

        .. class:: level-1

            Paragraph at level 1.

            .. class:: level-2

                Paragraphs at level 2.

                .. class:: level-3

                    Paragraph at level 3.

Which would results in:

.. code-block:: xml
   :hl_lines: 9 11 13 15

    <document>
        <title>
            Title
        <subtitle>
            Subtitle
        <section>
            <title>
                Section is a structural element
            <paragraph classes="level-0">
                Paragraph at level 0.
            <paragraph classes="level-1 level-0">
                Paragraph at level 1.
            <paragraph classes="level-2 level-1 level-0">
                Paragraphs at level 2.
            <paragraph classes="level-3 level-2 level-1 level-0">
                Paragraph at level 3.

That's pretty cool, right? |smiling-face|

.. |smiling-face| unicode:: 0x1F601

In all the above examples, we applied the class directive to the whole compound
body elements but it's also possible to do it to individual items, e.g. in
the case of a list:

.. code-block:: rst
   :hl_lines: 5

    .. class:: list

    - Bullet list,

        .. class:: list-item

    - is a compound
    - body element

The class in such case is applied to the second item only:

.. code-block:: xml
   :hl_lines: 5

    <bullet_list classes="list">
        <list_item>
            <paragraph>
                Bullet list,
        <list_item classes="list-item">
            <paragraph>
                is a compound
        <list_item>
            <paragraph>
                body element

Just remember that the class directive, in this case, must be properly aligned
with the preceding list item, otherwise it won't work as expected.

Now that we know everything (or at least enough |winking-face|) about the class
directive let's move to the main point.

Excluding nodes of a specific class
===================================

The lengthy explanation above led us to this point where we can now comfortably
try and tackle the main problem. This part will be much shorter.

In Docutils classes can be used for one more thing besides what classes are
usually used for: they allow to exclude nodes from the document. This can be
done by passing a class name to the :code:`--strip-elements-with-class` option
of the :code:`rst2xxx.py` family of commands, e.g.:

.. code-block:: console

    $ rst2html5.py --strip-elements-with-class=internal doc.rst

The above command will generate an HTML document with all of the nodes with
an :code:`internal` class removed. That's right, it's that easy |winking-face|.

So if the *doc.rst* looks like below:

.. code-block:: rst

    Title
    =====

    .. class:: internal

    Internal section
    ----------------

    Internal content.

    .. class:: external

    External section
    ----------------

    External content.

Then the HTML output will look something like:

.. code-block:: html

    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
    <!-- ... -->
    </head>
    <body>
        <div class="document" id="title">
        <h1 class="title">Title</h1>

        <div class="external section" id="external-section">
            <h1>External section</h1>
            <p>External content.</p>
        </div>
        </div>
    </body>
    </html>

Further, we'll explore how the class directive is implemented. Feel free to skip
that part if you're not interested.

How does it work?
=================

Docutils has two concepts that are involved in processing classes. There is
a *directive* and there is a *transform*.

Directive
---------

Directives [#]_ [#]_ are an extension mechanism for the reStructuredText markup
language. Each directive starts with a double full stop and whitespace and
ends with a double colon and whitespace with the directive type in between
e.g. :code:`.. class:: class-name`.

Directives are a very flexible way of extending Docutils [#]_ so let's take
a look at the code of the class directive [#]_.

Each directive extends the :code:`docutils.parsers.rst.Directive` [#]_ base
class and implements :code:`run` method:

.. code-block:: python3

    from docutils.parsers.rst import Directive

    class Class(Directive):
        required_arguments = 1
        optional_arguments = 0
        final_argument_whitespace = True
        has_content = True

        def run(self):
            # ...

We can pass some configuration parameters as class variables like the above
:code:`required_arguments = 1` which tells the parser to look for at least one
parameter for the directive, which in this case are the names of classes or
:code:`has_content = True` which indicates to the parser that the class
directive accepts indented blocks as it's content.

Further, let's look at what is inside the :code:`run` method:

.. code-block:: python3

    def run(self):
        class_value = directives.class_option(self.arguments[0])

        node_list = []
        if self.content:
            # ...
        else:
            # ...
        return node_list

The :code:`run` method deals with two cases:

* If the :code:`self.content` variable is not empty it means that there was
  a block (indented) passed to the directive.
* If the :code:`self.content` is empty the directive will affect the next node
  in the content tree (a next sibling).

The first case where an indented block was passed to the directive is handled
like below:

.. code-block:: python3

    container = nodes.Element()
    self.state.nested_parse(self.content, self.content_offset, container)
    for node in container:
        node['classes'].extend(class_value)
    node_list.extend(container.children)

First, we create an empty element that will serve as a container for the content
included in the nested block: :code:`container = nodes.Element()`.

Next, we parse the directive's content with the call to :code:`nested_parse()`
[#]_. This will add children elements created from :code:`self.content` and put
them into the :code:`container`.

We then iterate over all of the created children in the container and add the
class name to the node's :code:`classes` attribute.

As the last step, we add all of the :code:`container`'s children to the
:code:`node_list` which is going to be returned from the :code:`run` method.

In the second case:

.. code-block:: python3

    pending = nodes.pending(
        misc.ClassAttribute,
        {'class': class_value, 'directive': self.name},
        self.block_text)
    self.state_machine.document.note_pending(pending)
    node_list.append(pending)

Since there is no content directly associated with the class directive we will
apply the class to the next element in the element tree (in other words to a
sibling). To do that we need to defer this operation until the whole document
is parsed (since we don't know our sibling yet).

To postpone applying our class to the sibling we create and insert a *pending*
node. This node will then be processed by a Transform_.

To create the pending node we use the :code:`nodes.pending` method and pass
3 arguments to it: the :code:`misc.ClassAttribute` transform class (this is
the operation that will be executed on the pending node later), an options
dictionary and a :code:`self.block_text` (which is a string containing the
whole directive).

We then add this node to the :code:`node_list` which will be returned from
the :code:`run()` method.

That's pretty much everything that the class directive implementation is doing.
Next (Transform_) we'll see what happens with the pending node that we created.

Transform
---------

Transforms [#]_ are run after the whole document has been parsed and their
purpose is to change the document tree in place. They can perform different
operations like resolving references or removing elements based on a
certain condition.

We'll take a look at the :code:`ClassAttribute` [#]_ transform that is used by the
:code:`Class` directive class.

Each transform object derives from the :code:`docutils.tranforms.Transform` [#]_
class and implements the :code:`apply` method.

.. code-block:: python3

    class ClassAttribute(Transform):
        default_priority = 210

        def apply(self):
            # ...

That's pretty straightforward. One thing that is worth mentioning is that the
transforms are run in order according to their priorities hence the class
attribute :code:`default_priority` above.

Next, let's take a look at the :code:`apply` method implementation:

.. code-block:: python3

    def apply(self):
        pending = self.startnode
        parent = pending.parent
        child = pending
        while parent:
            for index in range(parent.index(child) + 1, len(parent)):
                # ...
                return
            else:
                child = parent
                parent = parent.parent
        error = self.document.reporter.error(...)
        pending.replace_self(error)

Let's look at how the :code:`for` loop works first and then we'll check what's
happening inside of it.

First, we get a reference to the pending node that was added in the :code:`Class`
class and to its parent. Then we go into a :code:`while` loop that will
loop as long as the :code:`parent` node exists.

In the :code:`while` loop there is :code:`for ... else` construct which in short
loops over indices in a range. If there are no indices to loop over (no elements
at all) or no :code:`break` is executed inside the loop, it will jump to the
:code:`else` block.

So in the above case, we generate a range of indices of children that are
"behind" the pending node (i.e. siblings of the pending node that are following
the node in the tree). If there are siblings like that we execute whatever is
inside the :code:`for` loop and return (well that depends on what's in the loop
of course). If there are no siblings following the pending node (which can
happen if we put :code:`.. class::` before for `example <listing-01_>`_ a
section) we go level up in the node tree (the :code:`else` clause) and repeat
the operation until we find a node that we're looking for.

Finally, if we don't find any nodes that we can apply our operations to, we
replace the pending node with an error node.

The operations we apply to the nodes once we find them are pretty
straightforward:

.. code-block:: python3

    for index in range(parent.index(child) + 1, len(parent)):
        element = parent[index]
        if (isinstance(element, nodes.Invisible) or
            isinstance(element, nodes.system_message)):
            continue
        element['classes'] += pending.details['class']
        pending.parent.remove(pending)
        return

The whole idea here is to get the first eligible sibling that exists after the
pending node (or its parent, or its parent's parent, etc.) and add the
:code:`classes` attribute to it (same as we did in the :code:`Class`
implementation) and then if that happens, remove the pending node and return.

There are some exceptions like the :code:`nodes.Invisible` and
:code:`nodes.system_message` nodes that are skipped over in the loop but that's
not important here. Let's just say that those node types don't qualify as
regular nodes so classes can't be applied to them.

Summary
=======

Classes are an excellent way of e.g. customising how a document looks without
writing any extensions to Docutils. They also allow control of what goes into
a document and what doesn't. Of course, there are certain limitations of this
mechanism but for a large number of the use cases, they should be a great, quick
and easy way to achieve the desired outcome when writing our documentation.

Further reading
===============

* `reStructuredText Markup Specification <https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html>`_
* `Docutils: Documentation Utilities <https://docutils.sourceforge.io/>`_
* `Docutils Hacker's Guide <https://docutils.sourceforge.io/docs/dev/hacking.html>`_
* `Docutils Configuration <https://docutils.sourceforge.io/docs/user/config.html>`_
* `The Docutils Document Tree <https://docutils.sourceforge.io/docs/ref/doctree.html>`_
* `Docutils repository <https://sourceforge.net/p/docutils/code/HEAD/tree/trunk/docutils/>`_

----

.. [#] `reStructuredText Markup Specification, Directives <https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#directives>`_
.. [#] `reStructuredText Directives <https://docutils.sourceforge.io/docs/ref/rst/directives.html>`_
.. [#] `Creating reStructuredText Directives <https://docutils.sourceforge.io/docs/howto/rst-directives.html>`_
.. [#] `https://github.com/docutils-mirror/docutils, docutils/parsers/rst/directives/misc.py:327 <https://github.com/docutils-mirror/docutils/blob/e88c5fb08d5cdfa8b4ac1020dd6f7177778d5990/docutils/parsers/rst/directives/misc.py#L327>`_
.. [#] `https://github.com/docutils-mirror/docutils, docutils/parsers/rst/__init__.py:194 <https://github.com/docutils-mirror/docutils/blob/e88c5fb08d5cdfa8b4ac1020dd6f7177778d5990/docutils/parsers/rst/__init__.py#L194>`_
.. [#] `https://github.com/docutils-mirror/docutils, docutils/parsers/rst/states.py:257 <https://github.com/docutils-mirror/docutils/blob/e88c5fb08d5cdfa8b4ac1020dd6f7177778d5990/docutils/parsers/rst/states.py#L257>`_
.. [#] `Docutils Transforms <https://docutils.sourceforge.io/docs/ref/transforms.html>`_
.. [#] `https://github.com/docutils-mirror/docutils, docutils/transforms/misc.py:35 <https://github.com/docutils-mirror/docutils/blob/e88c5fb08d5cdfa8b4ac1020dd6f7177778d5990/docutils/transforms/misc.py#L35>`_
.. [#] `https://github.com/docutils-mirror/docutils, docutils/transforms/__init__.py:33 <https://github.com/docutils-mirror/docutils/blob/e88c5fb08d5cdfa8b4ac1020dd6f7177778d5990/docutils/transforms/__init__.py#L33>`_
