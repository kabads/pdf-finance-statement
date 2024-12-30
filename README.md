# PDF Finance Statement Processor

A Python script for extracting and processing transaction data from PDF bank statements.

## Features

- Processes multiple PDF files in the current directory
- Extracts transaction data while excluding irrelevant information
- Cleans and formats the extracted text
- Outputs processed data to individual text files
- Handles common PDF formatting issues

## Usage

1. Place your PDF bank statements in the project directory
2. Run the script:
```bash
python pdf_processor.py
```

The script will:
- Process all PDF files in the current directory
- Create corresponding `.txt` files with cleaned transaction data
- Return a list of processed data for each month

## Requirements

- Python 3.x
- PyPDF2 library

Install dependencies with:
```bash
pip install PyPDF2
```

## How It Works

The script:
1. Identifies PDF files in the current directory
2. Extracts text from each PDF page
3. Removes unwanted patterns (account numbers, balances, etc.)
4. Fixes common formatting issues
5. Filters and organizes transaction data
6. Saves cleaned data to text files
