import fitz  # PyMuPDF

def extract_pdf_text(file_bytes: bytes, max_pages: int = 30) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")

    out = []
    n = min(doc.page_count, max_pages)
    for i in range(n):
        t = (doc.load_page(i).get_text("text") or "").strip()
        if t:
            out.append(t)

    doc.close()
    return "\n\n".join(out).strip()
