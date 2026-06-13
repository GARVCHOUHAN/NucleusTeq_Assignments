/* =====================================================
   claims.js — Claims Logic
   Used by:  manager.html  +  employee.html
   ===================================================== */

let rejectTargetClaimId  = null;
let approveTargetClaimId = null; // for approve-with-message modal
let managerClaimsPage    = 0;
let employeeClaimsPage   = 0;
const CLAIMS_PAGE_SIZE   = 10;

/* =====================================================
   MANAGER — Load and render assigned claims
   ===================================================== */
async function loadManagerClaims() {
    const user   = getSession();
    const grid   = document.getElementById('claimsGrid');
    const status = document.getElementById('statusFilter')
        ? document.getElementById('statusFilter').value : '';

    grid.innerHTML = renderClaimSkeletons();

    try {
        const result = await getClaimsByReviewer(user.id, { page: managerClaimsPage, size: CLAIMS_PAGE_SIZE });
        let claims = pageContent(result);
        if (status) claims = claims.filter(c => c.status === status);
        renderClaimsPagination('managerClaimsPagination', result, 'goManagerClaimsPage');

        const pending = claims.filter(c => c.status === 'SUBMITTED').length;
        const badge = document.getElementById('pendingBadge');
        if (badge) badge.textContent = pending || '0';

        if (!claims || claims.length === 0) {
            grid.innerHTML = '<div class="empty-state">No claims assigned to you yet.</div>';
            return;
        }

        grid.innerHTML = claims.map((c, idx) => renderClaimCard(c, idx, true)).join('');

    } catch (err) {
        grid.innerHTML = `<div class="empty-state">Error loading claims: ${esc(err.message)}</div>`;
        showToast('Could not load claims.', 'error');
    }
}

/* ─────────────────────────────────────────────────────
   renderClaimCard
───────────────────────────────────────────────────── */
function renderClaimCard(c, idx, showActions) {
    const delay      = idx * 0.05;
    const hasComment = c.comment && c.comment.trim() !== '';
    const canAct     = showActions && c.status === 'SUBMITTED';

    return `
    <div class="claim-card" style="animation-delay:${delay}s">
      <div class="claim-card-header">
        <span class="claim-type">Reimbursement Request</span>
        <span class="status-badge status-${c.status}">${esc(c.status)}</span>
      </div>
      <div>
        <div class="claim-amount">${formatCurrency(c.amount)}</div>
        <div class="claim-amount-label">${c.employeeName ? 'Submitted by ' + esc(c.employeeName) : 'Employee claim'}</div>
      </div>
      <div class="claim-desc">${esc(c.description)}</div>
      ${hasComment
        ? `<div class="claim-comment" style="display:block">Reviewer note: ${esc(c.comment)}</div>`
        : ''}
      ${canAct
        ? `<div class="claim-actions">
             <button class="btn btn-success btn-sm" onclick="openApproveModal(${c.id})">
               Approve
             </button>
             <button class="btn btn-danger btn-sm" onclick="openRejectModal(${c.id})">
               Reject
             </button>
           </div>`
        : ''}
    </div>`;
}

/* =====================================================
   APPROVE MODAL — optional message before approving
   ===================================================== */
function openApproveModal(claimId) {
    approveTargetClaimId = claimId;
    const commentEl = document.getElementById('approveComment');
    if (commentEl) commentEl.value = '';
    document.getElementById('approveOverlay').classList.add('open');
}

function closeApproveModal() {
    approveTargetClaimId = null;
    document.getElementById('approveOverlay').classList.remove('open');
}

async function confirmApprove() {
    if (!approveTargetClaimId) return;

    const comment = (document.getElementById('approveComment').value || '').trim();
    const user    = getSession();

    setButtonLoading('confirmApproveBtn', 'approveSpinner', true);

    try {
        await takeClaimAction(approveTargetClaimId, user.id, 'APPROVED', comment);
        showToast('Claim approved successfully.', 'success');
        closeApproveModal();
        loadManagerClaims();
    } catch (err) {
        showToast('Could not approve claim: ' + err.message, 'error');
    } finally {
        setButtonLoading('confirmApproveBtn', 'approveSpinner', false);
    }
}

/* =====================================================
   REJECT MODAL
   ===================================================== */
function openRejectModal(claimId) {
    rejectTargetClaimId = claimId;
    const commentEl = document.getElementById('rejectComment');
    if (commentEl) commentEl.value = '';
    const errEl = document.getElementById('errRejectComment');
    if (errEl) errEl.classList.remove('show');
    document.getElementById('rejectOverlay').classList.add('open');
}

function closeRejectModal() {
    rejectTargetClaimId = null;
    document.getElementById('rejectOverlay').classList.remove('open');
}

async function confirmReject() {
    if (!rejectTargetClaimId) return;

    const comment = (document.getElementById('rejectComment').value || '').trim();
    if (!comment) {
        document.getElementById('errRejectComment').classList.add('show');
        return;
    }
    document.getElementById('errRejectComment').classList.remove('show');

    const user = getSession();
    setButtonLoading('confirmRejectBtn', 'rejectSpinner', true);

    try {
        await takeClaimAction(rejectTargetClaimId, user.id, 'REJECTED', comment);
        showToast('Claim rejected.', 'info');
        closeRejectModal();
        loadManagerClaims();
    } catch (err) {
        showToast('Could not reject claim: ' + err.message, 'error');
    } finally {
        setButtonLoading('confirmRejectBtn', 'rejectSpinner', false);
    }
}

/* =====================================================
   EMPLOYEE — Submit a claim
   ===================================================== */
