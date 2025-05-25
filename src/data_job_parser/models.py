from enum import Enum

from pydantic import BaseModel, Field


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
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"


class Salary(BaseModel):
    min_amount: float | None = Field(None, description="Minimum salary amount")
    max_amount: float | None = Field(None, description="Maximum salary amount")
    currency: str | None = Field(None, description="Currency code")
    period: str | None = Field(
        None, description="Salary period (e.g., yearly, monthly)"
    )


class Location(BaseModel):
    city: str | None = None
    state: str | None = None
    country: str | None = None
    is_remote: bool = False


class JobPosting(BaseModel):
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: Location = Field(..., description="Job location details")
    description: str = Field(..., description="Full job description")

    experience_level: ExperienceLevel | None = None
    work_type: WorkType | None = None
    work_mode: WorkMode | None = None

    salary: Salary | None = None

    required_skills: list[str] = Field(
        default_factory=list, description="Required technical skills"
    )
    preferred_skills: list[str] = Field(
        default_factory=list, description="Nice-to-have skills"
    )

    responsibilities: list[str] = Field(
        default_factory=list, description="Key responsibilities"
    )
    requirements: list[str] = Field(
        default_factory=list, description="Job requirements"
    )
    benefits: list[str] = Field(default_factory=list, description="Benefits and perks")

    years_of_experience: int | None = Field(
        None, description="Minimum years of experience required"
    )
    education_requirements: str | None = Field(
        None, description="Education requirements"
    )

    department: str | None = None
    team_size: str | None = None

    application_deadline: str | None = None
    posted_date: str | None = None

    contact_email: str | None = None
    application_url: str | None = None
