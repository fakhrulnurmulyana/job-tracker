# Job Tracker

Job Tracker is a **Python-based application** that transforms unstructured job vacancy text into **validated, structured JSON** using **Google Gemini**.

This project demonstrates **production-oriented backend design**, **clean architecture principles**, and **practical LLM integration** for real-world data processing workflows.

> ⚠️ **Project Status**: This is an **early-stage / initial version (v1.0.0)**. The core pipeline is stable, but features, data schemas, and integrations are expected to evolve.

---

## Purpose

Version **1.0.0** focuses on:

* Converting unstructured job descriptions into structured machine-readable data
* Providing a solid architectural foundation for future features such as:

  * database persistence
  * search & analytics
  * CV and cover letter generation
  * RAG (Retrieval-Augmented Generation)

---

## Key Features

* Input job descriptions via a local editor
* Normalize and extract structured data using Gemini
* Validate LLM output using a schema
* Persist normalized data as JSON files
* Structured logging (application logs and error logs separated)
* Centralized and explicit configuration handling

---

## Project Structure

```
project-root/
├── data/                   # Data files (input/output, temporary storage)
├── logs/                   # Application log files
├── src/
│   └── job_tracker/        # Main application package
│       ├── core/           # Business logic & domain rules
│       ├── infrastructure/ # External services, API clients, integrations
│       ├── persistence/    # Database access & repositories
│       ├── prompts/        # Prompt templates for LLM
│       ├── schemas/        # Data validation schemas (DTO, Pydantic, etc.)
│       ├── services/       # Application services / use cases
│       ├── logging_config.py
│       ├── settings.py
│       └── main.py
├── tests/                  # Automated tests
│   └── test_gemini_client.py
├── .env                    # Local environment variables
├── .env.example            # Example environment configuration
├── .env.test               # Environment variables for testing
├── .gitignore
├── README.md
└── requirements.txt
```

This structure is based on the following principles:

* Single Responsibility Principle (SRP)
* Dependency Inversion Principle (DIP)
* Clean entry point and explicit application flow

---

## Requirements

* Python **3.10+**
* Google Gemini API key

---

## Configuration

Create a `.env` file at the project root:

```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3-flash-preview
```

All configuration is loaded and validated centrally via `settings.py`.

---

## How to Run

Run the application using the module entry point:

```bash
python -m job_tracker.main
```

### Application Flow

1. The user provides a file name
2. A local editor opens for entering the job description
3. The system reads the file content
4. The text is normalized using Gemini
5. The structured result is validated
6. The final JSON is saved to disk

---

## Logging

The application uses structured logging with a clear separation of concerns:

* `app.log` → normal execution flow and informational logs
* `error.log` → detailed error logs and stack traces

Log files are treated as generated artifacts and are excluded from version control.

---

## Design and Best Practices

* `main.py` contains orchestration logic only
* Business logic is independent of I/O operations
* The LLM client is abstracted for easy testing and substitution
* Configuration and logging do not leak into domain logic

This design enables easier:

* testing
* refactoring
* scaling
* replacement of LLM providers or storage backends

---

## Main Dependencies

* `google-genai`
* `pydantic`
* `python-dotenv`

---

## Roadmap (High Level)

Planned future improvements:

* Database-backed persistence layer
* REST API interface
* Web-based UI
* RAG with vector database
* CV & cover letter generation module
* Advanced schema versioning

---

## License

MIT License

---

## Notes

This project is intended as a:

* serious personal project
* internal tooling example
* backend / data / AI engineering portfolio piece

The architecture and documentation are intentionally designed to scale without requiring major structural changes as the project grows.