async function submitClaim() {
    const user   = getSession();
    const amount = document.getElementById('claimAmount').value;
    const date   = document.getElementById('claimDate').value;
    const desc   = document.getElementById('claimDesc').value.trim();

    hideEl('submitError');
    hideEl('submitSuccess');

    const amountNumber = parseFloat(amount);
    const amountOk = amount && amountNumber > 0 && amountNumber <= 100000;
    const dateOk   = date && new Date(date + 'T00:00:00') <= new Date();
    const descOk   = desc.length > 0;

    toggleErrEl('errAmount', !amountOk);
    toggleErrEl('errClaimDate', !dateOk);
    toggleErrEl('errDesc',   !descOk);
    if (!amountOk || !dateOk || !descOk) return;

    setButtonLoading('submitClaimBtn', 'submitSpinner', true);

    try {
        await submitClaimApi({ amount: amountNumber, claimDate: date, description: desc, employeeId: user.id });
        const successEl = document.getElementById('submitSuccess');
        successEl.textContent   = 'Your claim has been submitted successfully.';
        successEl.style.display = 'block';
        document.getElementById('claimAmount').value = '';
        document.getElementById('claimDate').value   = todayIsoDate();
        document.getElementById('claimDesc').value   = '';
        showToast('Claim submitted!', 'success');
    } catch (err) {
        const errorEl = document.getElementById('submitError');
        errorEl.textContent   = 'Submission failed: ' + err.message;
        errorEl.style.display = 'block';
    } finally {
        setButtonLoading('submitClaimBtn', 'submitSpinner', false);
    }
}

/* =====================================================
   EMPLOYEE — Load own claims history
   ===================================================== */
async function loadEmployeeClaims() {
    const user   = getSession();
    const tbody  = document.getElementById('empClaimsBody');
    const status = document.getElementById('empStatusFilter')
        ? document.getElementById('empStatusFilter').value : '';

    tbody.innerHTML = '<tr><td colspan="5" class="empty-cell">Loading…</td></tr>';

    try {
        const result = await getClaimsByEmployee(user.id, { page: employeeClaimsPage, size: CLAIMS_PAGE_SIZE });
        let claims = pageContent(result);
        if (status) claims = claims.filter(c => c.status === status);
        renderClaimsPagination('employeeClaimsPagination', result, 'goEmployeeClaimsPage');

        const badge = document.getElementById('claimCountBadge');
        if (badge) badge.textContent = claims.length || '0';

        if (!claims || claims.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="empty-cell">You have not submitted any claims yet.</td></tr>';
            return;
        }

        tbody.innerHTML = claims.map(c => `
      <tr>
        <td><strong>${formatCurrency(c.amount)}</strong></td>
        <td>${formatDate(c.date)}</td>
        <td>${esc(c.description)}</td>
        <td><span class="status-badge status-${c.status}">${esc(c.status)}</span></td>
        <td>${c.comment
            ? `<span style="color:var(--text-mid)">${esc(c.comment)}</span>`
            : `<span style="color:var(--text-muted)">–</span>`}
        </td>
      </tr>`).join('');

    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="5" class="empty-cell">Error: ${esc(err.message)}</td></tr>`;
    }
}

/* =====================================================
   SKELETONS
   ===================================================== */
function renderClaimSkeletons() {
    return Array(4).fill('').map(() => `
    <div class="skeleton-card">
      <div style="display:flex;justify-content:space-between">
        <div class="skel" style="height:18px;width:50px;border-radius:4px"></div>
        <div class="skel" style="height:18px;width:80px;border-radius:20px"></div>
      </div>
      <div>
        <div class="skel" style="height:26px;width:100px;margin-bottom:5px"></div>
        <div class="skel" style="height:11px;width:140px"></div>
      </div>
      <div class="skel" style="height:36px;width:100%"></div>
      <div class="skel" style="height:12px;width:60%"></div>
      <div style="display:flex;gap:8px">
        <div class="skel" style="height:32px;width:90px;border-radius:6px"></div>
        <div class="skel" style="height:32px;width:90px;border-radius:6px"></div>
      </div>
    </div>`).join('');
}

/* ── Helpers ── */
function renderClaimsPagination(containerId, pageData, handlerName) {
    const container = document.getElementById(containerId);
    if (!container || !pageData || Array.isArray(pageData)) return;

    const pages = pageData.totalPages || 0;
    if (pages <= 1) {
        container.innerHTML = '';
        return;
    }

    let html = `<button class="page-btn" onclick="${handlerName}(${pageData.page - 1})" ${pageData.first ? 'disabled' : ''}>&#8249;</button>`;
    for (let i = 0; i < pages; i++) {
        html += `<button class="page-btn ${i === pageData.page ? 'active' : ''}" onclick="${handlerName}(${i})">${i + 1}</button>`;
    }
    html += `<button class="page-btn" onclick="${handlerName}(${pageData.page + 1})" ${pageData.last ? 'disabled' : ''}>&#8250;</button>`;
    container.innerHTML = html;
}

function goManagerClaimsPage(page) {
    managerClaimsPage = Math.max(page, 0);
    loadManagerClaims();
}

function goEmployeeClaimsPage(page) {
    employeeClaimsPage = Math.max(page, 0);
    loadEmployeeClaims();
}

function todayIsoDate() {
    return new Date().toISOString().slice(0, 10);
}

function hideEl(id) { const el = document.getElementById(id); if (el) el.style.display = 'none'; }
function toggleErrEl(id, show) { const el = document.getElementById(id); if (el) el.classList.toggle('show', show); }

document.querySelectorAll('.overlay').forEach(ov => {
    ov.addEventListener('click', e => { if (e.target === ov) ov.classList.remove('open'); });
});
