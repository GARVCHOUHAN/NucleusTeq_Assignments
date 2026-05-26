window.addEventListener('DOMContentLoaded', async function () {
    guardPage('EMPLOYEE');
    populateSidebar();
    setupEmployeeTabs();
    // Always re-fetch the current user so manager assignment changes
    // made after login are immediately visible without re-logging in
    await refreshCurrentUser();
    showManagerBanner();
    setDefaultClaimDate();
});

/* Re-fetch logged-in user from API and update localStorage */
async function refreshCurrentUser() {
    const user = getSession();
    if (!user) return;
    try {
        const fresh = await getCurrentUserApi();
        // Merge fresh data back into session (keeps token/email/password intact)
        const updated = Object.assign({}, user, fresh);
        localStorage.setItem('rh_user', JSON.stringify(updated));
        // Also refresh sidebar name in case it changed
        populateSidebar();
    } catch (e) {
        // Non-critical — if it fails just use stale session data
        console.warn('Could not refresh user:', e.message);
    }
}

/* Show the correct manager info banner based on fresh session */
function showManagerBanner() {
    const user = getSession();
    if (!user) return;
    const hasMgr = user.managerName || user.managerId;
    document.getElementById('managerInfoBanner').style.display = hasMgr ? 'block' : 'none';
    document.getElementById('noManagerBanner').style.display   = hasMgr ? 'none'  : 'block';
    if (hasMgr && user.managerName) {
        document.getElementById('managerInfoName').textContent = user.managerName;
    }
}

/* ── Tab switching for employee sidebar ── */
function setupEmployeeTabs() {
    document.querySelectorAll('.nav-link[data-tab]').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const tab = this.dataset.tab;

            // Update active link
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');

            // Show/hide tab content
            document.getElementById('tabSubmit').style.display  = tab === 'submit'  ? 'block' : 'none';
            document.getElementById('tabHistory').style.display = tab === 'history' ? 'block' : 'none';

            // Update header
            document.getElementById('pageHeading').textContent = tab === 'submit'
                ? 'Submit a Claim' : 'My Claims';
            document.getElementById('pageSub').textContent = tab === 'submit'
                ? 'Fill in the form to request reimbursement'
                : 'Track the status of your submitted claims';

            if (tab === 'history') loadEmployeeClaims();
        });
    });
}

function setDefaultClaimDate() {
    const claimDate = document.getElementById('claimDate');
    if (claimDate) claimDate.value = todayIsoDate();
}
