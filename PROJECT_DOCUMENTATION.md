# AI-Assisted HR & Payroll Dashboard

## 🎯 Project Overview

This is a **simple, effective, and scalable** HR & Payroll management system built with AI assistance. The system manages employee records, tracks attendance, calculates payroll with statutory deductions, and provides an AI assistant for HR tasks.

### ✨ Key Features

1. **Employee Master Database**
   - Manage employee records (Add, Edit, Delete)
   - Store basic details: ID, Name, Department, Designation, Join Date
   - Salary components: Basic, HRA, Allowance, PF%, ESI%, PT
   - **Sample Data**: Starts with 5 employees, easily expandable

2. **Attendance & Leave Tracking**
   - Monthly attendance records
   - Track Present Days, Leave Days, and LOP (Loss of Pay) days
   - Simple formula: Paid Days = Present + Leave
   - LOP days automatically deduct from salary

3. **Payroll Calculation**
   - Automatic monthly salary calculation
   - **Earnings**: Basic + HRA + Allowance (adjusted for LOP)
   - **Deductions**: 
     - PF (Provident Fund) - 12% of Basic
     - ESI (Employee State Insurance) - 0.75% of Gross
     - PT (Professional Tax) - Fixed ₹200
   - **Net Salary** = Gross Salary - Total Deductions

4. **Payslip Generation**
   - Professional payslip view for any employee/month
   - Shows earnings, deductions, and net salary
   - Print-friendly format

5. **AI Assistant** (Powered by Emergent LLM)
   - **HR Email Templates**: Generate salary credit, leave approval/rejection emails
   - **HR Policy Generation**: Create leave policies, payroll policies
   - **Formula Suggestions**: Get help with payroll calculations and logic
   - Uses **Emergent LLM Key** (universal key for OpenAI, Claude, Gemini)

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** (Python) - REST API
- **MongoDB** - NoSQL database for flexible data storage
- **Emergent Integrations** - AI integration library
- **Motor** - Async MongoDB driver

### Frontend
- **React 19** - Modern UI framework
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client for API calls
- **React Router** - Client-side routing

### AI Integration
- **Emergent LLM Key** - Universal key for multiple AI providers
- **OpenAI GPT-4o-mini** - AI model for text generation

---

## 📊 Database Schema

### Employees Collection
```json
{
  "id": "uuid",
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
  "created_at": "2025-12-06T..."
}
```

### Attendance Collection
```json
{
  "id": "uuid",
  "emp_id": "EMP001",
  "month": "2025-01",
  "total_working_days": 22,
  "present_days": 20,
  "leave_days": 2,
  "lop_days": 0,
  "created_at": "2025-12-06T..."
}
```

---

## 📡 API Endpoints

### Employee APIs
- `GET /api/employees` - Get all employees
- `GET /api/employees/{emp_id}` - Get single employee
- `POST /api/employees` - Create new employee
- `PUT /api/employees/{emp_id}` - Update employee
- `DELETE /api/employees/{emp_id}` - Delete employee

### Attendance APIs
- `GET /api/attendance` - Get all attendance records
- `GET /api/attendance/{emp_id}` - Get employee attendance
- `GET /api/attendance/{emp_id}/{month}` - Get specific month attendance
- `POST /api/attendance` - Create attendance record
- `PUT /api/attendance/{emp_id}/{month}` - Update attendance
- `DELETE /api/attendance/{emp_id}/{month}` - Delete attendance

### Payroll APIs
- `GET /api/payroll/{emp_id}/{month}` - Calculate payroll for employee/month

### AI Assistant APIs
- `POST /api/ai-assistant` - Generate AI responses
  ```json
  {
    "request_type": "email_template",  // or "policy" or "formula_suggestion"
    "context": "Your request description",
    "additional_info": "Optional extra details"
  }
  ```

### Utility APIs
- `POST /api/initialize-sample-data` - Initialize 5 sample employees
- `GET /api/` - Health check

---

## 💻 Payroll Calculation Logic

### Step-by-Step Calculation

