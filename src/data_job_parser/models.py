from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ExperienceLevel(str, Enum):
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"


class WorkType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    INTERNSHIP = "internship"


class WorkMode(str, Enum):
    ONSITE = "onsite"
    REMOTE = "remote"
    HYBRID = "hybrid"


class Role(str, Enum):
    DATA_ENGINEER = "Data Engineer"
    SOFTWARE_ENGINEER = "Software Engineer"
    DATA_SCIENTIST = "Data Scientist"
    MACHINE_LEARNING_ENGINEER = "Machine Learning Engineer"
    DEVOPS_ENGINEER = "DevOps Engineer"
    FRONTEND_DEVELOPER = "Frontend Developer"
    BACKEND_DEVELOPER = "Backend Developer"
    FULLSTACK_DEVELOPER = "Fullstack Developer"
    PRODUCT_MANAGER = "Product Manager"
    SCRUM_MASTER = "Scrum Master"
    QA_ENGINEER = "QA Engineer"
    OTHER = "Other"


class Salary(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )  # equivalent to additionalProperties: false

    min_amount: Optional[float] = Field(
        None, description="Minimum salary amount (numeric, e.g. 50000)"
    )
    max_amount: Optional[float] = Field(
        None, description="Maximum salary amount (numeric, e.g. 70000)"
    )
    currency: Optional[str] = Field(
        None, description="Currency code (e.g., USD, EUR, GBP)"
    )
    period: Optional[str] = Field(
        None, description="Salary period (e.g., yearly, monthly)"
    )
    raw_text: Optional[str] = Field(
        None, description="Raw salary text as found in the posting"
    )
    reason: Optional[str] = Field(
        None, description="Reason why salary could not be extracted, if applicable"
    )


class Location(BaseModel):
    model_config = ConfigDict(extra="forbid")  # Keep strict validation

    city: Optional[str] = Field(None, description="City name")
    state: Optional[str] = Field(None, description="State or province")
    country: Optional[str] = Field(None, description="Country name")
    is_remote: bool = Field(False, description="Whether the position is remote")
    multiple_locations: List[str] = Field(
        default_factory=list,
        description="List of possible locations (if more than one)",
    )
    reason: Optional[str] = Field(
        None, description="Reason why location could not be extracted, if applicable"
    )


class JobPosting(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Required fields
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: Optional[Location] = Field(None, description="Job location details")
    location_reason: Optional[str] = Field(
        None, description="Reason why location could not be extracted, if applicable"
    )
    description: str = Field(..., description="Full job description")

    # Highly relevant structured fields
    responsibilities: List[str] = Field(
        default_factory=list, description="Key responsibilities"
    )
    responsibilities_reason: Optional[str] = Field(
        None,
        description="Reason why responsibilities could not be extracted, if applicable",
    )
    requirements: List[str] = Field(
        default_factory=list, description="Job requirements"
    )
    requirements_reason: Optional[str] = Field(
        None,
        description="Reason why requirements could not be extracted, if applicable",
    )
    benefits: List[str] = Field(default_factory=list, description="Benefits and perks")
    benefits_reason: Optional[str] = Field(
        None, description="Reason why benefits could not be extracted, if applicable"
    )

    # Nuovi campi richiesti
    tech_stack: List[str] = Field(
        default_factory=list,
        description="List of main technologies, frameworks, or programming languages mentioned in the job posting (e.g. Python, AWS, Docker, React, etc.)",
    )
    tech_stack_reason: Optional[str] = Field(
        None, description="Reason why tech stack could not be extracted, if applicable"
    )
    role: Optional[Role] = Field(
        None, description="Main job role, chosen from a predefined list of roles"
    )
    role_reason: Optional[str] = Field(
        None, description="Reason why role could not be determined, if applicable"
    )

    # Optional fields with enums
    experience_level: Optional[ExperienceLevel] = Field(
        None, description="Required experience level"
    )
    work_type: Optional[WorkType] = Field(None, description="Type of employment")
    work_mode: Optional[WorkMode] = Field(
        None, description="Work mode (onsite/remote/hybrid)"
    )

    # Optional nested objects
    salary: Optional[Salary] = Field(None, description="Salary information")
    salary_reason: Optional[str] = Field(
        None, description="Reason why salary could not be extracted, if applicable"
    )

    # Optional lists
    required_skills: List[str] = Field(
        default_factory=list, description="Required technical skills"
    )
    preferred_skills: List[str] = Field(
        default_factory=list, description="Nice-to-have skills"
    )

    # Other optional fields
    years_of_experience: Optional[int] = Field(
        None, description="Minimum years of experience required"
    )
    education_requirements: Optional[str] = Field(
        None, description="Education requirements"
    )
    department: Optional[str] = Field(None, description="Department name")
    team_size: Optional[str] = Field(None, description="Team size information")
    application_deadline: Optional[str] = Field(
        None, description="Application deadline (ISO format preferred)"
    )
    posted_date: Optional[str] = Field(
        None, description="Date when the job was posted (ISO format preferred)"
    )
    contact_email: Optional[str] = Field(None, description="Contact email address")
    application_url: Optional[str] = Field(
        None, description="URL to apply for the position"
    )
