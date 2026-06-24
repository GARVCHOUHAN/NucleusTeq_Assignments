// Base API URL for all authentication and user-related requests
const BASE_URL = 'http://localhost:8080/api';

/**
 * Authenticates user using Basic Authentication.
 * Password validation is handled by the backend through Spring Security.
 */
async function loginUser(email, password) {
    // Encode credentials in Base64 format (Basic Auth)
    const token = 'Basic ' + btoa(email + ':' + password);

    // Send request with Authorization header
    const res = await fetch(`${BASE_URL}/auth/me`, {
        headers: { 'Authorization': token }
    });

    // Handle authentication errors
    if (res.status === 401 || res.status === 403) {
        throw new Error('Invalid email or password.');
    }

    // Handle server-side errors
    if (!res.ok) {
        throw new Error('Server error. Please try again later.');
    }

    const json = await res.json();

    const user = (json && json.hasOwnProperty('data')) ? json.data : json;

    // Validate response structure
    if (!user || !user.email) {
        throw new Error('Unexpected response from server.');
    }

    return user;
}

/**
 * Stores authenticated session details in localStorage
 * Includes email, token, and full user object
 */
function saveSession(email, password, user) {
    localStorage.setItem('rh_email',    email);
    localStorage.setItem('rh_token',    btoa(email + ':' + password));
    localStorage.setItem('rh_user',     JSON.stringify(user));
}

/**
 * Retrieves logged-in user session from localStorage
 */
function getSession() {
    const raw = localStorage.getItem('rh_user');
    return raw ? JSON.parse(raw) : null;
}

/**
 * Retrieves stored authentication token for API usage
 */
function getAuthToken() {
    return localStorage.getItem('rh_token') || '';
}

/**
 * Redirects user to appropriate dashboard based on role
 */
function redirectByRole(role) {
    const pages = {
        ADMIN:    'admin.html',
        MANAGER:  'manager.html',
        EMPLOYEE: 'employee.html',
    };

    const target = pages[role];
    if (target) {
        window.location.href = target;
    } else {
        throw new Error('Unknown role: ' + role);
    }
}

/**
 * Route guard to restrict page access based on role
 * - Redirects to login if not authenticated
 * - Redirects to correct dashboard if role mismatch
 */
function guardPage(expectedRole) {
    const user = getSession();

    // If no session, redirect to login page
    if (!user) {
        window.location.href = 'index.html';
        return;
    }

    // If role mismatch, redirect to correct page
    if (user.role !== expectedRole) {
        redirectByRole(user.role);
    }
}

/**
 * Populates sidebar UI with user details
 * Includes name, email, and avatar initials
 */
function populateSidebar() {
    const user = getSession();
    if (!user) return;

    const nameEl   = document.getElementById('sidebarName');
    const emailEl  = document.getElementById('sidebarEmail');
    const avatarEl = document.getElementById('sidebarAvatar');

    if (nameEl)   nameEl.textContent   = user.name  || 'User';
    if (emailEl)  emailEl.textContent  = user.email || '';
    if (avatarEl) avatarEl.textContent = initials(user.name || 'U');
}

/**
 * Clears session data and redirects to login page
 */
function logout() {
    localStorage.removeItem('rh_email');
    localStorage.removeItem('rh_token');
    localStorage.removeItem('rh_user');
    window.location.href = 'index.html';
}

/**
 * Generates initials from user's name
 * Example: "Shubham Nema" → "SN"
 */
function initials(name) {
    return String(name)
        .split(' ')
        .slice(0, 2)
        .map(w => w[0])
        .join('')
        .toUpperCase();
}
