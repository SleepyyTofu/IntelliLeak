import PyPDF2
from docx import Document


# TXT Extraction
def extract_txt(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    return text


# PDF Extraction
def extract_pdf(file_path):

    text = ""
    metadata = {}

    with open(file_path, 'rb') as file:

        reader = PyPDF2.PdfReader(file)

        # Extract text
        for page in reader.pages:
            text += page.extract_text() + "\n"

        # Extract metadata
        if reader.metadata:
            metadata = {
                "Author": reader.metadata.author,
                "Title": reader.metadata.title,
                "Creator": reader.metadata.creator,
                "Producer": reader.metadata.producer
            }

    return text, metadata


# DOCX Extraction
def extract_docx(file_path):

    doc = Document(file_path)

    text = ""

    # ==========================
    # Extract paragraphs
    # ==========================
    for para in doc.paragraphs:
        if para.text.strip():
            text += para.text + "\n"

    # ==========================
    # Extract tables
    # ==========================
    for table in doc.tables:
        for row in table.rows:

            row_data = []

            for cell in row.cells:
                row_data.append(cell.text.strip())

            text += " | ".join(row_data) + "\n"

    # ==========================
    # Metadata
    # ==========================
    core_props = doc.core_properties

    metadata = {
        "Author": core_props.author,
        "Title": core_props.title,
        "Last Modified By": core_props.last_modified_by
    }

    return text, metadata