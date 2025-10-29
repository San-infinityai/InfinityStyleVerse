<<<<<<< HEAD
// dashboard
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const hamburgerMenu = document.getElementById('hamburger-menu');
    const mainContent = document.getElementById('main-content');
    const currentDateElement = document.getElementById('current-date');


    const today = new Date();
    const options = { month: 'long', day: 'numeric', year: 'numeric' };
    currentDateElement.textContent = today.toLocaleDateString('en-US', options);


    hamburgerMenu.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });


    mainContent.addEventListener('click', (event) => {
        if (window.innerWidth <= 768 && sidebar.classList.contains('active') && !sidebar.contains(event.target) && !hamburgerMenu.contains(event.target)) {
            sidebar.classList.remove('active');
        }
    });


    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('active');
            sidebar.classList.remove('hidden');
        } else {
            sidebar.classList.add('hidden');
        }
    });


    if (window.innerWidth <= 768) {
        sidebar.classList.add('hidden');
    }

    Chart.defaults.font.family = 'DM Sans, sans-serif';
    Chart.defaults.color = 'var(--text-gray)';
    Chart.defaults.font.size = 12;


    function createGradient(ctx) {
        const gradient = ctx.createLinearGradient(0, 0, 0, 220);
        gradient.addColorStop(0, 'rgba(193, 154, 107, 0.3)');
        gradient.addColorStop(1, 'rgba(193, 154, 107, 0)');
        return gradient;
    }


    const userGrowthCtx = document.getElementById('userGrowthChart').getContext('2d');
    let userGrowthChart = new Chart(userGrowthCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'User Growth',
                data: [100, 120, 150, 130, 180, 200, 250, 280, 320, 380, 450, 520],

                backgroundColor: createGradient(userGrowthCtx),
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: 'var(--accent-color)',
                pointBorderColor: '#C2A57D',
                pointBorderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    titleFont: { family: 'Inter', size: 14, weight: 'bold' },
                    bodyFont: { family: 'DM Sans', size: 12 },
                    backgroundColor: 'rgba(34,34,34,0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    padding: 10,
                    cornerRadius: 6,
                    borderColor: 'var(--accent-color)',
                    borderWidth: 1,
                    displayColors: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: 'var(--text-gray)',
                        font: { family: 'DM Sans', size: 11, weight: 'normal' }
                    },
                    border: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0,0,0,0.08)'
                    },
                    ticks: {
                        color: 'var(--text-gray)',
                        font: { family: 'DM Sans', size: 11, weight: 'normal' },
                        callback: function (value) {
                            return value > 999 ? (value / 1000).toFixed(0) + 'k' : value;
                        }
                    },
                    border: {
                        display: false
                    }
                }
            }
        }
    });


    const userDistributionCtx = document.getElementById('userDistributionChart').getContext('2d');
    let userDistributionChart = new Chart(userDistributionCtx, {
        type: 'doughnut',
        data: {
            labels: ['Admin', 'Executive', 'User', 'Guest'],
            datasets: [{
                data: [52.1, 22.8, 13.9, 11.2],
                backgroundColor: [
                    '#232321',
                    '#C19A6B',
                    '#E6C89C',
                    '#C27D7E'


                ],
                hoverOffset: 8,

                borderWidth: 2,
                spacing: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    titleFont: { family: 'Inter', size: 14, weight: 'bold' },
                    bodyFont: { family: 'DM Sans', size: 12 },
                    callbacks: {
                        label: function (context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed !== null) {
                                label += context.parsed.toFixed(1) + '%';
                            }
                            return label;
                        }
                    },
                    backgroundColor: 'rgba(34,34,34,0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    padding: 10,
                    cornerRadius: 6,
                    borderColor: 'var(--accent-color)',
                    borderWidth: 1,
                    displayColors: true,
                    boxWidth: 10,
                    boxHeight: 10
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            },
            elements: {
                arc: {
                    hoverBorderColor: 'var(--accent-color)',
                }
            }
        }
    });
    const weeklyBtn = document.getElementById('weeklyBtn');
    const monthlyBtn = document.getElementById('monthlyBtn');
    const yearlyBtn = document.getElementById('yearlyBtn');

    const updateChartData = (period) => {
        let newData;
        let newLabels;

        if (period === 'weekly') {
            newLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
            newData = [80, 100, 120, 90, 130, 110, 150];
        } else if (period === 'monthly') {
            newLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            newData = [100, 120, 150, 130, 180, 200, 250, 280, 320, 380, 450, 520];
        } else if (period === 'yearly') {
            newLabels = ['2022', '2023', '2024', '2025'];
            newData = [800, 1000, 1250, 1500];
        }

        userGrowthChart.data.labels = newLabels;
        userGrowthChart.data.datasets[0].data = newData;
        userGrowthChart.data.datasets[0].backgroundColor = createGradient(userGrowthCtx);
        userGrowthChart.update();


        [weeklyBtn, monthlyBtn, yearlyBtn].forEach(btn => btn.classList.remove('active'));
        if (period === 'weekly') weeklyBtn.classList.add('active');
        else if (period === 'monthly') monthlyBtn.classList.add('active');
        else if (period === 'yearly') yearlyBtn.classList.add('active');
    };

    weeklyBtn.addEventListener('click', () => updateChartData('weekly'));
    monthlyBtn.addEventListener('click', () => updateChartData('monthly'));
    yearlyBtn.addEventListener('click', () => updateChartData('yearly'));

    updateChartData('monthly');
});




