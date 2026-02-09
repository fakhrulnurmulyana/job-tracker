from typing import List, Optional, Literal
from pydantic import BaseModel, Field, HttpUrl, model_validator


class RibaSchema(BaseModel):
    is_riba: bool = Field(
        description="Whether the job involves riba or not"
    )
    relation: Literal["direct", "indirect", "none"] = Field(
        description="Level of involvement with riba"
    )
    reason: Optional[str] = Field(
        default=None,
        description="Reason why the job is considered riba"
    )

    @model_validator(mode="after")
    def validate_riba_logic(self):
        if self.is_riba:
            if not self.reason:
                raise ValueError("reason must be provided when is_riba is true")
            if self.relation == "none":
                raise ValueError("relation cannot be 'none' when is_riba is true")
        else:
            if self.reason is not None:
                raise ValueError("reason must be empty when is_riba is false")
            if self.relation != "none":
                raise ValueError("relation must be 'none' when is_riba is false")

        return self

class SalarySchema(BaseModel):
    """
    Structured salary information with validation rules
    aligned with LLM normalization constraints.
    """
    displayed: bool = Field(
        default=False,
        description="Whether salary information is explicitly mentioned"
    )
    currency: str = Field(
        default="IDR",
        description="ISO 4217 currency code"
    )
    min: Optional[int] = Field(
        default=None,
        description="Minimum salary in integer (IDR)"
    )
    max: Optional[int] = Field(
        default=None,
        description="Maximum salary in integer (IDR)"
    )

    @model_validator(mode="after")
    def validate_salary(self):
        if self.min is not None or self.max is not None:
            self.displayed = True

        if self.min is not None and self.max is not None:
            if self.min > self.max:
                raise ValueError("salary.min cannot be greater than salary.max")

        return self


class RequirementSchema(BaseModel):
    """
    Structured job requirement with semantic enrichment.
    """
    name: Optional[str] = Field(
        default=None,
        description="Requirement name (e.g. Python, Communication)"
    )
    category: Optional[
        Literal[
            "technical_skill",
            "soft_skill",
            "education",
            "experience",
            "certification",
            "other"
        ]
    ] = None
    level: Optional[
        Literal["beginner", "intermediate", "advanced"]
    ] = None
    priority: Optional[
        Literal["must_have", "nice_to_have"]
    ] = None
    years_experience: Optional[int] = Field(
        default=None,
        description="Years of experience required"
    )
    details: List[str] = Field(
        default_factory=list,
        description="Optional detailed sub-items related to the requirement"
    )

class ExperienceSchema(BaseModel):
    """
    Structured experience requirement in years.
    """
    min_experience: Optional[int] = Field(
        default=None,
        description="Minimum required experience in years"
    )
    max_experience: Optional[int] = Field(
        default=None,
        description="Maximum required experience in years"
    )

class EducationSchema(BaseModel):
    """
    Structured experience requirement in years.
    """
    min_education: Literal[
        "high_school",
        "diploma",
        "bachelor_degree",
        "master_degree",
        "doctoral_degree",
    ] = Field(
        default=None,
        description="Minimum required education in years"
    )
    max_education: Literal[
        "high_school",
        "diploma",
        "bachelor_degree",
        "master_degree",
        "doctoral_degree",
    ] = Field(
        default=None,
        description="Maximum required education in years"
    )

class JobSchema(BaseModel):
    """
    Core job-related information.
    """
    link: HttpUrl
    title: Optional[str] = None
    category: Literal[
        "ai engineer", 
        "ml engineer", 
        "data analyst", 
        "data engineer", 
        "odoo developer", 
        "python developer",
    ] = Field(default="unknown")
    employment_type: Optional[
        Literal["full_time", "part_time", "contract", "internship", "freelance"]
    ] = None
    work_mode: Optional[
        Literal["on_site", "remote", "hybrid"]
    ] = None
    experience_required: ExperienceSchema = Field(
        default_factory=ExperienceSchema,
        description="Structured experience requirement"
    )
    education_required: EducationSchema = Field(
        default_factory=EducationSchema,
        description="Structured education requirement"
    )
    posted_at: Optional[str] = None
    updated_at: Optional[str] = None
    salary: SalarySchema = Field(default_factory=SalarySchema)
    skills: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    requirements: List[RequirementSchema] = Field(default_factory=list)


class CompanySchema(BaseModel):
    """
    Company-related metadata.
    """
    name: Optional[str] = None
    industry: Optional[str] = None
    employee_size: Optional[str] = None
    address: Optional[str] = None
    about: Optional[str] = None


class RecruiterSchema(BaseModel):
    """
    Recruiter or hiring contact.
    """
    name: Optional[str] = None
    initials: Optional[str] = None
    last_active: Optional[str] = None


class ApplicationSchema(BaseModel):
    """
    Application lifecycle metadata.
    """
    status: Literal[
        "open",
        "applied",
        "interview",
        "offered",
        "rejected",
        "closed",
        "unknown"
    ] = Field(default="unknown")
    applied_at: Optional[str] = None
    deadline: Optional[str] = None
    notes: Optional[str] = None


class SourceSchema(BaseModel):
    """
    Source metadata of the job posting.
    """
    platform: Optional[str] = None
    language: Optional[str] = None


class JobDocumentSchema(BaseModel):
    """
    Aggregated normalized job document (schema v2).
    """
    riba: RibaSchema
    job: JobSchema
    company: CompanySchema
    recruiter: RecruiterSchema
    application: ApplicationSchema
    source: SourceSchema