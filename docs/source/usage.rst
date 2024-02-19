=========
Usage
=========

HotPdf Class
------------------------------------------

.. autoclass:: hotpdf.HotPdf

.. autofunction:: hotpdf.HotPdf.__init__

The HotPdf class is the wrapper around your PDF that allows for searching text and extracting text on your PDFs.

.. code-block:: python

   from hotpdf import HotPdf
   pdf_file_path = "path to your pdf file"

   # Load directly from Path
   hotpdf_document = HotPdf(pdf_file_path)

   # Load from file stream
   with open(pdf_file_path, "rb") as f:
      hotpdf_document_2 = HotPdf(f)

Alternatively you can defer loading, and use the `.load()` function instead. The outcome is the same, internally the constructor for `HotPdf` calls the `.load()` function

.. code-block:: python

   from hotpdf import HotPdf
   pdf_file_path = "path to your pdf file"

   # path
   hotpdf_document = HotPdf()
   hotpdf_document = hotpdf_document.load(pdf_file_path)

   # file stream
   hotpdf_document_2 = HotPdf()
   with open(pdf_file_path, "rb") as f:
      hotpdf_document_2 = hotpdf_document_2.load(f)


.. autofunction:: hotpdf.HotPdf.load

Sometimes pdfminer.six will not replace (cid:x) values with their corresponding Unicode values.
In that case, send the charset Encoder.

.. code-block:: python

   from hotpdf.encodings.encodings import EncodingType
   hotpdf_cid_removal_object = HotPdf(f, cid_overwrite_charset=EncodingType.LATIN)


File Operations
------------------------------------------

Length
~~~~~~~~~~~~~~~~~~~

The number of pages in the PDF file can be determined by checking the `len` of `pages` property of the hotpdf object.

.. code-block:: python

   num_pages = len(hotpdf_document.pages)

Search
------------------------------------------

find_text
~~~~~~~~~~~~~~~~~~~

To look for a string in the entire PDF File, you can use the `find_text` function.
You can also specify what pages you want to search in. By default it will look through the whole PDF.
To get the whole span where the string lies in, you can set `take_span` to True.

.. code-block:: python

   text_occurences = hotpdf_document.find_text("foo")
   text_occurences_with_span = hotpdf_document.find_text(
      "foo",
      take_span=True,
   )


.. autofunction:: hotpdf.HotPdf.find_text

Extraction
------------------------------------------

extract_text
~~~~~~~~~~~~~~~~~~~

To extract string from specific positions in the PDF, you can use the `extract_text` function.
This will extract the string that lies within the positions that have been specified on the page that it's specified (default is Page 0).

.. code-block:: python

    text_in_bbox = hotpdf_document.extract_text(
       x0=0,
       y0=0,
       x1=100,
       y1=10,
       page=0,
    )

.. autofunction:: hotpdf.HotPdf.extract_text

extract_spans
~~~~~~~~~~~~~~~~~~~

Instead of just the individual characters that lay within the bounds that you specify, if you want full words, or the complete spans that intersect within the specified bounds - you can use the `extract_spans` functions instead.
This will extract all the spans that intersect with the positions that have been specified on the page that it's specified (default is Page 0).


.. code-block:: python

    spans_in_bbox = hotpdf_document.extract_spans(
       x0=0,
       y0=0,
       x1=100,
       y1=10,
       page=0,
    )

.. autofunction:: hotpdf.HotPdf.extract_spans

extract_spans_text
~~~~~~~~~~~~~~~~~~~

Instead of handling the spans structures yourself, if you are only interested in the text of the spans, you can use the `extract_spans_text` function instead.

The function is the same as `extract_spans`_ except it returns you a `list` of `str`.

.. code-block:: python

    spans_text_in_bbox = hotpdf_document.extract_spans_text(
       x0=0,
       y0=0,
       x1=100,
       y1=10,
       page=0,
    )

.. autofunction:: hotpdf.HotPdf.extract_spans_text

extract_page_text
~~~~~~~~~~~~~~~~~~~

If you want to view the text of an entire page in plaintext `str` format, you can use the `extract_page_text` function.

The function accepts `page` as a parameter.

.. code-block:: python

    page_text = hotpdf_document.extract_page_text(page=0,)

.. autofunction:: hotpdf.HotPdf.extract_page_text
