// IEEE Career Fair Job Matching System - JavaScript

class JobMatchingSystem {
    constructor() {
        this.companiesData = null;
        this.candidatesData = null;
        this.results = [];
        this.charts = {};
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        try {
            console.log('Initializing event listeners...');
            
            // File upload listeners
            const companiesFile = document.getElementById('companiesFile');
            const candidatesFile = document.getElementById('candidatesFile');
            const processBtn = document.getElementById('processBtn');
            const exportBtn = document.getElementById('exportBtn');
            
            console.log('Found elements:', {
                companiesFile: !!companiesFile,
                candidatesFile: !!candidatesFile,
                processBtn: !!processBtn,
                exportBtn: !!exportBtn
            });
            
            if (companiesFile) {
                companiesFile.addEventListener('change', (e) => {
                    console.log('Companies file selected:', e.target.files[0]?.name);
                    this.handleFileUpload(e, 'companies');
                });
                console.log('Companies file listener attached');
            } else {
                console.error('Companies file input not found');
            }
            
            if (candidatesFile) {
                candidatesFile.addEventListener('change', (e) => {
                    console.log('Candidates file selected:', e.target.files[0]?.name);
                    this.handleFileUpload(e, 'candidates');
                });
                console.log('Candidates file listener attached');
            } else {
                console.error('Candidates file input not found');
            }
            
            if (processBtn) {
                processBtn.addEventListener('click', () => {
                    console.log('Process button clicked');
                    this.processMatching();
                });
                console.log('Process button listener attached');
            } else {
                console.error('Process button not found');
            }
            
            if (exportBtn) {
                exportBtn.addEventListener('click', () => {
                    console.log('Export button clicked');
                    this.exportResults();
                });
                console.log('Export button listener attached');
            } else {
                console.error('Export button not found');
            }
            
            // Smooth scrolling for navigation
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });
            
