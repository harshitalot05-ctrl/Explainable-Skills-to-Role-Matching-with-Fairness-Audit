from pypdf import PdfReader
from docx import Document


def extract_text_from_file(uploaded_file):

    file_name = uploaded_file.name.lower()

    # TXT file
    if file_name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    # PDF file
    elif file_name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    # DOCX file
    elif file_name.endswith(".docx"):
        document = Document(uploaded_file)
        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    else:
        return ""