import os
import shutil
import pathlib
import re

from urllib.parse import urljoin
from typing import List

from bs4 import BeautifulSoup
from pypdf import PdfWriter
import requests

BASE_URL = "https://www.tu.berlin/studieren/studienangebot/gesamtes-studienangebot"
DOWNLOAD_DIR = "temp_pdf_downloads"
MAX_FILE_SIZE = 500_000_000

def make_soup(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def get_program_lists():
    """Get all of the study program lists (all pages in the main list at https://www.tu.berlin/studieren/studienangebot/gesamtes-studienangebot)"""
    print(f"Finding all study program lists at {BASE_URL}")
    soup = make_soup(BASE_URL)
    program_lists = []
    for a in soup.find_all("a", href=True):
        if (
            re.match(r"^/studieren/studienangebot/gesamtes-studienangebot/[0-9]+$", a["href"]) is not None 
            and urljoin(BASE_URL, a["href"]) not in program_lists
        ):
            program_lists.append(urljoin(BASE_URL, a["href"]))
    return program_lists

def get_program_sites(program_lists: List[str]):
    program_sites = []
    iter = 1
    for pl in program_lists:
        print(f"({iter}/{len(program_lists)}) Finding all program info webpages that exist at {pl}")
        soup = make_soup(pl)
        for a in soup.find_all("a", href=True):
            if (
                "/studieren/studienangebot/gesamtes-studienangebot/studiengang" in a['href']
                and urljoin(BASE_URL, a['href']) not in program_sites
            ):
                program_sites.append(urljoin(BASE_URL, a['href']))
        iter += 1
    return program_sites

def html_to_markdown(program_sites: List[str]):
    print("\n Study program websites")
    content=[]
    iter = 1
    total_download_dir = os.path.join(pathlib.Path(__file__).parent.resolve(),DOWNLOAD_DIR)
    if not os.path.exists(total_download_dir):
        os.makedirs(total_download_dir)
    
    #https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder
    for filename in os.listdir(total_download_dir):
        file_path = os.path.join(total_download_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    for link in program_sites:
        print(f"({iter}/{len(program_sites)}) Extracting information from {link}")
        soup = make_soup(link)
        supported_types = ["h1","h2","h3","h4","p","li"]
        for entry in soup.find_all(supported_types):
            text = ""
            match entry.name:
                case "p":
                    text = entry.get_text() + "\n"
                    for link in entry.find_all("a"):
                        text = text.replace(link.get_text().strip(), f"[{link.get_text()}]({link["href"]})")
                case "h1":
                    text = "# " + entry.get_text().strip()
                case "h2":
                    text = "## " + entry.get_text().strip()
                case "h3":
                    text = "### " + entry.get_text().strip()
                case "h4":
                    text = "#### " + entry.get_text().strip()
                case "li":
                    if "class" in entry.attrs and "stupoDownloadList" in entry.attrs["class"]:
                        a_elem = entry.contents[0]
                        if a_elem["href"].endswith(".pdf"):
                            try:
                                _r = requests.get(a_elem["href"])
                                _r.raise_for_status()
                                if "download" in a_elem:
                                    filename = a_elem["download"]
                                else:
                                    filename = re.sub(r"[ \n]", "", a_elem.get_text())
                                    filename = re.sub(r"\(.*\)", "", filename)
                                    filename = re.sub(r"\/","", filename)
                                    filename = re.sub(r"(\.pdf)*$", ".pdf", filename)
                                with open(f"{total_download_dir}/{filename}", "wb") as f:
                                    f.write(_r.content)
                                text = f"Siehe StuPo Datei in der Knowledge (Link zu der StuPo pdf auf der TU Berlin Internetseite: {a_elem["href"]})."
                            except Exception as e:
                                print(f"Could not download file from {a_elem["href"]}:\n{e}")
                case _:
                    pass
            if text.strip() != "":
                content.append(text)
        iter += 1
    with open(os.path.join(pathlib.Path(__file__).parent.resolve(),"Studiengaenge_websites.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(content))
    
def join_pdf_files():
    print("Combining pdf files")
    total_download_dir = os.path.join(pathlib.Path(__file__).parent.resolve(),DOWNLOAD_DIR)
    pdf_files = pathlib.Path(total_download_dir).glob("*.pdf")
    files_left = [pdf for pdf in pdf_files if str(pdf).endswith(".pdf")]
    def file_sizes(files: List[str]):
        return sum([os.path.getsize(file) for file in files])
    counter = 0
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
            merger.write(os.path.join(pathlib.Path(__file__).parent.resolve(),f"StuPos_{counter}.pdf"))
            counter+=1
            merger.close()
            combined = True
        if not combined:
            break


def main():
    program_lists = get_program_lists()
    program_sites = get_program_sites(program_lists)
    html_to_markdown(program_sites)
    join_pdf_files()
    
if __name__ == "__main__":
    main()