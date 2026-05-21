/* =====================================================
   dashboard.js — Admin Dashboard Logic
   Handles: user listing, stat cards, add/delete user,
        tab switching, filtering, pagination
  ===================================================== */

const USERS_PER_PAGE = 12; // Show 12 users per page in the grid

let allUsers       = [];
let managers       = [];
let filteredUsers  = [];
let currentPage    = 1;
let deleteTargetId = null;
let assignTargetId = null;

window.addEventListener('DOMContentLoaded', function () {
    guardPage('ADMIN');
    populateSidebar();
    setupAdminTabs();
    loadUsers();
});

/* ── Tab switching ── */
function setupAdminTabs() {
    document.querySelectorAll('.nav-link[data-tab]').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const tab = this.dataset.tab;
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            document.getElementById('tabUsers').style.display  = tab === 'users'  ? 'block' : 'none';
            document.getElementById('tabClaims').style.display = tab === 'claims' ? 'block' : 'none';
            document.getElementById('pageHeading').textContent = tab === 'users' ? 'Team Members' : 'All Claims';
            document.getElementById('pageSub').textContent     = tab === 'users' ? 'Manage all users' : 'View all reimbursement claims';
            document.getElementById('addUserBtn').style.display = tab === 'users' ? 'inline-flex' : 'none';
            if (tab === 'claims') loadAllClaims();
        });
    });
}

/* ── Load users ── */
async function loadUsers() {
    showUserSkeletons();
    try {
        allUsers = await getAllUsers();
        managers = allUsers.filter(u => u.role === 'MANAGER');
        buildManagerDropdown();
        updateStats();
        currentPage = 1;
        filterUsersTable();
        const badge = document.getElementById('userCountBadge');
        if (badge) badge.textContent = allUsers.length;
    } catch (err) {
        showToast('Could not load users: ' + err.message, 'error');
    }
}

