from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.models import EstimateStatus, InvoiceStatus, ProjectStatus, SubscriptionPlan, TaskPriority, TaskStatus


class RegisterRequest(BaseModel):
    company_name: str = Field(min_length=2, max_length=150)
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str = Field(min_length=20, max_length=512)
    password: str = Field(min_length=10, max_length=128)


class TwoFactorCodeRequest(BaseModel):
    code: str = Field(min_length=6, max_length=12)


class TwoFactorSetupResponse(BaseModel):
    manual_entry_key: str
    account_name: EmailStr
    issuer: str = "BuildSmart AI"


class TwoFactorStatusResponse(BaseModel):
    enabled: bool


class UserResponse(BaseModel):
    id: int
    company_id: int
    email: EmailStr
    full_name: str
    role: str
    model_config = ConfigDict(from_attributes=True)


class ClientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    entity_type: Literal["individual", "company"] = "individual"
    nip: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    notes: str | None = None


class ClientResponse(ClientCreate):
    id: int
    regon: str | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    client_id: int | None = None
    status: ProjectStatus = ProjectStatus.planned
    budget: float | None = Field(default=None, ge=0)
    progress: int = Field(default=0, ge=0, le=100)
    location: str | None = None


class ProjectResponse(ProjectCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class DashboardResponse(BaseModel):
    active_projects: int
    completed_projects: int
    clients: int
    total_budget: float


class EmployeeCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr | None = None
    phone: str | None = None
    position: str | None = None


class EmployeeResponse(EmployeeCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    project_id: int | None = None
    assigned_employee_id: int | None = None
    description: str | None = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    due_date: date | None = None


class TaskResponse(TaskCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class InvoiceCreate(BaseModel):
    number: str = Field(min_length=1, max_length=80)
    client_id: int | None = None
    project_id: int | None = None
    amount: float = Field(gt=0)
    status: InvoiceStatus = InvoiceStatus.draft
    due_date: date | None = None
    issuer_name: str | None = Field(default=None, max_length=255)
    issuer_nip: str | None = Field(default=None, max_length=20)
    issuer_address: str | None = Field(default=None, max_length=255)
    issuer_postal_code: str | None = Field(default=None, max_length=12)
    issuer_city: str | None = Field(default=None, max_length=100)
    issuer_phone: str | None = Field(default=None, max_length=50)
    recipient_name: str | None = Field(default=None, max_length=255)
    recipient_nip: str | None = Field(default=None, max_length=20)
    recipient_address: str | None = Field(default=None, max_length=255)
    recipient_postal_code: str | None = Field(default=None, max_length=12)
    recipient_city: str | None = Field(default=None, max_length=100)
    recipient_phone: str | None = Field(default=None, max_length=50)


class InvoiceUpdate(BaseModel):
    number: str | None = Field(default=None, min_length=1, max_length=80)
    client_id: int | None = None
    project_id: int | None = None
    amount: float | None = Field(default=None, gt=0)
    status: InvoiceStatus | None = None
    due_date: date | None = None
    issuer_name: str | None = Field(default=None, max_length=255)
    issuer_nip: str | None = Field(default=None, max_length=20)
    issuer_address: str | None = Field(default=None, max_length=255)
    issuer_postal_code: str | None = Field(default=None, max_length=12)
    issuer_city: str | None = Field(default=None, max_length=100)
    issuer_phone: str | None = Field(default=None, max_length=50)
    recipient_name: str | None = Field(default=None, max_length=255)
    recipient_nip: str | None = Field(default=None, max_length=20)
    recipient_address: str | None = Field(default=None, max_length=255)
    recipient_postal_code: str | None = Field(default=None, max_length=12)
    recipient_city: str | None = Field(default=None, max_length=100)
    recipient_phone: str | None = Field(default=None, max_length=50)


class InvoiceResponse(InvoiceCreate):
    id: int
    created_at: datetime
    attachment_count: int = 0
    model_config = ConfigDict(from_attributes=True)


class InvoiceAttachmentResponse(BaseModel):
    id: int
    file_name: str
    content_type: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CompanyProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, max_length=255)
    nip: str | None = Field(default=None, max_length=20)
    regon: str | None = Field(default=None, max_length=20)
    krs: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=255)
    postal_code: str | None = Field(default=None, max_length=12)
    city: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, max_length=50)


class CompanyProfileResponse(CompanyProfileUpdate):
    company_id: int


class SubscriptionPlanUpdate(BaseModel):
    plan: SubscriptionPlan


class CheckoutSessionRequest(BaseModel):
    plan: SubscriptionPlan
    billing_cycle: Literal["monthly", "yearly"] = "monthly"


