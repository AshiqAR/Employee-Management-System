function openAddDepartmentModal() {
    document.getElementById('departmentForm').reset();
    document.getElementById('department_id').value = '';
    document.getElementById('modalTitle').innerText = 'Add Department';
    document.getElementById('departmentModal').style.display = 'block';
}

function openEditDepartmentModal(department_id) {
    // Populate form with existing department details (AJAX or form prefilling can be done here)
    document.getElementById('modalTitle').innerText = 'Edit Department';
    document.getElementById('department_id').value = department_id;
    document.getElementById('department_name').value = document.querySelector(`[data-department-id="${department_id}"] .department-name`).innerText;
    document.getElementById('departmentModal').style.display = 'block';
}

function closeDepartmentModal() {
    document.getElementById('departmentModal').style.display = 'none';
}

function searchDepartments() {
    // Implement department search logic here
}

function confirmDeleteDepartment(department_id) {
    // Implement delete confirmation logic here
}