/* ── Refresh button — reloads users and shows spinner on button ── */
async function refreshPage() {
    const btn = document.getElementById('refreshBtn');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation:spin 0.7s linear infinite"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg> Refreshing…`;
    }
    await loadUsers();
    if (btn) {
        btn.disabled = false;
        btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg> Refresh`;
    }
    showToast('Users refreshed.', 'success');
}

/* ── Stats ── */
function updateStats() {
    setText('statAdmin',    allUsers.filter(u => u.role === 'ADMIN').length);
    setText('statManager',  allUsers.filter(u => u.role === 'MANAGER').length);
    setText('statEmployee', allUsers.filter(u => u.role === 'EMPLOYEE').length);
    setText('statTotal',    allUsers.length);
}

/* ── Filter + search ── */
function filterUsersTable() {
    const query = (document.getElementById('userSearch').value || '').toLowerCase().trim();
    const role  = document.getElementById('roleFilter').value;
    filteredUsers = allUsers.filter(u => {
        const matchQ = u.name.toLowerCase().includes(query) || u.email.toLowerCase().includes(query);
        const matchR = !role || u.role === role;
        return matchQ && matchR;
    });
    filteredUsers.sort((a, b) => a.name.localeCompare(b.name));
    currentPage = 1;
    renderUserCards();
}

/* ── Render cards ── */
function renderUserCards() {
    const grid  = document.getElementById('userGrid');
    const total = filteredUsers.length;
    const start = (currentPage - 1) * USERS_PER_PAGE;
    const slice = filteredUsers.slice(start, start + USERS_PER_PAGE);

    if (total === 0) {
        grid.innerHTML = '<div class="empty-state">No users match your current filters.</div>';
        document.getElementById('userPagination').innerHTML = '';
        return;
    }

    grid.innerHTML = slice.map((u, idx) => {
        const color = avatarColor(u.name);
        const init  = initials(u.name);
        const delay = idx * 0.04;
        const roleLabel = { ADMIN: 'Admin', MANAGER: 'Manager', EMPLOYEE: 'Employee' }[u.role] || u.role;
        // Resolve manager name: backend DTO may not include it, so look up from allUsers
        const managerName = u.managerName ||
            (u.managerId ? (allUsers.find(m => m.id === u.managerId) || {}).name : null);
        // Count employees under this manager (for MANAGER cards)
        const reportCount = u.role === 'MANAGER'
            ? allUsers.filter(e => e.managerId === u.id || e.managerName === u.name).length
            : null;

        return `
      <div class="user-card user-card-${u.role}" style="animation-delay:${delay}s">

        <!-- Top: avatar + name + role pill inline -->
        <div class="user-card-top">
          <div class="user-avatar" style="background:${color}">${esc(init)}</div>
          <div class="user-info">
            <div class="user-name" title="${esc(u.name)}">${esc(u.name)}</div>
            <div class="user-email" title="${esc(u.email)}">${esc(u.email)}</div>
          </div>
          <div class="role-pill role-${u.role}">${esc(roleLabel)}</div>
        </div>

        <!-- Middle: role-specific info row -->
        <div class="card-meta">
          ${u.role === 'ADMIN' ? `
            <div class="meta-item">
              <span class="meta-label">Permissions : </span>
              <span class="meta-value">Full system access</span>
            </div>` : ''}
          ${u.role === 'MANAGER' ? `
            <div class="meta-item">
              <span class="meta-label">Manages : </span>
              <span class="meta-value">${reportCount} ${reportCount === 1 ? 'employee' : 'employees'}</span>
            </div>` : ''}
          ${u.role === 'EMPLOYEE' ? `
            <div class="meta-item">
              <span class="meta-label">Manager : </span>
              <span class="meta-value">${managerName
            ? esc(managerName)
            : '<span style="color:var(--text-muted);font-style:italic">Not assigned</span>'}</span>
            </div>` : ''}
        </div>

        <!-- Footer: ID + remove -->
        <div class="user-card-footer">
          <span class="user-id">ID #${u.id}</span>
          <div style="display:flex;gap:8px;align-items:center">
            ${u.role === 'EMPLOYEE'
              ? `<button class="btn-remove" onclick="openAssignManagerModal(${u.id})">Assign Manager</button>`
              : ''}
            <button class="btn-remove" onclick="openDeleteModal(${u.id})">Remove</button>
          </div>
        </div>
      </div>`;
    }).join('');

    renderPagination(total);
}

/* ── Pagination ── */
function renderPagination(total) {
    const pages = Math.ceil(total / USERS_PER_PAGE);
    const pg    = document.getElementById('userPagination');
    if (pages <= 1) { pg.innerHTML = ''; return; }
    let html = `<button class="page-btn" onclick="goPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>&#8249;</button>`;
    for (let i = 1; i <= pages; i++) {
        html += `<button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="goPage(${i})">${i}</button>`;
    }
    html += `<button class="page-btn" onclick="goPage(${currentPage + 1})" ${currentPage === pages ? 'disabled' : ''}>&#8250;</button>`;
    pg.innerHTML = html;
}

function goPage(p) { currentPage = p; renderUserCards(); }

/* ── Skeletons ── */
function showUserSkeletons() {
    document.getElementById('userGrid').innerHTML = Array(6).fill('').map(() => `
    <div class="skeleton-card">
      <div style="display:flex;gap:10px;align-items:center">
        <div class="skel" style="width:40px;height:40px;border-radius:10px;flex-shrink:0"></div>
        <div style="flex:1">
          <div class="skel" style="height:13px;width:65%;margin-bottom:7px"></div>
          <div class="skel" style="height:11px;width:50%"></div>
        </div>
      </div>
      <div class="skel" style="height:22px;width:80px;border-radius:20px"></div>
      <div class="skel" style="height:11px;width:60%"></div>
      <div style="display:flex;justify-content:space-between;padding-top:10px;border-top:1px solid var(--border)">
        <div class="skel" style="height:18px;width:50px;border-radius:4px"></div>
        <div class="skel" style="height:28px;width:70px;border-radius:6px"></div>
      </div>
    </div>`).join('');
}

/* ── Add User Modal ── */
function openAddUserModal() {
    clearAddUserForm();
    document.getElementById('addUserOverlay').classList.add('open');
}

function closeAddUserModal() {
    document.getElementById('addUserOverlay').classList.remove('open');
}

function toggleManagerField() {
    const role = document.getElementById('newRole').value;
    document.getElementById('managerField').style.display = role === 'EMPLOYEE' ? 'block' : 'none';
}

function buildManagerDropdown() {
    const sel = document.getElementById('newManager');
    if (!sel) return;
    sel.innerHTML = '<option value="">Admin fallback</option>';
    managers.forEach(m => {
        const opt = document.createElement('option');
        opt.value = m.id;
        opt.textContent = m.name;
        sel.appendChild(opt);
    });
}

