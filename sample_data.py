import pandas as pd
import numpy as np
from datetime import datetime

def create_sample_companies_data():
    """Create sample companies data"""
    companies_data = {
        'Company Name': [
            'TechCorp Inc',
            'DataFlow Solutions',
            'CloudTech Systems',
            'AI Innovations Ltd',
            'WebDev Pro',
            'MobileFirst Apps',
            'CyberSec Solutions',
            'FinTech Global'
        ],
        'Role': [
            'Software Engineer',
            'Data Scientist',
            'Cloud Architect',
            'Machine Learning Engineer',
            'Frontend Developer',
            'Mobile App Developer',
            'Security Analyst',
            'Financial Analyst'
        ],
        'Required Skills': [
            'Python, JavaScript, SQL, Git',
            'Python, R, SQL, Machine Learning, Statistics',
            'AWS, Azure, Docker, Kubernetes, Python',
            'Python, TensorFlow, PyTorch, Deep Learning, Statistics',
            'JavaScript, React, HTML, CSS, Git',
            'React Native, JavaScript, Mobile Development, Git',
            'Cybersecurity, Network Security, Python, Linux',
            'Excel, Financial Modeling, SQL, Python, Statistics'
        ],
        'Eligible Degrees': [
            'Computer Science, Software Engineering, Information Technology',
            'Computer Science, Data Science, Statistics, Mathematics',
            'Computer Science, Information Technology, Cloud Computing',
            'Computer Science, Data Science, Artificial Intelligence',
            'Computer Science, Web Development, Information Technology',
            'Computer Science, Mobile Development, Information Technology',
            'Computer Science, Cybersecurity, Information Technology',
            'Finance, Economics, Business Administration, Mathematics'
        ],
        'Country': [
            'USA',
            'Canada',
            'UK',
            'Germany',
            'USA',
            'India',
            'Australia',
            'Singapore'
        ],
        'Requirement Count': [3, 2, 1, 2, 4, 3, 2, 1]
    }
    
    return pd.DataFrame(companies_data)

def create_sample_candidates_data():
    """Create sample candidates data"""
    candidates_data = {
        'Name': [
            'John Smith',
            'Sarah Johnson',
            'Michael Chen',
            'Emily Davis',
            'David Wilson',
            'Lisa Brown',
            'Robert Taylor',
            'Jennifer Lee',
            'Christopher Garcia',
            'Amanda Martinez',
            'James Rodriguez',
            'Michelle Anderson',
            'Daniel Thompson',
            'Jessica White',
            'Matthew Harris'
        ],
        'Country': [
            'USA',
            'Canada',
            'USA',
            'UK',
            'Germany',
            'USA',
            'Australia',
            'Singapore',
            'USA',
            'Canada',
            'India',
            'UK',
            'Germany',
            'USA',
            'Australia'
        ],
        'Degree': [
            'Bachelor of Computer Science',
            'Master of Data Science',
            'Bachelor of Software Engineering',
            'Master of Computer Science',
            'Bachelor of Information Technology',
            'Master of Web Development',
            'Bachelor of Cybersecurity',
            'Master of Finance',
            'Bachelor of Computer Science',
            'Master of Statistics',
            'Bachelor of Mobile Development',
            'Master of Artificial Intelligence',
            'Bachelor of Cloud Computing',
            'Master of Business Administration',
            'Bachelor of Financial Technology'
        ],
        'Skills': [
            'Python, JavaScript, SQL, Git, React',
            'Python, R, SQL, Machine Learning, Statistics, TensorFlow',
            'Java, Python, SQL, Git, Spring Boot',
            'Python, JavaScript, SQL, Git, AWS',
            'Python, JavaScript, SQL, Git, Azure',
            'JavaScript, React, HTML, CSS, Git, Node.js',
            'Python, JavaScript, SQL, Git, Cybersecurity',
            'Excel, Financial Modeling, SQL, Python, Statistics',
            'Python, JavaScript, SQL, Git, Docker',
            'Python, R, SQL, Statistics, Tableau',
            'React Native, JavaScript, Mobile Development, Git',
            'Python, TensorFlow, PyTorch, Deep Learning, Statistics',
            'AWS, Azure, Docker, Kubernetes, Python',
            'Excel, Financial Modeling, SQL, Python, Business Analysis',
            'Python, JavaScript, SQL, Git, Financial Technology'
        ],
        'Resume Link': [
            'https://drive.google.com/file/d/sample_resume_1/view',
            'https://drive.google.com/file/d/sample_resume_2/view',
            'https://drive.google.com/file/d/sample_resume_3/view',
            'https://drive.google.com/file/d/sample_resume_4/view',
            'https://drive.google.com/file/d/sample_resume_5/view',
            'https://drive.google.com/file/d/sample_resume_6/view',
            'https://drive.google.com/file/d/sample_resume_7/view',
            'https://drive.google.com/file/d/sample_resume_8/view',
            'https://drive.google.com/file/d/sample_resume_9/view',
            'https://drive.google.com/file/d/sample_resume_10/view',
            'https://drive.google.com/file/d/sample_resume_11/view',
            'https://drive.google.com/file/d/sample_resume_12/view',
            'https://drive.google.com/file/d/sample_resume_13/view',
            'https://drive.google.com/file/d/sample_resume_14/view',
            'https://drive.google.com/file/d/sample_resume_15/view'
        ]
    }
    
    return pd.DataFrame(candidates_data)

def generate_sample_files():
    """Generate sample Excel files"""
    # Create sample data
    companies_df = create_sample_companies_data()
    candidates_df = create_sample_candidates_data()
    
    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save to Excel files
    companies_filename = f'sample_companies_{timestamp}.xlsx'
    candidates_filename = f'sample_candidates_{timestamp}.xlsx'
    
    companies_df.to_excel(companies_filename, index=False)
    candidates_df.to_excel(candidates_filename, index=False)
    
    print(f"✅ Sample files generated:")
    print(f"   - {companies_filename}")
    print(f"   - {candidates_filename}")
    
    return companies_filename, candidates_filename

if __name__ == "__main__":
    generate_sample_files() 