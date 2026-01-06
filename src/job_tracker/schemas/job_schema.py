from pydantic import BaseModel, Field, model_validator
from typing import List, Optional

class SalarySchema(BaseModel):
    displayed: bool = Field(
        default=False,
        description="wheter salary information is explicitly mentioned"
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
    def validate_range(self):
        if self.min is not None and self.max is not None:
            if self.min > self.max:
                raise ValueError("salary.min cannot be greater then salary.max")
            return self
        
    
class JobSchema(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    employment_type: Optional[str] = None
    work_mode: Optional[str] = None
    experience_required: Optional[str] = None
    education_required: Optional[str] = None
    posted_at: Optional[str] = None
    updated_at: Optional[str] = None
    salary: SalarySchema = Field(default_factory=SalarySchema)
    skills: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    requirements: List[str] = Field(default_factory=list)

class CompanySchema(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    employee_size: Optional[str] = None
    address: Optional[str] = None
    about: Optional[str] = None

class RecruiterSchema(BaseModel):
    name: Optional[str] = None
    initials: Optional[str] = None
    last_active: Optional[str] = None

class SourceSchema(BaseModel):
    paltform: Optional[str] = None
    language: Optional[str] = None

class JobDocumentSchema(BaseModel):
    job: JobSchema
    company: CompanySchema
    recruiter: RecruiterSchema
    source: SourceSchema