import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import requests
import re
from typing import List, Dict, Tuple
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

class JobMatchingSystem:
    def __init__(self):
        self.companies_data = None
        self.candidates_data = None
        self.resume_data = {}
        
    def load_excel_file(self, uploaded_file) -> pd.DataFrame:
        """Load Excel file and return DataFrame"""
        try:
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            elif uploaded_file.name.endswith('.xls'):
                df = pd.read_excel(uploaded_file, engine='xlrd')
            else:
                st.error("Please upload an Excel file (.xlsx or .xls)")
                return None
            return df
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return None
    
    def extract_resume_from_drive(self, drive_link: str) -> str:
        """Extract resume content from Google Drive link"""
        try:
            # Extract file ID from Google Drive link
            file_id_match = re.search(r'/d/([a-zA-Z0-9-_]+)', drive_link)
            if file_id_match:
                file_id = file_id_match.group(1)
                # For now, return placeholder content
                # In production, you'd use Google Drive API to extract actual content
                return f"Resume content from Drive ID: {file_id}"
            else:
                return "Invalid Drive link format"
        except Exception as e:
            return f"Error extracting resume: {str(e)}"
    
    def analyze_resume_eligibility(self, resume_content: str, required_skills: List[str]) -> Dict:
        """Analyze resume for skill matches and eligibility"""
        if not resume_content or resume_content == "Invalid Drive link format":
            return {"eligible": False, "skill_matches": [], "match_percentage": 0}
        
        # Convert skills to lowercase for comparison
        resume_lower = resume_content.lower()
        required_skills_lower = [skill.lower().strip() for skill in required_skills]
        
        # Find matching skills
        skill_matches = []
        for skill in required_skills_lower:
            if skill in resume_lower:
                skill_matches.append(skill)
        
        # Calculate match percentage
        match_percentage = (len(skill_matches) / len(required_skills_lower)) * 100 if required_skills_lower else 0
        
        # Consider eligible if at least 60% skills match
        eligible = match_percentage >= 60
        
        return {
            "eligible": eligible,
            "skill_matches": skill_matches,
            "match_percentage": round(match_percentage, 2)
        }
    
    def check_country_compatibility(self, company_country: str, candidate_country: str) -> bool:
        """Check if company and candidate are from the same country"""
        if pd.isna(company_country) or pd.isna(candidate_country):
            return False
        return company_country.strip().lower() == candidate_country.strip().lower()
    
    def process_skills(self, skills_str: str) -> List[str]:
        """Process skills string into list of individual skills"""
        if pd.isna(skills_str):
            return []
        
        # Split by common delimiters
        skills = re.split(r'[,;|]', str(skills_str))
        # Clean up each skill
        skills = [skill.strip() for skill in skills if skill.strip()]
        return skills
    
    def process_degrees(self, degrees_str: str) -> List[str]:
        """Process degrees string into list of individual degrees"""
        if pd.isna(degrees_str):
            return []
        
        # Split by common delimiters
        degrees = re.split(r'[,;|]', str(degrees_str))
        # Clean up each degree
        degrees = [degree.strip() for degree in degrees if degree.strip()]
        return degrees
    
    def match_candidates_to_jobs(self) -> pd.DataFrame:
        """Match candidates to job requirements and return results"""
        if self.companies_data is None or self.candidates_data is None:
            return pd.DataFrame()
        
        results = []
        
        for _, company_row in self.companies_data.iterrows():
            company_name = company_row.get('Company Name', 'Unknown')
            role = company_row.get('Role', 'Unknown')
            required_skills = self.process_skills(company_row.get('Required Skills', ''))
            eligible_degrees = self.process_degrees(company_row.get('Eligible Degrees', ''))
            company_country = company_row.get('Country', '')
            requirement_count = company_row.get('Requirement Count', 1)
            
            eligible_candidates = []
            
            for _, candidate_row in self.candidates_data.iterrows():
                candidate_name = candidate_row.get('Name', 'Unknown')
                candidate_country = candidate_row.get('Country', '')
                candidate_degree = candidate_row.get('Degree', '')
                candidate_skills = self.process_skills(candidate_row.get('Skills', ''))
                resume_link = candidate_row.get('Resume Link', '')
                
                # Check country compatibility
                country_match = self.check_country_compatibility(company_country, candidate_country)
                
                # Check degree eligibility
                degree_eligible = False
                if candidate_degree and eligible_degrees:
                    candidate_degree_lower = candidate_degree.lower()
                    degree_eligible = any(degree.lower() in candidate_degree_lower for degree in eligible_degrees)
                
                # Analyze resume if available
                resume_analysis = {"eligible": False, "skill_matches": [], "match_percentage": 0}
                if resume_link:
                    resume_content = self.extract_resume_from_drive(resume_link)
                    resume_analysis = self.analyze_resume_eligibility(resume_content, required_skills)
                
                # Determine overall eligibility
                overall_eligible = (
                    country_match and 
                    degree_eligible and 
                    resume_analysis["eligible"]
                )
                
                if overall_eligible:
                    eligible_candidates.append({
                        "name": candidate_name,
                        "country": candidate_country,
                        "degree": candidate_degree,
                        "skill_match_percentage": resume_analysis["match_percentage"],
                        "matched_skills": resume_analysis["skill_matches"]
                    })
            
            # Sort candidates by skill match percentage
            eligible_candidates.sort(key=lambda x: x["skill_match_percentage"], reverse=True)
            
            # Take top candidates based on requirement count
            top_candidates = eligible_candidates[:requirement_count]
            
            results.append({
                "Company Name": company_name,
                "Role": role,
                "Required Skills": ", ".join(required_skills),
                "Eligible Degrees": ", ".join(eligible_degrees),
                "Eligible Students (Partial List)": ", ".join([c["name"] for c in top_candidates]),
                "Requirement Count": requirement_count,
                "Candidates Count": len(eligible_candidates),
                "Country": company_country,
                "Top Candidate Match %": top_candidates[0]["skill_match_percentage"] if top_candidates else 0
            })
        
        return pd.DataFrame(results)

