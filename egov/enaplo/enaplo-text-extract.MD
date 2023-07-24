# E-NAPLÓ (and generic) PDF Text Extractor

Extract specific blocks of text from a PDF file based on customizable delimiters.

Works with PDF from enaplo.e-epites.hu/

## Table of Contents

- [Description](#description)
- [Requirements](#requirements)
- [Usage](#usage)
- [License](#license)

## Description

The script is designed to extract text blocks from a PDF based on customizable parameters. The default parameters extract text blocks between "Szöveg:" and "A bejegyzéshez csatolt fotók:" for each entry, and it uses the date format "YYYY.MM.DD" to determine each entry's date.

It provides an output with each date followed by the extracted text block, and at the end of the output, it provides a summary of the number of entries found for each month.

## Requirements

- Python 3+
- PyPDF2 library: Install using pip:

pip install pypdf2


## Usage

### Script Parameters

- **input_file**: Path to the input PDF file. (Required)
- **output_file**: Path to the output TXT file. (Optional; default is "output.txt")
- **start_block**: Start delimiter for each block. (Optional; default is "Bejegyzés dátum:")
- **text_start**: Delimiter to start the text extraction. (Optional; default is "Szöveg:")
- **text_end**: Delimiter to end the text extraction. (Optional; default is "A bejegyzéshez csatolt fotók:")

### Running the Script

1. Navigate to the directory containing the script:


Run the script with required and optional parameters:

python enaplo-text-extract.py --input_file path_to_input_pdf [--output_file path_to_output_txt] [--start_block custom_start_block] [--text_start custom_text_start] [--text_end custom_text_end]


## License

This project is licensed under the terms of the MIT license.

