import os
import PyPDF2
import re
from datetime import datetime



def process_pdfs():
    # Initialize list to hold all months
    year = []

    # Get all PDF files in current directory
    pdf_files = [f for f in os.listdir() if f.endswith(".pdf")]

    # Patterns to exclude
    exclude_patterns = [
        r"Statement Date:\s*\d{2}/\d{2}/\d{4}",
        r"Statement No:\s*\d+",
        r"Sort Code:\s*\d{2}-\d{2}-\d{2}",
        r"Account No:\s*\d+",
        r"Start Balance:\s*[\d,]+\.\d{2}",
        r"End Balance:\s*[\d,]+\.\d{2}",
        r"Average Credit Balance:\s*[\d,]+\.\d{2}",
        r"Average Debit Balance:\s*[\d,]+\.\d{2}",
        r"CurrentAccount\s*Statement\s*0572\s*YourFlexDirect\s*transactions",
        r"NAIAGB21\s*GB11NAIA07043620012667\s*MIDLGB22",
        r"Receiving an\s*International Payment\?",
        r"(BIC|IBAN|Swift|Intermediary Bank)",
        r"Nationwide BuildingSociety.*?106078\.",
        r"HeadOffice:.*?SN381NW",
        r"10/14\.4pt_DC83 \(30June2014\)_CSIS2023",
        r"Statement date: \d{2}[A-Za-z]+\d{4}Sortcode \d{2}-\d{2}-\d{2}",
        r"Statement no: \d+of\dAccountno \d+",
        r"Startbalance £[\d,]+\.\d{2}",
        r"Endbalance £[\d,]+\.\d{2}",
        r"Averagecredit\s*balance £[\d,]+\.\d{2}",
        r"Averagedebit\s*balance £[\d,]+\.\d{2}",
        r"Date Description £Out £In £Balance",
        r"Balancefromstatement \d+dated\d{2}/\d{2}/\d{4} [\d,]+\.\d{2}",
    ]

    # Patterns to fix formatting
    fix_patterns = [
        (r"(\d{2})([A-Za-z]{3})", r"\1 \2"),  # Add space between date and month
        (
            r"([A-Za-z])([A-Z][a-z])",
            r"\1 \2",
        ),  # Fix word breaks like "Londo n" -> "London"
        (
            r"([a-z])([A-Z])",
            r"\1 \2",
        ),  # Add space between lowercase and uppercase letters
        (r"\s{2,}", " "),  # Normalize multiple spaces to single space
        (
            r"([A-Za-z]+) ([A-Za-z]{1,2}) ([A-Za-z]+)",
            r"\1\2 \3",
        ),  # Fix remaining incorrect spaces
        (r"([A-Za-z]+)(\d)", r"\1 \2"),  # Add space between letters and numbers
        (r"(\d)([A-Za-z]+)", r"\1 \2"),  # Add space between numbers and letters
    ]

    for pdf_file in pdf_files:
        # Extract month name from filename (without .pdf extension)
        month_name = os.path.splitext(pdf_file)[0]

        # Read PDF content
        with open(pdf_file, "rb") as pdf_file_obj:
            reader = PyPDF2.PdfReader(pdf_file_obj)
            text_content = ""

            # Extract customer info from each page
            for page in reader.pages:
                page_text = page.extract_text()
                # Remove excluded patterns
                for pattern in exclude_patterns:
                    page_text = re.sub(pattern, "", page_text)

                # Fix formatting patterns
                for pattern, replacement in fix_patterns:
                    page_text = re.sub(pattern, replacement, page_text)

                text_content += page_text

            # Find all lines starting with dates in "DD Mon" format and capture the full line
            lines = text_content.splitlines()
            filtered_lines = []
            i = 0
            while i < len(lines):
                if re.match(
                    r"^\d{2} [A-Za-z]{3}", lines[i]
                ):  # Check if line starts with a date
                    entry = [lines[i].strip()]
                    i += 1
                    while i < len(lines) and not re.match(
                        r"^\d{2} [A-Za-z]{3}", lines[i]
                    ):
                        entry.append(lines[i].strip())
                        i += 1
                    filtered_lines.append("\n".join(entry))
                else:
                    i += 1

            # Join filtered lines with newlines
            filtered_content = "\n".join(filtered_lines)

            # Add to year list
            year.append(filtered_content)

            # Write to output file
            output_filename = f"{month_name}.txt"
            with open(output_filename, "w") as output_file:
                output_file.write(filtered_content)

    return year


if __name__ == "__main__":
    process_pdfs()
