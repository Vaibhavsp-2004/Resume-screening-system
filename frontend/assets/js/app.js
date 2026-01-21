// Use relative URL for same-origin serving (production/docker), or hardcoded for specific dev ports
const API_URL = (window.location.port === '5500' || window.location.port === '3000')
    ? "http://127.0.0.1:8000"
    : "";

async function login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    try {
        const response = await fetch(`${API_URL}/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        });
        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('token', data.access_token);
            window.location.href = 'dashboard.html';
        } else {
            alert(data.detail);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Login failed');
    }
}

async function register(username, email, password) {
    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        });
        const data = await response.json();
        if (response.ok) {
            alert('Registration successful! Please login.');
            window.location.href = 'index.html';
        } else {
            alert(data.detail);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Registration failed');
    }
}

async function getJobs() {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_URL}/jobs/`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    if (!response.ok) {
        const err = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(err.detail || response.statusText);
    }
    return await response.json();
}

async function createJob(jobData) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_URL}/jobs/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jobData)
    });
    return await response.json();
}

async function uploadResume(jobId, file) {
    const token = localStorage.getItem('token');
    const formData = new FormData();
    formData.append('job_id', jobId);
    formData.append('file', file);

    const response = await fetch(`${API_URL}/resumes/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    });
    return await response.json();
}

async function getCandidates(jobId) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_URL}/resumes/${jobId}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return await response.json();
}

async function getJobDetails(jobId) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_URL}/jobs/${jobId}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return await response.json();
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = 'index.html';
}


async function deleteJob(jobId) {
    if (!confirm('Are you sure you want to delete this job?')) return;

    const token = localStorage.getItem('token');
    const response = await fetch(`${API_URL}/jobs/${jobId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (response.ok) {
        alert('Job deleted successfully');
        loadJobs();
    } else {
        alert('Failed to delete job');
    }
}

// Utility to check auth
function checkAuth() {
    if (!localStorage.getItem('token')) {
        window.location.href = 'index.html';
    }
}
