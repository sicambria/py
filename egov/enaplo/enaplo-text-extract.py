import PyPDF2
import re
import argparse
import logging
from datetime import datetime
from collections import defaultdict

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text_from_pdf(pdf_path):
    logging.info(f"Reading PDF from {pdf_path}")
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    logging.info(f"Finished reading {pdf_path}")
    return text

def extract_desired_blocks(text, start_block, date_format, text_start, text_end):
    logging.info("Extracting desired blocks from the text...")
    pattern = rf'{start_block}({date_format}).*?{text_start}\s*(.*?)\s*{text_end}'
    matches = re.findall(pattern, text, re.DOTALL)
    logging.info(f"Found {len(matches)} desired blocks.")
    return matches

def extract_month_year(date_str):
    """Extract month and year from the date string."""
    parts = date_str.split('.')
    if len(parts) < 3:
        logging.error(f"Unexpected date format: {date_str}")
        return None, None
    year, month = parts[0], parts[1]
    return year, month

def get_month_statistics(matches):
    """Get statistics of entries for each month."""
    stats = defaultdict(int)
    for date, _ in matches:
        year, month = extract_month_year(date)
        if year and month:
            stats[f"{year}.{month}"] += 1
    return stats

def write_to_txt(matches, output_file, input_file_name):
    logging.info(f"Writing extracted blocks to {output_file}...")
    with open(output_file, 'w') as f:
        for date, content in matches:
            f.write(date.strip() + "\n")
            f.write(content.strip() + "\n\n")
        
        # Month statistics
        month_stats = get_month_statistics(matches)
        
        f.write("\n\n")
        f.write("Monthly Entry Statistics:\n")
        for month_year, count in sorted(month_stats.items()):
            year, month_num = month_year.split('.')
            month_name = datetime(int(year), int(month_num), 1).strftime('%B')
            f.write(f"{year}. {month_name}: {count} entries\n")
        
        # Add extra details to the end of the output file
        script_date = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        f.write("\n")
        f.write(f"Input File Name: {input_file_name}\n")
        f.write(f"Number of Blocks Found: {len(matches)}\n")
        f.write(f"Date of Script Running: {script_date}\n")
    logging.info(f"Finished writing to {output_file}")

def main(args):
    text = extract_text_from_pdf(args.input_file)
    matches = extract_desired_blocks(text, args.start_block, args.date_format, args.text_start, args.text_end)
    write_to_txt(matches, args.output_file, args.input_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text blocks from a PDF.")
    
    parser.add_argument("input_file", help="Path to the input PDF file.")
    parser.add_argument("-o", "--output_file", default="output.txt", help="Path to the output text file. Default is 'output.txt'.")
    parser.add_argument("--start_block", default="Bejegyzés dátum: ", help="Start block marker. Default is 'Bejegyzés dátum: '")
    parser.add_argument("--date_format", default=r"\d{4}\.\d{2}\.\d{2}", help="Regex pattern for date format. Default is \d{4}\.\d{2}\.\d{2}")
    parser.add_argument("--text_start", default="Szöveg:", help="Text start marker. Default is 'Szöveg:'")
    parser.add_argument("--text_end", default="A bejegyzéshez csatolt fotók:", help="Text end marker. Default is 'A bejegyzéshez csatolt fotók:'")

    args = parser.parse_args()
    main(args)
