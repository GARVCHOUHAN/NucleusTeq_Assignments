// Base URL for all API requests
const API_BASE = 'http://localhost:8080/api';

/**
 * Generates standard headers for API requests.
 * Includes Basic Authentication token and JSON content type.
 * Allows additional headers to be merged if provided.
 */
function authHeaders(extra = {}) {
    return {
        'Authorization': 'Basic ' + getAuthToken(),
        'Content-Type':  'application/json',
        ...extra,
    };
}

/**
 * Generic API handler for all HTTP requests.
 * - Attaches headers
 * - Handles error responses gracefully
 * - Parses JSON response if applicable
 * - Unwraps standardized API response (StandardAPIResponse)
 */
async function apiFetch(path, options = {}) {
    const res = await fetch(API_BASE + path, {
        ...options,
        headers: authHeaders(options.headers || {}),
    });

    // Handle non-success HTTP responses
    if (!res.ok) {
        let msg = `Request failed (${res.status})`;
        try {
            const errBody = await res.json();
            msg = errBody.message || msg;
        } catch (_) {}
        throw new Error(msg);
    }

    // Handle empty or non-JSON responses
    const contentType = res.headers.get('content-type') || '';
    if (res.status === 204 || !contentType.includes('application/json')) {
        return null;
    }

    const json = await res.json();

    // Extract actual payload from StandardAPIResponse wrapper
    return (json && json.hasOwnProperty('data')) ? json.data : json;
}

/**
 * API handler for public endpoints that do not require Basic Auth.
 */
async function publicApiFetch(path, options = {}) {
    const res = await fetch(API_BASE + path, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...(options.headers || {}),
        },
    });

    if (!res.ok) {
        let msg = `Request failed (${res.status})`;
        try {
            const errBody = await res.json();
            msg = errBody.message || msg;
        } catch (_) {}
        throw new Error(msg);
    }

    const json = await res.json();
    return (json && json.hasOwnProperty('data')) ? json.data : json;
}

function toQuery(params = {}) {
    const query = Object.entries(params)
        .filter(([, value]) => value !== undefined && value !== null && value !== '')
        .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
        .join('&');
    return query ? `?${query}` : '';
}

function pageContent(payload) {
    return Array.isArray(payload) ? payload : (payload && payload.content) || [];
}


// USER API METHODS

/**
 * Fetch all users
 */
async function getAllUsers() {
    return apiFetch('/users');
}

/**
 * Fetch user details by ID
 */
async function getUserById(id) {
    return apiFetch(`/users/${id}`);
}

/**
 * Fetch the currently authenticated user.
 */
async function getCurrentUserApi() {
    return apiFetch('/auth/me');
}

/**
 * Create a new user
 */
async function createUserApi(payload) {
    return apiFetch('/users', {
        method: 'POST',
        body:   JSON.stringify(payload),
    });
}

/**
 * Public signup for creating an account from the login screen.
 */
async function signupUserApi(payload) {
    const options = {
        method: 'POST',
        body:   JSON.stringify(payload),
    };

    try {
        return await publicApiFetch('/auth/signup', options);
    } catch (err) {
        // Older running backend builds may not have /auth/signup until restarted.
        if (String(err.message || '').includes('No static resource')) {
            return publicApiFetch('/users', options);
        }
        throw err;
    }
}

/**
 * Delete a user by ID
 */
async function deleteUserApi(id) {
    return apiFetch(`/users/${id}`, { method: 'DELETE' });
}

/**
 * Assign or clear manager for an employee.
 */
async function assignManagerApi(employeeId, managerId) {
    const query = managerId ? `?managerId=${encodeURIComponent(managerId)}` : '';
    try {
        return await apiFetch(`/users/${employeeId}/manager${query}`, { method: 'PUT' });
    } catch (err) {
        if (String(err.message || '').includes('No static resource')) {
            throw new Error('Backend is still running an older build. Restart Spring Boot and try again.');
        }
        throw err;
    }
}

/**
 * Fetch users assigned to a specific manager
 */
async function getUsersByManager(managerId) {
    return apiFetch(`/users/manager/${managerId}`);
}


// CLAIM API METHODS


/**
 * Fetch all reimbursement claims
 */
async function getAllClaims(params = {}) {
    return apiFetch('/claims' + toQuery(params));
}

/**
 * Fetch claims submitted by a specific employee
 */
async function getClaimsByEmployee(employeeId, params = {}) {
    return apiFetch(`/claims/employee/${employeeId}` + toQuery(params));
}

/**
 * Fetch claims assigned to a reviewer/manager
 */
async function getClaimsByReviewer(reviewerId, params = {}) {
    return apiFetch(`/claims/reviewer/${reviewerId}` + toQuery(params));
}

/**
 * Fetch claims filtered by status
 */
async function getClaimsByStatus(status, params = {}) {
    return apiFetch(`/claims/status/${status}` + toQuery(params));
}

/**
 * Submit a new reimbursement claim
 */
async function submitClaimApi(payload) {
    return apiFetch('/claims', {
        method: 'POST',
        body:   JSON.stringify(payload),
    });
}

/**
 * Perform action on a claim (Approve/Reject)
 * reviewerId is passed as a path variable as per backend design
 */
async function takeClaimAction(claimId, reviewerId, status, comment = '') {
    return apiFetch(`/claims/${claimId}/action/${reviewerId}`, {
        method: 'PUT',
        body:   JSON.stringify({ status, comment }),
    });
}


// UTILITY FUNCTIONS


/**
 * Escapes HTML characters to prevent XSS attacks
 */
function esc(str) {
    return String(str)
        .replace(/&/g,  '&amp;')
        .replace(/</g,  '&lt;')
        .replace(/>/g,  '&gt;')
        .replace(/"/g,  '&quot;')
        .replace(/'/g,  '&#39;');
}

/**
 * Displays toast notification messages in the UI
 * type: info | success | error
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<div class="toast-dot"></div><span>${esc(message)}</span>`;
    container.appendChild(toast);

    // Auto-remove toast after 4 seconds
    setTimeout(() => toast.remove(), 4000);
}

/**
 * Toggles loading state for buttons with spinner
 */
function setButtonLoading(btnId, spinnerId, loading) {
    const btn     = document.getElementById(btnId);
    const spinner = document.getElementById(spinnerId);
    if (!btn || !spinner) return;

    btn.disabled          = loading;
    spinner.style.display = loading ? 'inline-block' : 'none';
}

/**
 * Predefined color palette for user avatars
 */
const AVATAR_COLORS = [
    '#4e7f69', '#4f72a0', '#9e7035',
    '#7a6090', '#b84d57', '#3a7272',
];

/**
 * Generates a consistent avatar color based on user's name
 */
function avatarColor(name) {
    const idx = String(name).charCodeAt(0) % AVATAR_COLORS.length;
    return AVATAR_COLORS[idx];
}

function formatDate(value) {
    if (!value) return 'NA';
    return new Date(value + 'T00:00:00').toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: '2-digit',
    });
}

/**
 * Formats numeric amount into Indian currency format
 */
function formatCurrency(amount) {
    return '₹' + Number(amount).toLocaleString('en-IN');
}
