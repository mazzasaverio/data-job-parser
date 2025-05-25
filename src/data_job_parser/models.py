from enum import Enum
from typing import List, Optional

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
    min_amount: Optional[float] = Field(None, description="Minimum salary amount")
    max_amount: Optional[float] = Field(None, description="Maximum salary amount")
    currency: Optional[str] = Field(None, description="Currency code")
    period: Optional[str] = Field(
        None, description="Salary period (e.g., yearly, monthly)"
    )


class Location(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    is_remote: bool = False


class JobPosting(BaseModel):
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: Location = Field(..., description="Job location details")
    description: str = Field(..., description="Full job description")

    experience_level: Optional[ExperienceLevel] = None
    work_type: Optional[WorkType] = None
    work_mode: Optional[WorkMode] = None

    salary: Optional[Salary] = None

    required_skills: List[str] = Field(
        default_factory=list, description="Required technical skills"
    )
    preferred_skills: List[str] = Field(
        default_factory=list, description="Nice-to-have skills"
    )

    responsibilities: List[str] = Field(
        default_factory=list, description="Key responsibilities"
    )
    requirements: List[str] = Field(
        default_factory=list, description="Job requirements"
    )
    benefits: List[str] = Field(default_factory=list, description="Benefits and perks")

    years_of_experience: Optional[int] = Field(
        None, description="Minimum years of experience required"
    )
    education_requirements: Optional[str] = Field(
        None, description="Education requirements"
    )

    department: Optional[str] = None
    team_size: Optional[str] = None

    application_deadline: Optional[str] = None
    posted_date: Optional[str] = None

    contact_email: Optional[str] = None
    application_url: Optional[str] = None
