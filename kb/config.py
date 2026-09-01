SITE_TITLE = "IT Support Knowledge Base Lab"
SITE_SUBTITLE = "Simulated Tier 1 troubleshooting and runbooks"
BUILD_VERSION = "3.1.0"

CATEGORY_ORDER = [
    "Start Here",
    "Identity & Access",
    "Microsoft 365",
    "Windows Endpoint",
    "Networking & VPN",
    "Printing",
    "User Lifecycle",
    "Security & Escalation",
    "Support Operations",
    "Hardware & Peripherals",
    "Accessibility",
]

CATEGORY_META = {
    "Start Here": {
        "slug": "start-here",
        "short": "Start here",
        "description": "First-contact triage, symptom routing, and safe technician quick references.",
    },
    "Identity & Access": {
        "slug": "identity-access",
        "short": "Identity",
        "description": "Account access, authentication, MFA, and safe identity handoffs.",
    },
    "Microsoft 365": {
        "slug": "microsoft-365",
        "short": "M365",
        "description": "Outlook, Teams, OneDrive, Exchange Online, and collaboration support.",
    },
    "Windows Endpoint": {
        "slug": "windows-endpoint",
        "short": "Windows",
        "description": "Windows 11 recovery, performance, software, and endpoint support.",
    },
    "Networking & VPN": {
        "slug": "networking-vpn",
        "short": "Network",
        "description": "Wi-Fi, DNS, routing, connectivity, and remote-access troubleshooting.",
    },
    "Printing": {
        "slug": "printing",
        "short": "Printing",
        "description": "Printer status, Windows queues, and spooler troubleshooting.",
    },
    "User Lifecycle": {
        "slug": "user-lifecycle",
        "short": "Lifecycle",
        "description": "Controlled onboarding, offboarding, licensing, and asset handoffs.",
    },
    "Security & Escalation": {
        "slug": "security-escalation",
        "short": "Security",
        "description": "Safe incident intake, evidence capture, and resolver-group boundaries.",
    },
    "Support Operations": {
        "slug": "support-operations",
        "short": "Operations",
        "description": "Remote support, communication, ticket notes, and validation habits.",
    },
    "Hardware & Peripherals": {
        "slug": "hardware-peripherals",
        "short": "Hardware",
        "description": "Displays, docks, audio, USB, power, and known-good hardware isolation.",
    },
    "Accessibility": {
        "slug": "accessibility",
        "short": "Accessibility",
        "description": "Consent-centered support for Windows accessibility and assistive technology.",
    },
}

ARTICLE_TYPES = (
    "FAQ",
    "How-To",
    "Runbook",
    "Troubleshooting",
    "Checklist",
    "Quick Reference",
    "Concept",
    "Security Response",
)
RISK_LEVELS = ("Low", "Moderate", "High")
AUDIENCES = ("Technician", "End User", "Technician and End User")
DIFFICULTIES = ("Foundational", "Intermediate", "Advanced")
EVIDENCE_STATUSES = (
    "concept_reviewed",
    "vendor_source_checked",
    "lab_executed",
    "needs_review",
    "archived",
)
EVIDENCE_STATUS_LABELS = {
    "concept_reviewed": "Concept reviewed",
    "vendor_source_checked": "Vendor source checked",
    "lab_executed": "Lab executed",
    "needs_review": "Needs review",
    "archived": "Archived",
}

REQUIRED_FIELDS = (
    "title",
    "author",
    "category",
    "article_type",
    "last_updated",
    "kb_id",
    "tags",
    "platforms",
    "support_tier",
    "risk",
    "evidence_status",
)

OPTIONAL_METADATA_DEFAULTS = {
    "audience": "Technician",
    "difficulty": "Foundational",
    "prerequisites": ["Authorized support context"],
    "content_type": "Troubleshooting",
}

REQUIRED_SECTIONS = (
    "Summary",
    "Scope and safety",
    "Symptoms or trigger",
    "Information to collect",
    "Diagnostic steps",
    "Resolution or next action",
    "Validation",
    "Ticket note example",
    "Escalation criteria",
    "References",
)

ARCHETYPE_SECTIONS = {
    "Troubleshooting": REQUIRED_SECTIONS,
    "How-To": (
        "Summary",
        "Scope and safety",
        "Prerequisites",
        "Procedure",
        "Expected result",
        "Recovery or rollback",
        "Ticket note example",
        "Escalation criteria",
        "References",
    ),
    "Checklist": (
        "Summary",
        "Scope and safety",
        "Checklist",
        "Completion evidence",
        "Exceptions and escalation",
        "Ticket note example",
        "References",
    ),
    "Quick Reference": (
        "Summary",
        "Scope and safety",
        "Reference",
        "Interpretation",
        "Common mistakes",
        "Ticket note example",
        "Escalation criteria",
        "References",
    ),
    "Concept": (
        "Summary",
        "Why support cares",
        "Core concepts",
        "Examples and boundaries",
        "Related procedures",
        "References",
    ),
    "Security Response": (
        "Summary",
        "Scope and safety",
        "Indicators",
        "Immediate safe action",
        "Evidence to preserve",
        "Do not",
        "Escalation criteria",
        "Ticket note example",
        "References",
    ),
}

TAG_ALIASES = {
    "active directory": "Active Directory",
    "activedirectory": "Active Directory",
    "azure ad": "Microsoft Entra ID",
    "azure-ad": "Microsoft Entra ID",
    "azuread": "Microsoft Entra ID",
    "entra id": "Microsoft Entra ID",
    "m365": "Microsoft 365",
    "o365": "Microsoft 365",
    "office 365": "Microsoft 365",
    "wifi": "Wi-Fi",
    "wi-fi": "Wi-Fi",
    "fileshares": "File Shares",
    "file shares": "File Shares",
}
