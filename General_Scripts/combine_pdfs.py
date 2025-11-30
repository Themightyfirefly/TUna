import os
import shutil
import pathlib
import re
import sys

from urllib.parse import urljoin
from typing import List

from pypdf import PdfWriter

MAX_FILE_SIZE = 500_000_000

def main():
    DOWNLOAD_DIR = str(sys.argv[1])
    print("Download dir: " + str(DOWNLOAD_DIR))
    FILENAME = re.sub(r".*combine_([^\\\/]*)[\\\/]*", r"\1", DOWNLOAD_DIR)
    print("Filename: " + str(FILENAME))
    
    print("Combining pdf files")
    total_download_dir = os.path.join(pathlib.Path(__file__).parent.resolve(),DOWNLOAD_DIR)
    pdf_files = pathlib.Path(total_download_dir).glob("*.pdf")
    files_left = [pdf for pdf in pdf_files if str(pdf).endswith(".pdf")]
    def file_sizes(files: List[str]):
        return sum([os.path.getsize(file) for file in files])
    counter = 0
    print("found: " + str(len(files_left)))
    while(files_left):
        files_to_combine = []
        combined = False
        i = 0
        while i < len(files_left):
            if file_sizes(files_to_combine + [files_left[i]]) < MAX_FILE_SIZE:
                files_to_combine.append(files_left[i])
                files_left.remove(files_left[i])
                continue
            i += 1
        if files_to_combine:
            merger = PdfWriter()
            for pdf in files_to_combine:
                try:
                    merger.append(pdf, import_outline=False)
                except Exception:
                    print(f"Could not write {str(pdf)}")
            if counter == 0: target = os.path.join(pathlib.Path(total_download_dir).parent.resolve(),f"{FILENAME}.pdf")
            else: target = os.path.join(pathlib.Path(total_download_dir).parent.resolve(),f"{FILENAME}_{counter}.pdf")
            print("target: " + str(target))
            merger.write(target)
            counter+=1
            merger.close()
            combined = True
        if not combined:
            break

if __name__ == "__main__":
    main()