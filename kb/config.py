SITE_TITLE = "IT Support Knowledge Base Lab"
SITE_SUBTITLE = "Simulated Tier 1 troubleshooting and runbooks"
BUILD_VERSION = "2.0.0"

CATEGORY_ORDER = [
    "Identity & Access",
    "Microsoft 365",
    "Windows Endpoint",
    "Networking & VPN",
    "Printing",
    "User Lifecycle",
    "Security & Escalation",
    "Support Operations",
]

CATEGORY_META = {
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
}

ARTICLE_TYPES = ("FAQ", "How-To", "Runbook")
RISK_LEVELS = ("Low", "Moderate", "High")

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
)

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
