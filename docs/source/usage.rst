Usage
=====

HotPdf Class
------------------------------------------

.. autoclass:: hotpdf.HotPdf

The HotPdf class is the wrapper around your PDF that allows for searching text and extracting text on your PDFs.

Loading a file
------------------------------------------

Before you can perform operations on your PDFs, you will need to load it first.

.. code-block:: python

   from hotpdf import HotPdf
   pdf_file_path = "path to your pdf file"
   hotpdf_document = HotPdf()
   hotpdf_document = hotpdf_document.load(pdf_file_path)

.. autofunction:: hotpdf.HotPdf.load

File Operations
------------------------------------------

Length
^^^^^^^

The number of pages in the PDF file can be determined by checking the `len` of `pages` property of the hotpdf object.

.. code-block:: python

   num_pages = len(hotpdf_document.pages)

Search
------------------------------------------

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

To extract string from specific positions in the PDF, you can use the `extract_text` function.
This will extract the string that lies within the positions that have been specified on the page that it's specified (default is Page 0).

Extraction
------------------------------------------

.. code-block:: python

    text_in_bbox = hotpdf_document.extract_text(
       x0=0,
       y0=0,
       x1=100,
       y1=10,
       page=0,
    )

.. autofunction:: hotpdf.HotPdf.extract_text

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
