const API_BASE = "http://localhost:8000/api/v1";

async function apiRequest(endpoint, method = "GET", body = null, isFileUpload = false) {
    const headers = {};
    if (!isFileUpload) {
        headers["Content-Type"] = "application/json";
    }

    const token = localStorage.getItem("token");
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const config = {
        method,
        headers
    };

    if (body) {
        config.body = isFileUpload ? body : JSON.stringify(body);
    }

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, config);

        if (response.status === 401) {
            localStorage.removeItem("token");
            window.location.href = "login.html";
            return null;
        }

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "API Request Failed");
        }

        return await response.json();
    } catch (error) {
        console.error("API Request Error:", error);
        throw error;
    }
}

async function loginUser(email, password) {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem("token", data.access_token);
            return true;
        } else {
            const err = await response.json();
            alert(err.detail || "Login failed");
            return false;
        }
    } catch (e) {
        console.error(e);
        alert("Connection error");
        return false;
    }
}

async function registerUser(email, password, fullName) {
    return await apiRequest("/auth/register", "POST", {
        email,
        password,
        full_name: fullName
    });
}