//permissions
document.addEventListener('DOMContentLoaded', () => {

    const sidebar = document.getElementById('sidebar');
    const hamburgerMenu = document.getElementById('hamburger-menu');
    const mainContent = document.getElementById('main-content');
    const currentDateElement = document.getElementById('current-date');


    const managePermissionsModal = document.getElementById('managePermissionsModal');
    const openManagePermissionsModalBtn = document.getElementById('openManagePermissionsModalBtn');
    const closeManageModalBtn = document.getElementById('closeManageModalBtn');
    const cancelManageBtn = document.getElementById('cancelManageBtn');
    const savePermissionsBtn = document.getElementById('savePermissionsBtn');
    const roleSelectModal = document.getElementById('roleSelectModal');
    const permissionsListContainer = document.getElementById('permissionsList');


    const permissionDetailsModal = document.getElementById('permissionDetailsModal');
    const openAddEditPermissionModalBtn = document.getElementById('openAddEditPermissionModalBtn');
    const closePermissionDetailsModalBtn = document.getElementById('closePermissionDetailsModalBtn');
    const cancelPermissionDetailsBtn = document.getElementById('cancelPermissionDetailsBtn');
    const savePermissionDetailsBtn = document.getElementById('savePermissionDetailsBtn');
    const permissionDetailsModalTitle = document.getElementById('permissionDetailsModalTitle');
    const permissionModuleInput = document.getElementById('permissionModule');
    const permissionNameInput = document.getElementById('permissionName');
    const permissionDescriptionInput = document.getElementById('permissionDescription');
    const defaultAccessSelect = document.getElementById('defaultAccess');
    const permissionsTableBody = document.getElementById('permissionsTableBody');


    const customAlertModal = document.getElementById('customAlertModal');
    const customAlertTitle = document.getElementById('customAlertTitle');
    const customAlertMessage = document.getElementById('customAlertMessage');
    const customAlertButtons = document.getElementById('customAlertButtons');


    let allPermissions = [
        { id: 'perm-1', module: 'Dashboard', name: 'View Dashboard Stats', description: 'Allows viewing of overall system statistics and KPIs.', defaultAccess: 'read-only' },
        { id: 'perm-2', module: 'Users', name: 'Manage Users', description: 'Grants full control over user accounts (add, edit, delete).', defaultAccess: 'full-access' },
        { id: 'perm-3', module: 'Roles', name: 'Edit Roles', description: 'Allows modification of existing roles and their descriptions.', defaultAccess: 'restricted' },
        { id: 'perm-4', module: 'Permissions', name: 'Assign Permissions', description: 'Allows assigning specific permissions to roles.', defaultAccess: 'full-access' },
        { id: 'perm-5', module: 'Reports', name: 'Generate Custom Reports', description: 'Enables creation and generation of ad-hoc reports.', defaultAccess: 'read-only' },
    ];

    let dummyRoles = [
        { id: 'role1', name: 'Admin', assignedPermissions: ['perm-1', 'perm-2', 'perm-3', 'perm-4', 'perm-5'] },
        { id: 'role2', name: 'Editor', assignedPermissions: ['perm-1', 'perm-3', 'perm-5'] },
        { id: 'role3', name: 'Viewer', assignedPermissions: ['perm-1', 'perm-5'] },
        { id: 'role4', name: 'Contributor', assignedPermissions: ['perm-1', 'perm-4'] },
        { id: 'role5', name: 'Support', assignedPermissions: ['perm-1'] },
    ];

    let isEditingPermission = false;
    let currentEditingPermissionId = null;


    const showAlert = (title, message, type = 'info') => {
        customAlertTitle.textContent = title;
        customAlertMessage.textContent = message;
        customAlertButtons.innerHTML = `<button class="btn-ok">OK</button>`;
        customAlertModal.style.display = 'block';

        customAlertButtons.querySelector('.btn-ok').onclick = () => {
            customAlertModal.style.display = 'none';
        };
    };

    const showConfirm = (title, message, callback) => {
        customAlertTitle.textContent = title;
        customAlertMessage.textContent = message;
        customAlertButtons.innerHTML = `
                    <button class="btn-ok">Yes</button>
                    <button class="btn-cancel">No</button>
                `;
        customAlertModal.style.display = 'block';

        customAlertButtons.querySelector('.btn-ok').onclick = () => {
            customAlertModal.style.display = 'none';
            callback(true);
        };
        customAlertButtons.querySelector('.btn-cancel').onclick = () => {
            customAlertModal.style.display = 'none';
            callback(false);
        };
    };



    const renderPermissionsTable = () => {
        permissionsTableBody.innerHTML = '';
        allPermissions.forEach(permission => {
            const row = document.createElement('tr');
            const accessBadgeClass = {
                'read-only': 'read-only',
                'full-access': 'full-access',
                'restricted': 'restricted'
            }[permission.defaultAccess] || '';

            const accessBadgeText = {
                'read-only': 'Read-Only',
                'full-access': 'Full Access',
                'restricted': 'Restricted'
            }[permission.defaultAccess] || 'N/A';

            row.innerHTML = `
                        <td>${permission.module}</td>
                        <td>${permission.name}</td>
                        <td>${permission.description}</td>
                        <td><span class="access-badge ${accessBadgeClass}">${accessBadgeText}</span></td>
                        <td>
                            <div class="permission-action-buttons">
                                <button class="permission-action-btn edit" data-id="${permission.id}">Edit</button>
                                <button class="permission-action-btn delete" data-id="${permission.id}">Delete</button>
                            </div>
                        </td>
                    `;
            permissionsTableBody.appendChild(row);
        });


        attachPermissionActionListeners();
    };

    const attachPermissionActionListeners = () => {
        document.querySelectorAll('.permission-action-btn.edit').forEach(button => {
            button.onclick = (event) => editPermission(event.target.dataset.id);
        });
        document.querySelectorAll('.permission-action-btn.delete').forEach(button => {
            button.onclick = (event) => deletePermission(event.target.dataset.id);
        });
    };

    const openPermissionDetailsModal = (permission = null) => {
        permissionDetailsModal.style.display = 'block';
        if (permission) {
            isEditingPermission = true;
            currentEditingPermissionId = permission.id;
            permissionDetailsModalTitle.textContent = 'Edit Permission';
            permissionModuleInput.value = permission.module;
            permissionNameInput.value = permission.name;
            permissionDescriptionInput.value = permission.description;
            defaultAccessSelect.value = permission.defaultAccess;
        } else {
            isEditingPermission = false;
            currentEditingPermissionId = null;
            permissionDetailsModalTitle.textContent = 'Add New Permission';
            permissionModuleInput.value = '';
            permissionNameInput.value = '';
            permissionDescriptionInput.value = '';
            defaultAccessSelect.value = 'read-only';
        }
    };

    const closePermissionDetailsModal = () => {
        permissionDetailsModal.style.display = 'none';
    };

    const savePermissionDetails = () => {
        const module = permissionModuleInput.value.trim();
        const name = permissionNameInput.value.trim();
        const description = permissionDescriptionInput.value.trim();
        const defaultAccess = defaultAccessSelect.value;

        if (!module || !name || !description) {
            showAlert('Validation Error', 'Please fill in all permission fields.');
            return;
        }

        if (isEditingPermission) {

            const index = allPermissions.findIndex(p => p.id === currentEditingPermissionId);
            if (index !== -1) {
                allPermissions[index] = {
                    id: currentEditingPermissionId,
                    module,
                    name,
                    description,
                    defaultAccess
                };
                showAlert('Success', 'Permission updated successfully!');
            } else {
                showAlert('Error', 'Permission not found for editing.');
            }
        } else {

            const newPermission = {
                id: `perm-${crypto.randomUUID().substring(0, 8)}`,
                module,
                name,
                description,
                defaultAccess
            };
            allPermissions.push(newPermission);
            showAlert('Success', 'New permission added successfully!');
        }
        renderPermissionsTable();
        closePermissionDetailsModal();
    };

    const editPermission = (id) => {
        const permissionToEdit = allPermissions.find(p => p.id === id);
        if (permissionToEdit) {
            openPermissionDetailsModal(permissionToEdit);
        } else {
            showAlert('Error', 'Permission not found.');
        }
    };

    const deletePermission = (id) => {
        showConfirm('Confirm Deletion', 'Are you sure you want to delete this permission?', (confirmed) => {
            if (confirmed) {
                allPermissions = allPermissions.filter(p => p.id !== id);
                renderPermissionsTable();
                showAlert('Success', 'Permission deleted successfully!');
            } else {
                showAlert('Cancelled', 'Permission deletion cancelled.');
            }
        });
    };



    const populateRoleDropdown = () => {
        roleSelectModal.innerHTML = '<option value="">Select a role</option>';
        dummyRoles.forEach(role => {
            const option = document.createElement('option');
            option.value = role.id;
            option.textContent = role.name;
            roleSelectModal.appendChild(option);
        });
    };

    const loadPermissionsForRole = (roleId) => {
        const selectedRole = dummyRoles.find(role => role.id === roleId);
        const assignedPerms = selectedRole ? selectedRole.assignedPermissions : [];

        permissionsListContainer.innerHTML = '<h4>Available Permissions:</h4>';

        allPermissions.forEach(permission => {
            const permItem = document.createElement('div');
            permItem.classList.add('permission-item');

            const label = document.createElement('label');
            label.htmlFor = `permission-${permission.id}`;
            label.textContent = permission.name;

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = `permission-${permission.id}`;
            checkbox.dataset.permissionId = permission.id;
            checkbox.checked = assignedPerms.includes(permission.id);

            permItem.appendChild(label);
            permItem.appendChild(checkbox);
            permissionsListContainer.appendChild(permItem);
        });
    };

    const openManageRoleModal = () => {
        populateRoleDropdown();
        managePermissionsModal.style.display = 'block';
        roleSelectModal.value = '';
        permissionsListContainer.innerHTML = '<h4>Available Permissions:</h4>';
    };

    const closeManageRoleModal = () => {
        managePermissionsModal.style.display = 'none';
    };

    const saveRolePermissions = () => {
        const selectedRoleId = roleSelectModal.value;
        if (!selectedRoleId) {
            showAlert('Validation Error', 'Please select a role first!');
            return;
        }

        const selectedPermissionIds = Array.from(
            permissionsListContainer.querySelectorAll('input[type="checkbox"]:checked')
        ).map(cb => cb.dataset.permissionId);


        setTimeout(() => {
            const roleIndex = dummyRoles.findIndex(r => r.id === selectedRoleId);
            if (roleIndex > -1) {
                dummyRoles[roleIndex].assignedPermissions = selectedPermissionIds;
                showAlert('Success', `Permissions for "${dummyRoles[roleIndex].name}" saved successfully!`);
            } else {
                showAlert('Error', 'Role not found in dummy data.');
            }
            closeManageRoleModal();
        }, 500);
    };



    hamburgerMenu.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });

    mainContent.addEventListener('click', (event) => {
        if (window.innerWidth <= 768 && sidebar.classList.contains('active') && !sidebar.contains(event.target) && !hamburgerMenu.contains(event.target)) {
            sidebar.classList.remove('active');
        }
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('active');
            sidebar.classList.remove('hidden');
        } else {
            sidebar.classList.add('hidden');
        }
    });


    if (window.innerWidth <= 768) {
        sidebar.classList.add('hidden');
    }


    const today = new Date();
    const options = { month: 'long', day: 'numeric', year: 'numeric' };
    currentDateElement.textContent = today.toLocaleDateString('en-US', options);


    openManagePermissionsModalBtn.addEventListener('click', openManageRoleModal);
    closeManageModalBtn.addEventListener('click', closeManageRoleModal);
    cancelManageBtn.addEventListener('click', closeManageRoleModal);
    savePermissionsBtn.addEventListener('click', saveRolePermissions);
    roleSelectModal.addEventListener('change', (event) => {
        const selectedRoleId = event.target.value;
        if (selectedRoleId) {
            loadPermissionsForRole(selectedRoleId);
        } else {
            permissionsListContainer.innerHTML = '<h4>Available Permissions:</h4>';
        }
    });


    openAddEditPermissionModalBtn.addEventListener('click', () => openPermissionDetailsModal());
    closePermissionDetailsModalBtn.addEventListener('click', closePermissionDetailsModal);
    cancelPermissionDetailsBtn.addEventListener('click', closePermissionDetailsModal);
    savePermissionDetailsBtn.addEventListener('click', savePermissionDetails);

    window.addEventListener('click', (event) => {
        if (event.target === managePermissionsModal) {
            closeManageRoleModal();
        }
        if (event.target === permissionDetailsModal) {
            closePermissionDetailsModal();
        }
        if (event.target === customAlertModal) {
            customAlertModal.style.display = 'none';
        }
    });


    renderPermissionsTable();
});

