import os
import re
from PyPDF2 import PdfReader
from pytesseract import image_to_string
from pdf2image import convert_from_path
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from rake_nltk import Rake
from textblob import TextBlob
from collections import Counter
import tabula

# Function to extract text from a PDF using PyPDF2
def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF using PyPDF2.
    If the PDF has scanned pages, fallback to OCR.
    """
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    except Exception as e:
        print(f"Error extracting text using PyPDF2: {e}")
        text = ""

    if not text.strip():  # If no text, fallback to OCR
        print("Fallback to OCR for text extraction.")
        text = ocr_from_pdf(file_path)
    return text

# Function to perform OCR on a PDF using pytesseract
def ocr_from_pdf(file_path):
    """
    Perform OCR on PDF using Tesseract and pdf2image.
    """
    pages = convert_from_path(file_path)
    text = ""
    for page in pages:
        text += image_to_string(page)
    return text

# Function to clean text
def clean_text(text):
    """
    Clean extracted text by removing extra whitespace and special characters.
    """
    text = re.sub(r"\s+", " ", text)  # Normalize whitespace
    text = re.sub(r"[^a-zA-Z0-9\s,.?!]", "", text)  # Remove unwanted characters
    return text.strip()

# Function to extract tables using Tabula
def extract_tables_tabula(file_path, output_folder="tables"):
    """
    Extract tables from a PDF using Tabula and save them as CSV files.
    """
    try:
        os.makedirs(output_folder, exist_ok=True)
        tables = tabula.read_pdf(file_path, pages="all", multiple_tables=True)
        for i, table in enumerate(tables):
            table.to_csv(f"{output_folder}/table_{i + 1}.csv", index=False)
        print(f"Extracted {len(tables)} tables to {output_folder}/")
    except Exception as e:
        print(f"Error extracting tables using Tabula: {e}")

# Function to summarize text using Sumy
def summarize_text(text, num_sentences=5):
    """
    Summarize the text using Sumy's LSA Summarizer.
    """
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, num_sentences)
        return " ".join(str(sentence) for sentence in summary)
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return "Summary could not be generated."

# Function to extract keywords
def extract_keywords(text):
    """
    Extract keywords from the text using RAKE (Rapid Automatic Keyword Extraction).
    """
    rake = Rake()
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()

# Function to analyze sentiment
def analyze_sentiment(text):
    """
    Perform sentiment analysis on the text using TextBlob.
    """
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Returns a float: -1 (negative) to +1 (positive)

# Function to count words
def word_count(text):
    """
    Count the occurrences of each word in the text.
    """
    words = text.split()
    return Counter(words)

# Function to save results to a file
def save_results_to_file(data, file_path):
    """
    Save the processed data (e.g., summary, keywords) to a file.
    """
    with open(file_path, "w") as file:
        file.write(data)

# Main function to process the PDF
def process_pdf(file_path, output_text_file="output.txt", table_output_folder="tables"):
    """
    Full pipeline: Extract text, clean it, extract tables, and perform additional text processing.
    """
    print("Starting PDF processing...")

    # Extract and clean text
    raw_text = extract_text_from_pdf(file_path)
    cleaned_text = clean_text(raw_text)

    # Save cleaned text
    with open(output_text_file, "w") as file:
        file.write(cleaned_text)
    print(f"Cleaned text saved to {output_text_file}")

    # Extract tables using Tabula
    extract_tables_tabula(file_path, table_output_folder)

    # Perform additional processing
    print("Performing additional text processing...")
    summary = summarize_text(cleaned_text)
    keywords = extract_keywords(cleaned_text)
    sentiment = analyze_sentiment(cleaned_text)
    word_frequencies = word_count(cleaned_text)

    # Save additional results
    save_results_to_file(summary, r"D:\\self study\\python\\PDFProcess\\summary.txt")
    save_results_to_file(", ".join(keywords), r"D:\\self study\\python\\PDFProcess\\keywords.txt")
    save_results_to_file(str(word_frequencies), r"D:\\self study\\python\\PDFProcess\\word_frequencies.txt")
    print(f"Sentiment Polarity: {sentiment}")
    print("PDF processing completed.")

# File path for the PDF
file_path = r"D:\self study\python\PDFProcess\RawPDF.pdf"
output_text_file = r"D:\self study\python\PDFProcess\cleaned_output.txt"
table_output_folder = r"D:\self study\python\PDFProcess\tables"

# Run the process
process_pdf(file_path, output_text_file, table_output_folder)