async function createUser() {
    if (!validateAddUserForm()) return;
    const name      = document.getElementById('newName').value.trim();
    const email     = document.getElementById('newEmail').value.trim();
    const password  = document.getElementById('newPassword').value;
    const role      = document.getElementById('newRole').value;
    const managerId = document.getElementById('newManager').value;
    const payload   = { name, email, password, role };
    if (managerId) payload.managerId = parseInt(managerId, 10);

    setButtonLoading('createUserBtn', 'createUserSpinner', true);
    hide('addUserError');
    hide('addUserSuccess');

    try {
        const created = await createUserApi(payload);
        allUsers.push(created);
        if (created.role === 'MANAGER') { managers.push(created); buildManagerDropdown(); }
        updateStats();
        filterUsersTable();
        closeAddUserModal();
        showToast(`${created.name} has been added to the team.`, 'success');
    } catch (err) {
        document.getElementById('addUserError').textContent   = err.message;
        document.getElementById('addUserError').style.display = 'block';
    } finally {
        setButtonLoading('createUserBtn', 'createUserSpinner', false);
    }
}

function validateAddUserForm() {
    const name  = document.getElementById('newName').value.trim();
    const email = document.getElementById('newEmail').value.trim();
    const pass  = document.getElementById('newPassword').value;
    const role  = document.getElementById('newRole').value;
    const ok = {
        name:  name.length >= 2 && name.length <= 30,
        email: email.endsWith('@company.com') && email.length > 12,
        pass:  pass.length >= 6,
        role:  role !== '',
    };
    toggleError('errNewName',     !ok.name);
    toggleError('errNewEmail',    !ok.email);
    toggleError('errNewPassword', !ok.pass);
    toggleError('errNewRole',     !ok.role);
    return Object.values(ok).every(Boolean);
}

function clearAddUserForm() {
    ['newName', 'newEmail', 'newPassword'].forEach(id => { const el = document.getElementById(id); if (el) el.value = ''; });
    document.getElementById('newRole').value    = '';
    document.getElementById('newManager').value = '';
    document.getElementById('managerField').style.display = 'none';
    document.querySelectorAll('#addUserOverlay .form-error').forEach(el => el.classList.remove('show'));
    hide('addUserError');
    hide('addUserSuccess');
}

/* ════════════════════════════════════════════════════
   DELETE USER — fixed to show friendly errors in modal
   ════════════════════════════════════════════════════ */
/* Assign manager for existing employee */
function openAssignManagerModal(employeeId) {
    const employee = allUsers.find(u => u.id === employeeId);
    if (!employee || employee.role !== 'EMPLOYEE') {
        showToast('Manager can be assigned only to employees.', 'error');
        return;
    }

    assignTargetId = employeeId;
    setText('assignEmployeeName', employee.name);
    hide('assignManagerError');
    buildAssignManagerDropdown(employee.managerId);
    document.getElementById('assignManagerOverlay').classList.add('open');
}

function closeAssignManagerModal() {
    assignTargetId = null;
    hide('assignManagerError');
    document.getElementById('assignManagerOverlay').classList.remove('open');
}

function buildAssignManagerDropdown(selectedManagerId) {
    const sel = document.getElementById('assignManagerSelect');
    if (!sel) return;
    sel.innerHTML = '<option value="">Admin fallback</option>';
    managers.forEach(m => {
        const opt = document.createElement('option');
        opt.value = m.id;
        opt.textContent = m.name;
        if (selectedManagerId && Number(selectedManagerId) === Number(m.id)) {
            opt.selected = true;
        }
        sel.appendChild(opt);
    });
}

async function confirmAssignManager() {
    if (!assignTargetId) return;
    const managerId = document.getElementById('assignManagerSelect').value;
    setButtonLoading('assignManagerBtn', 'assignManagerSpinner', true);
    hide('assignManagerError');

    try {
        const updated = await assignManagerApi(assignTargetId, managerId || null);
        allUsers = allUsers.map(u => u.id === updated.id ? updated : u);
        managers = allUsers.filter(u => u.role === 'MANAGER');
        buildManagerDropdown();
        filterUsersTable();
        closeAssignManagerModal();
        showToast(managerId ? 'Manager assigned successfully.' : 'Manager cleared. Admin will review new claims.', 'success');
    } catch (err) {
        const box = document.getElementById('assignManagerError');
        box.textContent = err.message || 'Could not assign manager.';
        box.style.display = 'block';
    } finally {
        setButtonLoading('assignManagerBtn', 'assignManagerSpinner', false);
    }
}

