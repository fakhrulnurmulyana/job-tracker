import logging

from typing import List
# Module-level logger for prompt generation
logger = logging.getLogger(__name__)

def _build_job_normalization_prompt(raw_text: str) -> str:
    """
    Build a deterministic prompt for extracting and normalizing
    job vacancy data into a strictly valid JSON structure.

    The prompt enforces strict rules for:
      - Salary normalization
      - Experience extraction
      - Requirements extraction and atomicity
      - Requirement priority, level, and category
      - Riba detection
      - Enum constraints for job and application fields

    Args:
        raw_text (str): Raw job vacancy text to be normalized.

    Returns:
        str: Formatted LLM prompt ready for job normalization.

    Notes:
        This is a private helper function and intended to be called
        either individually or as part of a batch prompt generator.
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

ENUM CONSTRAINTS:
- requirement.level: beginner, intermediate, advanced, null
- requirement.priority: must_have, nice_to_have, null
- requirement.category:
  technical_skill, soft_skill, education, experience, certification, other
- employment_type:
  full_time, part_time, contract, internship, freelance
- work_mode:
  on_site, remote, hybrid
- application.current_status AND application.timeline.status:
  applied, interview, offered, rejected, unknown
- job.category:
  ai engineer, ml engineer, data analyst, data engineer, odoo developer, python developer, data_scientist, other.
- job.education_required.min_education and  job.education_required.max_education:
  "high_school", "diploma", "bachelor_degree", "master_degree", "doctoral_degree",

COMPANY NORMALIZATION RULES:
- Company names must contain only lowercase letters and spaces.
- Remove company prefixes such as: pt, cv, inc, ltd, corp, co., tbk.
- Do not include numbers in company names.

COMPANY ADDRESS EXTRACTION RULES:
- Extract the company address into a structured object under "address".
- Always preserve the original address text in "full_address".
- Extract the following fields when they are explicitly mentioned:
  - "street"
  - "village"
  - "district"
  - "city"
  - "province"
  - "postal_code"
- Use Indonesian administrative hierarchy when identifying locations:
  - "village" refers to "kelurahan" or "desa".
  - "district" refers to "kecamatan".
  - "city" refers to "kota" or "kabupaten".
  - "province" refers to "provinsi".
- Keep location names exactly as written in the source text.
- Do NOT translate or modify location names.
- If a component is not explicitly mentioned, set the field to null.
- Do NOT infer, assume, or guess missing address components.
- If no company address is mentioned, set all address fields to null.
- Recognize common abbreviations such as "Jl.", "Kel.", "Kec.", "Kab.", and "Kota".

SALARY NORMALIZATION RULES:
- Salary values MUST represent millions of IDR.
- `min` and `max` MUST be numeric integers only.
- Do NOT include symbols, separators, decimals, or unit letters.
- Always set "unit": "million".
- Always set "currency": "IDR" (must be written in uppercase).
- If a salary range is mentioned, extract both `min` and `max`.
- If only one value is mentioned, set both `min` and `max` to that value.
- If salary is mentioned in another currency, convert it to IDR before normalization.
- If salary is not mentioned, set `min` and `max` to null and `displayed` to false.

EXPERIENCE NORMALIZATION RULES:
- Normalize experience into one of the following categories ONLY:
  - "No experience"
  - "< 1 year"
  - "1-3 years"
  - "3-5 years"
  - "> 5 years"
- If experience is explicitly mentioned, map it to the closest matching category.
- If a range is mentioned (e.g., 2-4 years), choose the category that best represents the range.
- If "fresh graduate", "no experience required", or similar wording is mentioned, use "No experience".
- If experience is not explicitly mentioned, return null.
- Do NOT infer or assume experience if it is not clearly stated.
- Do NOT create new categories outside the list above.

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
    "experience_required": null,
    "education_required": {{
      "min_education": null,
      "max_education": null
    }},
    "salary": {{
      "displayed": false,
      "currency": "IDR",
      "unit": "million",
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
    "address": {{
      "full_address": null,
      "street": null,
      "village": null,
      "district": null,
      "city": null,
      "province": null,
      "postal_code": null
    }},
    "about": null
  }},
  "application": {{
    "current_status": "unknown",
    "timeline": [
      {{"status": "unknown", "event_date": null}}
    ]
  }}
}}

INPUT:
{raw_text}
"""
    # Log prompt generation for observability and debugging
    logger.info("Job normalization prompt generated successfully.")
    return prompt

def build_batch_job_normalization_prompt(
      raw_text_list: List[str], 
    ) -> List[str]:
    """
    Generate a batch of job normalization prompts from raw texts.

    Args:
        raw_text_list (List[str]): List of raw job vacancy texts.

    Returns:
        List[str]: List of formatted prompts for each raw text.

    Notes:
        Each prompt is built using `_build_job_normalization_prompt`,
        ensuring consistency and strict JSON schema enforcement.
    """
    logger.debug("Starting batch prompt generation.")

    if not raw_text_list:
        logger.warning("Received empty raw_text_list for prompt generation.")
        return []

    total_items = len(raw_text_list)
    logger.info("Generating normalization prompts for %d items.", total_items)

    prompts: List[str] = []
    
    for raw_text in raw_text_list:
        prompt = _build_job_normalization_prompt(raw_text=raw_text)
        prompts.append(prompt)

    logger.info("Successfully generated %d normalization prompts.", len(prompts))
    logger.debug("Batch prompt generation completed.")
    
    return prompts