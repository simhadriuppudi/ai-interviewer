// Report Page - Display Performance Results

const API_BASE = 'http://localhost:8000/api/v1';

// DOM Elements
const overallScoreEl = document.getElementById('overallScore');
const accuracyScoreEl = document.getElementById('accuracyScore');
const clarityScoreEl = document.getElementById('clarityScore');
const confidenceScoreEl = document.getElementById('confidenceScore');
const strengthsList = document.getElementById('strengthsList');
const weaknessesList = document.getElementById('weaknessesList');
const suggestionsList = document.getElementById('suggestionsList');
const summaryText = document.getElementById('summaryText');
const comparisonSection = document.getElementById('comparisonSection');
const previousScoreEl = document.getElementById('previousScore');
const currentScoreEl = document.getElementById('currentScore');
const improvementEl = document.getElementById('improvement');

// Load report data
async function loadReport() {
    // First try to get from session storage
    const reportData = sessionStorage.getItem('performanceReport');

    if (reportData) {
        displayReport(JSON.parse(reportData));
    } else {
        // Fetch from API
        const urlParams = new URLSearchParams(window.location.search);
        const interviewId = urlParams.get('id');

        if (!interviewId) {
            alert('No interview ID found');
            window.location.href = 'dashboard.html';
            return;
        }

        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`${API_BASE}/analytics/report/${interviewId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch report');
            }

            const data = await response.json();
            displayReport(data);

        } catch (error) {
            console.error('Error loading report:', error);
            alert('Failed to load report');
        }
    }
}

// Display report data
function displayReport(report) {
    // Overall score with animation
    animateScore(overallScoreEl, report.overall_score || 0);

    // Metrics
    animateScore(accuracyScoreEl, report.accuracy_score || 0, 10);
    animateScore(clarityScoreEl, report.clarity_score || 0, 10);
    animateScore(confidenceScoreEl, report.confidence_score || 0, 10);

    // Strengths
    if (report.strengths && report.strengths.length > 0) {
        strengthsList.innerHTML = report.strengths.map(s => `<li>${s}</li>`).join('');
    } else {
        strengthsList.innerHTML = '<li>No specific strengths identified</li>';
    }

    // Weaknesses
    if (report.weaknesses && report.weaknesses.length > 0) {
        weaknessesList.innerHTML = report.weaknesses.map(w => `<li>${w}</li>`).join('');
    } else {
        weaknessesList.innerHTML = '<li>No major weaknesses identified</li>';
    }

    // Suggestions
    if (report.improvements && report.improvements.length > 0) {
        suggestionsList.innerHTML = report.improvements.map(i => `<li>${i}</li>`).join('');
    } else {
        suggestionsList.innerHTML = '<li>Keep up the good work!</li>';
    }

    // Summary
    summaryText.textContent = report.summary || 'Great job completing the interview!';

    // Comparison
    if (report.comparison) {
        comparisonSection.style.display = 'block';
        previousScoreEl.textContent = report.comparison.previous_score.toFixed(1);
        currentScoreEl.textContent = report.comparison.current_score.toFixed(1);

        const improvement = report.comparison.improvement;
        const improvementText = improvement >= 0 ? `+${improvement.toFixed(1)}` : improvement.toFixed(1);
        improvementEl.textContent = improvementText;
        improvementEl.className = improvement >= 0 ? '' : 'negative';
    }
}

// Animate score counting
function animateScore(element, targetValue, maxValue = 100) {
    let currentValue = 0;
    const increment = targetValue / 50; // 50 steps
    const duration = 1500; // 1.5 seconds
    const stepTime = duration / 50;

    const timer = setInterval(() => {
        currentValue += increment;
        if (currentValue >= targetValue) {
            currentValue = targetValue;
            clearInterval(timer);
        }

        if (maxValue === 10) {
            element.textContent = currentValue.toFixed(1);
        } else {
            element.textContent = Math.round(currentValue);
        }
    }, stepTime);
}

// Download PDF report
async function downloadReport() {
    const urlParams = new URLSearchParams(window.location.search);
    const interviewId = urlParams.get('id') || sessionStorage.getItem('interviewId');

    if (!interviewId) {
        alert('No interview ID found');
        return;
    }

    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE}/report/download/${interviewId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to download report');
        }

        // Create blob and download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `interview_report_${interviewId}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

    } catch (error) {
        console.error('Error downloading report:', error);
        alert('Failed to download PDF report. This feature may not be fully implemented yet.');
    }
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = 'index.html';
}

// Load report on page load
document.addEventListener('DOMContentLoaded', loadReport);