//add product
const fileInput = document.getElementById('product-images');
const previewContainer = document.getElementById('preview-container');

fileInput.addEventListener('change', function () {
  previewContainer.innerHTML = '';
  const files = this.files;

  Array.from(files).forEach(file => {
    const reader = new FileReader();
    reader.onload = function (e) {
      const img = document.createElement('img');
      img.src = e.target.result;
      previewContainer.appendChild(img);
    };
    reader.readAsDataURL(file);
  });
});


//onboarding

window.addEventListener('load', () => {
  const modal = new bootstrap.Modal(document.getElementById('welcomeModal'));
  modal.show();
});

function goToHome() {
  window.location.href = "index.html";
}

//profile

 function showTab(tabId, event) {
      document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      event.target.classList.add('active');
    }

    function saveCard(button) {
      const card = button.closest('.card');
      card.classList.add('saved');
      button.disabled = true;
      button.textContent = '✔';
      setTimeout(() => {
        card.classList.remove('saved');
        button.disabled = false;
        button.textContent = '💾';
      }, 2000);
    }


=======
// dashboard
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const hamburgerMenu = document.getElementById('hamburger-menu');
    const mainContent = document.getElementById('main-content');
    const currentDateElement = document.getElementById('current-date');


    const today = new Date();
    const options = { month: 'long', day: 'numeric', year: 'numeric' };
    currentDateElement.textContent = today.toLocaleDateString('en-US', options);


    hamburgerMenu.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });


    mainContent.addEventListener('click', (event) => {
        if (window.innerWidth <= 768 && sidebar.classList.contains('active') && !sidebar.contains(event.target) && !hamburgerMenu.contains(event.target)) {
            sidebar.classList.remove('active');
        }
    });


    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('active');
            sidebar.classList.remove('hidden');
        } else {
            sidebar.classList.add('hidden');
        }
    });


    if (window.innerWidth <= 768) {
        sidebar.classList.add('hidden');
    }

    Chart.defaults.font.family = 'DM Sans, sans-serif';
    Chart.defaults.color = 'var(--text-gray)';
    Chart.defaults.font.size = 12;


    function createGradient(ctx) {
        const gradient = ctx.createLinearGradient(0, 0, 0, 220);
        gradient.addColorStop(0, 'rgba(193, 154, 107, 0.3)');
        gradient.addColorStop(1, 'rgba(193, 154, 107, 0)');
        return gradient;
    }


    const userGrowthCtx = document.getElementById('userGrowthChart').getContext('2d');
    let userGrowthChart = new Chart(userGrowthCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'User Growth',
                data: [100, 120, 150, 130, 180, 200, 250, 280, 320, 380, 450, 520],

                backgroundColor: createGradient(userGrowthCtx),
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: 'var(--accent-color)',
                pointBorderColor: '#C2A57D',
                pointBorderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    titleFont: { family: 'Inter', size: 14, weight: 'bold' },
                    bodyFont: { family: 'DM Sans', size: 12 },
                    backgroundColor: 'rgba(34,34,34,0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    padding: 10,
                    cornerRadius: 6,
                    borderColor: 'var(--accent-color)',
                    borderWidth: 1,
                    displayColors: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: 'var(--text-gray)',
                        font: { family: 'DM Sans', size: 11, weight: 'normal' }
                    },
                    border: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0,0,0,0.08)'
                    },
                    ticks: {
                        color: 'var(--text-gray)',
                        font: { family: 'DM Sans', size: 11, weight: 'normal' },
                        callback: function (value) {
                            return value > 999 ? (value / 1000).toFixed(0) + 'k' : value;
                        }
                    },
                    border: {
                        display: false
                    }
                }
            }
        }
    });


    const userDistributionCtx = document.getElementById('userDistributionChart').getContext('2d');
    let userDistributionChart = new Chart(userDistributionCtx, {
        type: 'doughnut',
        data: {
            labels: ['Admin', 'Executive', 'User', 'Guest'],
            datasets: [{
                data: [52.1, 22.8, 13.9, 11.2],
                backgroundColor: [
                    '#232321',
                    '#C19A6B',
                    '#E6C89C',
                    '#C27D7E'


                ],
                hoverOffset: 8,

                borderWidth: 2,
                spacing: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    titleFont: { family: 'Inter', size: 14, weight: 'bold' },
                    bodyFont: { family: 'DM Sans', size: 12 },
                    callbacks: {
                        label: function (context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed !== null) {
                                label += context.parsed.toFixed(1) + '%';
                            }
                            return label;
                        }
                    },
                    backgroundColor: 'rgba(34,34,34,0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    padding: 10,
                    cornerRadius: 6,
                    borderColor: 'var(--accent-color)',
                    borderWidth: 1,
                    displayColors: true,
                    boxWidth: 10,
                    boxHeight: 10
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            },
            elements: {
                arc: {
                    hoverBorderColor: 'var(--accent-color)',
                }
            }
        }
    });
    const weeklyBtn = document.getElementById('weeklyBtn');
    const monthlyBtn = document.getElementById('monthlyBtn');
    const yearlyBtn = document.getElementById('yearlyBtn');

    const updateChartData = (period) => {
        let newData;
        let newLabels;

        if (period === 'weekly') {
            newLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
            newData = [80, 100, 120, 90, 130, 110, 150];
        } else if (period === 'monthly') {
            newLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            newData = [100, 120, 150, 130, 180, 200, 250, 280, 320, 380, 450, 520];
        } else if (period === 'yearly') {
            newLabels = ['2022', '2023', '2024', '2025'];
            newData = [800, 1000, 1250, 1500];
        }

        userGrowthChart.data.labels = newLabels;
        userGrowthChart.data.datasets[0].data = newData;
        userGrowthChart.data.datasets[0].backgroundColor = createGradient(userGrowthCtx);
        userGrowthChart.update();


        [weeklyBtn, monthlyBtn, yearlyBtn].forEach(btn => btn.classList.remove('active'));
        if (period === 'weekly') weeklyBtn.classList.add('active');
        else if (period === 'monthly') monthlyBtn.classList.add('active');
        else if (period === 'yearly') yearlyBtn.classList.add('active');
    };

    weeklyBtn.addEventListener('click', () => updateChartData('weekly'));
    monthlyBtn.addEventListener('click', () => updateChartData('monthly'));
    yearlyBtn.addEventListener('click', () => updateChartData('yearly'));

    updateChartData('monthly');
});