function openDeleteModal(id) {
    // Block deleting an ADMIN — find the user in allUsers
    const target = allUsers.find(u => u.id === id);
    if (target && target.role === 'ADMIN') {
        showToast('Admin accounts cannot be deleted.', 'error');
        return;
    }
    deleteTargetId = id;
    document.getElementById('deleteUserName').textContent = target ? target.name : 'this user';
    hideDeleteError();
    document.getElementById('deleteOverlay').classList.add('open');
}

function closeDeleteModal() {
    deleteTargetId = null;
    hideDeleteError();
    document.getElementById('deleteOverlay').classList.remove('open');
}

async function confirmDeleteUser() {
    if (!deleteTargetId) return;

    setButtonLoading('confirmDeleteBtn', 'deleteSpinner', true);
    hideDeleteError();

    try {
        await deleteUserApi(deleteTargetId);

        // Success — remove from local state and close modal
        allUsers  = allUsers.filter(u => u.id !== deleteTargetId);
        managers  = managers.filter(u => u.id !== deleteTargetId);
        updateStats();
        filterUsersTable();
        closeDeleteModal();
        showToast('User removed successfully.', 'success');

    } catch (err) {
        // Show a friendly message INSIDE the modal so it stays open
        // The user can read why deletion failed and cancel or take action
        showDeleteError(parseDeleteError(err.message));
    } finally {
        setButtonLoading('confirmDeleteBtn', 'deleteSpinner', false);
    }
}

/*
  parseDeleteError(raw)
  -----------------------
  The backend returns either:
    - Plain text:  "Cannot delete manager with assigned employees"
    - JSON string: {"timestamp":"...","status":500,"error":"Internal Server Error","path":"..."}

  We parse both and return a beginner-friendly sentence.
*/
function parseDeleteError(raw) {
    // 1. Try to parse as JSON (Spring Boot default error envelope)
    try {
        const obj = JSON.parse(raw);
        if (obj.message) return friendlyMessage(obj.message);
        if (obj.error)   return friendlyMessage(obj.error);
    } catch (_) { /* not JSON */ }

    // 2. Raw string from our own GlobalExceptionHandler
    return friendlyMessage(raw || 'Deletion failed. Please try again.');
}

/*
  friendlyMessage(msg)
  ---------------------
  Maps known backend phrases to human-readable explanations.
*/
function friendlyMessage(msg) {
    const m = (msg || '').toLowerCase();

    if (m.includes('manager with assigned employees')) {
        return 'This manager has employees assigned to them. Please reassign or remove those employees first, then try again.';
    }
    if (m.includes('constraint') || m.includes('foreign key') || m.includes('referential')) {
        return 'This user has existing claims in the system. Delete their claims first before removing the user.';
    }
    if (m.includes('internal server error') || m.includes('500')) {
        return 'This user cannot be deleted because they are linked to existing claims or records. Remove those records first.';
    }
    if (m.includes('not found')) {
        return 'User not found. They may have already been deleted. Refresh the page.';
    }

    // Return the original message if nothing matched
    return msg;
}

/* Show / hide inline error inside the delete modal */
function showDeleteError(msg) {
    let box = document.getElementById('deleteErrorBox');
    if (!box) {
        // Create the error box once and insert it above the modal footer
        box = document.createElement('div');
        box.id        = 'deleteErrorBox';
        box.className = 'alert alert-error';
        box.style.marginTop    = '12px';
        box.style.marginBottom = '0';
        const footer = document.querySelector('#deleteOverlay .modal-footer');
        if (footer) footer.parentNode.insertBefore(box, footer);
    }
    box.textContent  = msg;
    box.style.display = 'block';
}

function hideDeleteError() {
    const box = document.getElementById('deleteErrorBox');
    if (box) box.style.display = 'none';
}

/* ── Admin claim action state ── */
let adminActionClaimId = null;

