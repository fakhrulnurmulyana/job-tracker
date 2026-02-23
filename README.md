# Job Tracker

Job Tracker is a **Python-based backend application** that transforms unstructured job vacancy text into **validated, structured JSON** using **Google Gemini**.

This project demonstrates:

* Production-oriented backend design
* Clean architecture principles
* Strong separation of concerns
* Practical LLM integration for real-world data workflows

> ⚠️ **Project Status**: Active development  
> Current version: **v3.0.0**

---

# What's New in v3.0.0

This release introduces a simplified user workflow and improvements to file handling and pipeline execution.

## Changes

- Input filenames are now generated automatically based on execution time.
- Improved file organization under `finalized_data/`.
- Added validation for company and job position names.
- Refactored pipeline to operate on validated variables instead of repeated file reads.
- Simplified saving workflow and removed unnecessary intermediate outputs.
- General refactoring, cleanup, and documentation improvements.

---

# Previous Updates (v2.1.1)

This version introduced improvements focused on output consistency and developer experience:

- Improved output naming consistency
- Minor internal refinements and cleanup

# Purpose

Job Tracker aims to:

* Convert unstructured job descriptions into structured machine-readable JSON
* Provide a scalable foundation for:

  * database persistence
  * search & analytics
  * CV & cover letter generation
  * RAG (Retrieval-Augmented Generation)
  * automated scraping from job portals

---

# Key Features

## 1. Multi-Job Input (NEW)

Previously:

* 1 file = 1 job

Now:

* 1 file can contain **multiple jobs**
* Jobs are separated using:

```
==JOB==
```

Example:

```
Frontend Developer - Jakarta
Requirements: ...

==JOB==

Data Engineer - Remote
Requirements: ...
```

The system will:

* Split jobs automatically
* Process each job independently
* Generate structured JSON output per job

---

## 2. HTML Input Support

Some job portals prevent direct copy-paste of clean text.

You can now:

* Paste raw HTML (e.g., from browser Inspect Element)
* The system automatically:

  * Cleans HTML
  * Extracts readable text
  * Normalizes it using Gemini

This prepares the project for future evolution into:

* URL-based input
* Automated scraping pipeline
* Fully automated job ingestion system

---

## 3. Structured Data Normalization

* Uses **Google Gemini**
* Converts unstructured job text into validated schema
* Schema validation via `pydantic`
* Strict output validation before persistence

---

## 4. Clean Logging

* `app.log` → execution flow
* `error.log` → stack traces & detailed failures

Logs are excluded from version control.

---

# Project Structure (v2.1.0)

```
JOB-TRACKER
│
├── data/
├── logs/
│
├── src/
│   └── job_tracker/
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── job_normalizer.py
│       │   ├── job_validator.py
│       │   ├── llm_client.py
│       │   └── text_cleaner.py
│       │
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   ├── editor.py
│       │   ├── file_naming.py
│       │   ├── file_splitter.py
│       │   ├── files_handler.py
│       │   ├── job_document_saver.py
│       │   ├── loading.py
│       │   └── path.py
│       │
│       ├── prompts/
│       │   ├── __init__.py
│       │   └── job_normalization.py
│       │
│       ├── schemas/
│       │   ├── __init__.py
│       │   └── job_schema.py
│       │
│       └── services/
│           │
│           ├── interface/
│           │   ├── __init__.py
│           │   ├── editor_launcer.py
│           │   ├── file_handler.py
│           │   ├── file_split.py
│           │   ├── job_document_sever.py
│           │   ├── job_normalizer.py
│           │   └── path_resolver.py
│           │
│           ├── __init__.py
│           ├── gemini_client.py
│           ├── job_pipeline_services.py
│           ├── job_processor.py
│           ├── logging_config.py
│           ├── main.py
│           └── settings.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```
---

# Requirements

* Python 3.10+
* Google Gemini API key

---

# Configuration

Create `.env` at project root:

```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3-flash-preview
```

All configuration is centrally managed in `settings.py`.

---

# How to Run

Set PYTHONPATH:

```bash
set PYTHONPATH=src
```

Run:

```bash
python -m job_tracker.main
```

---

# Application Flow (v2.1.0)

1. Local editor opens
2. User inputs:

   * Plain text OR
   * Raw HTML OR
   * Multiple jobs separated by `==JOB==`
3. System:

   * Splits jobs
   * Cleans HTML
   * Normalizes each job via Gemini
   * Validates schema
   * Saves structured JSON output

---

# Main Dependencies

* `google-genai`
* `pydantic`
* `python-dotenv`
* `beautifulsoup4` (for HTML parsing)

---

# Roadmap

Planned improvements:

* Database-backed persistence
* REST API interface
* Web UI
* Vector database integration (RAG)
* Automatic URL ingestion
* Schema versioning strategy
* Pluggable LLM providers

---

# License

MIT License

---

# Notes

This project serves as:

* A serious personal backend/AI engineering project
* Internal tooling
* Portfolio-grade clean architecture implementation
* LLM-integrated data processing pipeline