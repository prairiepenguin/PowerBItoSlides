# -*- coding: utf-8 -*-
"""
Created on Wed May 21 11:33:53 2025

@author: jingalls
"""

import fitz  # PyMuPDF
import pdfplumber
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

class PDFtoPNGApp:
    def __init__(self, root):
        self.root = root
        root.title("PDF to PNG Converter")

        # Labels and Entry boxes
        tk.Label(root, text="PDF File:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.pdf_entry = tk.Entry(root, width=50)
        self.pdf_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse...", command=self.browse_pdf).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(root, text="Output Folder:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.out_entry = tk.Entry(root, width=50)
        self.out_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse...", command=self.browse_output).grid(row=1, column=2, padx=5, pady=5)

        # Run and Quit buttons
        self.run_button = tk.Button(root, text="Run", width=12, bg="#99ee99", relief="raised", command=self.run)
        self.run_button.grid(row=2, column=1, pady=20, sticky="e")
        self.quit_button = tk.Button(root, text="Quit", width=12, bg="#ee9999", relief="raised", command=root.quit)
        self.quit_button.grid(row=2, column=2, pady=20, sticky="w")

    def browse_pdf(self):
        filename = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")], title="Select PDF File")
        if filename:
            self.pdf_entry.delete(0, tk.END)
            self.pdf_entry.insert(0, filename)

    def browse_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.out_entry.delete(0, tk.END)
            self.out_entry.insert(0, folder)

    def run(self):
        pdf_file = self.pdf_entry.get()
        output_folder = self.out_entry.get()
        if not pdf_file or not os.path.isfile(pdf_file):
            messagebox.showerror("Error", "Please select a valid PDF file.")
            return
        if not output_folder:
            messagebox.showerror("Error", "Please select a valid output folder.")
            return

        os.makedirs(output_folder, exist_ok=True)

        try:
            doc = fitz.open(pdf_file)
            with pdfplumber.open(pdf_file) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
                        if lines:
                            title = lines[0]
                            safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)
                            filename = f"{safe_title[:50]}.png"
                        else:
                            filename = f"{i+1:02d}_untitled.png"
                    else:
                        filename = f"{i+1:02d}_no_text.png"
                    output_path = os.path.join(output_folder, filename)
                    page_pix = doc.load_page(i).get_pixmap(dpi=300)
                    page_pix.save(output_path)
            doc.close()
            messagebox.showinfo("Done", "PDF pages have been saved as PNGs.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFtoPNGApp(root)
    root.resizable(False, False)
    root.mainloop()