1. **Get Employee Salary Components**
   - Basic Salary
   - HRA (House Rent Allowance)
   - Other Allowances

2. **Get Attendance Data**
   - Total Working Days
   - Present Days
   - Leave Days (Paid)
   - LOP Days (Loss of Pay)

3. **Calculate Paid Days**
   ```
   Paid Days = Present Days + Leave Days
   ```

4. **Adjust Salary for LOP**
   ```
   Daily Rate = (Basic + HRA + Allowance) / Total Working Days
   
   Adjusted Basic = Basic - (Basic / Total Working Days * LOP Days)
   Adjusted HRA = HRA - (HRA / Total Working Days * LOP Days)
   Adjusted Allowance = Allowance - (Allowance / Total Working Days * LOP Days)
   ```

5. **Calculate Gross Salary**
   ```
   Gross Salary = Adjusted Basic + Adjusted HRA + Adjusted Allowance
   ```

6. **Calculate Deductions**
   ```
   PF Deduction = Adjusted Basic × PF% (typically 12%)
   ESI Deduction = Gross Salary × ESI% (typically 0.75%)
   PT Deduction = Fixed amount (₹200)
   
   Total Deductions = PF + ESI + PT
   ```

7. **Calculate Net Salary**
   ```
   Net Salary = Gross Salary - Total Deductions
   ```

### Example Calculation

**Employee**: Rajesh Kumar (EMP001)
**Month**: January 2025

**Salary Components:**
- Basic: ₹40,000
- HRA: ₹16,000
- Allowance: ₹8,000

**Attendance:**
- Working Days: 22
- Present: 20
- Leave: 2
- LOP: 0

**Calculation:**
```
Paid Days = 20 + 2 = 22
Gross Salary = 40,000 + 16,000 + 8,000 = ₹64,000

PF = 40,000 × 12% = ₹4,800
ESI = 64,000 × 0.75% = ₹480
PT = ₹200

Total Deductions = 4,800 + 480 + 200 = ₹5,480

Net Salary = 64,000 - 5,480 = ₹58,520
```

---

## 🤖 AI Assistant Features

### 1. HR Email Templates
**Examples:**
- Salary credit notification
- Leave approval emails
- Leave rejection with reasons
- Warning emails for late coming
- Offer letters
- Salary revision letters

**How to use:**
1. Select "HR Email Templates"
2. Describe what email you need
3. AI generates professional email template
4. Copy and customize as needed

### 2. HR Policy Generation
**Examples:**
- Leave policy (CL, SL, LOP rules)
- Payroll policy
- Attendance policy
- Work from home policy
- Late coming policy

**How to use:**
1. Select "HR Policy Generation"
2. Specify policy type and requirements
3. AI creates comprehensive policy document
4. Review and adapt to your company

### 3. Formula & Logic Suggestions
**Examples:**
- PF calculation improvements
- ESI deduction explanation
- LOP formula validation
- Gross to net salary logic
- Bonus calculation suggestions

**How to use:**
1. Select "Formula & Logic Suggestions"
2. Describe your calculation question
3. AI provides explanation and suggestions
4. Implement recommended improvements

---

## 🚀 Getting Started

### Prerequisites
- Backend and Frontend services are already running
- MongoDB is configured and running
- Sample data is automatically initialized on first run

### Accessing the Application
1. Open your browser
2. Navigate to the frontend URL
3. The system will automatically initialize with 5 sample employees

### Initial Sample Employees
1. **EMP001** - Rajesh Kumar (Engineering)
2. **EMP002** - Priya Sharma (HR)
3. **EMP003** - Amit Patel (Finance)
4. **EMP004** - Sneha Reddy (Marketing)
5. **EMP005** - Vikram Singh (Operations)

All have attendance records for January 2025.

---

## 📝 Usage Guide

### Adding a New Employee
1. Go to "Employee Master" tab
2. Click "Add Employee"
3. Fill in all required fields
4. Click "Add Employee" to save

