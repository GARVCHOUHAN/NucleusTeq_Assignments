
/* ── Boot: guard page, populate sidebar, load claims ── */
window.addEventListener('DOMContentLoaded', function () {
    guardPage('MANAGER');
    populateSidebar();
    loadManagerClaims();
});