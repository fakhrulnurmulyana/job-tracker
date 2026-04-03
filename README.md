# Job Tracker

Job Tracker is a **Python-based backend application** that transforms unstructured job vacancy text into **validated, structured JSON** using **Google Gemini**.

This project demonstrates:

* Production-oriented backend design
* Clean architecture principles
* Strong separation of concerns
* Practical LLM integration for real-world data workflows

> ⚠️ **Project Status**: Active development  
> Current version: **v4.0.0**
---
# What's New in v4.0.0
This release introduces a major overhaul to the user input workflow, replacing manual HTML inspection with a simpler link-based input system.
## Changes
- User input method changed from plain text/HTML (via inspect) to direct URL input (single or multiple links).
- Added web scraping system to automatically extract data from provided links.
- Output data structure and content updated to reflect the new scraping-based pipeline.
- Temporarily removed data cleaning step due to inconsistent results from scraped output.
---
# Previous Updates (v3.0.0)
This version introduced a simplified user workflow and improvements to file handling and pipeline execution:
- Input filenames are now generated automatically based on execution time.
- Improved file organization under `finalized_data/`.
- Added validation for company and job position names.
- Refactored pipeline to operate on validated variables instead of repeated file reads.
- Simplified saving workflow and removed unnecessary intermediate outputs.
- General refactoring, cleanup, and documentation improvements.
--- 

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
Now:

* Just input link or multiple links.
* Links are separated using space.

Example:

```
https://job_tranker.com https://job_tranker.com https://job_tranker.com
```

The system will:

* Split jobs automatically
* Process each job independently
* Generate structured JSON output per job

---

## 2. HTML Input Support

You can now:

* Paste just link or links.
* The system automatically:

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
├── data/
├── logs/
├── src/
│   └── job_tracker/
│       ├── core/
│       │   ├── interface/
│       │   ├── __init__.py
│       │   ├── job_normalizer.py
│       │   ├── job_validator.py
│       │   ├── text_cleaner.py
│       │   └── text_parser.py
│       │
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   ├── editor.py
│       │   ├── file_naming.py
│       │   ├── files_handler.py
│       │   ├── job_document_saver.py
│       │   ├── link_splitter.py
│       │   ├── loading.py
│       │   ├── path.py
│       │   └── scraper.py
│       │
│       ├── orchestration/
│       │   ├── interface/
│       │   ├── __init__.py
│       │   ├── distribution_chart.py
│       │   ├── job_pipeline_services.py
│       │   └── job_processor.py
│       │
│       ├── prompts/
│       │   ├── __init__.py
│       │   └── job_normalization.py
│       │
│       ├── schemas/
│       │   ├── __init__.py
│       │   └── job_schema.py
│       │
│       ├── services/
│       │   ├── __init__.py
│       │   └── gemini_client.py
│       │
│       └── visualization/
│           ├── __init__.py
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

   * link.
   * Multiple links separated by space.

3. System:

   * Splits links.
   * scrap html.
   * Normalizes each job via Gemini
   * Validates schema
   * Saves structured JSON output

---

# Main Dependencies

* `google-genai`
* `pydantic`
* `python-dotenv`
* `beautifulsoup4` (for HTML parsing)
* requests
* undetected-chromedriver

---

# Roadmap

Planned improvements:

* Database-backed persistence
* REST API interface
* Web UI
* Vector database integration (RAG)
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