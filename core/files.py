"""
File text extraction — converts uploaded files to plain text for the LLM.

Supports: PDF, Excel (.xlsx/.xls), CSV, and any plain-text format.
All other file types are attempted as UTF-8 text with a fallback error message.
"""
import io


CODE_EXTENSIONS = {".py", ".js", ".ts", ".java", ".go", ".rs", ".cpp", ".c", ".sh", ".sql"}


def extract_text(filename: str, data: bytes) -> str:
    """Return the text content of an uploaded file."""
    ext = _ext(filename)

    if ext == ".pdf":
        return _from_pdf(data)
    if ext in (".xlsx", ".xls"):
        return _from_excel(data)
    if ext == ".csv":
        return data.decode("utf-8", errors="replace")

    # Everything else treated as plain text
    return data.decode("utf-8", errors="replace")


def file_type_label(filename: str) -> str:
    ext = _ext(filename)
    if ext in CODE_EXTENSIONS:
        return "code"
    return "doc"


def _ext(filename: str) -> str:
    from pathlib import Path
    return Path(filename).suffix.lower()


def _from_pdf(data: bytes) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        return "\n\n".join(pages).strip()
    except ImportError:
        return "[PDF extraction requires pdfplumber: pip install pdfplumber]"
    except Exception as e:
        return f"[Could not extract PDF: {e}]"


def _from_excel(data: bytes) -> str:
    try:
        import openpyxl
        wb = openpyxl.load_workbook(io.BytesIO(data), data_only=True)
        sections = []
        for sheet in wb.worksheets:
            rows = []
            for row in sheet.iter_rows(values_only=True):
                rows.append("\t".join("" if v is None else str(v) for v in row))
            sections.append(f"## Sheet: {sheet.title}\n" + "\n".join(rows))
        return "\n\n".join(sections).strip()
    except ImportError:
        return "[Excel extraction requires openpyxl: pip install openpyxl]"
    except Exception as e:
        return f"[Could not extract Excel: {e}]"
