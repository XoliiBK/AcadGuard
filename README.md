# AcadGuard 🌱

I designed and built this system to stay on top of my final-year academics. With constant assessments, it was difficult to tell whether I was actually on track to reach my goals, before it was too late tp adjust.

AcadGuard is a web app that combines structured academic data with AI-driven analysis to track performance, calculate weighted outcomes, identify risk early, and generate actionable study guidance.

## What it does:
1.Grade tracking
  Add your degree, modules, and assessments with weights. Enter marks as they come in and your       weighted averages update automatically.

2.Risk detection
  Colour-coded dashboard highlights modules that are on track, at risk, or require immediate         attention.

3.Mark needed calculator
  Calculates exactly what you need in remaining assessments to reach your target — based on          current performance.

4.What-if simulator
  Test hypothetical marks for upcoming assessments and instantly see projected final outcomes.

5.AI risk report
  Processes structured academic data and generates a consistent, JSON-formatted risk analysis        using LLaMA 3.1 (via Groq API).
Outputs include:
-overall academic risk level
-module-by-module breakdown
-three prioritised weekly actions

6.Quiz generator
  Upload a past paper or paste content. The system generates multiple-choice questions with          explanations and immediate feedback.

7.Study tips
  Per-module AI guidance tailored to weak topics and performance trends.

8.Performance chart
  Grouped bar chart comparing current marks, targets, and pass thresholds — generated with           Matplotlib and rendered in-app.

## How it works
1. Setup wizard → add your degree, modules, and assessment weights
2. Enter marks as you receive them throughout the semester
3. Dashboard updates in real time (weighted averages, risk level, mark needed)
4. Run AI analysis anytime for a full risk report and study guidance
5. Use the what-if simulator to plan before assessments
6. Generate quizzes from past papers or a given topic when you need to test yourself

## Tech stack
Backend:  Python, Flask 
AI     : Groq API
Data handling : Pandas, NumPy, Matplotlib 
Frontend: HTML, CSS, JavaScript
Storage : CSV files(relational structure)
Security :Flask-Limiter, input sanitisation, file upload validation 
Config : python-dotenv

---

## Getting started
You'll need Python 3.9+ and a free Groq API key from [console.groq.com](https://console.groq.com)

git clone https://github.com/yourusername/acadguard.git
cd acadguard

# Set up virtual environment
python -m venv venv

# Activate environment
venv\Scripts\activate.bat    # Windows
source venv/bin/activate      # Mac/Linux

pip install -r requirements.txt


Create a `.env` file in the root folder:

GROQ_API_KEY=your_key_here

Then run:
python app.py


Then open 
http://localhost:5000` and go through the setup wizard.


## Data structure
AcadGuard uses CSV files as a lightweight relational database:

degree.csv        - id, name, goal  
modules.csv       - id, degree_id, name  
assessments.csv   -  id, module_id, name, weight, mark, max_mark  

Data flows through a simple ETL pipeline:
Pandas handles extraction/loading
NumPy performs weighted calculations and risk scoring

## Security
This is a local-first application and not production-ready yet. Current protections include:
Input sanitisation across all forms
File upload validation (.txt, .pdf)
Rate limiting on AI endpoints (Flask-Limiter)

Planned upgrades before deployment:
Authentication system
Migration from CSV to SQLite

## What I learned
- FLASK routing and REST APIs
- Designing a data model without a database and making it actually work
- ETL thinking — structuring data flow properly instead of just reading and writing files
- Prompt engineering for structured outputs — getting consistent JSON back from an LLM takes         iteration
- NumPy for real math - weighted averages, dot products, clipping — not just array basics
-Treating security as a core concern, even in small applications

## What's missing / what's next
- Authentication system (highest priority)
- SQLite integration for scalability
- Improved PDF parsing for quiz generation
- Assessment reminders and notifications
- Time-based performance tracking (progress over semester)
- Agentic layer for proactive AI-driven recommendations

## Status
Fully functional v1 with core features implemented.  
Built as a learning-focused project and not yet production-ready.

What it looks like :
<img width="1910" height="910" alt="Screenshot 2026-03-20 084018" src="https://github.com/user-attachments/assets/2c8f7345-7d2e-4556-8244-5ac4192e2ed3" />
<img width="1891" height="907" alt="Screenshot 2026-03-20 084910" src="https://github.com/user-attachments/assets/2917ff30-e40e-4c2d-9c58-4bfadd13a802" />
<img width="1905" height="892" alt="Screenshot 2026-03-20 115638" src="https://github.com/user-attachments/assets/46198842-3c18-49f4-b069-af16bcbfd667" />
