# HR & Payroll Dashboard - AI Assisted Employee Management System

A **HR & Payroll Management System** developed using **FastAPI + MongoDB + React**, designed to manage employees, attendance, payroll calculations, and basic AI-assisted HR tasks in one place.


## **Features**

### **1. Dashboard**

* Summary cards: **Total Employees, Departments, Average Salary, Average Attendance**
* Quick navigation: **Employee Master**, **Attendance**, **Payroll**, **AI Assistant**

### **2. Employee Master**

Complete employee table with full CRUD operations.

**Employee Fields:**

* Employee ID, Full Name
* Department, Designation
* Join Date
* Basic Salary, HRA, Allowance
* PF %, ESI %, Professional Tax (PT)

### **3. Attendance Management**

Monthly attendance tracker capturing:

* Total Working Days
* Present Days
* Leave Days
* LOP (Loss of Pay)

Attendance values directly impact payroll calculations.

### **4. Payroll Calculator & Payslip**

Calculate monthly payroll using employee salary structure + attendance.

**Calculates:**

* Gross Salary (adjusted for LOP)
* PF, ESI, Professional Tax deductions
* Total Deductions
* **Net Salary (Take-Home)**

Generates a **professional payslip** ready for download/print.

### **5. AI Assistant (Rule-Based)**

AI-inspired HR assistant with:

#### **Email Templates**

* Salary credit confirmation
* Leave approval email
* Leave rejection email
* Late-coming warning email

#### **HR Policy Generator**

* Leave policy (CL, SL, LOP)
* Basic payroll policy
* Work-from-home policy

#### **Formula & Logic Suggestions**

* PF, ESI calculation logic
* LOP deduction formula
* Gross-to-Net salary formulas

> Note: This module uses **rule-based templates** locally but is API-ready for OpenAI / Emergent / Gemini integration.


## **Tech Stack**

### **Frontend**

* React
* JavaScript / TypeScript
* CRACO
* Axios

### **Backend**

* FastAPI (Python)
* Uvicorn
* Motor (MongoDB async driver)

### **Database**

* MongoDB Community Server


## **Project Structure**

```
HR-PROJ/
├── backend/
│   ├── server.py          # FastAPI routes, models, MongoDB connection
│   ├── requirements.txt   # Python dependencies
│   └── .env               # Environment variables
└── frontend/
    ├── src/               # React components & pages
    ├── public/            # Static files
    ├── package.json       # Frontend dependencies
    └── .env               # Frontend environment configuration
```


## **Setup & Installation**

### **Prerequisites**

* Node.js (LTS)
* Python 3.10+
* MongoDB server running on: `mongodb://localhost:27017`



### **1. Clone the Repository**

```bash
git clone <your-repo-url>
cd "HR PROJ"
```


## Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in **backend**:

```
MONGO_URL="mongodb://localhost:27017"
DB_NAME="test_database"
CORS_ORIGINS="*"
EMERGENT_LLM_KEY=your-local-placeholder-key
```

Run the backend:

```bash
uvicorn server:app --reload
```

Backend runs at: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**



## Frontend Setup 

Open a second terminal:

```bash
cd frontend
npm install --legacy-peer-deps
```

Create a `.env` file in **frontend**:

```
REACT_APP_BACKEND_URL=http://127.0.0.1:8000
WDS_SOCKET_PORT=443
REACT_APP_ENABLE_VISUAL_EDITS=false
ENABLE_HEALTH_CHECK=false
```

Start the frontend:

```bash
npm start
```

Frontend runs at: **[http://localhost:3000](http://localhost:3000)**


## **How to Use**

### **1. Employee Master**

Add sample employees with salary structure, PF, ESI, PT values.

### **2. Attendance**

Add attendance month-wise:

* Working Days
* Present
* Leave
* LOP

### **3. Payroll & Payslip**

Choose employee + month → **Calculate Payroll** → view salary breakup & payslip.

### **4. AI Assistant**

Choose templates/policies → enter your prompt → generate output.


## 🎓 **Learning Outcomes**

* Implemented a mini-HRIS payroll workflow (PF, ESI, LOP, PT, Net Salary)
* Built async CRUD APIs using FastAPI + MongoDB
* Designed a modern React HR Dashboard UI
* Integrated a rule-based AI assistant with scalable API structure for LLMs


## **Dashboard Outcomes**

* Dashboard
* Employee Master
* Attendance
* Payroll Calculator
* Payslip
* AI Assistant


##  **Outcomes**

* Dashboard view
* Employee Master form
* Monthly attendance module
* Payroll computation
* Professional payslip
* HR AI Assistant