class CheckoutSessionResponse(BaseModel):
    checkout_url: str


class SubscriptionResponse(BaseModel):
    plan: SubscriptionPlan
    status: str
    trial_ends_at: datetime | None
    model_config = ConfigDict(from_attributes=True)


class AiProjectPlanRequest(BaseModel):
    project_type: str = Field(min_length=2, max_length=100)
    location: str | None = Field(default=None, max_length=200)
    budget: float | None = Field(default=None, ge=0)
    scope: str = Field(min_length=10, max_length=5000)


class AiProjectPlanResponse(BaseModel):
    summary: str
    phases: list[str]
    tasks: list[str]
    risks: list[str]


class AiConsultantMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=2000)


class AiConsultantRequest(BaseModel):
    messages: list[AiConsultantMessage] = Field(min_length=1, max_length=12)


class AiConsultantResponse(BaseModel):
    answer: str


class EstimateItemCreate(BaseModel):
    description: str = Field(min_length=2, max_length=300)
    quantity: float = Field(gt=0, le=1_000_000)
    unit: str = Field(default="szt.", min_length=1, max_length=30)
    unit_price: float = Field(ge=0, le=100_000_000)


class EstimateItemResponse(EstimateItemCreate):
    id: int
    line_total: float


class EstimateCreate(BaseModel):
    number: str = Field(min_length=1, max_length=80)
    client_id: int | None = None
    project_id: int | None = None
    status: EstimateStatus = EstimateStatus.draft
    tax_rate: float = Field(default=23, ge=0, le=100)
    notes: str | None = Field(default=None, max_length=3000)
    items: list[EstimateItemCreate] = Field(min_length=1, max_length=250)
    issuer_name: str | None = Field(default=None, max_length=255)
    issuer_nip: str | None = Field(default=None, max_length=20)
    issuer_address: str | None = Field(default=None, max_length=255)
    issuer_postal_code: str | None = Field(default=None, max_length=12)
    issuer_city: str | None = Field(default=None, max_length=100)
    issuer_phone: str | None = Field(default=None, max_length=50)
    recipient_name: str | None = Field(default=None, max_length=255)
    recipient_nip: str | None = Field(default=None, max_length=20)
    recipient_address: str | None = Field(default=None, max_length=255)
    recipient_postal_code: str | None = Field(default=None, max_length=12)
    recipient_city: str | None = Field(default=None, max_length=100)
    recipient_phone: str | None = Field(default=None, max_length=50)


class EstimateUpdate(BaseModel):
    number: str | None = Field(default=None, min_length=1, max_length=80)
    client_id: int | None = None
    project_id: int | None = None
    status: EstimateStatus | None = None
    tax_rate: float | None = Field(default=None, ge=0, le=100)
    notes: str | None = Field(default=None, max_length=3000)
    items: list[EstimateItemCreate] | None = Field(default=None, min_length=1, max_length=250)
    issuer_name: str | None = Field(default=None, max_length=255)
    issuer_nip: str | None = Field(default=None, max_length=20)
    issuer_address: str | None = Field(default=None, max_length=255)
    issuer_postal_code: str | None = Field(default=None, max_length=12)
    issuer_city: str | None = Field(default=None, max_length=100)
    issuer_phone: str | None = Field(default=None, max_length=50)
    recipient_name: str | None = Field(default=None, max_length=255)
    recipient_nip: str | None = Field(default=None, max_length=20)
    recipient_address: str | None = Field(default=None, max_length=255)
    recipient_postal_code: str | None = Field(default=None, max_length=12)
    recipient_city: str | None = Field(default=None, max_length=100)
    recipient_phone: str | None = Field(default=None, max_length=50)


class EstimateResponse(BaseModel):
    id: int
    number: str
    client_id: int | None
    project_id: int | None
    status: EstimateStatus
    tax_rate: float
    notes: str | None
    created_at: datetime
    net_total: float
    tax_total: float
    gross_total: float
    items: list[EstimateItemResponse]
    issuer_name: str | None = None
    issuer_nip: str | None = None
    issuer_address: str | None = None
    issuer_postal_code: str | None = None
    issuer_city: str | None = None
    issuer_phone: str | None = None
    recipient_name: str | None = None
    recipient_nip: str | None = None
    recipient_address: str | None = None
    recipient_postal_code: str | None = None
    recipient_city: str | None = None
    recipient_phone: str | None = None
    attachment_count: int = 0


class EstimateAttachmentResponse(BaseModel):
    id: int
    file_name: str
    content_type: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
