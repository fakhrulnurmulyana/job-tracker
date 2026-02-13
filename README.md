# Job Tracker

Job Tracker is a **Python-based backend application** that transforms unstructured job vacancy text into **validated, structured JSON** using **Google Gemini**.

This project demonstrates:

* Production-oriented backend design
* Clean architecture principles
* Strong separation of concerns
* Practical LLM integration for real-world data workflows

> ⚠️ **Project Status**: Active development.
> Current version: **v2.0.0**

---

# What's New in v2.0.0

This version introduces significant architectural improvements and new features:

## Architectural Improvements

* Refactored folder structure with clearer separation of responsibilities
* Dedicated **pipeline module** for orchestration logic
* Entry point fully decoupled from business logic
* Added additional **type hints** for better readability and maintainability
* Introduced **abstract methods / interfaces** to improve testability
* Improved modularization between:

  * domain logic
  * infrastructure
  * persistence
  * services
  * prompts

This makes the system more:

* Testable
* Extensible
* Maintainable
* Replaceable (LLM provider, storage, UI layer)

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

## 2. HTML Input Support (NEW)

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

# Project Structure (v2.0.0)

```
JOB_TRACKER/
│
├── data/                      # Runtime data (generated files, exports, etc.)
├── logs/                      # Application logs
│
├── src/
│   └── job_tracker/
│       │
│       ├── core/              # Pure business logic (domain layer)
│       │   ├── job_normalizer.py
│       │   └── text_cleaner.py
│       │
│       ├── schemas/           # Data contracts / validation models
│       │   └── job_schema.py
│       │
│       ├── services/          # Application services
│       │   ├── job_pipeline_services.py
│       │   └── gemini_client.py
│       │
│       ├── infrastructure/    # Technical implementations
│       │   ├── cli.py
│       │   ├── editor.py
│       │   ├── file_naming.py
│       │   ├── file_splitter.py
│       │   ├── files_handler.py
│       │   ├── loading.py
│       │   └── path.py
│       │
│       ├── persistence/       # Data storage logic
│       │   └── job_document.py
│       │
│       ├── prompts/           # LLM prompt templates
│       │   └── job_normalization.py
│       │
│       ├── logging_config.py
│       ├── settings.py
│       └── main.py
│
├── tests/
│
├── .env
├── .env.example
├── .env.test
├── .gitignore
├── README.md
└── requirements.txt
```

---

# Architecture Principles

This project follows:

* Single Responsibility Principle (SRP)
* Dependency Inversion Principle (DIP)
* Explicit dependency flow
* Clear separation between:

  * Domain
  * Application
  * Infrastructure
  * Persistence

## Pipeline-Oriented Flow

The orchestration logic is now isolated into a dedicated pipeline layer.

`main.py`:

* Only handles entry point
* Delegates execution to pipeline service

Pipeline:

* Coordinates:

  * File handling
  * HTML cleaning
  * Job splitting
  * LLM normalization
  * Validation
  * Persistence

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

# Application Flow (v2.0.0)

1. User provides file name
2. Local editor opens
3. User inputs:

   * Plain text OR
   * Raw HTML OR
   * Multiple jobs separated by `==JOB==`
4. System:

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

The architecture is intentionally designed to scale without requiring major structural changes as the system evolves.