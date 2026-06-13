document.getElementById('signupForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const name     = document.getElementById('signupName').value.trim();
    const email    = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value;
    const role     = document.getElementById('signupRole').value;
    const errBox   = document.getElementById('signupError');
    const okBox    = document.getElementById('signupSuccess');

    errBox.style.display = 'none';
    okBox.style.display = 'none';

    if (!validateSignupForm(name, email, password, role)) {
        errBox.textContent = 'Please fix the highlighted fields.';
        errBox.style.display = 'block';
        return;
    }

    setSignupLoading(true);

    try {
        const user = await signupUserApi({ name, email, password, role });

        okBox.textContent = 'Account created. Signing you in...';
        okBox.style.display = 'block';

        saveSession(email, password, user);
        setTimeout(() => redirectByRole(user.role), 500);
    } catch (err) {
        errBox.textContent = err.message || 'Could not create account.';
        errBox.style.display = 'block';
    } finally {
        setSignupLoading(false);
    }
});

function validateSignupForm(name, email, password, role) {
    const ok = {
        name: name.length >= 2 && name.length <= 30,
        email: /^[^\s@]+@company\.com$/i.test(email),
        password: password.length >= 6,
        role: role !== '',
    };

    toggleSignupError('errSignupName', !ok.name);
    toggleSignupError('errSignupEmail', !ok.email);
    toggleSignupError('errSignupPassword', !ok.password);
    toggleSignupError('errSignupRole', !ok.role);

    return Object.values(ok).every(Boolean);
}

function toggleSignupError(id, show) {
    const el = document.getElementById(id);
    if (el) el.classList.toggle('show', show);
}

function setSignupLoading(on) {
    document.getElementById('signupBtn').disabled = on;
    document.getElementById('signupSpinner').style.display = on ? 'inline-block' : 'none';
}
