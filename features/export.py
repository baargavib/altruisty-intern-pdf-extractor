from fpdf import FPDF

def export_to_pdf(title, content, filename="output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=12)
    pdf.multi_cell(0, 10, txt=f"{title}\n\n{content}")
    pdf.output(filename)
    return filename