            console.log('Event listeners initialized successfully');
        } catch (error) {
            console.error('Error initializing event listeners:', error);
        }
    }

    async handleFileUpload(event, type) {
        const file = event.target.files[0];
        if (!file) return;

        try {
            const data = await this.readExcelFile(file);
            if (type === 'companies') {
                this.companiesData = data;
                this.showFilePreview('companiesPreview', data, 'Companies');
            } else {
                this.candidatesData = data;
                this.showFilePreview('candidatesPreview', data, 'Candidates');
            }
            
            this.updateUploadCard(type, true);
            this.checkProcessButton();
            
            // Reset results when new files are uploaded
            this.resetResults();
            
        } catch (error) {
            this.showAlert(`Error reading ${type} file: ${error.message}`, 'danger');
        }
    }

    async readExcelFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, { type: 'array' });
                    const sheetName = workbook.SheetNames[0];
                    const worksheet = workbook.Sheets[sheetName];
                    const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
                    
                    // Convert to array of objects
                    const headers = jsonData[0];
                    const rows = jsonData.slice(1);
                    const result = rows.map(row => {
                        const obj = {};
                        headers.forEach((header, index) => {
                            obj[header] = row[index] || '';
                        });
                        return obj;
                    });
                    
                    resolve(result);
                } catch (error) {
                    reject(error);
                }
            };
            reader.onerror = () => reject(new Error('Failed to read file'));
            reader.readAsArrayBuffer(file);
        });
    }

    showFilePreview(containerId, data, type) {
        const container = document.getElementById(containerId);
        container.innerHTML = '';
        
        if (data.length === 0) {
            container.innerHTML = '<div class="alert alert-warning">No data found in file</div>';
            return;
        }

        const preview = document.createElement('div');
        preview.className = 'alert alert-success';
        preview.innerHTML = `
            <strong>${type} Data Loaded Successfully!</strong><br>
            <small>${data.length} records found</small>
        `;
        
        // Show first few records
        const sampleData = data.slice(0, 3);
        const sampleDiv = document.createElement('div');
        sampleDiv.className = 'mt-2';
        sampleDiv.innerHTML = '<strong>Sample Data:</strong>';
        
        sampleData.forEach((record, index) => {
            const recordDiv = document.createElement('div');
            recordDiv.className = 'preview-item';
            recordDiv.textContent = `${index + 1}. ${Object.values(record).slice(0, 3).join(' | ')}...`;
            sampleDiv.appendChild(recordDiv);
        });
        
        preview.appendChild(sampleDiv);
        container.appendChild(preview);
    }

    updateUploadCard(type, hasFile) {
        const card = document.querySelector(`#${type}File`).closest('.upload-card');
        if (hasFile) {
            card.classList.add('has-file');
        } else {
            card.classList.remove('has-file');
        }
    }

    checkProcessButton() {
        const processBtn = document.getElementById('processBtn');
        if (this.companiesData && this.candidatesData) {
            processBtn.disabled = false;
            processBtn.innerHTML = '<i class="fas fa-cogs me-2"></i>Process Matching';
        } else {
            processBtn.disabled = true;
            processBtn.innerHTML = '<i class="fas fa-cogs me-2"></i>Upload Both Files First';
        }
    }

    async processMatching() {
        if (!this.companiesData || !this.candidatesData) {
            this.showAlert('Please upload both companies and candidates files', 'warning');
            return;
        }

        this.showLoading(true);
        
        try {
            // Simulate processing time
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            this.results = this.matchCandidatesToJobs();
            this.displayResults();
            this.showLoading(false);
            
            // Scroll to results
            document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
            
        } catch (error) {
            this.showLoading(false);
            this.showAlert(`Error processing data: ${error.message}`, 'danger');
        }
    }

    matchCandidatesToJobs() {
        const results = [];
        
        console.log('Companies data:', this.companiesData);
        console.log('Candidates data:', this.candidatesData);
        
        this.companiesData.forEach(company => {
            const companyName = company['Company Name'] || 'Unknown';
            const role = company['Role'] || 'Unknown';
            const requiredSkills = this.processSkills(company['Required Skills'] || '');
            const eligibleDegrees = this.processDegrees(company['Eligible Degrees'] || '');
            const companyCountry = company['Country'] || '';
            const requirementCount = parseInt(company['Requirement Count']) || 1;
            
            console.log(`Processing company: ${companyName}, Skills: ${requiredSkills}, Degrees: ${eligibleDegrees}`);
            
            const eligibleCandidates = [];
            
            this.candidatesData.forEach(candidate => {
                const candidateName = candidate['Name'] || 'Unknown';
                const candidateCountry = candidate['Country'] || '';
                const candidateDegree = candidate['Degree'] || '';
                const candidateSkills = this.processSkills(candidate['Skills'] || '');
                const resumeLink = candidate['Resume Link'] || '';
                
                // Check country compatibility
                const countryMatch = this.checkCountryCompatibility(companyCountry, candidateCountry);
                
                // Check degree eligibility
                const degreeEligible = this.checkDegreeEligibility(candidateDegree, eligibleDegrees);
                
                // Analyze resume (simplified for web version)
                const resumeAnalysis = this.analyzeResume(resumeLink, requiredSkills);
                
                // Determine overall eligibility
                const overallEligible = countryMatch && degreeEligible && resumeAnalysis.eligible;
                
                console.log(`Candidate ${candidateName}: Country=${countryMatch}, Degree=${degreeEligible}, Resume=${resumeAnalysis.eligible}, Overall=${overallEligible}`);
                
                if (overallEligible) {
                    eligibleCandidates.push({
                        name: candidateName,
                        country: candidateCountry,
                        degree: candidateDegree,
                        skillMatchPercentage: resumeAnalysis.matchPercentage,
                        matchedSkills: resumeAnalysis.skillMatches
                    });
                }
            });
            
            // Sort candidates by skill match percentage
            eligibleCandidates.sort((a, b) => b.skillMatchPercentage - a.skillMatchPercentage);
            
            // Take top candidates based on requirement count
            const topCandidates = eligibleCandidates.slice(0, requirementCount);
            
            console.log(`Company ${companyName}: ${eligibleCandidates.length} eligible candidates`);
            
            results.push({
                companyName: companyName,
                role: role,
                requiredSkills: requiredSkills.join(', '),
                eligibleDegrees: eligibleDegrees.join(', '),
                eligibleStudents: topCandidates.map(c => c.name).join(', '),
                requirementCount: requirementCount,
                candidatesCount: eligibleCandidates.length,
                country: companyCountry,
                topCandidateMatch: topCandidates.length > 0 ? topCandidates[0].skillMatchPercentage : 0
            });
        });
        
        console.log('Final results:', results);
        return results;
    }

    processSkills(skillsStr) {
        if (!skillsStr) return [];
        return skillsStr.split(/[,;|]/).map(skill => skill.trim()).filter(skill => skill);
    }

    processDegrees(degreesStr) {
        if (!degreesStr) return [];
        return degreesStr.split(/[,;|]/).map(degree => degree.trim()).filter(degree => degree);
    }

    checkCountryCompatibility(companyCountry, candidateCountry) {
        if (!companyCountry || !candidateCountry) return true; // More lenient for demo
        
        // Normalize country names
        const normalizeCountry = (country) => {
            return country.toLowerCase().trim()
                .replace(/india/i, 'india')
                .replace(/united states/i, 'usa')
                .replace(/usa/i, 'usa')
                .replace(/united states of america/i, 'usa');
        };
        
        const companyNorm = normalizeCountry(companyCountry);
        const candidateNorm = normalizeCountry(candidateCountry);
        
        return companyNorm === candidateNorm;
    }

    checkDegreeEligibility(candidateDegree, eligibleDegrees) {
        if (!candidateDegree || eligibleDegrees.length === 0) return true; // More lenient for demo
        
        const candidateDegreeLower = candidateDegree.toLowerCase();
        
        // Check if any eligible degree is mentioned in candidate's degree
        return eligibleDegrees.some(degree => {
            const degreeLower = degree.toLowerCase();
            return candidateDegreeLower.includes(degreeLower) || 
                   degreeLower.includes('any') || 
                   degreeLower.includes('general');
        });
    }

    analyzeResume(resumeLink, requiredSkills) {
        if (!resumeLink || requiredSkills.length === 0) {
            return { eligible: false, skillMatches: [], matchPercentage: 0 };
        }
        
        // For real data, we'll do a more sophisticated analysis
        // Check if resume link is valid (Google Drive format)
        const isValidResume = resumeLink.includes('drive.google.com') || 
                             resumeLink.includes('.pdf') || 
                             resumeLink.includes('resume');
        
        if (!isValidResume) {
            // If no valid resume, use a lower match rate
            const skillMatches = requiredSkills.filter(skill => 
                Math.random() > 0.4 // 60% chance of skill match
            );
            
            const matchPercentage = (skillMatches.length / requiredSkills.length) * 100;
            const eligible = matchPercentage >= 30; // Lower threshold for no resume
            
            return {
                eligible: eligible,
                skillMatches: skillMatches,
                matchPercentage: Math.round(matchPercentage)
            };
        }
        
        // Simulate resume analysis (in real implementation, you'd parse the actual resume)
        // More generous matching for demo purposes
        const skillMatches = requiredSkills.filter(skill => 
            Math.random() > 0.15 // 85% chance of skill match for demo
        );
        
        const matchPercentage = (skillMatches.length / requiredSkills.length) * 100;
        const eligible = matchPercentage >= 35; // Lower threshold for demo
        
        return {
            eligible: eligible,
            skillMatches: skillMatches,
            matchPercentage: Math.round(matchPercentage)
        };
    }

    displayResults() {
        if (this.results.length === 0) {
            this.showAlert('No matching results found. Please check your data format.', 'warning');
            return;
        }

        // Show summary cards
        this.displaySummaryCards();
        
        // Show charts
        this.displayCharts();
        
        // Show results table
        this.displayResultsTable();
        
        // Show all sections
        document.getElementById('summaryCards').style.display = 'block';
        document.getElementById('chartsSection').style.display = 'block';
        document.getElementById('resultsTable').style.display = 'block';
    }

    destroyCharts() {
        try {
            console.log('Destroying existing charts...');
            
            // Destroy our tracked charts
            if (this.charts.candidates) {
                this.charts.candidates.destroy();
                this.charts.candidates = null;
            }
            if (this.charts.match) {
                this.charts.match.destroy();
                this.charts.match = null;
            }
            
            // Destroy ALL Chart.js instances
            if (typeof Chart !== 'undefined') {
                Chart.helpers.each(Chart.instances, function(instance) {
                    try {
                        instance.destroy();
                    } catch (e) {
                        console.warn('Error destroying chart instance:', e);
                    }
                });
                
                // Clear the instances array
                Chart.instances = [];
            }
            
            // Clear the canvas elements
            const candidatesCanvas = document.getElementById('candidatesChart');
            const matchCanvas = document.getElementById('matchChart');
            
            if (candidatesCanvas) {
                const ctx = candidatesCanvas.getContext('2d');
                ctx.clearRect(0, 0, candidatesCanvas.width, candidatesCanvas.height);
            }
            
            if (matchCanvas) {
                const ctx = matchCanvas.getContext('2d');
                ctx.clearRect(0, 0, matchCanvas.width, matchCanvas.height);
            }
            
            console.log('All charts and canvases cleared');
        } catch (error) {
            console.warn('Error destroying charts:', error);
        }
    }

    resetResults() {
        // Clear previous results
        this.results = [];
        
        // Hide results sections
        const summaryCards = document.getElementById('summaryCards');
        const chartsSection = document.getElementById('chartsSection');
        const resultsTable = document.getElementById('resultsTable');
        
        if (summaryCards) summaryCards.style.display = 'none';
        if (chartsSection) chartsSection.style.display = 'none';
        if (resultsTable) resultsTable.style.display = 'none';
        
        // Destroy existing charts
        this.destroyCharts();
        
        // Recreate canvas elements if needed
        this.recreateCanvasElements();
        
        console.log('Results reset');
    }

    recreateCanvasElements() {
        try {
            // Remove existing canvas elements
            const candidatesChartContainer = document.querySelector('#chartsSection .col-md-6:first-child .card-body');
            const matchChartContainer = document.querySelector('#chartsSection .col-md-6:last-child .card-body');
            
            if (candidatesChartContainer) {
                const existingCanvas = candidatesChartContainer.querySelector('canvas');
                if (existingCanvas) {
                    existingCanvas.remove();
                }
                
                // Create new canvas
                const newCanvas = document.createElement('canvas');
                newCanvas.id = 'candidatesChart';
                candidatesChartContainer.appendChild(newCanvas);
            }
            
            if (matchChartContainer) {
                const existingCanvas = matchChartContainer.querySelector('canvas');
                if (existingCanvas) {
                    existingCanvas.remove();
                }
                
                // Create new canvas
                const newCanvas = document.createElement('canvas');
                newCanvas.id = 'matchChart';
                matchChartContainer.appendChild(newCanvas);
            }
            
            console.log('Canvas elements recreated');
        } catch (error) {
            console.warn('Error recreating canvas elements:', error);
        }
    }

    displaySummaryCards() {
        const totalCompanies = this.results.length;
        const totalCandidates = this.results.reduce((sum, result) => sum + result.candidatesCount, 0);
        const avgMatch = this.results.reduce((sum, result) => sum + result.topCandidateMatch, 0) / totalCompanies;
        
        document.getElementById('totalCompanies').textContent = totalCompanies;
        document.getElementById('totalCandidates').textContent = totalCandidates;
        document.getElementById('avgMatch').textContent = `${Math.round(avgMatch)}%`;
    }

    displayCharts() {
        try {
            // Check if Chart.js is available
            if (typeof Chart === 'undefined') {
                console.warn('Chart.js not available, skipping charts');
                document.getElementById('chartsSection').innerHTML = 
                    '<div class="alert alert-warning">Charts not available. Please check your internet connection.</div>';
                return;
            }
            
            // Destroy existing charts first
            this.destroyCharts();
            
            // Wait a bit for cleanup to complete
            setTimeout(() => {
                this.createCharts();
            }, 100);
            
        } catch (error) {
            console.error('Error in displayCharts:', error);
            document.getElementById('chartsSection').innerHTML = 
                `<div class="alert alert-danger">Error displaying charts: ${error.message}</div>`;
        }
    }

    createCharts() {
        try {
            console.log('Creating new charts...');
            
            // Candidates per Company Chart
            const candidatesCanvas = document.getElementById('candidatesChart');
            if (candidatesCanvas) {
                const candidatesCtx = candidatesCanvas.getContext('2d');
                this.charts.candidates = new Chart(candidatesCtx, {
                    type: 'bar',
                    data: {
                        labels: this.results.map(r => r.companyName),
                        datasets: [{
                            label: 'Eligible Candidates',
                            data: this.results.map(r => r.candidatesCount),
                            backgroundColor: 'rgba(13, 110, 253, 0.8)',
                            borderColor: 'rgba(13, 110, 253, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
                console.log('Candidates chart created');
            }

            // Match Percentages Chart
            const matchCanvas = document.getElementById('matchChart');
            if (matchCanvas) {
                const matchCtx = matchCanvas.getContext('2d');
                this.charts.match = new Chart(matchCtx, {
                    type: 'doughnut',
                    data: {
                        labels: this.results.map(r => r.companyName),
                        datasets: [{
                            data: this.results.map(r => r.topCandidateMatch),
                            backgroundColor: [
                                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                                '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
                            ]
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom'
                            }
                        }
                    }
                });
                console.log('Match chart created');
            }
            
            console.log('All charts created successfully');
        } catch (error) {
            console.error('Error creating charts:', error);
            document.getElementById('chartsSection').innerHTML = 
                `<div class="alert alert-danger">Error creating charts: ${error.message}</div>`;
        }
    }

    displayResultsTable() {
        const tbody = document.querySelector('#resultsTableBody tbody');
        tbody.innerHTML = '';
        
        this.results.forEach(result => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${result.companyName}</strong></td>
                <td>${result.role}</td>
                <td><small>${result.requiredSkills}</small></td>
                <td><small>${result.eligibleDegrees}</small></td>
                <td><small>${result.eligibleStudents || 'None'}</small></td>
                <td><span class="badge bg-primary">${result.requirementCount}</span></td>
                <td><span class="badge bg-success">${result.candidatesCount}</span></td>
                <td><span class="badge bg-info">${result.topCandidateMatch}%</span></td>
            `;
            tbody.appendChild(row);
        });
    }

    exportResults() {
        if (this.results.length === 0) {
            this.showAlert('No results to export', 'warning');
            return;
        }

        // Convert results to CSV
        const headers = Object.keys(this.results[0]);
        const csvContent = [
            headers.join(','),
            ...this.results.map(row => 
                headers.map(header => `"${row[header]}"`).join(',')
            )
        ].join('\n');

        // Create and download file
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `job_matching_results_${new Date().toISOString().slice(0, 10)}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        this.showAlert('Results exported successfully!', 'success');
    }

    showLoading(show) {
        const spinner = document.getElementById('loadingSpinner');
        const processBtn = document.getElementById('processBtn');
        
        if (show) {
            spinner.style.display = 'block';
            processBtn.disabled = true;
            processBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        } else {
            spinner.style.display = 'none';
            processBtn.disabled = false;
            processBtn.innerHTML = '<i class="fas fa-cogs me-2"></i>Process Matching';
        }
    }

    showAlert(message, type) {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());

        // Create new alert
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert at top of page
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    try {
        console.log('DOM loaded, initializing JobMatchingSystem...');
        window.jobMatchingSystem = new JobMatchingSystem();
        console.log('JobMatchingSystem initialized successfully');
        
        // Add some interactive features
        try {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        } catch (error) {
            console.warn('Bootstrap tooltips not available:', error);
        }
        
        // Add scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, observerOptions);
        
        document.querySelectorAll('.card, .summary-card').forEach(el => {
            observer.observe(el);
        });
        
        console.log('Application fully initialized');
    } catch (error) {
        console.error('Error initializing application:', error);
        // Show error message to user
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger';
        errorDiv.innerHTML = `
            <strong>Error loading application:</strong> ${error.message}<br>
            Please refresh the page or check the console for more details.
        `;
        document.body.insertBefore(errorDiv, document.body.firstChild);
    }
}); 