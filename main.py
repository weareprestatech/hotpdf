# USAGE
from hotpdf import HotPdf

if __name__ == "__main__":
    hot_pdf = HotPdf()
    hot_pdf.load("tests/resources/PDF.pdf")
    occurences = hot_pdf.find_text("EXPERIENCE")
    for page_num, occurence in occurences.items():
        print(page_num, "::::", occurence)
        print()
