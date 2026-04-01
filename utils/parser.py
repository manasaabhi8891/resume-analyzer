import PyPDF2

def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    return text