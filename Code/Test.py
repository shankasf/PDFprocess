from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

text = """
Sumy is a library for automatic summarization of text documents and webpages.
It supports several summarization algorithms such as LexRank, TextRank, and LSA.
You can also use it with NLTK for natural language processing.
"""

# Parse the text
parser = PlaintextParser.from_string(text, Tokenizer("english"))

# Use LSA summarizer
summarizer = LsaSummarizer()
summary = summarizer(parser.document, 2)  # Summarize into 2 sentences

# Print the summary
for sentence in summary:
    print(sentence)
