import re

import pymupdf
from PyPDF2 import PdfReader


# ============================================================
# CLEAN PDF TEXT
# ============================================================

def clean_extracted_text(text):

    if not text:
        return ""

    # Email markdown links
    text = re.sub(
        r"\[([^\]]+)\]\(mailto:[^)]+\)",
        r"\1",
        text,
        flags=re.IGNORECASE,
    )

    # Web markdown links
    text = re.sub(
        r"\[([^\]]+)\]\(https?://[^)]+\)",
        r"\1",
        text,
        flags=re.IGNORECASE,
    )

    # Markdown formatting
    text = re.sub(
        r"[*_~`]+",
        "",
        text,
    )

    # Encoding artifacts
    replacements = {
        "â‚¹": "₹",
        "â€“": "-",
        "â€”": "-",
        "â€¢": "•",
        "â€˜": "'",
        "â€™": "'",
        "â€œ": '"',
        "â€": '"',
        "â€¦": "...",
        "Â": "",
        "\xa0": " ",
    }

    for old, new in replacements.items():
        text = text.replace(
            old,
            new,
        )

    # Common extraction junk
    text = re.sub(
        r"\bsvg\b",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Normalize whitespace
    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    # Clean line spacing
    text = re.sub(
        r" *\n *",
        "\n",
        text,
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(
        lines
    ).strip()


# ============================================================
# PDF EXTRACTION
# ============================================================

def extract_text_from_pdf(file):

    # --------------------------------------------------------
    # PyMuPDF
    # --------------------------------------------------------

    try:

        file.seek(0)

        pdf_bytes = file.read()

        pdf = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf",
        )

        pages = []

        for page in pdf:

            page_text = page.get_text(
                "text"
            )

            if page_text:
                pages.append(
                    page_text
                )

        pdf.close()

        text = clean_extracted_text(
            "\n".join(pages)
        )

        if text:
            return text

    except Exception:
        pass


    # --------------------------------------------------------
    # PyPDF2 fallback
    # --------------------------------------------------------

    try:

        file.seek(0)

        reader = PdfReader(
            file
        )

        pages = []

        for page in reader.pages:

            try:

                page_text = (
                    page.extract_text()
                    or ""
                )

                if page_text:
                    pages.append(
                        page_text
                    )

            except Exception:
                continue

        text = clean_extracted_text(
            "\n".join(pages)
        )

        if text:
            return text

        return (
            "ERROR: No readable text found in PDF."
        )

    except Exception as exc:

        return (
            "ERROR: Could not read PDF "
            f"({exc})"
        )


# ============================================================
# VALIDATE RESUME
# ============================================================

def is_valid_resume_text(text):

    if not text:
        return False

    if text.startswith("ERROR"):
        return False

    return len(
        text.split()
    ) >= 30


# ============================================================
# TEXT STATISTICS
# ============================================================

def get_text_statistics(text):

    if not text:

        return {
            "characters": 0,
            "words": 0,
            "lines": 0,
        }

    return {

        "characters": len(text),

        "words": len(
            text.split()
        ),

        "lines": len(
            text.splitlines()
        ),
    }