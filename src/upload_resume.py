import boto3
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import os

# Constants
BUCKET_NAME = 'resume-versioning-bucket'
UPLOAD_DIR = 'resume-uploads'

def upload_to_s3(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        s3 = boto3.client('s3')
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        versioned_key = f'{UPLOAD_DIR}/resume-{timestamp}.pdf'

        with open(file_path, 'rb') as file_data:
            s3.upload_fileobj(
                file_data,
                BUCKET_NAME,
                versioned_key,
                ExtraArgs={'ContentType': 'application/pdf'}
            )
        # Also upload as root resume.pdf (overwrite)
        with open(file_path, 'rb') as file_data:
            s3.upload_fileobj(
                file_data,
                BUCKET_NAME,
                'resume.pdf',
                ExtraArgs={'ContentType': 'application/pdf'}
            )

        return True, versioned_key

    except Exception as e:
        return False, str(e)

def select_and_upload():
    file_path = filedialog.askopenfilename(
        title="Select Resume PDF",
        filetypes=[("PDF files", "*.pdf")]
    )
    if not file_path:
        return

    success, msg = upload_to_s3(file_path)
    if success:
        messagebox.showinfo("Success", f"Resume uploaded as {msg}")
        root.destroy()
    else:
        messagebox.showerror("Upload Failed", f"Error: {msg}")

root = tk.Tk()
root.title("Resume Uploader")
root.geometry("400x200")

label = tk.Label(root, text="Click to select and upload your resume PDF", font=("Arial", 12))
label.pack(pady=30)

upload_button = tk.Button(root, text="Select PDF", font=("Arial", 12), command=select_and_upload)
upload_button.pack()

root.mainloop()
