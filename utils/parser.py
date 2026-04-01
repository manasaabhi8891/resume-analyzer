import PyPDF2

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        return text

    except Exception as e:
        return f"PDF Error: {str(e)}"