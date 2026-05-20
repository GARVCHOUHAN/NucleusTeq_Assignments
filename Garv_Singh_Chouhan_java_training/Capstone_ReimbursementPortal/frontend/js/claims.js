/* =====================================================
   claims.js — Claims Logic
   Used by:  manager.html  +  employee.html
   ===================================================== */

let rejectTargetClaimId  = null;
let approveTargetClaimId = null; // for approve-with-message modal

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
        let claims = await getClaimsByReviewer(user.id);
        if (status) claims = claims.filter(c => c.status === status);

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
        <span class="claim-id">ID #${c.id}</span>
        <span class="status-badge status-${c.status}">${esc(c.status)}</span>
      </div>
      <div>
        <div class="claim-amount">${formatCurrency(c.amount)}</div>
        <div class="claim-amount-label">Reimbursement Request</div>
      </div>
      <div class="claim-desc">${esc(c.description)}</div>
      ${c.employeeName
        ? `<div class="claim-employee">Submitted by <strong>${esc(c.employeeName)}</strong></div>`
        : ''}
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
    const desc   = document.getElementById('claimDesc').value.trim();

    hideEl('submitError');
    hideEl('submitSuccess');

    const amountOk = amount && parseFloat(amount) > 0;
    const descOk   = desc.length > 0;

    toggleErrEl('errAmount', !amountOk);
    toggleErrEl('errDesc',   !descOk);
    if (!amountOk || !descOk) return;

    setButtonLoading('submitClaimBtn', 'submitSpinner', true);

    try {
        await submitClaimApi({ amount: parseFloat(amount), description: desc, employeeId: user.id });
        const successEl = document.getElementById('submitSuccess');
        successEl.textContent   = 'Your claim has been submitted successfully.';
        successEl.style.display = 'block';
        document.getElementById('claimAmount').value = '';
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
        let claims = await getClaimsByEmployee(user.id);
        if (status) claims = claims.filter(c => c.status === status);

        const badge = document.getElementById('claimCountBadge');
        if (badge) badge.textContent = claims.length || '0';

        if (!claims || claims.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="empty-cell">You have not submitted any claims yet.</td></tr>';
            return;
        }

        tbody.innerHTML = claims.map(c => `
      <tr>
        <td>#${c.id}</td>
        <td><strong>${formatCurrency(c.amount)}</strong></td>
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
function hideEl(id) { const el = document.getElementById(id); if (el) el.style.display = 'none'; }
function toggleErrEl(id, show) { const el = document.getElementById(id); if (el) el.classList.toggle('show', show); }

document.querySelectorAll('.overlay').forEach(ov => {
    ov.addEventListener('click', e => { if (e.target === ov) ov.classList.remove('open'); });
});