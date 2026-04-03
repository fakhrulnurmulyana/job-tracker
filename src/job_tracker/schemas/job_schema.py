from datetime import date
from enum import Enum
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, HttpUrl, model_validator


class RibaSchema(BaseModel):
    """
    Schema representing whether a job involves riba-related activities.

    Attributes:
        is_riba (bool): Whether the job involves riba or not.
        relation (Literal['direct', 'indirect', 'none']): Level of involvement.
        reason (Optional[str]): Explanation why the job is considered riba.
    """
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
        """
        Validate logical consistency between `is_riba`, `relation`, and `reason`.

        Raises:
            ValueError: If combination of fields is inconsistent.
        """
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
    Structured salary information.

    Attributes:
        displayed (bool): Whether salary is explicitly mentioned.
        currency (str): Currency code (ISO 4217), default 'IDR'.
        unit (str): Salary normalization into million, default 'million'.
        min (Optional[int]): Minimum salary.
        max (Optional[int]): Maximum salary.
    """
    displayed: bool = Field(
        default=False,
        description="Whether salary information is explicitly mentioned"
    )
    currency: str = Field(
        default="IDR",
        description="ISO 4217 currency code"
    )
    unit: str = Field(
        default="million",
        description="Salary normalization into million"
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
        """
        Ensure displayed is True if min or max exists,
        and min <= max.
        """
        if self.min is not None or self.max is not None:
            self.displayed = True

        if self.min is not None and self.max is not None:
            if self.min > self.max:
                raise ValueError("salary.min cannot be greater than salary.max")

        return self


class RequirementSchema(BaseModel):
    """
    Structured job requirement.

    Attributes:
        name (Optional[str]): Requirement name (short, atomic, e.g., 'Python').
        category (Optional[Literal[...]): Requirement category.
        level (Optional[Literal['beginner','intermediate','advanced']]): Skill level.
        priority (Optional[Literal['must_have','nice_to_have']]): Importance of requirement.
        years_experience (Optional[int]): Required experience years.
        details (List[str]): Supplementary atomic details (e.g., technologies).
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

class EducationSchema(BaseModel):
    """
    Structured education requirement.

    Attributes:
        min_education (Literal[...]): Minimum required education level.
        max_education (Optional[Literal[...]]): Maximum education level.
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
    max_education: Optional[
        Literal[
            "high_school",
            "diploma",
            "bachelor_degree",
            "master_degree",
            "doctoral_degree",
        ]
    ] = Field(
        default=None,
        description="Maximum required education level"
    )

class JobSchema(BaseModel):
    """
    Core job-related information.

    Attributes:
        link (HttpUrl): Job posting link.
        title (Optional[str]): Job title.
        category (Literal[...]): Job category.
        employment_type (Optional[Literal[...]): Employment type.
        work_mode (Optional[Literal[...]): Work mode.
        education_required (EducationSchema): Structured education requirement.
        posted_at (Optional[str]): Posting date.
        updated_at (Optional[str]): Last update date.
        salary (SalarySchema): Structured salary.
        skills (List[str]): Skills required.
        description (Optional[str]): Full job description.
        requirements (List[RequirementSchema]): List of structured requirements.
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
        "data_scientist", 
        "other",
    ] = Field(default="other")
    employment_type: Optional[
        Literal["full_time", "part_time", "contract", "internship", "freelance"]
    ] = None
    work_mode: Optional[
        Literal["on_site", "remote", "hybrid"]
    ] = None
    experience_required: Literal[
        "No experience",
        "< 1 year",
        "1-3 years",
        "3-5 years",
        "> 5 years",
    ] = Field(default="No experience")
    education_required: EducationSchema = Field(
        default_factory=EducationSchema,
        description="Structured education requirement"
    )
    salary: SalarySchema = Field(default_factory=SalarySchema)
    skills: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    requirements: List[RequirementSchema] = Field(default_factory=list)


class CompanyAddress(BaseModel):
    """
    Structured representation of a company address.

    This model stores both the original address string and its parsed
    administrative components. All fields are optional because
    address extraction may be incomplete depending on the source.

    Attributes:
    full_address (Optional[str]): The original full address text as it appears in the source.
    street (Optional[str]): Street name, building name, or detailed street-level location.
    village (Optional[str]): Village or subdistrict level ("Kelurahan" or "Desa").
    district (Optional[str]): District level administrative area ("Kecamatan").
    city (Optional[str]): City or regency ("Kota" or "Kabupaten").
    province (Optional[str]): Province where the company is located.
    postal_code (Optional[str]): Postal or ZIP code associated with the address.
    """

    full_address: Optional[str] = None
    street: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None

class CompanySchema(BaseModel):
    """
    Company-related metadata extracted from job postings or company profiles.

    This schema captures structured information about the company
    associated with a job listing.

    Attributes:
    name (Optional[str]): Official company name.
    industry (Optional[str]): Industry or sector where the company operates (e.g., Technology, Finance, Healthcare).
    employee_size (Optional[str]): Estimated number of employees in the company (e.g., "11-50", "51-200", "1000+").
    address (Optional[CompanyAddress]): Structured company address containing both the original address string and its parsed administrative components.
    about (Optional[str]): Short description or overview of the company.
    """

    name: Optional[str] = None
    industry: Optional[str] = None
    employee_size: Optional[str] = None
    address: Optional[CompanyAddress] = None
    about: Optional[str] = None


class ApplicationStatus(str, Enum):
    applied = "applied"
    interview = "interview"
    offered = "offered"
    rejected = "rejected"
    unknown = "unknown"


class TimelineEntry(BaseModel):
    """
    Represent one status event in the application timeline.
    """

    status: ApplicationStatus = Field(
        ...,
        description="Application status at a specific time."
    )
    event_date: Optional[date] = Field(
        None,
        description="Date when the status occurred."
    )


class ApplicationSchema(BaseModel):
    """
    Application tracking schema.

    Stores current status and full status timeline.
    """

    current_status: ApplicationStatus = ApplicationStatus.unknown
    timeline: List[TimelineEntry] = Field(
        default_factory=lambda: [
            TimelineEntry(
                status=ApplicationStatus.unknown,
                event_date=None
            )
        ]
    )

    @model_validator(mode="after")
    def validate_current_status_exists(self):
        """
        Ensure current_status exists inside timeline.
        """
        statuses = [entry.status for entry in self.timeline]

        if self.current_status not in statuses:
            raise ValueError(
                "current_status must exist in timeline."
            )

        return self


class JobDocumentSchema(BaseModel):
    riba: RibaSchema = Field(default_factory=lambda: RibaSchema(is_riba=False, relation="none"))
    job: JobSchema = Field(default_factory=lambda: JobSchema(link="https://placeholder.com"))
    company: CompanySchema = Field(default_factory=CompanySchema)
    application: ApplicationSchema = Field(default_factory=ApplicationSchema)