import enum
from datetime import date, datetime
from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, LargeBinary, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base


class ProjectStatus(str, enum.Enum):
    planned = "planned"
    active = "active"
    completed = "completed"
    on_hold = "on_hold"


class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class InvoiceStatus(str, enum.Enum):
    draft = "draft"
    sent = "sent"
    paid = "paid"
    overdue = "overdue"


class SubscriptionPlan(str, enum.Enum):
    free = "free"
    basic = "basic"
    professional = "professional"
    enterprise = "enterprise"


class EstimateStatus(str, enum.Enum):
    draft = "draft"
    sent = "sent"
    accepted = "accepted"
    rejected = "rejected"


class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class CompanyProfile(Base):
    __tablename__ = "company_profiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    nip: Mapped[str | None] = mapped_column(String(20), nullable=True)
    regon: Mapped[str | None] = mapped_column(String(20), nullable=True)
    krs: Mapped[str | None] = mapped_column(String(20), nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(12), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(150))
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32), default="owner")
    session_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    two_factor_secret: Mapped[str | None] = mapped_column(String(512), nullable=True)
    two_factor_enabled: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    company: Mapped[Company] = relationship()


class AuditLog(Base):
    """Minimalny, niezmienialny ślad kluczowych działań w obrębie firmy."""
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), index=True)
    actor_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(80), index=True)
    entity_type: Mapped[str] = mapped_column(String(80))
    entity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Client(Base):
    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(50))
    address: Mapped[str | None] = mapped_column(String(255))
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    client_id: Mapped[int | None] = mapped_column(ForeignKey("clients.id"))
    name: Mapped[str] = mapped_column(String(200))
    status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus), default=ProjectStatus.planned)
    budget: Mapped[float | None] = mapped_column(Numeric(14, 2))
    progress: Mapped[int] = mapped_column(Integer, default=0)
    location: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    full_name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(50))
    position: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    assigned_employee_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id"))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.todo)
    priority: Mapped[TaskPriority] = mapped_column(Enum(TaskPriority), default=TaskPriority.medium)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Invoice(Base):
    __tablename__ = "invoices"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    client_id: Mapped[int | None] = mapped_column(ForeignKey("clients.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    number: Mapped[str] = mapped_column(String(80))
    amount: Mapped[float] = mapped_column(Numeric(14, 2))
    status: Mapped[InvoiceStatus] = mapped_column(Enum(InvoiceStatus), default=InvoiceStatus.draft)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class InvoiceDetails(Base):
    __tablename__ = "invoice_details"
    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id", ondelete="CASCADE"), unique=True, index=True)
    issuer_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    issuer_nip: Mapped[str | None] = mapped_column(String(20), nullable=True)
    issuer_address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    issuer_postal_code: Mapped[str | None] = mapped_column(String(12), nullable=True)
    issuer_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    issuer_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    recipient_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recipient_nip: Mapped[str | None] = mapped_column(String(20), nullable=True)
    recipient_address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recipient_postal_code: Mapped[str | None] = mapped_column(String(12), nullable=True)
    recipient_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    recipient_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)


class InvoiceAttachment(Base):
    __tablename__ = "invoice_attachments"
    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id", ondelete="CASCADE"), index=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    content: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Subscription(Base):
    __tablename__ = "subscriptions"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), unique=True, index=True)
    plan: Mapped[SubscriptionPlan] = mapped_column(Enum(SubscriptionPlan), default=SubscriptionPlan.free)
    status: Mapped[str] = mapped_column(String(32), default="active")
    trial_ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Estimate(Base):
    __tablename__ = "estimates"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    client_id: Mapped[int | None] = mapped_column(ForeignKey("clients.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    number: Mapped[str] = mapped_column(String(80))
    status: Mapped[EstimateStatus] = mapped_column(Enum(EstimateStatus), default=EstimateStatus.draft)
    tax_rate: Mapped[float] = mapped_column(Numeric(5, 2), default=23)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class EstimateItem(Base):
    __tablename__ = "estimate_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    estimate_id: Mapped[int] = mapped_column(ForeignKey("estimates.id", ondelete="CASCADE"), index=True)
    description: Mapped[str] = mapped_column(String(300))
    quantity: Mapped[float] = mapped_column(Numeric(12, 3))
    unit: Mapped[str] = mapped_column(String(30), default="szt.")
    unit_price: Mapped[float] = mapped_column(Numeric(14, 2))


class EstimateDetails(Base):
    __tablename__ = "estimate_details"
    id: Mapped[int] = mapped_column(primary_key=True)
    estimate_id: Mapped[int] = mapped_column(ForeignKey("estimates.id", ondelete="CASCADE"), unique=True, index=True)
    issuer_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    issuer_nip: Mapped[str | None] = mapped_column(String(20), nullable=True)
    issuer_address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    issuer_postal_code: Mapped[str | None] = mapped_column(String(12), nullable=True)
    issuer_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    issuer_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    recipient_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recipient_nip: Mapped[str | None] = mapped_column(String(20), nullable=True)
    recipient_address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recipient_postal_code: Mapped[str | None] = mapped_column(String(12), nullable=True)
    recipient_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    recipient_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)


class EstimateAttachment(Base):
    __tablename__ = "estimate_attachments"
    id: Mapped[int] = mapped_column(primary_key=True)
    estimate_id: Mapped[int] = mapped_column(ForeignKey("estimates.id", ondelete="CASCADE"), index=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    content: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ClientCompanyDetails(Base):
    __tablename__ = "client_company_details"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"), unique=True, index=True)
    nip: Mapped[str] = mapped_column(String(10), index=True)
    regon: Mapped[str | None] = mapped_column(String(14), nullable=True)
    # Existing database column names are retained so an upgrade does not require data migration.
    company_name: Mapped[str] = mapped_column("gus_name", String(255), nullable=False)
    company_address: Mapped[str | None] = mapped_column("gus_address", String(300), nullable=True)
