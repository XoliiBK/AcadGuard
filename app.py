# app.py - FIXED VERSION
from flask import Flask, render_template, request, jsonify, redirect
import google.generativeai as genai
import csv
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
app = Flask(__name__)

# Gemini setup
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    print("✅ Gemini API ready")
else:
    print("⚠️  No API key - using demo mode")

# CSV file for data
DATA_FILE = 'data.csv'

# ========== HELPER FUNCTIONS ==========
def init_csv():
    """Create CSV file if it doesn't exist"""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'course_name', 'modules', 'test1', 'test2', 'test3', 'final', 'goal', 'risk_score'])

def save_course(course_name, modules, goal=75):
    """Save course to CSV"""
    init_csv()
    
    # Count existing courses for ID
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        lines = sum(1 for _ in f)
    
    course_id = lines  # First course gets ID 1 (0 is header)
    
    with open(DATA_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Ensure all values are strings, not None
        writer.writerow([
            str(course_id), 
            str(course_name), 
            str(modules), 
            "0",  # test1
            "0",  # test2
            "0",  # test3
            "0",  # final
            str(goal), 
            "50"  # risk_score
        ])
    
    return course_id

def get_courses():
    """Get all courses from CSV - FIXED to handle None values"""
    if not os.path.exists(DATA_FILE):
        return []
    
    courses = []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)  # Read header
        
        if not headers:
            return []
        
        for row in reader:
            if len(row) < len(headers):
                # Pad row with empty strings if too short
                row += [''] * (len(headers) - len(row))
            
            # Create dictionary with defaults for all headers
            course_dict = {}
            for i, header in enumerate(headers):
                value = row[i] if i < len(row) else ''
                course_dict[header] = str(value).strip() if value is not None else ''
            
            courses.append(course_dict)
    
    return courses

def update_marks(course_id, test1, test2, test3, final):
    """Update marks for a course"""
    if not os.path.exists(DATA_FILE):
        return False
    
    # Read all data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = reader.fieldnames
    
    # Update the course
    updated = False
    for row in rows:
        if row['id'] == str(course_id):
            # Ensure values are strings, not None
            row['test1'] = str(test1) if test1 is not None else "0"
            row['test2'] = str(test2) if test2 is not None else "0"
            row['test3'] = str(test3) if test3 is not None else "0"
            row['final'] = str(final) if final is not None else "0"
            updated = True
            break
    
    # Save back
    if updated:
        with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for row in rows:
                # Clean each row before writing
                cleaned_row = {}
                for key, value in row.items():
                    if value is None:
                        cleaned_row[key] = ""
                    else:
                        cleaned_row[key] = str(value)
                writer.writerow(cleaned_row)
    
    return updated

def calculate_risk(test1, test2, test3, final, goal):
    """Simple risk calculation - FIXED to handle strings"""
    try:
        # Convert to numbers, handle empty strings
        t1 = float(test1) if test1 and test1.strip() else 0
        t2 = float(test2) if test2 and test2.strip() else 0
        t3 = float(test3) if test3 and test3.strip() else 0
        f = float(final) if final and final.strip() else 0
        g = float(goal) if goal and goal.strip() else 75
        
        # Average of tests (60%) + final (40%)
        test_avg = (t1 + t2 + t3) / 3 if (t1 + t2 + t3) > 0 else 0
        current_score = (test_avg * 0.6) + (f * 0.4)
        
        # Simple risk: how close to goal?
        if current_score >= g:
            risk = 10  # Low risk (10% chance of failing)
        else:
            # Higher gap = higher risk
            gap = g - current_score
            risk = min(90, 30 + (gap * 2))
        
        return int(risk), int(current_score)
    except:
        return 50, 0

def get_ai_advice(course_name, modules, marks):
    """Get simple AI advice"""
    try:
        if not api_key:
            return "Study regularly and practice past papers. Ask for help if needed."
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Course: {course_name}
        Modules: {modules}
        Current marks: Test1={marks['test1']}%, Test2={marks['test2']}%, Test3={marks['test3']}%, Final={marks['final']}%
        
        Give 2 simple suggestions to improve. Be specific to these modules.
        Keep it under 50 words.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except:
        return "Focus on your weakest topics. Practice regularly."

