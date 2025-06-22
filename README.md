# centr-seek-revised

This project is an extension of a Faculty Assistance in Data Science (FADS) project, CEnTR*SEEK, and will explore and identify approaches to three critical questions/tasks that are foundational for a machine learning-based approach:

  1. How can unstructured texts from diverse sources be processed to create optimal input data for machine learning algorithms in the context of community engaged research projects?
  2. Which machine learning classification techniques provide the best balance between accuracy and interpretability for categorizing community engaged research projects?
  3. What database schema and data storage strategies best facilitate the interoperability, transparency, and scalability of community engaged research project attributes?

By exploring these questions, efforts for identifying and categorizing community engaged and public scholarship will be enhanced.


# Approach:
## Overview
This project implements a PDF classification pipeline using a Retrieval-Augmented Generation (RAG) approach. The process involves:
- Extracting and preprocessing text from PDF documents
- Chunking and embedding sentence data
- Storing and retrieving vectors using Qdrant
- Classifying document type using a Large Language Model (LLM) like ChatGPT or Groq

---

## Libraries and Tools Used

| Tool               | Purpose                                           |
|--------------------|---------------------------------------------------|
| PyMuPDF            | PDF text extraction                              |
| spaCy + Sentencier | Sentence segmentation and chunking               |
| SentenceTransformers | Embedding sentence chunks using transformer models |
| Qdrant             | Vector storage and retrieval                     |
| OpenAI GPT / Groq  | Final document classification using LLM         |

---

## Pipeline Architecture

```mermaid
graph LR
A[PDF Upload] --> B[Text Extraction (PyMuPDF)]
B --> C[Sentence Segmentation (spaCy + Sentencier)]
C --> D[Chunking & Embedding (SentenceTransformers)]
D --> E[Vector Storage (Qdrant)]

F[Classification Request] --> G[Query Embedding + Top-K Retrieval]
G --> H[Relevant Chunks]
H --> I[LLM Classification (ChatGPT/Groq)]
```

---

## Project Structure

```
pdf_classification_rag/
|
├── extract_text.py           # PDF text extraction
├── chunk_sentences.py        # Sentence segmentation and chunking
├── vector_store.py           # Embedding and Qdrant integration
├── classify_document.py      # RAG-based classification via LLM
├── config.py                 # Configuration for Qdrant, model, etc.
└── utils.py                  # Helper functions
```

---

## Step-by-Step Workflow

### 1. Extract Text from PDF
```python
import fitz  # PyMuPDF

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)
```

### 2. Sentence Segmentation and Chunking
```python
import spacy
from spacy_sentencizer import SpacySentencizer

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("sentencizer")

def segment_sentences(text):
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 0]
```

### 3. Embedding and Storing in Qdrant
```python
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(host="localhost", port=6333)

def embed_and_store(sentences, collection_name="pdf_chunks"):
    vectors = model.encode(sentences)
    points = [PointStruct(id=i, vector=vec, payload={"text": sent})
              for i, (vec, sent) in enumerate(zip(vectors, sentences))]
    client.upsert(collection_name=collection_name, points=points)
```

### 4. Top-K Retrieval from Qdrant
```python
def retrieve_top_k(query, k=5):
    query_vector = model.encode([query])[0]
    search_result = client.search(
        collection_name="pdf_chunks",
        query_vector=query_vector,
        limit=k
    )
    return [hit.payload["text"] for hit in search_result]
```

### 5. LLM-based Classification
```python
import openai  # or use Groq API
openai.api_key = "your-api-key"

def classify_with_llm(query, retrieved_chunks):
    context = "\n".join(retrieved_chunks)
    prompt = f"""You are a document classification assistant. Given the following content:\n\n{context}\n\nClassify the type of document (e.g., invoice, report, contract, etc.):"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"].strip()
```

---

## Example Usage
```python
pdf_text = extract_text("sample.pdf")
sentences = segment_sentences(pdf_text)
embed_and_store(sentences)

retrieved = retrieve_top_k("What is this document about?")
classification = classify_with_llm("Classify this document", retrieved)

print("Predicted Document Type:", classification)
```

---

## Configuration Tips
- Use Docker for local Qdrant setup
- Ensure consistent vector dimension across embedding and Qdrant
- Choose between OpenAI or Groq depending on latency and cost

---

## Future Improvements
- Metadata filtering (e.g., filename, page number)
- Multi-label classification support
- Fine-tuning a classification model on labeled chunks

---

## License
MIT

---

## Author
Kirthivasan PN

