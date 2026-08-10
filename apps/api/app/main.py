import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.db import Base, engine, get_db
from app.models import Client, Company, Employee, Estimate, EstimateItem, Invoice, Project, ProjectStatus, Subscription, SubscriptionPlan, Task, User
from app.schemas import (AiProjectPlanRequest, AiProjectPlanResponse, ClientCreate, ClientResponse, DashboardResponse, EmployeeCreate, EmployeeResponse, EstimateCreate, EstimateItemResponse, EstimateResponse, InvoiceCreate, InvoiceResponse, LoginRequest, ProjectCreate, ProjectResponse, RegisterRequest, SubscriptionPlanUpdate, SubscriptionResponse, TaskCreate, TaskResponse, TokenResponse, UserResponse)
from app.security import create_access_token, get_current_user, hash_password, verify_password

settings = get_settings()
app = FastAPI(
    title="BuildSmart AI — API",
    description="Interfejs programistyczny platformy do zarządzania firmą budowlaną.",
    version="0.1.0",
)
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(",")], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    company = Company(name=data.company_name)
    db.add(company)
    db.flush()
    user = User(company_id=company.id, full_name=data.full_name, email=str(data.email), password_hash=hash_password(data.password), role="owner")
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(access_token=create_access_token(user))


@app.post("/api/v1/auth/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == data.email))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return TokenResponse(access_token=create_access_token(user))


@app.get("/api/v1/auth/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return user


@app.get("/api/v1/dashboard", response_model=DashboardResponse)
def dashboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cid = user.company_id
    return DashboardResponse(
        active_projects=db.scalar(select(func.count()).select_from(Project).where(Project.company_id == cid, Project.status == ProjectStatus.active)) or 0,
        completed_projects=db.scalar(select(func.count()).select_from(Project).where(Project.company_id == cid, Project.status == ProjectStatus.completed)) or 0,
        clients=db.scalar(select(func.count()).select_from(Client).where(Client.company_id == cid)) or 0,
        total_budget=float(db.scalar(select(func.coalesce(func.sum(Project.budget), 0)).where(Project.company_id == cid)) or 0),
    )


@app.get("/api/v1/clients", response_model=list[ClientResponse])
def list_clients(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(select(Client).where(Client.company_id == user.company_id).order_by(Client.created_at.desc())).all()


@app.post("/api/v1/clients", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(data: ClientCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    client = Client(company_id=user.company_id, **data.model_dump())
    db.add(client); db.commit(); db.refresh(client)
    return client


@app.get("/api/v1/projects", response_model=list[ProjectResponse])
def list_projects(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(select(Project).where(Project.company_id == user.company_id).order_by(Project.created_at.desc())).all()


@app.post("/api/v1/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if data.client_id and not db.scalar(select(Client).where(Client.id == data.client_id, Client.company_id == user.company_id)):
        raise HTTPException(status_code=404, detail="Client not found")
    project = Project(company_id=user.company_id, **data.model_dump())
    db.add(project); db.commit(); db.refresh(project)
    return project


@app.get("/api/v1/employees", response_model=list[EmployeeResponse])
def list_employees(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(select(Employee).where(Employee.company_id == user.company_id).order_by(Employee.created_at.desc())).all()


@app.post("/api/v1/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(data: EmployeeCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    employee = Employee(company_id=user.company_id, **data.model_dump())
    db.add(employee); db.commit(); db.refresh(employee)
    return employee


@app.get("/api/v1/tasks", response_model=list[TaskResponse])
def list_tasks(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(select(Task).where(Task.company_id == user.company_id).order_by(Task.created_at.desc())).all()


@app.post("/api/v1/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if data.project_id and not db.scalar(select(Project).where(Project.id == data.project_id, Project.company_id == user.company_id)):
        raise HTTPException(status_code=404, detail="Project not found")
    if data.assigned_employee_id and not db.scalar(select(Employee).where(Employee.id == data.assigned_employee_id, Employee.company_id == user.company_id)):
        raise HTTPException(status_code=404, detail="Employee not found")
    task = Task(company_id=user.company_id, **data.model_dump())
    db.add(task); db.commit(); db.refresh(task)
    return task


@app.get("/api/v1/invoices", response_model=list[InvoiceResponse])
def list_invoices(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(select(Invoice).where(Invoice.company_id == user.company_id).order_by(Invoice.created_at.desc())).all()


@app.post("/api/v1/invoices", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(data: InvoiceCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if data.client_id and not db.scalar(select(Client).where(Client.id == data.client_id, Client.company_id == user.company_id)):
        raise HTTPException(status_code=404, detail="Client not found")
    if data.project_id and not db.scalar(select(Project).where(Project.id == data.project_id, Project.company_id == user.company_id)):
        raise HTTPException(status_code=404, detail="Project not found")
    invoice = Invoice(company_id=user.company_id, **data.model_dump())
    db.add(invoice); db.commit(); db.refresh(invoice)
    return invoice


def serialize_estimate(estimate: Estimate, items: list[EstimateItem]) -> EstimateResponse:
    net_total = sum(float(item.quantity) * float(item.unit_price) for item in items)
    tax_total = net_total * float(estimate.tax_rate) / 100
    return EstimateResponse(
        id=estimate.id,
        number=estimate.number,
        client_id=estimate.client_id,
        project_id=estimate.project_id,
        status=estimate.status,
        tax_rate=float(estimate.tax_rate),
        notes=estimate.notes,
        created_at=estimate.created_at,
        net_total=round(net_total, 2),
        tax_total=round(tax_total, 2),
        gross_total=round(net_total + tax_total, 2),
        items=[
            EstimateItemResponse(
                id=item.id,
                description=item.description,
                quantity=float(item.quantity),
                unit=item.unit,
                unit_price=float(item.unit_price),
                line_total=round(float(item.quantity) * float(item.unit_price), 2),
            )
            for item in items
        ],
    )


@app.get("/api/v1/estimates", response_model=list[EstimateResponse])
def list_estimates(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    estimates = db.scalars(select(Estimate).where(Estimate.company_id == user.company_id).order_by(Estimate.created_at.desc())).all()
    return [
        serialize_estimate(estimate, db.scalars(select(EstimateItem).where(EstimateItem.estimate_id == estimate.id)).all())
        for estimate in estimates
    ]


@app.post("/api/v1/estimates", response_model=EstimateResponse, status_code=status.HTTP_201_CREATED)
def create_estimate(data: EstimateCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if db.scalar(select(Estimate).where(Estimate.company_id == user.company_id, Estimate.number == data.number)):
        raise HTTPException(status_code=409, detail="Estimate number already exists")
    if data.client_id and not db.scalar(select(Client).where(Client.id == data.client_id, Client.company_id == user.company_id)):
        raise HTTPException(status_code=404, detail="Client not found")
    if data.project_id and not db.scalar(select(Project).where(Project.id == data.project_id, Project.company_id == user.company_id)):
        raise HTTPException(status_code=404, detail="Project not found")

    estimate = Estimate(
        company_id=user.company_id,
        client_id=data.client_id,
        project_id=data.project_id,
        number=data.number,
        status=data.status,
        tax_rate=data.tax_rate,
        notes=data.notes,
    )
    db.add(estimate)
    db.flush()
    items = [EstimateItem(estimate_id=estimate.id, **item.model_dump()) for item in data.items]
    db.add_all(items)
    db.commit()
    db.refresh(estimate)
    for item in items:
        db.refresh(item)
    return serialize_estimate(estimate, items)


def get_or_create_subscription(user: User, db: Session) -> Subscription:
    subscription = db.scalar(select(Subscription).where(Subscription.company_id == user.company_id))
    if subscription:
        return subscription
    subscription = Subscription(company_id=user.company_id, plan=SubscriptionPlan.free, status="active")
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


@app.get("/api/v1/billing/subscription", response_model=SubscriptionResponse)
def current_subscription(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_or_create_subscription(user, db)


@app.post("/api/v1/billing/plan", response_model=SubscriptionResponse)
def select_subscription_plan(data: SubscriptionPlanUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subscription = get_or_create_subscription(user, db)
    subscription.plan = data.plan
    if data.plan == SubscriptionPlan.free:
        subscription.status = "active"
        subscription.trial_ends_at = None
    else:
        subscription.status = "trial"
        subscription.trial_ends_at = datetime.now(timezone.utc) + timedelta(days=14)
    db.commit()
    db.refresh(subscription)
    return subscription


@app.post("/api/v1/ai/project-plan", response_model=AiProjectPlanResponse)
def generate_project_plan(data: AiProjectPlanRequest, user: User = Depends(get_current_user)):
    if not settings.openai_api_key:
        raise HTTPException(status_code=503, detail="AI is not configured. Add OPENAI_API_KEY to the server environment.")

    prompt = f"""Jesteś asystentem kierownika projektów budowlanych w Polsce.
Przygotuj praktyczny, ostrożny plan roboczy po polsku. Nie zastępujesz uprawnionego projektanta,
kierownika budowy ani kosztorysanta. Nie twórz porad prawnych ani gwarancji cen lub terminów.

Typ inwestycji: {data.project_type}
Lokalizacja: {data.location or 'nie podano'}
Budżet orientacyjny: {data.budget if data.budget is not None else 'nie podano'} PLN
Zakres prac: {data.scope}

Zwróć WYŁĄCZNIE poprawny JSON bez znaków markdown, zgodny z tym schematem:
{{"summary":"krótkie podsumowanie", "phases":["3-6 etapów"], "tasks":["4-8 konkretnych zadań"], "risks":["3-6 ryzyk do weryfikacji"]}}"""
    try:
        request = Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps({
                "model": settings.openai_model,
                "input": prompt,
                "reasoning": {"effort": "medium"},
                "text": {"verbosity": "medium"},
                "safety_identifier": f"company-{user.company_id}",
            }).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urlopen(request, timeout=60) as response:
            response_data = json.loads(response.read().decode("utf-8"))
        output_text = "".join(
            content.get("text", "")
            for item in response_data.get("output", [])
            for content in item.get("content", [])
            if content.get("type") == "output_text"
        )
        payload = json.loads(output_text)
        return AiProjectPlanResponse.model_validate(payload)
    except HTTPError as exc:
        if exc.code == 401:
            detail = "AI could not authenticate. Check the server-side API key."
        elif exc.code == 429:
            detail = "AI is temporarily unavailable because the API limit was reached."
        elif exc.code in (403, 404):
            detail = "The configured AI model is not available for this API project."
        else:
            detail = "AI generation is temporarily unavailable."
        raise HTTPException(status_code=502, detail=detail) from exc
    except (URLError, TimeoutError) as exc:
        raise HTTPException(status_code=503, detail="The AI server cannot reach OpenAI. Check the server network connection.") from exc
    except (json.JSONDecodeError, ValueError) as exc:
        raise HTTPException(status_code=502, detail="AI returned an invalid project plan") from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="AI generation is temporarily unavailable") from exc


web_directory = Path(__file__).resolve().parents[2] / "web" / "public"
app.mount("/", StaticFiles(directory=str(web_directory), html=True), name="web")
