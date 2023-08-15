from enum import Enum


class ApplicationStatus(str, Enum):
    draft = "draft"
    submitted = "submitted"
    accepted = "accepted"
    rejected = "rejected"
    withdrawn = "withdrawn"


class CompanyQuickAction(str, Enum):
    yes = "yes"
    no = "no"
    maybe = "maybe"
