AI Resume Screening & Candidate Ranking System

​About This Project
​AI-Driven Screening: Automates candidate evaluation using a Random Forest classifier and TF-IDF vectorization for 25+ professional categories.
​Information Extraction: Uses NLP & Regex to automatically capture Name, Email, and Phone from digital PDF resumes.
​Candidate Ranking: Employs a proprietary scoring algorithm to rank candidates into Top, Mid, or Lower Tiers based on JD match.
​Skill Gap Analysis: Directly identifies and highlights Missing Skills in red, providing instant feedback for HR decision-making.
​Hybrid Intelligence: Combines Machine Learning with Heuristic Rule-Based logic to ensure 100% accuracy and eliminate model bias.

​Final Year Project - BCA 6th Semester (Task 3)
​This project is an automated recruitment solution that leverages Machine Learning to screen resumes, categorize them into professional fields, and rank candidates based on their alignment with specific job requirements.
​ Task 3: Key Features & Deliverables
​As per the requirements for Task 3: Resume / Candidate Screening System, this application implements:
​ Resume Text Cleaning & Parsing: Uses advanced Regular Expressions (Regex) to remove noise (URLs, special characters, extra spaces) from raw PDF/TXT data.
​ Skill Extraction: Automatically identifies technical and soft skills from the uploaded resume.
 Candidate Ranking: Proprietary scoring logic that assigns a rank (Top Tier, Mid Tier, or Lower Tier) based on a percentage match with the Job Description.
​ Skill Gap Identification: A specialized "Gap Analysis" feature that lists Missing Skills in red, helping recruiters understand exactly what a candidate lacks.

​ Machine Learning & Logic
​The system uses a Hybrid Intelligence approach to ensure high accuracy:
​The Model: A Random Forest Classifier trained on thousands of data points to categorize resumes into 25+ distinct professional fields.
​Vectorization: Employs TF-IDF (Term Frequency-Inverse Document Frequency) to understand the importance of specific technical keywords.
​Bias Correction: Includes a custom Keyword Mapping Logic to override model bias (specifically fixing the "Arts" category bug), ensuring technical resumes are classified correctly based on tools like Python, Java, or SQL.
​Information Extraction: Uses Natural Language Processing (NLP) patterns to extract the candidate's Name, Email, and Phone Number automatically.

​🛠️ Technical Stack
​Programming Language & Core
​Python 3.11+ (Primary Development Language)
​Flask (Web Framework for Backend Deployment)
​Machine Learning & Data Science Libraries
​Scikit-learn (sklearn): Used for TF-IDF Vectorization and Random Forest Modeling.
​Joblib / Pickle: For model serialization and loading.
​NumPy & Pandas: For data handling and array manipulations.
​Text Processing & Utilities
​PyPDF2: For high-speed PDF text extraction.
​Re (Regular Expressions): For advanced text cleaning, URL removal, and entity extraction (Phone/Email).
​IO: For handling in-memory file streams during PDF uploads.
​Frontend & UI
​HTML5 & CSS3
​Bootstrap 5: For a responsive, mobile-friendly HR dashboard.
​Jinja2: Flask’s templating engine for dynamic data rendering.
