import logging

# Module-level logger for prompt generation
logger = logging.getLogger(__name__)

def build_job_normalization_prompt(raw_text: str) -> str:
    """
    Build a deterministic prompt for extracting and normalizing job vacancy data
    into a strictly valid JSON structure.
    """
    # Use explicit and restrictive instructions to minimize LLM output variance
    prompt =  f"""
Your task is to extract, normalize, and enrich job vacancy information
into a structured JSON object following the schema below.

You may perform light semantic inference ONLY for:
- requirement level
- requirement priority
- riba relation (only if clearly implied)

GENERAL RULES:
- Output MUST be a single valid JSON object
- Do NOT include explanations
- Do NOT wrap output with markdown
- Do NOT add trailing commas
- Do NOT invent data
- Use null if a value is not found
- Always return arrays as empty arrays, never null
- Always return the salary object, never null
- Use English for all values
- Use lowercase letters only for all string values
- If salary min or max is not null, displayed MUST be true

SALARY NORMALIZATION RULES:
- Salary values MUST be numeric integers only
- Do NOT include symbols, separators, or decimals
- Use IDR as currency
- If salary is mentioned in any other currency, convert it to IDR
- If only one value is found, set both min and max to that value
- If salary is not mentioned, set min and max to null and displayed to false

EXPERIENCE NORMALIZATION RULES:
- Experience values MUST be numeric integers (years)
- If a range is mentioned (e.g. 2-4 years), extract min and max
- If only one value is mentioned, set both min_experience and max_experience
- If experience is not mentioned, set both fields to null
- Do NOT infer experience if not explicitly stated

REQUIREMENTS EXTRACTION RULES:
- Extract requirements as structured objects
- Do NOT copy full sentences into requirement.name
- requirement.name MUST be short and atomic (max 3-5 words)
- Each requirement MUST represent only ONE concept
- Always split combined requirements into multiple items
- Always split programming languages, frameworks, tools, and technologies
- Remove examples, explanations, and text inside parentheses
- Do NOT guess technologies or skills not mentioned
- Group only truly identical concepts

ATOMICITY ENFORCEMENT (MANDATORY):
- Parentheses MUST NOT appear in requirement.name
- Commas MUST NOT appear in requirement.name
- Slashes MUST NOT appear in requirement.name
- Lists MUST be split into separate requirement objects

ATOMIC SPLITTING EXAMPLES:
- "bachelor's degree in computer science, mathematics, statistics"
  → name: "bachelor's degree"

- "fluency in programming languages (python, javascript, go)"
  → name: "python"
  → name: "javascript"
  → name: "go"

- "hands-on experience with api frameworks like flask or fastapi"
  → name: "flask"
  → name: "fastapi"

- "experience in machine learning and deep learning"
  → name: "machine learning"
  → name: "deep learning"

REQUIREMENT PRIORITY RULES:
- If explicitly required, mark priority as must_have
- If preferred or optional, mark priority as nice_to_have
- If not specified, use null

REQUIREMENT LEVEL RULES:
- Infer level ONLY if clearly implied
- Use one of: beginner, intermediate, advanced
- Otherwise, use null

REQUIREMENT CATEGORY RULES:
- technical_skill: languages, frameworks, tools, algorithms
- soft_skill: communication, reasoning, collaboration
- education: formal degrees
- experience: general experience statements
- certification: official certifications
- other: anything else

RIBA EXTRACTION RULES:
- Determine whether the job involves riba-related activities
- Set is_riba to true ONLY if involvement is clearly stated or strongly implied
- relation must be one of: direct, indirect, none
- If is_riba is false:
  - relation MUST be "none"
  - reason MUST be null
- If is_riba is true:
  - relation MUST be "direct" or "indirect"
  - reason MUST be provided
- Do NOT assume riba involvement without explicit evidence

ENUM CONSTRAINTS:
- requirement.level: beginner, intermediate, advanced, null
- requirement.priority: must_have, nice_to_have, null
- requirement.category:
  technical_skill, soft_skill, education, experience, certification, other
- employment_type:
  full_time, part_time, contract, internship, freelance
- work_mode:
  on_site, remote, hybrid
- application.status:
  open, applied, interview, offered, rejected, closed, unknown
- job.category:
  ai engineer, ml engineer, data analyst, data engineer, odoo developer, python developer

REQUIREMENT DETAILS RULES:
- Use requirement.details ONLY for supplementary information
- details MUST be an array of short atomic strings
- details MUST NOT repeat requirement.name
- details MUST NOT contain full sentences
- details MUST NOT contain parentheses or explanations
- details MUST be empty if no clear sub-items are mentioned
- details MUST be lowercase

DETAIL EXTRACTION EXAMPLES:
- "bachelor's degree in statistics, mathematics, or computer science"
  → name: "bachelor's degree"
  → details: ["statistics", "mathematics", "computer science"]

- "experience with databases such as mysql and postgresql"
  → name: "databases"
  → details: ["mysql", "postgresql"]

- "api frameworks like flask or fastapi"
  → name: "api frameworks"
  → details: ["flask", "fastapi"]

JSON SCHEMA:
{{
  "riba": {{
    "is_riba": null,
    "relation": null,
    "reason": null
  }},
  "job": {{
    "link": null,
    "title": null,
    "category": null,
    "employment_type": null,
    "work_mode": null,
    "experience_required": {{
      "min_experience": null,
      "max_experience": null
    }},
    "education_required": null,
    "posted_at": null,
    "updated_at": null,
    "salary": {{
      "displayed": false,
      "currency": "IDR",
      "min": null,
      "max": null
    }},
    "skills": [],
    "description": null,
    "requirements": []
  }},
  "company": {{
    "name": null,
    "industry": null,
    "employee_size": null,
    "address": null,
    "about": null
  }},
  "recruiter": {{
    "name": null,
    "initials": null,
    "last_active": null
  }},
  "application": {{
    "status": "unknown",
    "applied_at": null,
    "deadline": null,
    "notes": null
  }},
  "source": {{
    "platform": null,
    "language": null
  }}
}}

INPUT:
{raw_text}
"""
    # Log prompt generation for observability and debugging
    logger.info("Job normalization prompt generated successfully.")
    return prompt