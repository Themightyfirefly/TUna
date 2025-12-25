#!/usr/bin/env python3
"""
Combine all markdown files in a directory into a single markdown file.
"""
import os
from pathlib import Path


def combine_markdown_files(input_dir, output_file):
    """
    Combine all .md files from input_dir into a single output_file.
    
    Args:
        input_dir: Path to directory containing markdown files
        output_file: Path to the combined output file
    """
    input_path = Path(input_dir)
    
    # Get all .md files, sorted alphabetically
    md_files = sorted(input_path.glob("*.md"))
    
    if not md_files:
        print(f"No markdown files found in {input_dir}")
        return
    
    print(f"Found {len(md_files)} markdown files")
    
    # Combine all files
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, md_file in enumerate(md_files):
            print(f"Processing: {md_file.name}")
            
            # Add separator between files (except for the first one)
            if i > 0:
                outfile.write("\n\n---\n\n")
            
            # Add filename as header
            outfile.write(f"# {md_file.stem}\n\n")
            
            # Write file content
            with open(md_file, 'r', encoding='utf-8') as infile:
                content = infile.read()
                outfile.write(content)
                
                # Ensure there's a newline at the end
                if not content.endswith('\n'):
                    outfile.write('\n')
    
    print(f"\nCombined {len(md_files)} files into {output_file}")


if __name__ == "__main__":
    # Default paths
    input_directory = "Knowledge/Pruefungsamt_Thesis/Stupo_Thesis_Sections"
    output_filename = "combined_thesis_sections.md"
    
    # Uncomment to use command line arguments
    # import sys
    # if len(sys.argv) >= 2:
    #     input_directory = sys.argv[1]
    # if len(sys.argv) >= 3:
    #     output_filename = sys.argv[2]
    
    combine_markdown_files(input_directory, output_filename)