//permissions
document.addEventListener('DOMContentLoaded', () => {

    const sidebar = document.getElementById('sidebar');
    const hamburgerMenu = document.getElementById('hamburger-menu');
    const mainContent = document.getElementById('main-content');
    const currentDateElement = document.getElementById('current-date');


    const managePermissionsModal = document.getElementById('managePermissionsModal');
    const openManagePermissionsModalBtn = document.getElementById('openManagePermissionsModalBtn');
    const closeManageModalBtn = document.getElementById('closeManageModalBtn');
    const cancelManageBtn = document.getElementById('cancelManageBtn');
    const savePermissionsBtn = document.getElementById('savePermissionsBtn');
    const roleSelectModal = document.getElementById('roleSelectModal');
    const permissionsListContainer = document.getElementById('permissionsList');


    const permissionDetailsModal = document.getElementById('permissionDetailsModal');
    const openAddEditPermissionModalBtn = document.getElementById('openAddEditPermissionModalBtn');
    const closePermissionDetailsModalBtn = document.getElementById('closePermissionDetailsModalBtn');
    const cancelPermissionDetailsBtn = document.getElementById('cancelPermissionDetailsBtn');
    const savePermissionDetailsBtn = document.getElementById('savePermissionDetailsBtn');
    const permissionDetailsModalTitle = document.getElementById('permissionDetailsModalTitle');
    const permissionModuleInput = document.getElementById('permissionModule');
    const permissionNameInput = document.getElementById('permissionName');
    const permissionDescriptionInput = document.getElementById('permissionDescription');
    const defaultAccessSelect = document.getElementById('defaultAccess');
    const permissionsTableBody = document.getElementById('permissionsTableBody');


    const customAlertModal = document.getElementById('customAlertModal');
    const customAlertTitle = document.getElementById('customAlertTitle');
    const customAlertMessage = document.getElementById('customAlertMessage');
    const customAlertButtons = document.getElementById('customAlertButtons');


    let allPermissions = [
        { id: 'perm-1', module: 'Dashboard', name: 'View Dashboard Stats', description: 'Allows viewing of overall system statistics and KPIs.', defaultAccess: 'read-only' },
        { id: 'perm-2', module: 'Users', name: 'Manage Users', description: 'Grants full control over user accounts (add, edit, delete).', defaultAccess: 'full-access' },
        { id: 'perm-3', module: 'Roles', name: 'Edit Roles', description: 'Allows modification of existing roles and their descriptions.', defaultAccess: 'restricted' },
        { id: 'perm-4', module: 'Permissions', name: 'Assign Permissions', description: 'Allows assigning specific permissions to roles.', defaultAccess: 'full-access' },
        { id: 'perm-5', module: 'Reports', name: 'Generate Custom Reports', description: 'Enables creation and generation of ad-hoc reports.', defaultAccess: 'read-only' },
    ];

    let dummyRoles = [
        { id: 'role1', name: 'Admin', assignedPermissions: ['perm-1', 'perm-2', 'perm-3', 'perm-4', 'perm-5'] },
        { id: 'role2', name: 'Editor', assignedPermissions: ['perm-1', 'perm-3', 'perm-5'] },
        { id: 'role3', name: 'Viewer', assignedPermissions: ['perm-1', 'perm-5'] },
        { id: 'role4', name: 'Contributor', assignedPermissions: ['perm-1', 'perm-4'] },
        { id: 'role5', name: 'Support', assignedPermissions: ['perm-1'] },
    ];

    let isEditingPermission = false;
    let currentEditingPermissionId = null;


    const showAlert = (title, message, type = 'info') => {
        customAlertTitle.textContent = title;
        customAlertMessage.textContent = message;
        customAlertButtons.innerHTML = `<button class="btn-ok">OK</button>`;
        customAlertModal.style.display = 'block';

        customAlertButtons.querySelector('.btn-ok').onclick = () => {
            customAlertModal.style.display = 'none';
        };
    };

    const showConfirm = (title, message, callback) => {
        customAlertTitle.textContent = title;
        customAlertMessage.textContent = message;
        customAlertButtons.innerHTML = `
                    <button class="btn-ok">Yes</button>
                    <button class="btn-cancel">No</button>
                `;
        customAlertModal.style.display = 'block';

        customAlertButtons.querySelector('.btn-ok').onclick = () => {
            customAlertModal.style.display = 'none';
            callback(true);
        };
        customAlertButtons.querySelector('.btn-cancel').onclick = () => {
            customAlertModal.style.display = 'none';
            callback(false);
        };
    };



    const renderPermissionsTable = () => {
        permissionsTableBody.innerHTML = '';
        allPermissions.forEach(permission => {
            const row = document.createElement('tr');
            const accessBadgeClass = {
                'read-only': 'read-only',
                'full-access': 'full-access',
                'restricted': 'restricted'
            }[permission.defaultAccess] || '';

            const accessBadgeText = {
                'read-only': 'Read-Only',
                'full-access': 'Full Access',
                'restricted': 'Restricted'
            }[permission.defaultAccess] || 'N/A';

            row.innerHTML = `
                        <td>${permission.module}</td>
                        <td>${permission.name}</td>
                        <td>${permission.description}</td>
                        <td><span class="access-badge ${accessBadgeClass}">${accessBadgeText}</span></td>
                        <td>
                            <div class="permission-action-buttons">
                                <button class="permission-action-btn edit" data-id="${permission.id}">Edit</button>
                                <button class="permission-action-btn delete" data-id="${permission.id}">Delete</button>
                            </div>
                        </td>
                    `;
            permissionsTableBody.appendChild(row);
        });


        attachPermissionActionListeners();
    };

    const attachPermissionActionListeners = () => {
        document.querySelectorAll('.permission-action-btn.edit').forEach(button => {
            button.onclick = (event) => editPermission(event.target.dataset.id);
        });
        document.querySelectorAll('.permission-action-btn.delete').forEach(button => {
            button.onclick = (event) => deletePermission(event.target.dataset.id);
        });
    };

    const openPermissionDetailsModal = (permission = null) => {
        permissionDetailsModal.style.display = 'block';
        if (permission) {
            isEditingPermission = true;
            currentEditingPermissionId = permission.id;
            permissionDetailsModalTitle.textContent = 'Edit Permission';
            permissionModuleInput.value = permission.module;
            permissionNameInput.value = permission.name;
            permissionDescriptionInput.value = permission.description;
            defaultAccessSelect.value = permission.defaultAccess;
        } else {
            isEditingPermission = false;
            currentEditingPermissionId = null;
            permissionDetailsModalTitle.textContent = 'Add New Permission';
            permissionModuleInput.value = '';
            permissionNameInput.value = '';
            permissionDescriptionInput.value = '';
            defaultAccessSelect.value = 'read-only';
        }
    };

    const closePermissionDetailsModal = () => {
        permissionDetailsModal.style.display = 'none';
    };

    const savePermissionDetails = () => {
        const module = permissionModuleInput.value.trim();
        const name = permissionNameInput.value.trim();
        const description = permissionDescriptionInput.value.trim();
        const defaultAccess = defaultAccessSelect.value;

        if (!module || !name || !description) {
            showAlert('Validation Error', 'Please fill in all permission fields.');
            return;
        }

        if (isEditingPermission) {

            const index = allPermissions.findIndex(p => p.id === currentEditingPermissionId);
            if (index !== -1) {
                allPermissions[index] = {
                    id: currentEditingPermissionId,
                    module,
                    name,
                    description,
                    defaultAccess
                };
                showAlert('Success', 'Permission updated successfully!');
            } else {
                showAlert('Error', 'Permission not found for editing.');
            }
        } else {

            const newPermission = {
                id: `perm-${crypto.randomUUID().substring(0, 8)}`,
                module,
                name,
                description,
                defaultAccess
            };
            allPermissions.push(newPermission);
            showAlert('Success', 'New permission added successfully!');
        }
        renderPermissionsTable();
        closePermissionDetailsModal();
    };

    const editPermission = (id) => {
        const permissionToEdit = allPermissions.find(p => p.id === id);
        if (permissionToEdit) {
            openPermissionDetailsModal(permissionToEdit);
        } else {
            showAlert('Error', 'Permission not found.');
        }
    };

    const deletePermission = (id) => {
        showConfirm('Confirm Deletion', 'Are you sure you want to delete this permission?', (confirmed) => {
            if (confirmed) {
                allPermissions = allPermissions.filter(p => p.id !== id);
                renderPermissionsTable();
                showAlert('Success', 'Permission deleted successfully!');
            } else {
                showAlert('Cancelled', 'Permission deletion cancelled.');
            }
        });
    };



    const populateRoleDropdown = () => {
        roleSelectModal.innerHTML = '<option value="">Select a role</option>';
        dummyRoles.forEach(role => {
            const option = document.createElement('option');
            option.value = role.id;
            option.textContent = role.name;
            roleSelectModal.appendChild(option);
        });
    };

    const loadPermissionsForRole = (roleId) => {
        const selectedRole = dummyRoles.find(role => role.id === roleId);
        const assignedPerms = selectedRole ? selectedRole.assignedPermissions : [];

        permissionsListContainer.innerHTML = '<h4>Available Permissions:</h4>';

        allPermissions.forEach(permission => {
            const permItem = document.createElement('div');
            permItem.classList.add('permission-item');

            const label = document.createElement('label');
            label.htmlFor = `permission-${permission.id}`;
            label.textContent = permission.name;

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = `permission-${permission.id}`;
            checkbox.dataset.permissionId = permission.id;
            checkbox.checked = assignedPerms.includes(permission.id);

            permItem.appendChild(label);
            permItem.appendChild(checkbox);
            permissionsListContainer.appendChild(permItem);
        });
    };

    const openManageRoleModal = () => {
        populateRoleDropdown();
        managePermissionsModal.style.display = 'block';
        roleSelectModal.value = '';
        permissionsListContainer.innerHTML = '<h4>Available Permissions:</h4>';
    };

    const closeManageRoleModal = () => {
        managePermissionsModal.style.display = 'none';
    };

    const saveRolePermissions = () => {
        const selectedRoleId = roleSelectModal.value;
        if (!selectedRoleId) {
            showAlert('Validation Error', 'Please select a role first!');
            return;
        }

        const selectedPermissionIds = Array.from(
            permissionsListContainer.querySelectorAll('input[type="checkbox"]:checked')
        ).map(cb => cb.dataset.permissionId);


        setTimeout(() => {
            const roleIndex = dummyRoles.findIndex(r => r.id === selectedRoleId);
            if (roleIndex > -1) {
                dummyRoles[roleIndex].assignedPermissions = selectedPermissionIds;
                showAlert('Success', `Permissions for "${dummyRoles[roleIndex].name}" saved successfully!`);
            } else {
                showAlert('Error', 'Role not found in dummy data.');
            }
            closeManageRoleModal();
        }, 500);
    };



    hamburgerMenu.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });

    mainContent.addEventListener('click', (event) => {
        if (window.innerWidth <= 768 && sidebar.classList.contains('active') && !sidebar.contains(event.target) && !hamburgerMenu.contains(event.target)) {
            sidebar.classList.remove('active');
        }
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('active');
            sidebar.classList.remove('hidden');
        } else {
            sidebar.classList.add('hidden');
        }
    });


    if (window.innerWidth <= 768) {
        sidebar.classList.add('hidden');
    }


    const today = new Date();
    const options = { month: 'long', day: 'numeric', year: 'numeric' };
    currentDateElement.textContent = today.toLocaleDateString('en-US', options);


    openManagePermissionsModalBtn.addEventListener('click', openManageRoleModal);
    closeManageModalBtn.addEventListener('click', closeManageRoleModal);
    cancelManageBtn.addEventListener('click', closeManageRoleModal);
    savePermissionsBtn.addEventListener('click', saveRolePermissions);
    roleSelectModal.addEventListener('change', (event) => {
        const selectedRoleId = event.target.value;
        if (selectedRoleId) {
            loadPermissionsForRole(selectedRoleId);
        } else {
            permissionsListContainer.innerHTML = '<h4>Available Permissions:</h4>';
        }
    });


    openAddEditPermissionModalBtn.addEventListener('click', () => openPermissionDetailsModal());
    closePermissionDetailsModalBtn.addEventListener('click', closePermissionDetailsModal);
    cancelPermissionDetailsBtn.addEventListener('click', closePermissionDetailsModal);
    savePermissionDetailsBtn.addEventListener('click', savePermissionDetails);

    window.addEventListener('click', (event) => {
        if (event.target === managePermissionsModal) {
            closeManageRoleModal();
        }
        if (event.target === permissionDetailsModal) {
            closePermissionDetailsModal();
        }
        if (event.target === customAlertModal) {
            customAlertModal.style.display = 'none';
        }
    });


    renderPermissionsTable();
});

//add product
const fileInput = document.getElementById('product-images');
const previewContainer = document.getElementById('preview-container');

fileInput.addEventListener('change', function () {
  previewContainer.innerHTML = '';
  const files = this.files;

  Array.from(files).forEach(file => {
    const reader = new FileReader();
    reader.onload = function (e) {
      const img = document.createElement('img');
      img.src = e.target.result;
      previewContainer.appendChild(img);
    };
    reader.readAsDataURL(file);
  });
});


//onboarding

window.addEventListener('load', () => {
  const modal = new bootstrap.Modal(document.getElementById('welcomeModal'));
  modal.show();
});

function goToHome() {
  window.location.href = "index.html";
}

//profile

 function showTab(tabId, event) {
      document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      event.target.classList.add('active');
    }

    function saveCard(button) {
      const card = button.closest('.card');
      card.classList.add('saved');
      button.disabled = true;
      button.textContent = '✔';
      setTimeout(() => {
        card.classList.remove('saved');
        button.disabled = false;
        button.textContent = '💾';
      }, 2000);
    }


>>>>>>> bea11e5788aecc70f7901d78c8def434955aa7d5
