import fitz
def compare_pdfs(pdf_path1, pdf_path2):
    pdf1 = fitz.open(pdf_path1)
    pdf2 = fitz.open(pdf_path2)

    if pdf1.page_count != pdf2.page_count:
        return False

    for page_num in range(pdf1.page_count):
        page1 = pdf1[page_num]
        page2 = pdf2[page_num]

        if page1.get_text() != page2.get_text():
            return False

    return True
