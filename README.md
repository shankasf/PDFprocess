# PDF Processing Pipeline

This project is a **PDF Processing Pipeline** written in Python that automates text extraction, table extraction, text summarization, keyword extraction, sentiment analysis, and word frequency analysis from PDF documents.

---

## Features

- Extract text from normal and scanned PDFs (fallback to OCR using Tesseract).
- Clean and normalize extracted text.
- Extract tables from PDFs and export them as CSV using Tabula.
- Summarize text using **Sumy's LSA Summarizer**.
- Extract keywords using **RAKE (Rapid Automatic Keyword Extraction)**.
- Perform sentiment analysis using **TextBlob**.
- Compute word frequencies.
- Save all outputs (text, summary, keywords, tables, word frequencies) into organized files.

---

## Dependencies

Install the following Python libraries before running the project:

```bash
pip install PyPDF2 pytesseract pdf2image sumy rake-nltk textblob tabula-py
```

> Note:
> - You need to have **Java** installed for Tabula.
> - You need **Tesseract OCR** installed and properly configured in your system's PATH.

---

## Project Structure

```
PDFProcess/
│
├── RawPDF.pdf                 # Input PDF file
├── cleaned_output.txt         # Extracted and cleaned text
├── summary.txt                # Generated summary
├── keywords.txt               # Extracted keywords
├── word_frequencies.txt       # Word frequency dictionary
├── tables/                    # Extracted CSV tables
└── pdf_processor.py           # Main script (the provided code)
```

---

## How it Works

1. Extracts text from the PDF using `PyPDF2`. If not extractable (scanned PDFs), performs OCR using `pytesseract`.
2. Cleans the extracted text (removes unwanted characters and extra whitespace).
3. Extracts all tables into CSV files using `Tabula`.
4. Summarizes the text (top 5 sentences by default).
5. Extracts keywords using RAKE.
6. Performs sentiment analysis.
7. Calculates word frequency.
8. Saves all results into respective output files.

---

## Usage

Make sure to update the `file_path`, `output_text_file`, and `table_output_folder` variables in the `process_pdf()` call at the bottom of `pdf_processor.py`:

```python
file_path = r"D:\self study\python\PDFProcess\RawPDF.pdf"
output_text_file = r"D:\self study\python\PDFProcess\cleaned_output.txt"
table_output_folder = r"D:\self study\python\PDFProcess\tables"
```

Then simply run:

```bash
python pdf_processor.py
```

---

## Output Example

- Cleaned Text: `cleaned_output.txt`
- Summarized Text: `summary.txt`
- Keywords: `keywords.txt`
- Word Frequencies: `word_frequencies.txt`
- Extracted Tables: `tables/table_1.csv`, `tables/table_2.csv`, ...

---

## Notes

- If OCR is slow, optimize `pdf2image.convert_from_path()` by setting `dpi=200` or lower.
- Sentiment polarity ranges from `-1` (negative) to `1` (positive).
- Adjust `num_sentences` in `summarize_text()` function to change the summary length.

---

## Author

Developed by **Sagar Shankaran**  
Feel free to fork, enhance, and share your version.

