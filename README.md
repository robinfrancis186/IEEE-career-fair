# 🎯 IEEE Career Fair - Job Matching System

A modern web application that intelligently matches candidates with job opportunities using Excel data analysis, country compatibility checks, and resume analysis.

## 🌐 Live Demo

**Visit the live application:** [IEEE Career Fair Job Matching System](https://robinfrancis186.github.io/IEEE-career-fair/)

## ✨ Features

- **📁 Excel File Upload**: Drag-and-drop interface for uploading companies and candidates data
- **🌍 Country Compatibility**: Automatic verification of company-candidate country matches
- **📄 Resume Analysis**: Smart analysis of Google Drive resume links for skill matching
- **🎯 Intelligent Matching**: Advanced algorithm considering skills, degrees, and location
- **📊 Interactive Dashboard**: Real-time visualizations with Chart.js
- **📈 Analytics**: Comprehensive statistics and detailed breakdowns
- **💾 Export Results**: Download matching results as CSV files
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile devices

## 🚀 Quick Start

1. **Visit the application**: Go to [https://robinfrancis186.github.io/IEEE-career-fair/](https://robinfrancis186.github.io/IEEE-career-fair/)

2. **Upload your data**:
   - Upload companies Excel file
   - Upload candidates Excel file

3. **Process matching**: Click "Process Matching" to analyze data

4. **View results**: Explore interactive charts and detailed results

5. **Export data**: Download results as CSV for further analysis

## 📋 Data Format Requirements

### Companies Excel File
| Column | Description | Example |
|--------|-------------|---------|
| Company Name | Name of the company | "TechCorp Inc" |
| Role | Job position title | "Software Engineer" |
| Required Skills | Comma-separated skills | "Python, JavaScript, SQL, Git" |
| Eligible Degrees | Comma-separated degrees | "Computer Science, Software Engineering" |
| Country | Company location | "USA" |
| Requirement Count | Number of candidates needed | 3 |

### Candidates Excel File
| Column | Description | Example |
|--------|-------------|---------|
| Name | Candidate's full name | "John Smith" |
| Country | Candidate's country | "USA" |
| Degree | Educational qualification | "Bachelor of Computer Science" |
| Skills | Comma-separated skills | "Python, JavaScript, SQL, Git, React" |
| Resume Link | Google Drive link to resume | "https://drive.google.com/..." |

## 🔧 How It Works

### Matching Algorithm
The system considers a candidate eligible if **ALL** criteria are met:

1. **🌍 Country Match**: Company and candidate must be from the same country
2. **🎓 Degree Eligibility**: Candidate's degree must match required qualifications
3. **💼 Skill Match**: At least 60% of required skills found in resume
4. **📄 Resume Analysis**: Resume content must be accessible and analyzable

### Processing Steps
1. **Data Validation**: System validates uploaded Excel files
2. **Country Check**: Verifies geographical compatibility
3. **Degree Matching**: Compares educational qualifications
4. **Resume Analysis**: Extracts and analyzes resume content
5. **Skill Matching**: Calculates skill match percentages
6. **Ranking**: Sorts candidates by match quality
7. **Results Generation**: Creates comprehensive reports

## 📊 Output Format

The system generates detailed results including:

- **Company Name**: Name of the company
- **Role**: Job position
- **Required Skills**: Skills required for the position
- **Eligible Degrees**: Acceptable educational qualifications
- **Eligible Students (Partial List)**: Top matching candidates
- **Requirement Count**: Number of candidates needed
- **Candidates Count**: Total number of eligible candidates found
- **Top Candidate Match %**: Skill match percentage of the best candidate

## 🎨 User Interface

### Modern Design
- **Bootstrap 5**: Latest responsive framework
- **Font Awesome**: Beautiful icons throughout
- **Chart.js**: Interactive data visualizations
- **Custom CSS**: Smooth animations and transitions

### Interactive Features
- **File Upload Preview**: See data before processing
- **Real-time Validation**: Instant feedback on data format
- **Progress Indicators**: Visual feedback during processing
- **Responsive Charts**: Interactive bar and doughnut charts
- **Export Functionality**: One-click CSV download

## 🛠️ Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5.3.0
- **Charts**: Chart.js
- **File Processing**: SheetJS (XLSX)
- **Icons**: Font Awesome 6.4.0
- **Hosting**: GitHub Pages

## 📁 Project Structure

```
IEEE-career-fair/
├── index.html          # Main application page
├── styles.css          # Custom CSS styles
├── script.js           # JavaScript functionality
├── README.md           # Project documentation
├── sample_data.py      # Sample data generator
├── job_matching_system.py  # Streamlit version (backup)
└── requirements.txt    # Python dependencies
```

## 🚀 Deployment

This application is hosted on **GitHub Pages** and automatically deploys from the main branch.

### Local Development
To run the application locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/robinfrancis186/IEEE-career-fair.git
   cd IEEE-career-fair
   ```

2. **Open in browser**:
   - Simply open `index.html` in your web browser
   - Or use a local server: `python -m http.server 8000`

3. **For Python version** (Streamlit):
   ```bash
   pip install -r requirements.txt
   streamlit run job_matching_system.py
   ```

## 📝 Sample Data

Generate sample Excel files for testing:

```bash
python sample_data.py
```

This creates:
- `sample_companies_[timestamp].xlsx`
- `sample_candidates_[timestamp].xlsx`

## 🔍 Troubleshooting

### Common Issues

1. **File Upload Errors**:
   - Ensure files are `.xlsx` or `.xls` format
   - Check column names match exactly
   - Verify file is not corrupted

2. **No Matching Results**:
   - Check country names match exactly
   - Verify degree names are similar
   - Ensure resume links are accessible

3. **Browser Compatibility**:
   - Use modern browsers (Chrome, Firefox, Safari, Edge)
   - Enable JavaScript
   - Allow file uploads

### Performance Tips

- Use smaller Excel files for faster processing
- Ensure resume links are accessible
- Close other browser tabs to free up memory

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow existing code style
- Add comments for complex logic
- Test thoroughly before submitting
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **IEEE**: For inspiring this career fair matching system
- **Bootstrap**: For the excellent UI framework
- **Chart.js**: For beautiful data visualizations
- **SheetJS**: For Excel file processing capabilities

## 📞 Support

For support or questions:

1. **Check the troubleshooting section** above
2. **Review the data format requirements**
3. **Open an issue** on GitHub
4. **Contact the maintainer** through GitHub

---

**Made with ❤️ for IEEE Career Fair**

**Live Demo**: [https://robinfrancis186.github.io/IEEE-career-fair/](https://robinfrancis186.github.io/IEEE-career-fair/) 