# ========== ROUTES ==========
@app.route('/')
def home():
    """Main dashboard"""
    courses = get_courses()
    if not courses:
        return redirect('/setup')
    return render_template('index.html', courses=courses)

@app.route('/setup')
def setup():
    """Setup wizard"""
    return render_template('setup.html')

@app.route('/add-course', methods=['POST'])
def add_course():
    """Add a new course"""
    data = request.json
    course_name = data.get('course_name', 'Course')
    modules = data.get('modules', 'Module 1, Module 2')
    goal = data.get('goal', 75)
    
    course_id = save_course(course_name, modules, goal)
    
    return jsonify({
        'success': True,
        'course_id': course_id,
        'message': 'Course added!'
    })

@app.route('/update-marks', methods=['POST'])
def update_course_marks():
    """Update marks for a course"""
    data = request.json
    course_id = data.get('course_id')
    test1 = data.get('test1', 0)
    test2 = data.get('test2', 0)
    test3 = data.get('test3', 0)
    final = data.get('final', 0)
    
    if update_marks(course_id, test1, test2, test3, final):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Course not found'})

@app.route('/get-analysis', methods=['POST'])
def get_analysis():
    """Get risk analysis for a course"""
    data = request.json
    course_id = data.get('course_id')
    
    courses = get_courses()
    course = None
    for c in courses:
        if c['id'] == str(course_id):
            course = c
            break
    
    if not course:
        return jsonify({'success': False, 'error': 'Course not found'})
    
    # Calculate risk
    risk, current_score = calculate_risk(
        course.get('test1', '0'), 
        course.get('test2', '0'), 
        course.get('test3', '0'), 
        course.get('final', '0'),
        course.get('goal', '75')
    )
    
    # Get AI advice
    marks = {
        'test1': course.get('test1', '0'),
        'test2': course.get('test2', '0'),
        'test3': course.get('test3', '0'),
        'final': course.get('final', '0')
    }
    advice = get_ai_advice(course.get('course_name', 'Course'), course.get('modules', ''), marks)
    
    # Determine risk level
    if risk <= 30:
        risk_level = 'low'
        risk_text = '🟢 LOW RISK'
    elif risk <= 60:
        risk_level = 'medium'
        risk_text = '🟡 MEDIUM RISK'
    else:
        risk_level = 'high'
        risk_text = '🔴 HIGH RISK'
    
    return jsonify({
        'success': True,
        'risk_score': risk,
        'risk_level': risk_level,
        'risk_text': risk_text,
        'current_score': current_score,
        'goal': course.get('goal', '75'),
        'ai_advice': advice,
        'pass_chance': 100 - risk  # Simple: inverse of risk
    })

# ========== FIX CSV FILE ==========
def fix_csv_file():
    """Fix existing CSV file if it has None values"""
    if not os.path.exists(DATA_FILE):
        return
    
    # Read and clean the CSV
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = reader.fieldnames
    
    # Clean all rows
    cleaned_rows = []
    for row in rows:
        cleaned_row = {}
        for key in headers:
            value = row.get(key)
            if value is None or str(value).strip() == 'None':
                cleaned_row[key] = ""
            else:
                cleaned_row[key] = str(value).strip()
        cleaned_rows.append(cleaned_row)
    
    # Write back
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(cleaned_rows)
    
    print("✅ CSV file cleaned and fixed")

# ========== RUN APP ==========
if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎓 AEGIS ACADEMIC - FIXED VERSION")
    print("="*50)
    
    # Fix CSV file first
    fix_csv_file()
    
    print("📊 Dashboard: http://localhost:5000")
    print("📝 Setup: http://localhost:5000/setup")
    print("="*50 + "\n")
    
    init_csv()  # Create CSV file
    app.run(debug=True, port=5000)