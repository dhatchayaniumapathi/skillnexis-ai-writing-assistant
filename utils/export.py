
from pathlib import Path
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def export_txt(content):

    return content.encode("utf-8")


def export_pdf(content, title="AI Generated Content"):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = [
        Paragraph(title, styles["Title"]),
        Spacer(1, 20)
    ]

    for paragraph in content.split("\n"):

        if paragraph.strip():
            story.append(
                Paragraph(
                    paragraph.replace("&", "&amp;"),
                    styles["BodyText"]
                )
            )

            story.append(Spacer(1, 10))

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()
