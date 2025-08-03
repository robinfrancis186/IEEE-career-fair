import pandas as pd
import numpy as np
from datetime import datetime

def convert_company_requirements(input_file, output_file):
    """Convert company requirements Excel to our expected format"""
    print(f"Converting company requirements from {input_file}...")
    
    # Read the original file
    df = pd.read_excel(input_file)
    
    # Map the columns to our expected format
    converted_data = []
    
    for index, row in df.iterrows():
        try:
            # Extract relevant information
            company_name = row.get('Name of the Company', 'Unknown')
            job_roles = row.get('Job Roles (Junior Analyst, Software Engineering Trainee, Graduate Engineering Trainee etc.). Incase of multiple roles, please add it in the single line separated with comma.  ', '')
            required_skills = row.get('Please mention if you are looking for any specific skill sets, please add it in the single line separated with comma.  ', '')
            education_qualification = row.get('Could you please mention the education qualification of candidates you are looking for', '')
            country = row.get('Company/Organization country', '')
            openings = row.get('No of Total Openings', 1)
            
            # Clean and process the data
            if pd.isna(company_name) or company_name == '':
                company_name = f"Company_{index + 1}"
            
            if pd.isna(job_roles) or job_roles == '':
                job_roles = 'General Role'
            
            if pd.isna(required_skills) or required_skills == '':
                required_skills = 'General Skills'
            
            if pd.isna(education_qualification) or education_qualification == '':
                education_qualification = 'Any Degree'
            
            if pd.isna(country) or country == '':
                country = 'India'
            
            if pd.isna(openings) or openings == '':
                openings = 1
            
            # Create the converted row
            converted_row = {
                'Company Name': company_name,
                'Role': job_roles,
                'Required Skills': required_skills,
                'Eligible Degrees': education_qualification,
                'Country': country,
                'Requirement Count': int(openings) if isinstance(openings, (int, float)) else 1
            }
            
            converted_data.append(converted_row)
            
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            continue
    
    # Create the converted DataFrame
    converted_df = pd.DataFrame(converted_data)
    
    # Save to new file
    converted_df.to_excel(output_file, index=False)
    print(f"Converted {len(converted_data)} company records to {output_file}")
    
    return converted_df

def convert_student_registrations(input_file, output_file):
    """Convert student registrations Excel to our expected format"""
    print(f"Converting student registrations from {input_file}...")
    
    # Read the original file
    df = pd.read_excel(input_file)
    
    # Map the columns to our expected format
    converted_data = []
    
    for index, row in df.iterrows():
        try:
            # Extract relevant information
            full_name = row.get('Full Name', 'Unknown')
            country = row.get(' Country', '')  # Note the space before 'Country'
            if pd.isna(country) or country == '':
                country = row.get('Country', '')  # Try without space
            
            field_of_study = row.get('Field of Study (Specialization /Department)\nPlease mention your UG and PG study details', '')
            highest_qualification = row.get('Highest academic qualification', '')
            technical_skills = row.get('Please mention your technical skills', '')
            resume_link = row.get('Please upload your recent resume', '')
            
            # Clean and process the data
            if pd.isna(full_name) or full_name == '':
                full_name = f"Student_{index + 1}"
            
            if pd.isna(country) or country == '':
                country = 'India'
            
            if pd.isna(field_of_study) or field_of_study == '':
                field_of_study = 'General Studies'
            
            if pd.isna(highest_qualification) or highest_qualification == '':
                highest_qualification = 'Bachelor Degree'
            
            if pd.isna(technical_skills) or technical_skills == '':
                technical_skills = 'General Skills'
            
            if pd.isna(resume_link) or resume_link == '':
                resume_link = 'https://drive.google.com/sample_resume'
            
            # Create the converted row
            converted_row = {
                'Name': full_name,
                'Country': country,
                'Degree': f"{highest_qualification} in {field_of_study}",
                'Skills': technical_skills,
                'Resume Link': resume_link
            }
            
            converted_data.append(converted_row)
            
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            continue
    
    # Create the converted DataFrame
    converted_df = pd.DataFrame(converted_data)
    
    # Save to new file
    converted_df.to_excel(output_file, index=False)
    print(f"Converted {len(converted_data)} student records to {output_file}")
    
    return converted_df

def main():
    """Main function to convert both files"""
    print("IEEE Career Fair Data Converter")
    print("=" * 40)
    
    # Convert company requirements
    company_input = "Detailed Company Requirements - IEEE Career Fair (Responses).xlsx"
    company_output = "converted_companies.xlsx"
    
    if pd.io.common.file_exists(company_input):
        companies_df = convert_company_requirements(company_input, company_output)
        print(f"✅ Company requirements converted successfully!")
        print(f"   - Input: {company_input}")
        print(f"   - Output: {company_output}")
        print(f"   - Records: {len(companies_df)}")
    else:
        print(f"❌ Company requirements file not found: {company_input}")
    
    print()
    
    # Convert student registrations
    student_input = "IEEE R10 Career Fair - Student Registration (Responses).xlsx"
    student_output = "converted_candidates.xlsx"
    
    if pd.io.common.file_exists(student_input):
        candidates_df = convert_student_registrations(student_input, student_output)
        print(f"✅ Student registrations converted successfully!")
        print(f"   - Input: {student_input}")
        print(f"   - Output: {student_output}")
        print(f"   - Records: {len(candidates_df)}")
    else:
        print(f"❌ Student registrations file not found: {student_input}")
    
    print()
    print("🎯 Conversion complete! You can now use the converted files in the job matching system:")
    print(f"   - Companies: {company_output}")
    print(f"   - Candidates: {student_output}")

if __name__ == "__main__":
    main() 