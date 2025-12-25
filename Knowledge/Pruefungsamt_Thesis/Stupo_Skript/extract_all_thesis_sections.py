"""
Script to extract thesis sections from all study programs listed in test.txt.
It matches study programs with their StuPo PDFs from Studiengaenge_websites.md,
downloads the PDFs, and extracts the Bachelorarbeit/Masterarbeit sections.
"""

import os
import re
import requests
import tempfile
from pathlib import Path
from extract_thesis_section import extract_text_from_pdf, extract_thesis_section, clean_text


# Base paths
BASE_DIR = Path(__file__).parent.parent.parent.parent
STUDIENGAENGE_MD = BASE_DIR / "Studiengaenge_websites.md"
TEST_TXT = BASE_DIR / "test.txt"
OUTPUT_DIR = BASE_DIR / "Knowledge" / "Pruefungsamt_Thesis" / "Stupo_Thesis_Sections_v2"


def parse_study_programs(test_file: Path) -> list[dict]:
    """
    Parse the study programs from test.txt.
    Each line format: <Name> <Degree> <Year> [optional: (pdf, xxx KB)]
    Returns list of dicts with 'name', 'degree', 'year', 'full_name'
    """
    programs = []
    with open(test_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Remove (pdf, xxx KB) suffix if present
            line = re.sub(r'\s*\(pdf,\s*[\d,]+\s*KB\)\s*$', '', line)
            
            # Match pattern: Name Degree Year
            # Degree patterns: B.Sc., M.Sc., B.A., M.A., M.Ed., B.Eng., MBA, MBL, S
            match = re.match(r'^(.+?)\s+(B\.Sc\.|M\.Sc\.|B\.A\.|M\.A\.|M\.Ed\.|B\.Eng\.|MBA|MBL|S)\s+(\d{4})\s*$', line)
            if match:
                name = match.group(1).strip()
                degree = match.group(2)
                year = match.group(3)
                programs.append({
                    'name': name,
                    'degree': degree,
                    'year': year,
                    'full_name': f"{name} {degree} {year}"
                })
            else:
                print(f"Warning: Could not parse line: {line}")
    
    return programs


def extract_stupo_urls(md_file: Path) -> list[dict]:
    """
    Extract all StuPo PDF URLs from the Studiengaenge_websites.md file.
    Returns list of dicts with 'url', 'filename', 'name', 'degree', 'year'
    """
    urls = []
    url_pattern = r'https://www\.static\.tu\.berlin/fileadmin/www/10000000/Studiengaenge/StuPOs/[^\s\)]+\.pdf'
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all StuPo URLs
    found_urls = set(re.findall(url_pattern, content))
    
    for url in found_urls:
        # Remove trailing period if present
        url = url.rstrip('.')
        
        # Extract filename
        filename = url.split('/')[-1]
        
        # Parse filename to extract study program info
        # Pattern: <Name>_<Degree>_<Year>.pdf
        # Examples: Architektur_B.Sc._2018.pdf, AudiokommTech_M.Sc._2024.pdf
        name_match = re.match(r'^(.+?)_(B\.Sc\.|M\.Sc\.|B\.A\.|M\.A\.|M\.Ed\.|B\.Eng\.|MBA|MBL|S)_(\d{4})\.pdf$', filename)
        
        if name_match:
            urls.append({
                'url': url,
                'filename': filename,
                'name_in_file': name_match.group(1),
                'degree': name_match.group(2),
                'year': name_match.group(3)
            })
    
    return urls


def normalize_name(name: str) -> str:
    """Normalize a study program name for matching."""
    # Convert to lowercase
    name = name.lower()
    # Remove special characters except spaces and hyphens
    name = re.sub(r'[^\w\s\-äöüß]', '', name)
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name).strip()
    # Common replacements
    replacements = {
        'und': '',
        ' ': '',
        '-': '',
        'ue': 'ü',
        'oe': 'ö',
        'ae': 'ä',
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    return name


def find_matching_url(program: dict, stupo_urls: list[dict]) -> str | None:
    """
    Find the matching StuPo URL for a study program.
    """
    target_name = program['name']
    target_degree = program['degree']
    target_year = program['year']
    
    # Normalize target name
    target_normalized = normalize_name(target_name)
    
    # First, try exact match on degree and year
    for stupo in stupo_urls:
        if stupo['degree'] == target_degree and stupo['year'] == target_year:
            stupo_normalized = normalize_name(stupo['name_in_file'])
            
            # Check if names match (fuzzy)
            if (target_normalized in stupo_normalized or 
                stupo_normalized in target_normalized or
                target_normalized == stupo_normalized):
                return stupo['url']
    
    # Second pass: more lenient matching
    for stupo in stupo_urls:
        if stupo['degree'] == target_degree and stupo['year'] == target_year:
            # Try partial matching on significant parts
            stupo_name = stupo['name_in_file'].lower().replace('_', '')
            target_parts = target_name.lower().split()
            
            # Check if any significant word matches
            matches = 0
            for part in target_parts:
                if len(part) > 3 and part in stupo_name:
                    matches += 1
            
            if matches >= 1:
                return stupo['url']
    
    return None


def download_pdf(url: str, temp_dir: str) -> str | None:
    """Download a PDF to a temporary directory."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        filename = url.split('/')[-1]
        filepath = os.path.join(temp_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        return filepath
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None


def process_program(program: dict, url: str, output_dir: Path, temp_dir: str) -> bool:
    """
    Process a single study program: download PDF and extract thesis section.
    Returns True if successful.
    """
    print(f"\nProcessing: {program['full_name']}")
    print(f"  URL: {url}")
    
    # Download PDF
    pdf_path = download_pdf(url, temp_dir)
    if not pdf_path:
        print(f"  ERROR: Failed to download PDF")
        return False
    
    # Extract text from PDF
    try:
        text = extract_text_from_pdf(pdf_path)
    except Exception as e:
        print(f"  ERROR: Failed to extract text: {e}")
        return False
    
    # Extract thesis section
    thesis_section = extract_thesis_section(text)
    
    if thesis_section is None:
        print(f"  WARNING: No thesis section found")
        return False
    
    # Clean the extracted text
    thesis_section = clean_text(thesis_section)
    
    # Create output filename
    safe_name = re.sub(r'[^\w\s\-.]', '', program['full_name']).replace(' ', '_')
    output_path = output_dir / f"{safe_name}_Thesis.md"
    
    # Save to markdown
    markdown_content = f"# {program['full_name']}\n\n"
    markdown_content += f"## Thesis-Regelungen (Studien- und Prüfungsordnung)\n\n"
    markdown_content += f"**Quelle:** [{url.split('/')[-1]}]({url})\n\n"
    markdown_content += thesis_section + "\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"  SUCCESS: Saved to {output_path.name}")
    return True


def main():
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Parse study programs from test.txt
    print("Parsing study programs from test.txt...")
    programs = parse_study_programs(TEST_TXT)
    print(f"Found {len(programs)} study programs")
    
    # Extract all StuPo URLs from Studiengaenge_websites.md
    print("\nExtracting StuPo URLs from Studiengaenge_websites.md...")
    stupo_urls = extract_stupo_urls(STUDIENGAENGE_MD)
    print(f"Found {len(stupo_urls)} unique StuPo URLs")
    
    # Process each program
    success_count = 0
    failed_programs = []
    no_url_programs = []
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for program in programs:
            # Find matching URL
            url = find_matching_url(program, stupo_urls)
            
            if url is None:
                print(f"\nNo URL found for: {program['full_name']}")
                no_url_programs.append(program['full_name'])
                continue
            
            # Process the program
            if process_program(program, url, OUTPUT_DIR, temp_dir):
                success_count += 1
            else:
                failed_programs.append(program['full_name'])
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total programs: {len(programs)}")
    print(f"Successfully processed: {success_count}")
    print(f"No URL found: {len(no_url_programs)}")
    print(f"Processing failed: {len(failed_programs)}")
    
    if no_url_programs:
        print("\nPrograms without matching URL:")
        for p in no_url_programs:
            print(f"  - {p}")
    
    if failed_programs:
        print("\nPrograms that failed processing:")
        for p in failed_programs:
            print(f"  - {p}")
    
    print(f"\nOutput saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
