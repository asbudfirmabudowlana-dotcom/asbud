from datetime import date, datetime
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


class UserResponse(BaseModel):
    id: int
    company_id: int
    email: EmailStr
    full_name: str
    role: str
    model_config = ConfigDict(from_attributes=True)


class ClientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    notes: str | None = None


class ClientResponse(ClientCreate):
    id: int
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


class InvoiceResponse(InvoiceCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class SubscriptionPlanUpdate(BaseModel):
    plan: SubscriptionPlan


class CheckoutSessionRequest(BaseModel):
    plan: SubscriptionPlan


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
