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
Step-by-Step Workflow (Summary)

1. Text Extraction: PDF content is extracted using PyMuPDF, ensuring accurate parsing of structured and unstructured data.

2. Sentence Segmentation: The extracted text is segmented into logical sentences using spaCy and Sentencier, preparing it for effective chunking.

3. Embedding: Sentence chunks are transformed into dense vector representations using pre-trained SentenceTransformer models.

4. Vector Storage: These embeddings are stored in a Qdrant vector database for fast similarity search and retrieval.

5. Top-K Retrieval: At classification time, a query is embedded and matched against stored vectors to retrieve the top-k most relevant sentence chunks.

6. LLM Classification: The retrieved content is provided as context to a Large Language Model (e.g., ChatGPT or Groq), which identifies the type of document.
---

## Future Improvements
- Metadata filtering (e.g., filename, page number)
- Multi-label classification support
- Fine-tuning a classification model on labeled chunks

---

