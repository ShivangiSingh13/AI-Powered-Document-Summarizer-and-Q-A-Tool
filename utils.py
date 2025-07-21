import os
import uuid
import io
from werkzeug.utils import secure_filename

from my_socx_script import extract_text_from_docx, extract_text_from_pdf

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """
    Check if the uploaded file is an allowed type.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    """
    Save the uploaded file to the upload folder with a unique name.
    Returns both path and original name.
    """
    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(file_path)
    return file_path

def extract_text(file_path_or_stream, filename=None):
    """
    Extract text from a given file path or BytesIO stream.
    """
    if isinstance(file_path_or_stream, io.BytesIO) and filename:
        ext = filename.rsplit('.', 1)[1].lower()
        if ext == 'pdf':
            return extract_text_from_pdf(file_path_or_stream)
        elif ext == 'docx':
            return extract_text_from_docx(file_path_or_stream)
    elif isinstance(file_path_or_stream, str):
        if file_path_or_stream.endswith('.pdf'):
            return extract_text_from_pdf(file_path_or_stream)
        elif file_path_or_stream.endswith('.docx'):
            return extract_text_from_docx(file_path_or_stream)

    return "Unsupported file format or input type."

def get_file_history():
    """
    Return the list of uploaded files (filenames only).
    """
    files = os.listdir(UPLOAD_FOLDER)
    return sorted(files, reverse=True)