/* ── All claims tab — admin can approve/reject SUBMITTED claims ── */
async function loadAllClaims() {
    const tbody  = document.getElementById('allClaimsBody');
    const status = document.getElementById('claimStatusFilter').value;
    const admin  = getSession();
    tbody.innerHTML = '<tr><td colspan="7" class="empty-cell">Loading…</td></tr>';
    try {
        const claims = status ? await getClaimsByStatus(status) : await getAllClaims();
        if (!claims || claims.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="empty-cell">No claims found.</td></tr>';
            return;
        }
        tbody.innerHTML = claims.map(c => {
            const canAdminAct = c.status === 'SUBMITTED' &&
                admin && Number(c.reviewerId) === Number(admin.id);
            const actionText = c.status === 'SUBMITTED' ? 'Assigned to manager' : 'NA';

            return `
      <tr>
        <td>#${c.id}</td>
        <td>${esc(c.employeeName || c.employeeId || '–')}</td>
        <td><strong>${formatCurrency(c.amount)}</strong></td>
        <td>${esc(c.description)}</td>
        <td><span class="status-badge status-${c.status}">${esc(c.status)}</span></td>
        <td>${c.comment ? esc(c.comment) : '<span style="color:var(--text-muted)">NA</span>'}</td>
        <td>
          ${canAdminAct
            ? `<div style="display:flex;gap:6px">
                <button class="btn btn-success btn-sm"
                  onclick="openAdminApproveModal(${c.id})">Approve</button>
                <button class="btn btn-danger btn-sm"
                  onclick="openAdminRejectModal(${c.id})">Reject</button>
               </div>`
            : `<span style="color:var(--text-muted);font-size:12px">${esc(actionText)}</span>`}
        </td>
      </tr>`;
        }).join('');
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="7" class="empty-cell">Error: ${esc(err.message)}</td></tr>`;
    }
}

/* ── Admin Approve Modal ── */
function openAdminApproveModal(claimId) {
    adminActionClaimId = claimId;
    const el = document.getElementById('adminApproveComment');
    if (el) el.value = '';
    document.getElementById('adminApproveOverlay').classList.add('open');
}

function closeAdminApproveModal() {
    adminActionClaimId = null;
    document.getElementById('adminApproveOverlay').classList.remove('open');
}

async function confirmAdminApprove() {
    if (!adminActionClaimId) return;
    const user    = getSession();
    const comment = (document.getElementById('adminApproveComment').value || '').trim();
    setButtonLoading('adminApproveBtn', 'adminApproveSpinner', true);
    try {
        await takeClaimAction(adminActionClaimId, user.id, 'APPROVED', comment);
        showToast('Claim approved successfully.', 'success');
        closeAdminApproveModal();
        loadAllClaims();
    } catch (err) {
        showToast('Could not approve: ' + err.message, 'error');
    } finally {
        setButtonLoading('adminApproveBtn', 'adminApproveSpinner', false);
    }
}

/* ── Admin Reject Modal ── */
function openAdminRejectModal(claimId) {
    adminActionClaimId = claimId;
    const el = document.getElementById('adminRejectComment');
    if (el) el.value = '';
    const errEl = document.getElementById('errAdminRejectComment');
    if (errEl) errEl.classList.remove('show');
    document.getElementById('adminRejectOverlay').classList.add('open');
}

function closeAdminRejectModal() {
    adminActionClaimId = null;
    document.getElementById('adminRejectOverlay').classList.remove('open');
}

async function confirmAdminReject() {
    if (!adminActionClaimId) return;
    const user    = getSession();
    const comment = (document.getElementById('adminRejectComment').value || '').trim();
    if (!comment) {
        document.getElementById('errAdminRejectComment').classList.add('show');
        return;
    }
    document.getElementById('errAdminRejectComment').classList.remove('show');
    setButtonLoading('adminRejectBtn', 'adminRejectSpinner', true);
    try {
        await takeClaimAction(adminActionClaimId, user.id, 'REJECTED', comment);
        showToast('Claim rejected.', 'info');
        closeAdminRejectModal();
        loadAllClaims();
    } catch (err) {
        showToast('Could not reject: ' + err.message, 'error');
    } finally {
        setButtonLoading('adminRejectBtn', 'adminRejectSpinner', false);
    }
}

/* ── Close overlays on backdrop click ── */
document.querySelectorAll('.overlay').forEach(ov => {
    ov.addEventListener('click', e => { if (e.target === ov) ov.classList.remove('open'); });
});

/* ── DOM helpers ── */
function setText(id, val) { const el = document.getElementById(id); if (el) el.textContent = val; }
function hide(id)         { const el = document.getElementById(id); if (el) el.style.display = 'none'; }
function toggleError(id, show) { const el = document.getElementById(id); if (el) el.classList.toggle('show', show); }