def main():
    st.set_page_config(
        page_title="Job Matching System",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 Job Matching System")
    st.markdown("Compare Excel sheets to match candidates with job requirements")
    
    # Initialize system
    if 'matching_system' not in st.session_state:
        st.session_state.matching_system = JobMatchingSystem()
    
    matching_system = st.session_state.matching_system
    
    # Sidebar for file uploads
    st.sidebar.header("📁 Upload Files")
    
    # Upload companies Excel file
    companies_file = st.sidebar.file_uploader(
        "Upload Companies Excel File",
        type=['xlsx', 'xls'],
        help="Excel file containing company job requirements"
    )
    
    # Upload candidates Excel file
    candidates_file = st.sidebar.file_uploader(
        "Upload Candidates Excel File", 
        type=['xlsx', 'xls'],
        help="Excel file containing candidate information"
    )
    
    # Load data
    if companies_file:
        matching_system.companies_data = matching_system.load_excel_file(companies_file)
        if matching_system.companies_data is not None:
            st.sidebar.success(f"✅ Companies data loaded: {len(matching_system.companies_data)} records")
    
    if candidates_file:
        matching_system.candidates_data = matching_system.load_excel_file(candidates_file)
        if matching_system.candidates_data is not None:
            st.sidebar.success(f"✅ Candidates data loaded: {len(matching_system.candidates_data)} records")
    
    # Main content area
    if matching_system.companies_data is not None and matching_system.candidates_data is not None:
        st.header("📊 Data Preview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Companies Data")
            st.dataframe(matching_system.companies_data.head())
        
        with col2:
            st.subheader("Candidates Data")
            st.dataframe(matching_system.candidates_data.head())
        
        # Run matching
        if st.button("🚀 Run Job Matching Analysis", type="primary"):
            with st.spinner("Analyzing job-candidate matches..."):
                results_df = matching_system.match_candidates_to_jobs()
                
                if not results_df.empty:
                    st.header("📈 Matching Results")
                    
                    # Display results table
                    st.dataframe(results_df, use_container_width=True)
                    
                    # Download results
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"job_matching_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
                    # Visualizations
                    st.header("📊 Analytics Dashboard")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Candidates count by company
                        fig_candidates = px.bar(
                            results_df,
                            x="Company Name",
                            y="Candidates Count",
                            title="Eligible Candidates per Company",
                            color="Candidates Count",
                            color_continuous_scale="viridis"
                        )
                        fig_candidates.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig_candidates, use_container_width=True)
                    
                    with col2:
                        # Top candidate match percentage
                        fig_match = px.bar(
                            results_df,
                            x="Company Name",
                            y="Top Candidate Match %",
                            title="Top Candidate Skill Match %",
                            color="Top Candidate Match %",
                            color_continuous_scale="plasma"
                        )
                        fig_match.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig_match, use_container_width=True)
                    
                    # Summary statistics
                    st.subheader("📋 Summary Statistics")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Companies", len(results_df))
                    
                    with col2:
                        st.metric("Total Candidates", results_df["Candidates Count"].sum())
                    
                    with col3:
                        avg_candidates = results_df["Candidates Count"].mean()
                        st.metric("Avg Candidates/Company", f"{avg_candidates:.1f}")
                    
                    with col4:
                        avg_match = results_df["Top Candidate Match %"].mean()
                        st.metric("Avg Top Match %", f"{avg_match:.1f}%")
                    
                    # Detailed analysis
                    st.header("🔍 Detailed Analysis")
                    
                    for _, row in results_df.iterrows():
                        with st.expander(f"📋 {row['Company Name']} - {row['Role']}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write("**Company Details:**")
                                st.write(f"- Role: {row['Role']}")
                                st.write(f"- Country: {row['Country']}")
                                st.write(f"- Required Skills: {row['Required Skills']}")
                                st.write(f"- Eligible Degrees: {row['Eligible Degrees']}")
                                st.write(f"- Requirement Count: {row['Requirement Count']}")
                            
                            with col2:
                                st.write("**Matching Results:**")
                                st.write(f"- Total Eligible Candidates: {row['Candidates Count']}")
                                st.write(f"- Top Candidate Match: {row['Top Candidate Match %']}%")
                                st.write(f"- Selected Candidates: {row['Eligible Students (Partial List)']}")
                
                else:
                    st.warning("No matching results found. Please check your data format.")
    
    else:
        st.info("👆 Please upload both companies and candidates Excel files to begin analysis.")
        
        # Sample data format
        st.header("📋 Expected Data Format")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Companies Excel Format")
            st.markdown("""
            **Required Columns:**
            - Company Name
            - Role
            - Required Skills (comma-separated)
            - Eligible Degrees (comma-separated)
            - Country
            - Requirement Count
            """)
        
        with col2:
            st.subheader("Candidates Excel Format")
            st.markdown("""
            **Required Columns:**
            - Name
            - Country
            - Degree
            - Skills (comma-separated)
            - Resume Link (Google Drive)
            """)

if __name__ == "__main__":
    main() 