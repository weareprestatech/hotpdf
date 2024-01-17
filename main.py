from hotpdf import HotPdf

pdf = HotPdf()
pdf.load("tests/resources/PDF.pdf")
test = pdf.find_text("Hello World")
print(test)
