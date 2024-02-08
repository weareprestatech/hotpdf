from hotpdf import HotPdf
from hotpdf.utils import to_text

pdf = HotPdf("/Users/smartlandindteammachine/Downloads/6663e89b-c10d-4537-9b66-fabead71e959.pdf")
print(pdf.extract_page_text(0))

pdf = HotPdf("/Users/smartlandindteammachine/Downloads/0168 UNICREDIT TRIMESTRALE 01.2019 - 03.2019 (1).pdf")
print(to_text(pdf.find_text("Saldo", take_span=True)[0][0]))
