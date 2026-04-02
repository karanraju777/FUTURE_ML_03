from flask import Flask, request, render_template
import pickle
import re
import PyPDF2
import io

app = Flask(__name__)

# Load your models - Ensure these .pkl files are in the same folder as app.py
clf = pickle.load(open('rf_classifier_categorization.pkl', 'rb'))
tfidf = pickle.load(open('tfidf_vectorizer_categorization.pkl', 'rb'))


def clean_resume(txt):
    cleanText = re.sub('http\S+\s*', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub('#\S+', ' ', cleanText)
    cleanText = re.sub('@\S+', ' ', cleanText)
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
    cleanText = re.sub(r'\s+', ' ', cleanText)
    return cleanText.strip()


def extract_phone(text):
    pattern = re.compile(r'\b\d{10}\b|\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
    match = pattern.search(text)
    return match.group() if match else "Not Found"


def extract_email(text):
    pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    match = pattern.search(text)
    return match.group() if match else "Not Found"


@app.route('/')
def home():
    return render_template('resume.html')


@app.route('/pred', methods=['POST'])
def predict():
    if 'resume' in request.files:
        file = request.files['resume']
        job_desc = request.form.get('job_description', '').lower()

        # 1. Read PDF/Text
        if file.filename.endswith('.pdf'):
            pdf_file = io.BytesIO(file.read())
            reader = PyPDF2.PdfReader(pdf_file)
            raw_text = ""
            for page in reader.pages:
                content = page.extract_text()
                if content: raw_text += content
        else:
            raw_text = file.read().decode('utf-8', errors='ignore')

        if not raw_text.strip():
            return "Error: Could not extract text. Please use a digital (non-scanned) PDF."

        # 2. Information Extraction
        email = extract_email(raw_text)
        phone = extract_phone(raw_text)
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
        name = lines[0] if lines else "Candidate"

        # 3. AI Categorization & Keyword Rules (20+ Categories)
        cleaned_resume = clean_resume(raw_text).lower()
        vectorized_text = tfidf.transform([cleaned_resume])
        prediction = clf.predict(vectorized_text)[0]

        category_rules = {
            'DATA SCIENCE': ['python', 'machine learning', 'data science', 'pandas', 'scikit', 'deep learning'],
            'HR': ['recruitment', 'payroll', 'onboarding', 'human resources', 'sourcing'],
            'ADVOCATE': ['legal', 'court', 'lawyer', 'advocate', 'litigation', 'justice'],
            'WEB DESIGNING': ['html', 'css', 'javascript', 'bootstrap', 'ui/ux', 'photoshop', 'figma'],
            'MECHANICAL ENGINEER': ['autocad', 'solidworks', 'mechanical', 'thermodynamics', 'cad'],
            'SALES': ['sales', 'lead generation', 'business development', 'marketing', 'retail'],
            'JAVA DEVELOPER': ['java', 'spring boot', 'hibernate', 'j2ee', 'maven'],
            'BUSINESS ANALYST': ['business analyst', 'requirement gathering', 'user stories', 'agile'],
            'AUTOMATION TESTING': ['selenium', 'automation testing', 'testng', 'cucumber', 'qa automation'],
            'ELECTRICAL ENGINEERING': ['electrical', 'circuit', 'power system', 'matlab', 'plc'],
            'PYTHON DEVELOPER': ['django', 'flask', 'fastapi', 'backend', 'api development'],
            'DEVOPS ENGINEER': ['docker', 'kubernetes', 'jenkins', 'aws', 'azure', 'ansible', 'terraform'],
            'NETWORK SECURITY ENGINEER': ['firewall', 'network security', 'cybersecurity', 'cisco', 'ccna'],
            'DATABASE': ['sql', 'mysql', 'mongodb', 'oracle', 'database administrator', 'dba'],
            'DOTNET DEVELOPER': ['dotnet', 'c#', 'asp.net', 'entity framework', 'visual studio'],
            'TESTING': ['manual testing', 'black box', 'test cases', 'qa', 'defect tracking'],
            'OPERATIONS MANAGER': ['operations manager', 'supply chain', 'logistics', 'process improvement'],
            'PMO': ['pmo', 'project management', 'governance', 'stakeholder', 'portfolio'],
            'HEALTH AND FITNESS': ['fitness', 'gym', 'trainer', 'nutrition', 'yoga', 'workout'],
            'CIVIL ENGINEER': ['construction', 'civil engineering', 'surveying', 'site engineer', 'autocad civil']
        }

        for category, keywords in category_rules.items():
            if any(word in cleaned_resume for word in keywords):
                if prediction == "ARTS": prediction = category
                break

                # 4. Ranking & Skill Matching
        required_skills = [s.strip().lower() for s in job_desc.split(',') if s.strip()]
        found_skills = [skill for skill in required_skills if skill in cleaned_resume]
        missing_skills = [skill for skill in required_skills if skill not in cleaned_resume]

        match_score = int((len(found_skills) / len(required_skills)) * 100) if required_skills else 0
        rank = "Top Tier" if match_score >= 80 else "Mid Tier" if match_score >= 50 else "Lower Tier"

        return render_template('resume.html', prediction=prediction, match_score=match_score,
                               name=name, email=email, phone=phone, rank=rank,
                               found=found_skills, missing=missing_skills)
    return render_template('resume.html')


if __name__ == '__main__':
    app.run(debug=True)