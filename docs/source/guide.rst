==================
User Guide
==================

This guide contains a couple of common use cases that your application might have. Since HotPdf returns data in its own structure, its readability may not be optimal.

To mitigate this issue, we are writing this guide to help you get started with using HotPdf.

Text Operations
------------------------------------------

Start by loading the file.

You can load a PDF either by giving the path to the file, or you can also send the opened PDF file as bytes.

.. code-block:: python

    from hotpdf import HotPdf
    pdf_file_path = "path to your pdf file"

    # Loading from path
    hotpdf_document = HotPdf()
    hotpdf_document = hotpdf_document.load(pdf_file_path)

    # Loading opened file
    hotpdf_document_2 = HotPdf()
    with open(pdf_file_path, "rb") as f:
        hotpdf_document_2 = hotpdf_document_2.load(f.read())

The `HotPdf` object has many attributes that you can use to solve your problems. One of them is `pages`, representing each page of the PDF stored in data structures (trie & sparse matrix) to help with text operations.
Locked PDFs can be loaded passing the password as the password argument:

.. code-block:: python

    hotpdf_document = HotPdf()
    hotpdf_document = hotpdf_document.load(locked_pdf_file_path, password="your_password")

Number of Pages
~~~~~~~~~~~~~~~~~~

Begin by getting the number of loaded pages or the total pages in the PDF.

.. code-block:: python

    len_pages: int = len(hotpdf_document.pages)

Each `page` in the `pages` list is an in-memory representation of a page of the loaded PDF. All operations are performed on a page.

Looking up Text
~~~~~~~~~~~~~~~~~~

To look up text, use the `find_text` function.

You can attempt to find the full span the text lies in by setting `take_span` to `True`.

.. code-block:: python

    text_occurrences = hotpdf_document.find_text("foo")

This will return a `dict` of `list` of `list` of `HotCharacter`:

- The `dict` keys are the page numbers.
- The outer `list` is all the occurrences found on the page.
- The inner `list` contains character-wise all the words that were found.
  The `HotCharacter` object contains the value and the coordinates of the character on the PDF.

To get the entire span of the found occurrence, you could reuse the implementation of `get_element_dimension` that is found under `hotpdf.utils`.

.. code-block:: python

    from hotpdf.utils import get_element_dimension

    # Getting the dimension of the first element that was found on page 0.
    element_dimension = get_element_dimension(text_occurrences[0][0])

`element_dimension` will return an `ElementDimension` data object which has the `x0`, `y0`, `x1`, `y1` values. These coordinates represent the position the text was found in.

You can set `take_span` to `True` to find the whole span that it lies in. Usage remains the same.

.. code-block:: python

    text_occurrences = hotpdf_document.find_text("foo", take_span=True)

    # Getting the dimension of the first element that was found on page 0.
    element_dimension = get_element_dimension(text_occurrences[0][0])

For example, if you are looking for a text like "hotpdf v23" but you know that the part "v23" is variable, you can simply search for "hotpdf v" or just "hotpdf".
This will return the spans of the text as well, so you could also find "hotpdf v24" just by searching for "hotpdf v" or "hotpdf".

**Please note:** The text children of a `Span` depend on the PDF producing software, so it could be unpredictable. Either way, if it works for you, then it works. Please test it!

Extracting Text
~~~~~~~~~~~~~~~~~~

If you know the coordinates of the text that you are going to extract, you can use the `extract_text` function.

This will extract the text that lay in the specified coordinates (`x0`, `y0`, `x1`, `y1`) of the specified `page`.
If you don't specify a `page` it will default to 0 (i.e., the first page).

.. code-block:: python

    text = pdf.extract_text(x0=0, y0=0, x1=600, y1=500, page=0)

This will return a `str` in plain text format. Characters, if they are on different lines, will be separated by `\n`.

Extracting Spans Text
~~~~~~~~~~~~~~~~~~~~~~

If you want to extract text of all spans that lay or intersect the coordinates (`x0`, `y0`, `x1`, `y1`) that you specify on the `page` that you specify, you need to use the `extract_spans_text` function.

In case you want more granular view of the spans, use `extract_spans` instead.

.. code-block:: python

    text_spans = pdf.extract_spans_text(x0=0, y0=0, x1=600, y1=500, page=0)

This will return a `list` of `str`.

The `list` contains text of spans that lay within the given coordinates.

Extracting Spans
~~~~~~~~~~~~~~~~~~

If you want to extract all spans that lay or intersect the coordinates (`x0`, `y0`, `x1`, `y1`) that you specify on the `page` that you specify, you need to use the `extract_spans` function.

.. code-block:: python

    text_spans = pdf.extract_spans(x0=0, y0=0, x1=600, y1=500, page=0)

This will return a `list` of `Span`.

The `list` contains the spans that lay within the given coordinates. A `Span` is a collection of `HotCharacter`

To access a span, you can access it by index. For example, if you want to get the dimensions of the first span that was returned, you can do this:

.. code-block:: python

    from hotpdf.utils import get_element_dimension

    # Get the dimensions of the first span
    first_span_dimensions = spans[0].get_element_dimension()

    # Get the text of the first span
    span_text = spans[0].to_text()

This will give you the dimension of the span.

If you want to extract the text, you can iterate over a span and get the `value` attribute of the `HotCharacter`.

.. code-block:: python

    extracted_span = "".join([hc.value for hc in text_spans[0]])

Extracting Text of Page
~~~~~~~~~~~~~~~~~~~~~~~~~

In case you want to view the text of a specified page, you can use the `extract_page_text` function.

This will return you an `str` of the whole page of the PDF.

.. code-block:: python

    page_text = pdf.extract_page_text(page=0)

---

We will keep adding more functions to help with various operations. In any case please feel free to open an issue on our github.
