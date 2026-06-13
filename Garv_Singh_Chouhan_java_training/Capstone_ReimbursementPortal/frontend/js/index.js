
/* ── Handle login form submission ── */
document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const email    = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    const errBox   = document.getElementById('loginError');

    // Hide any previous errors
    errBox.style.display = 'none';

    // Show loading state on button
    setLoginLoading(true);

    try {
        // Attempt to fetch the current user using Basic Auth
        const user = await loginUser(email, password);

        // Save credentials and user info to localStorage
        saveSession(email, password, user);

        // Redirect based on role
        redirectByRole(user.role);

    } catch (err) {
        errBox.textContent  = err.message || 'Invalid email or password. Please try again.';
        errBox.style.display = 'block';
    } finally {
        setLoginLoading(false);
    }
});

function setLoginLoading(on) {
    document.getElementById('loginBtn').disabled         = on;
    document.getElementById('loginSpinner').style.display = on ? 'inline-block' : 'none';
}