from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
#from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# ============= MODELS =============

# Employee Models
class Employee(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    emp_id: str
    name: str
    department: str
    designation: str
    join_date: str
    basic_salary: float
    hra: float
    allowance: float
    pf_percent: float = 12.0
    esi_percent: float = 0.75
    pt: float = 200.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class EmployeeCreate(BaseModel):
    emp_id: str
    name: str
    department: str
    designation: str
    join_date: str
    basic_salary: float
    hra: float
    allowance: float
    pf_percent: float = 12.0
    esi_percent: float = 0.75
    pt: float = 200.0

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    join_date: Optional[str] = None
    basic_salary: Optional[float] = None
    hra: Optional[float] = None
    allowance: Optional[float] = None
    pf_percent: Optional[float] = None
    esi_percent: Optional[float] = None
    pt: Optional[float] = None

# Attendance Models
class Attendance(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    emp_id: str
    month: str
    total_working_days: int
    present_days: int
    leave_days: int
    lop_days: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AttendanceCreate(BaseModel):
    emp_id: str
    month: str
    total_working_days: int
    present_days: int
    leave_days: int
    lop_days: int

class AttendanceUpdate(BaseModel):
    total_working_days: Optional[int] = None
    present_days: Optional[int] = None
    leave_days: Optional[int] = None
    lop_days: Optional[int] = None

# Payroll Models
class PayrollCalculation(BaseModel):
    emp_id: str
    name: str
    month: str
    basic_salary: float
    hra: float
    allowance: float
    gross_salary: float
    pf_deduction: float
    esi_deduction: float
    pt_deduction: float
    total_deductions: float
    net_salary: float
    paid_days: int
    total_working_days: int

# AI Assistant Models
class AIRequest(BaseModel):
    request_type: str
    context: str
    additional_info: Optional[str] = None

class AIResponse(BaseModel):
    request_type: str
    generated_text: str

# ============= ROUTES =============

# Employee Routes
@api_router.post("/employees", response_model=Employee)
async def create_employee(employee: EmployeeCreate):
    existing = await db.employees.find_one({"emp_id": employee.emp_id}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    
    employee_obj = Employee(**employee.model_dump())
    doc = employee_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.employees.insert_one(doc)
    return employee_obj

@api_router.get("/employees", response_model=List[Employee])
async def get_employees():
    employees = await db.employees.find({}, {"_id": 0}).to_list(1000)
    
    for emp in employees:
        if isinstance(emp['created_at'], str):
            emp['created_at'] = datetime.fromisoformat(emp['created_at'])
    
    return employees

@api_router.get("/employees/{emp_id}", response_model=Employee)
async def get_employee(emp_id: str):
    employee = await db.employees.find_one({"emp_id": emp_id}, {"_id": 0})
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if isinstance(employee['created_at'], str):
        employee['created_at'] = datetime.fromisoformat(employee['created_at'])
    
    return employee

@api_router.put("/employees/{emp_id}", response_model=Employee)
async def update_employee(emp_id: str, employee_update: EmployeeUpdate):
    existing = await db.employees.find_one({"emp_id": emp_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    update_data = {k: v for k, v in employee_update.model_dump().items() if v is not None}
    
    if update_data:
        await db.employees.update_one(
            {"emp_id": emp_id},
            {"$set": update_data}
        )
    
    updated = await db.employees.find_one({"emp_id": emp_id}, {"_id": 0})
    if isinstance(updated['created_at'], str):
        updated['created_at'] = datetime.fromisoformat(updated['created_at'])
    
    return updated

@api_router.delete("/employees/{emp_id}")
async def delete_employee(emp_id: str):
    result = await db.employees.delete_one({"emp_id": emp_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    await db.attendance.delete_many({"emp_id": emp_id})
    
    return {"message": "Employee deleted successfully"}

# Attendance Routes
@api_router.post("/attendance", response_model=Attendance)
async def create_attendance(attendance: AttendanceCreate):
    employee = await db.employees.find_one({"emp_id": attendance.emp_id}, {"_id": 0})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    existing = await db.attendance.find_one(
        {"emp_id": attendance.emp_id, "month": attendance.month},
        {"_id": 0}
    )
    if existing:
        raise HTTPException(status_code=400, detail="Attendance already exists for this employee and month")
    
    attendance_obj = Attendance(**attendance.model_dump())
    doc = attendance_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.attendance.insert_one(doc)
    return attendance_obj

@api_router.get("/attendance", response_model=List[Attendance])
async def get_all_attendance():
    attendance_list = await db.attendance.find({}, {"_id": 0}).to_list(1000)
    
    for att in attendance_list:
        if isinstance(att['created_at'], str):
            att['created_at'] = datetime.fromisoformat(att['created_at'])
    
    return attendance_list

@api_router.get("/attendance/{emp_id}", response_model=List[Attendance])
async def get_employee_attendance(emp_id: str):
    attendance_list = await db.attendance.find({"emp_id": emp_id}, {"_id": 0}).to_list(1000)
    
    for att in attendance_list:
        if isinstance(att['created_at'], str):
            att['created_at'] = datetime.fromisoformat(att['created_at'])
    
    return attendance_list

@api_router.get("/attendance/{emp_id}/{month}", response_model=Attendance)
async def get_attendance_by_month(emp_id: str, month: str):
    attendance = await db.attendance.find_one(
        {"emp_id": emp_id, "month": month},
        {"_id": 0}
    )
    
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    if isinstance(attendance['created_at'], str):
        attendance['created_at'] = datetime.fromisoformat(attendance['created_at'])
    
    return attendance

@api_router.put("/attendance/{emp_id}/{month}", response_model=Attendance)
async def update_attendance(emp_id: str, month: str, attendance_update: AttendanceUpdate):
    existing = await db.attendance.find_one(
        {"emp_id": emp_id, "month": month},
        {"_id": 0}
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    update_data = {k: v for k, v in attendance_update.model_dump().items() if v is not None}
    
    if update_data:
        await db.attendance.update_one(
            {"emp_id": emp_id, "month": month},
            {"$set": update_data}
        )
    
    updated = await db.attendance.find_one(
        {"emp_id": emp_id, "month": month},
        {"_id": 0}
    )
    if isinstance(updated['created_at'], str):
        updated['created_at'] = datetime.fromisoformat(updated['created_at'])
    
    return updated

@api_router.delete("/attendance/{emp_id}/{month}")
async def delete_attendance(emp_id: str, month: str):
    result = await db.attendance.delete_one({"emp_id": emp_id, "month": month})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    return {"message": "Attendance deleted successfully"}

# Payroll Calculation Route
@api_router.get("/payroll/{emp_id}/{month}", response_model=PayrollCalculation)
async def calculate_payroll(emp_id: str, month: str):
    employee = await db.employees.find_one({"emp_id": emp_id}, {"_id": 0})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    attendance = await db.attendance.find_one(
        {"emp_id": emp_id, "month": month},
        {"_id": 0}
    )
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found for this month")
    
    paid_days = attendance['present_days'] + attendance['leave_days']
    total_working_days = attendance['total_working_days']
    lop_days = attendance['lop_days']
    
    basic_for_month = employee['basic_salary'] - (employee['basic_salary'] / total_working_days * lop_days)
    hra_for_month = employee['hra'] - (employee['hra'] / total_working_days * lop_days)
    allowance_for_month = employee['allowance'] - (employee['allowance'] / total_working_days * lop_days)
    
    gross_salary = basic_for_month + hra_for_month + allowance_for_month
    
    pf_deduction = (basic_for_month * employee['pf_percent']) / 100
    esi_deduction = (gross_salary * employee['esi_percent']) / 100
    pt_deduction = employee['pt'] if paid_days > 0 else 0
    
    total_deductions = pf_deduction + esi_deduction + pt_deduction
    net_salary = gross_salary - total_deductions
    
    return PayrollCalculation(
        emp_id=emp_id,
        name=employee['name'],
        month=month,
        basic_salary=basic_for_month,
        hra=hra_for_month,
        allowance=allowance_for_month,
        gross_salary=gross_salary,
        pf_deduction=pf_deduction,
        esi_deduction=esi_deduction,
        pt_deduction=pt_deduction,
        total_deductions=total_deductions,
        net_salary=net_salary,
        paid_days=paid_days,
        total_working_days=total_working_days
    )

# AI Assistant Route
@api_router.post("/ai-assistant", response_model=AIResponse)
async def ai_assistant(request: AIRequest):
    main_request = request.context.strip().lower()
    extra = (request.additional_info or "").strip()

    # ----- EMAIL TEMPLATES -----
    if request.request_type == "email_template":
        if "salary credit" in main_request:
            body = (
                "Subject: Salary Credit Confirmation\n\n"
                "Dear [Employee Name],\n\n"
                "This is to inform you that your salary for the month has been "
                "processed and credited to your registered bank account.\n"
                "If you notice any discrepancy in the credited amount, please "
                "reach out to HR/Payroll within 2 working days.\n"
            )
        elif "leave approval" in main_request:
            body = (
                "Subject: Leave Request – Approval\n\n"
                "Dear [Employee Name],\n\n"
                "Your leave request has been reviewed and approved as per the "
                "details shared in your application.\n"
                "Kindly ensure proper handover of your ongoing tasks before "
                "proceeding on leave.\n"
            )
        elif "leave rejection" in main_request:
            body = (
                "Subject: Leave Request – Regret\n\n"
                "Dear [Employee Name],\n\n"
                "This is with reference to your recent leave request.\n"
                "We regret to inform you that the request cannot be approved "
                "due to business/operational requirements during the requested period.\n"
                "You may discuss with your manager and raise a fresh request "
                "for alternate dates, if required.\n"
            )
        elif "warning" in main_request or "late coming" in main_request:
            body = (
                "Subject: Advisory on Late Coming\n\n"
                "Dear [Employee Name],\n\n"
                "It has been observed that there are repeated instances of late "
                "reporting to work.\n"
                "You are requested to adhere strictly to the prescribed office "
                "timings. Continued non‑compliance may lead to further action "
                "as per company policy.\n"
            )
        else:
            body = (
                "Subject: HR Communication\n\n"
                "Dear [Employee Name],\n\n"
                "This is a system‑generated HR communication based on your request.\n"
            )

        if extra:
            body += f"\nAdditional details: {extra}\n"

        body += "\nRegards,\nHR Team"

    # ----- POLICY GENERATION -----
    elif request.request_type == "policy":
        if "leave policy" in main_request or "cl" in main_request or "sl" in main_request:
            body = (
                "Leave Policy (CL, SL and LOP) – Draft\n\n"
                "1. Casual Leave (CL): Granted for short‑term personal reasons with prior approval.\n"
                "2. Sick Leave (SL): Applicable in case of medical illness; medical proof may be requested.\n"
                "3. Loss of Pay (LOP): Applied when leave exceeds available balance or is unapproved.\n"
                "4. All leave requests must be recorded in the HR system and approved by the reporting manager.\n"
            )
        elif "payroll policy" in main_request:
            body = (
                "Basic Payroll Policy – Draft\n\n"
                "1. Salaries are processed monthly and credited to employees’ bank accounts.\n"
                "2. Statutory deductions such as PF, ESI and Professional Tax are applied as per regulations.\n"
                "3. Any adjustments for LOP, incentives or arrears are reflected in the same or subsequent month.\n"
            )
        elif "attendance" in main_request or "late coming" in main_request:
            body = (
                "Attendance and Late Coming Policy – Draft\n\n"
                "1. Employees must follow the defined shift/office timings.\n"
                "2. Late coming beyond the grace period may be adjusted against leave or treated as LOP.\n"
                "3. Attendance must be recorded through the official system (biometric/portal).\n"
            )
        elif "work from home" in main_request:
            body = (
                "Work From Home (WFH) Policy – Draft\n\n"
                "1. WFH is allowed only with prior manager approval except in emergencies.\n"
                "2. Employees must be available during working hours on official communication channels.\n"
                "3. Daily work updates and task status must be shared with the reporting manager.\n"
            )
        else:
            body = "Draft HR policy based on the given context.\n"

        if extra:
            body += f"\nContext: {extra}\n"

    # ----- FORMULA & LOGIC SUGGESTIONS -----
    elif request.request_type == "formula_suggestion":
        if "pf" in main_request:
            body = (
                "PF Calculation Suggestion:\n"
                "PF = Basic Salary × PF% / 100\n"
                "Example: If Basic Salary = ₹30,000 and PF% = 12, PF = 30,000 × 12 / 100 = ₹3,600.\n"
            )
        elif "esi" in main_request:
            body = (
                "ESI Deduction Logic:\n"
                "ESI = Gross Salary × ESI% / 100 (subject to eligibility and statutory wage limits).\n"
            )
        elif "lop" in main_request:
            body = (
                "LOP Salary Deduction Formula:\n"
                "Per‑day salary = Gross Salary / Total Working Days.\n"
                "LOP Amount = Per‑day salary × LOP Days.\n"
            )
        elif "gross to net" in main_request or "net salary" in main_request:
            body = (
                "Gross to Net Salary Calculation:\n"
                "Net Salary = Gross Salary – (PF + ESI + PT + other deductions).\n"
            )
        else:
            body = "Payroll formula suggestion based on the given context.\n"

        if extra:
            body += f"\nData/Notes: {extra}\n"

    else:
        # Fallback
        body = request.context
        if extra:
            body += f"\n\nDetails: {extra}"

    return AIResponse(
        request_type=request.request_type,
        generated_text=body,
    )



# Sample Data Initialization Route
@api_router.post("/initialize-sample-data")
async def initialize_sample_data():
    existing_count = await db.employees.count_documents({})
    if existing_count > 0:
        return {"message": "Sample data already exists", "count": existing_count}
    
    sample_employees = [
        {
            "id": str(uuid.uuid4()),
            "emp_id": "EMP001",
            "name": "Rajesh Kumar",
            "department": "Engineering",
            "designation": "Senior Software Engineer",
            "join_date": "2022-01-15",
            "basic_salary": 40000.0,
            "hra": 16000.0,
            "allowance": 8000.0,
            "pf_percent": 12.0,
            "esi_percent": 0.75,
            "pt": 200.0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "emp_id": "EMP002",
            "name": "Priya Sharma",
            "department": "HR",
            "designation": "HR Manager",
            "join_date": "2021-06-10",
            "basic_salary": 35000.0,
            "hra": 14000.0,
            "allowance": 6000.0,
            "pf_percent": 12.0,
            "esi_percent": 0.75,
            "pt": 200.0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "emp_id": "EMP003",
            "name": "Amit Patel",
            "department": "Finance",
            "designation": "Accountant",
            "join_date": "2023-03-20",
            "basic_salary": 30000.0,
            "hra": 12000.0,
            "allowance": 5000.0,
            "pf_percent": 12.0,
            "esi_percent": 0.75,
            "pt": 200.0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "emp_id": "EMP004",
            "name": "Sneha Reddy",
            "department": "Marketing",
            "designation": "Marketing Executive",
            "join_date": "2022-09-01",
            "basic_salary": 28000.0,
            "hra": 11200.0,
            "allowance": 4500.0,
            "pf_percent": 12.0,
            "esi_percent": 0.75,
            "pt": 200.0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "emp_id": "EMP005",
            "name": "Vikram Singh",
            "department": "Operations",
            "designation": "Operations Manager",
            "join_date": "2020-11-15",
            "basic_salary": 38000.0,
            "hra": 15200.0,
            "allowance": 7000.0,
            "pf_percent": 12.0,
            "esi_percent": 0.75,
            "pt": 200.0,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.employees.insert_many(sample_employees)
    
    sample_attendance = [
        {
            "id": str(uuid.uuid4()),
            "emp_id": "EMP001",
            "month": "2025-01",
            "total_working_days": 22,
            "present_days": 20,
            "leave_days": 2,
            "lop_days": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "emp_id": "EMP002",
            "month": "2025-01",
            "total_working_days": 22,
            "present_days": 22,
            "leave_days": 0,
            "lop_days": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "emp_id": "EMP003",
            "month": "2025-01",
            "total_working_days": 22,
            "present_days": 19,
            "leave_days": 2,
            "lop_days": 1,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "emp_id": "EMP004",
            "month": "2025-01",
            "total_working_days": 22,
            "present_days": 21,
            "leave_days": 1,
            "lop_days": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "emp_id": "EMP005",
            "month": "2025-01",
            "total_working_days": 22,
            "present_days": 20,
            "leave_days": 1,
            "lop_days": 1,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.attendance.insert_many(sample_attendance)
    
    return {
        "message": "Sample data initialized successfully",
        "employees": len(sample_employees),
        "attendance_records": len(sample_attendance)
    }

@api_router.get("/")
async def root():
    return {"message": "HR & Payroll API is running"}

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