### Recording Attendance
1. Go to "Attendance" tab
2. Click "Add Attendance"
3. Select employee and month
4. Enter working days, present, leave, and LOP days
5. Click "Add Attendance" to save

### Calculating Payroll
1. Go to "Payroll & Payslip" tab
2. Select employee from dropdown
3. Select month
4. Click "Calculate Payroll"
5. View detailed payslip with all deductions
6. Click "Print Payslip" to print or save as PDF

### Using AI Assistant
1. Go to "AI Assistant" tab
2. Choose request type (Email/Policy/Formula)
3. Review example requests for inspiration
4. Enter your specific request
5. Add optional additional information
6. Click "Generate with AI"
7. Copy the generated response

---

## 🔑 Key Advantages

1. **Simple & Effective**
   - Clean, intuitive interface
   - Easy to understand and use
   - No unnecessary complexity

2. **Scalable Design**
   - Starts with 5 employees
   - Easily add more employees anytime
   - Database structure supports growth

3. **AI-Powered**
   - Emergent LLM integration
   - Professional HR content generation
   - Time-saving automation

4. **Practical Payroll**
   - Real-world salary components
   - Indian statutory deductions (PF, ESI, PT)
   - Accurate calculations

5. **Professional Output**
   - Clean payslips
   - Print-ready documents
   - Professional HR emails

---

## 📊 System Status

### Backend Status
- ✅ FastAPI server running on port 8001
- ✅ MongoDB connected and operational
- ✅ All API endpoints functional
- ✅ AI integration active with Emergent LLM key

### Frontend Status
- ✅ React app running and compiled
- ✅ All components loaded
- ✅ Responsive design implemented
- ✅ Connected to backend API

### Features Status
- ✅ Employee CRUD operations
- ✅ Attendance tracking
- ✅ Payroll calculation
- ✅ Payslip generation
- ✅ AI Assistant (Email/Policy/Formula)
- ✅ Sample data initialization

---

## 📝 Project Statement

**"I built a simple but effective HR & payroll model where I started with just a small sample list of employees and designed it in such a way that I can easily add more employees later."**

**"It manages basic employee details, attendance, and monthly salary calculation in one place. I also used an AI assistant (Emergent AI) to help me design the logic, draft HR policies, and create sample HR emails."**

**"The focus was on keeping it very simple, easy to maintain, and scalable. I didn't want something too complicated or unrealistic. I wanted a small, working model that clearly shows I understand HR and payroll basics and can extend it anytime."**

---

## 🌟 Highlights for Presentation

1. **Practical Approach**: Real-world HR & payroll scenario
2. **AI Integration**: Uses Emergent LLM (OpenAI) for intelligent assistance
3. **Scalable Design**: Starts small (5 employees) but built to grow
4. **Complete Solution**: Employee management + Attendance + Payroll + AI
5. **Professional UI**: Clean, modern interface with Tailwind CSS
6. **Working System**: Fully functional, tested, and ready to use

---

## 🔧 Technical Implementation

### Backend Architecture
- RESTful API design
- Async/await for database operations
- Pydantic models for data validation
- UUID-based IDs (no MongoDB ObjectID issues)
- Clean error handling

### Frontend Architecture
- Component-based React structure
- State management with useState/useEffect
- Responsive design with Tailwind
- Axios for API communication
- Clean separation of concerns

### AI Integration
- Emergent Integrations library
- OpenAI GPT-4o-mini model
- Context-aware prompts
- Structured request/response handling

---

## 🛡️ Security & Best Practices

- Environment variables for sensitive data
- CORS configuration for API security
- Input validation on both frontend and backend
- Clean data separation (no hardcoded values)
- UUID instead of sequential IDs

---

## 🎯 Conclusion

This HR & Payroll Dashboard demonstrates:
- **Understanding of HR/Payroll concepts**
- **Full-stack development skills**
- **AI integration capabilities**
- **Practical problem-solving approach**
- **Scalable system design**

The system is **simple, effective, and ready to extend** with more features as needed.

---

**Built with ❤️ using Emergent AI assistance**
