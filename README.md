# Job Tracker

Job Tracker is a **Python-based application** that transforms unstructured job vacancy text into **validated structured JSON** using **Google Gemini**.
This project demonstrates production-oriented backend design, clean architecture principles, and practical LLM integration for real-world data processing workflows.

---

## Purpose

- Version 1.0.0 = Transform unstructured job descriptions into structured data

---

## Key Features

- Input job descriptions via a local editor
- Normalize and extract structured data using Gemini
- Validate LLM output using a schema
- Persist normalized data as JSON files
- Structured logging (application logs and error logs separated)
- Centralized and explicit configuration handling

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

- Single Responsibility Principle
- Dependency Inversion
- Clean Entry Point

---

## Requirements

- Python 3.10 or newer
- Google Gemini API key

---

## Configuration

Create a `.env` file at the project root:

```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3-flash-preview
```

Configuration is loaded and validated centrally via `settings.py`.

---

## How to Run

Run the application using the module entry point:

```bash
python -m job_tracker.main
```

Application flow:

1. The user provides a file name
2. A local editor opens for entering the job description
3. The system reads the file content
4. The text is normalized using Gemini
5. The structured result is saved as a JSON file

---

## Logging

The application uses structured logging with a clear separation of concerns:

- `app.log` → normal execution flow and informational logs
- `error.log` → detailed error logs and stack traces

Log files are generated artifacts and are excluded from version control.

---

## Design and Best Practices

- `main.py` contains orchestration logic only
- Business logic is independent of I/O operations
- The LLM client is abstracted to enable easy testing and substitution
- Configuration and logging do not leak into core logic

This design enables easier:

- testing
- refactoring
- replacement of LLM providers or storage backends

---

## Main Dependencies

- google-genai
- pydantic
- python-dotenv

---

## License

MIT License

---

## Notes

This project is intended as a:

- serious personal project
- internal tooling example
- backend / data / AI engineering portfolio piece

The architecture and documentation are intentionally designed to scale without requiring major structural changes.
