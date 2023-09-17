# USAGE
from hotpdf import HotPdf
if __name__ == "__main__":
    hot_pdf = HotPdf(width=827, height=1170, precision=0.5)
    hot_pdf.load("test.pdf")
    occurences = hot_pdf.find_text("Balance")
    for page_num, occurence in occurences.items():
        print(page_num, "::::", occurence)
        print()