from docx import Document

doc = Document()
doc.add_paragraph("This is a test document created using python-docx.")
doc.save("test.docx")
