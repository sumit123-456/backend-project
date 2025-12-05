// Leave Approval Management JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Pagination state
    let currentPage = 1;
    let recordsPerPage = 10;
    let filteredData = [];
    let currentLeaveRequest = null;

    // Sample leave requests data
    const leaveRequestsData = [
        {
            id: 'LV001',
            employeeId: 'EMP001',
            employeeName: 'John Smith',
            department: 'IT',
            leaveType: 'annual',
            leaveTypeDisplay: 'Annual Leave',
            startDate: '2025-11-25',
            endDate: '2025-11-27',
            days: 3,
            reason: 'Family vacation planned',
            appliedOn: '2025-11-15',
            status: 'pending',
            requestedBy: 'John Smith',
            contactInfo: 'john.smith@company.com',
            emergencyContact: 'Jane Smith (Spouse) - +1-555-0123'
        },
        {
            id: 'LV002',
            employeeId: 'EMP002',
            employeeName: 'Sarah Johnson',
            department: 'HR',
            leaveType: 'sick',
            leaveTypeDisplay: 'Sick Leave',
            startDate: '2025-11-19',
            endDate: '2025-11-19',
            days: 1,
            reason: 'Flu symptoms, need rest',
            appliedOn: '2025-11-18',
            status: 'pending',
            requestedBy: 'Sarah Johnson',
            contactInfo: 'sarah.johnson@company.com',
            emergencyContact: 'Mike Johnson (Father) - +1-555-0124'
        },
        {
            id: 'LV003',
            employeeId: 'EMP003',
            employeeName: 'Michael Brown',
            department: 'Sales',
            leaveType: 'emergency',
            leaveTypeDisplay: 'Emergency Leave',
            startDate: '2025-11-20',
            endDate: '2025-11-21',
            days: 2,
            reason: 'Medical emergency in family',
            appliedOn: '2025-11-19',
            status: 'approved',
            requestedBy: 'Michael Brown',
            contactInfo: 'michael.brown@company.com',
            emergencyContact: 'Lisa Brown (Sister) - +1-555-0125'
        },
        {
            id: 'LV004',
            employeeId: 'EMP004',
            employeeName: 'Emily Davis',
            department: 'Finance',
            leaveType: 'annual',
            leaveTypeDisplay: 'Annual Leave',
            startDate: '2025-12-01',
            endDate: '2025-12-05',
            days: 5,
            reason: 'Winter break with family',
            appliedOn: '2025-11-10',
            status: 'approved',
            requestedBy: 'Emily Davis',
            contactInfo: 'emily.davis@company.com',
            emergencyContact: 'Robert Davis (Husband) - +1-555-0126'
        },
        {
            id: 'LV005',
            employeeId: 'EMP005',
            employeeName: 'David Wilson',
            department: 'IT',
            leaveType: 'sick',
            leaveTypeDisplay: 'Sick Leave',
            startDate: '2025-11-22',
            endDate: '2025-11-24',
            days: 3,
            reason: 'Recovering from surgery',
            appliedOn: '2025-11-20',
            status: 'pending',
            requestedBy: 'David Wilson',
            contactInfo: 'david.wilson@company.com',
            emergencyContact: 'Dr. Sarah Wilson (Sister) - +1-555-0127'
        },
        {
            id: 'LV006',
            employeeId: 'EMP006',
            employeeName: 'Lisa Anderson',
            department: 'Operations',
            leaveType: 'personal',
            leaveTypeDisplay: 'Personal Leave',
            startDate: '2025-11-28',
            endDate: '2025-11-28',
            days: 1,
            reason: 'Personal matters',
            appliedOn: '2025-11-16',
            status: 'rejected',
            requestedBy: 'Lisa Anderson',
            contactInfo: 'lisa.anderson@company.com',
            emergencyContact: 'Tom Anderson (Brother) - +1-555-0128'
        },
        {
            id: 'LV007',
            employeeId: 'EMP007',
            employeeName: 'Robert Taylor',
            department: 'Sales',
            leaveType: 'annual',
            leaveTypeDisplay: 'Annual Leave',
            startDate: '2025-12-15',
            endDate: '2025-12-19',
            days: 5,
            reason: 'Christmas vacation',
            appliedOn: '2025-11-12',
            status: 'pending',
            requestedBy: 'Robert Taylor',
            contactInfo: 'robert.taylor@company.com',
            emergencyContact: 'Mary Taylor (Wife) - +1-555-0129'
        },
        {
            id: 'LV008',
            employeeId: 'EMP008',
            employeeName: 'Jennifer Martinez',
            department: 'HR',
            leaveType: 'maternity',
            leaveTypeDisplay: 'Maternity Leave',
            startDate: '2025-12-01',
            endDate: '2026-03-01',
            days: 90,
            reason: 'Maternity leave',
            appliedOn: '2025-11-01',
            status: 'approved',
            requestedBy: 'Jennifer Martinez',
            contactInfo: 'jennifer.martinez@company.com',
            emergencyContact: 'Carlos Martinez (Husband) - +1-555-0130'
        }
    ];

    // Initialize
    filteredData = [...leaveRequestsData];
    populateLeaveTable();
    setupFilters();
    setupViewButtons();
    setupPagination();
    setupRecordsPerPage();

    // Populate the leave table
    function populateLeaveTable(data = filteredData) {
        const tableBody = document.getElementById('leaveTableBody');
        const paginationControls = document.getElementById('paginationControls');
        if (!tableBody) return;

        // Show/hide pagination controls based on data length
        if (data.length > recordsPerPage) {
            paginationControls.style.display = 'flex';
        } else {
            paginationControls.style.display = 'none';
        }

        // Calculate start and end indices for current page
        const startIndex = (currentPage - 1) * recordsPerPage;
        const endIndex = Math.min(startIndex + recordsPerPage, data.length);
        const pageData = data.slice(startIndex, endIndex);

        tableBody.innerHTML = '';
        
        pageData.forEach(leave => {
            const row = document.createElement('tr');
            
            // Status badge styling
            let statusBadge = '';
            if (leave.status === 'pending') {
                statusBadge = '<span class="badge bg-warning text-dark">Pending</span>';
            } else if (leave.status === 'approved') {
                statusBadge = '<span class="badge bg-success">Approved</span>';
            } else {
                statusBadge = '<span class="badge bg-danger">Rejected</span>';
            }

            // Leave type badge
            let leaveTypeBadge = '';
            switch(leave.leaveType) {
                case 'annual':
                    leaveTypeBadge = '<span class="badge bg-primary">Annual</span>';
                    break;
                case 'sick':
                    leaveTypeBadge = '<span class="badge bg-info">Sick</span>';
                    break;
                case 'emergency':
                    leaveTypeBadge = '<span class="badge bg-danger">Emergency</span>';
                    break;
                case 'maternity':
                    leaveTypeBadge = '<span class="badge bg-purple" style="background-color: #6f42c1;">Maternity</span>';
                    break;
                case 'personal':
                    leaveTypeBadge = '<span class="badge bg-secondary">Personal</span>';
                    break;
            }

            // Action buttons based on status
            let actionButtons = '';
            if (leave.status === 'pending') {
                actionButtons = `
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="viewLeaveDetails('${leave.id}')">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-success me-1" onclick="quickApprove('${leave.id}')">
                        <i class="fas fa-check"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="quickReject('${leave.id}')">
                        <i class="fas fa-times"></i>
                    </button>
                `;
            } else {
                actionButtons = `
                    <button class="btn btn-sm btn-outline-primary" onclick="viewLeaveDetails('${leave.id}')">
                        <i class="fas fa-eye"></i>
                    </button>
                `;
            }

            row.innerHTML = `
                <td class="px-4 py-3" style="font-size:14px; color:#333;">
                    <div>
                        <div style="font-weight:600;">${leave.employeeName}</div>
                        <div style="font-size:12px; color:#666;">${leave.employeeId} • ${leave.department}</div>
                    </div>
                </td>
                <td class="px-4 py-3">${leaveTypeBadge}</td>
                <td class="px-4 py-3" style="font-size:14px; color:#333;">${formatDate(leave.startDate)}</td>
                <td class="px-4 py-3" style="font-size:14px; color:#333;">${formatDate(leave.endDate)}</td>
                <td class="px-4 py-3" style="font-size:14px; color:#333; font-weight:600;">${leave.days}</td>
                <td class="px-4 py-3" style="font-size:14px; color:#333;">
                    <div style="max-width:200px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${leave.reason}">
                        ${leave.reason}
                    </div>
                </td>
                <td class="px-4 py-3" style="font-size:14px; color:#333;">${formatDate(leave.appliedOn)}</td>
                <td class="px-4 py-3">${statusBadge}</td>
                <td class="px-4 py-3">${actionButtons}</td>
            `;
            
            tableBody.appendChild(row);
        });

        // Update pagination
        updatePagination(data.length);
    }

    // Format date helper
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
    }

    // View leave details
    window.viewLeaveDetails = function(leaveId) {
        const leave = leaveRequestsData.find(l => l.id === leaveId);
        if (!leave) return;

        currentLeaveRequest = leave;
        const modalContent = document.getElementById('leaveModalContent');
        const modal = new bootstrap.Modal(document.getElementById('leaveDetailsModal'));

        modalContent.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <div class="mb-3">
                        <label class="form-label fw-bold text-dark">Employee Information</label>
                        <div class="bg-light p-3 rounded border">
                            <p class="mb-2"><strong>Name:</strong> ${leave.employeeName}</p>
                            <p class="mb-2"><strong>Employee ID:</strong> ${leave.employeeId}</p>
                            <p class="mb-2"><strong>Department:</strong> ${leave.department}</p>
                            <p class="mb-0"><strong>Contact:</strong> ${leave.contactInfo}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="mb-3">
                        <label class="form-label fw-bold text-dark">Leave Details</label>
                        <div class="bg-light p-3 rounded border">
                            <p class="mb-2"><strong>Leave Type:</strong> ${leave.leaveTypeDisplay}</p>
                            <p class="mb-2"><strong>Start Date:</strong> ${formatDate(leave.startDate)}</p>
                            <p class="mb-2"><strong>End Date:</strong> ${formatDate(leave.endDate)}</p>
                            <p class="mb-0"><strong>Total Days:</strong> ${leave.days} day(s)</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-12">
                    <div class="mb-3">
                        <label class="form-label fw-bold text-dark">Reason for Leave</label>
                        <div class="bg-light p-3 rounded border">
                            <p style="margin:0; line-height:1.6;">${leave.reason}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-6">
                    <div class="mb-3">
                        <label class="form-label fw-bold text-dark">Application Details</label>
                        <div class="bg-light p-3 rounded border">
                            <p class="mb-2"><strong>Applied On:</strong> ${formatDate(leave.appliedOn)}</p>
                            <p class="mb-0"><strong>Requested By:</strong> ${leave.requestedBy}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="mb-3">
                        <label class="form-label fw-bold text-dark">Emergency Contact</label>
                        <div class="bg-light p-3 rounded border">
                            <p class="mb-0">${leave.emergencyContact}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-12">
                    <div class="mb-3">
                        <label class="form-label fw-bold text-dark">Current Status</label>
                        <div class="bg-light p-3 rounded border">
                            <span class="badge ${leave.status === 'pending' ? 'bg-warning text-dark' : leave.status === 'approved' ? 'bg-success' : 'bg-danger'} fs-6">
                                ${leave.status.charAt(0).toUpperCase() + leave.status.slice(1)}
                            </span>
                            <small class="text-muted ms-2">Applied ${formatDate(leave.appliedOn)}</small>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Show/hide approve/reject buttons based on status
        const approveBtn = document.getElementById('approveBtn');
        const rejectBtn = document.getElementById('rejectBtn');
        
        if (leave.status === 'pending') {
            approveBtn.style.display = 'inline-block';
            rejectBtn.style.display = 'inline-block';
        } else {
            approveBtn.style.display = 'none';
            rejectBtn.style.display = 'none';
        }

        modal.show();
    };

    // Quick approve
    window.quickApprove = function(leaveId) {
        const leave = leaveRequestsData.find(l => l.id === leaveId);
        if (leave && leave.status === 'pending') {
            if (confirm(`Approve leave request for ${leave.employeeName}?`)) {
                leave.status = 'approved';
                filteredData = [...leaveRequestsData];
                populateLeaveTable();
                showToast(`Leave approved for ${leave.employeeName}`, 'success');
            }
        }
    };

    // Quick reject
    window.quickReject = function(leaveId) {
        const leave = leaveRequestsData.find(l => l.id === leaveId);
        if (leave && leave.status === 'pending') {
            currentLeaveRequest = leave;
            const modal = new bootstrap.Modal(document.getElementById('rejectionReasonModal'));
            modal.show();
        }
    };

    // Approve leave
    window.approveLeave = function() {
        if (currentLeaveRequest && currentLeaveRequest.status === 'pending') {
            currentLeaveRequest.status = 'approved';
            filteredData = [...leaveRequestsData];
            populateLeaveTable();
            
            const modal = bootstrap.Modal.getInstance(document.getElementById('leaveDetailsModal'));
            modal.hide();
            
            showToast(`Leave approved for ${currentLeaveRequest.employeeName}`, 'success');
        }
    };

    // Reject leave with reason
    window.confirmRejection = function() {
        const reason = document.getElementById('rejectionReason').value.trim();
        if (!reason) {
            alert('Please provide a rejection reason.');
            return;
        }

        if (currentLeaveRequest && currentLeaveRequest.status === 'pending') {
            currentLeaveRequest.status = 'rejected';
            currentLeaveRequest.rejectionReason = reason;
            filteredData = [...leaveRequestsData];
            populateLeaveTable();
            
            const rejectionModal = bootstrap.Modal.getInstance(document.getElementById('rejectionReasonModal'));
            const detailsModal = bootstrap.Modal.getInstance(document.getElementById('leaveDetailsModal'));
            
            rejectionModal.hide();
            if (detailsModal) detailsModal.hide();
            
            showToast(`Leave rejected for ${currentLeaveRequest.employeeName}`, 'danger');
        }
    };

    // Reject leave (from details modal)
    window.rejectLeave = function() {
        if (currentLeaveRequest && currentLeaveRequest.status === 'pending') {
            const detailsModal = bootstrap.Modal.getInstance(document.getElementById('leaveDetailsModal'));
            detailsModal.hide();
            
            const rejectionModal = new bootstrap.Modal(document.getElementById('rejectionReasonModal'));
            rejectionModal.show();
        }
    };

    // Setup filters
    function setupFilters() {
        const statusFilter = document.getElementById('statusFilter');
        const leaveTypeFilter = document.getElementById('leaveTypeFilter');
        const departmentFilter = document.getElementById('departmentFilter');
        const dateFilter = document.getElementById('dateFilter');
        const searchInput = document.getElementById('searchInput');

        statusFilter?.addEventListener('change', applyFilters);
        leaveTypeFilter?.addEventListener('change', applyFilters);
        departmentFilter?.addEventListener('change', applyFilters);
        dateFilter?.addEventListener('change', applyFilters);
        searchInput?.addEventListener('input', applyFilters);
    }

    // Apply filters
    function applyFilters() {
        const statusFilter = document.getElementById('statusFilter').value;
        const leaveTypeFilter = document.getElementById('leaveTypeFilter').value;
        const departmentFilter = document.getElementById('departmentFilter').value;
        const dateFilter = document.getElementById('dateFilter').value;
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();

        filteredData = leaveRequestsData.filter(leave => {
            const matchesStatus = statusFilter === 'all' || leave.status === statusFilter;
            const matchesLeaveType = leaveTypeFilter === 'all' || leave.leaveType === leaveTypeFilter;
            const matchesDepartment = departmentFilter === 'all' || leave.department === departmentFilter;
            const matchesDate = !dateFilter || leave.startDate >= dateFilter;
            const matchesSearch = !searchTerm || 
                leave.employeeName.toLowerCase().includes(searchTerm) ||
                leave.reason.toLowerCase().includes(searchTerm) ||
                leave.employeeId.toLowerCase().includes(searchTerm);

            return matchesStatus && matchesLeaveType && matchesDepartment && matchesDate && matchesSearch;
        });

        currentPage = 1;
        populateLeaveTable();
    }

    // Setup view buttons
    function setupViewButtons() {
        const allViewBtn = document.getElementById('allViewBtn');
        const pendingViewBtn = document.getElementById('pendingViewBtn');
        const approvedViewBtn = document.getElementById('approvedViewBtn');
        const rejectedViewBtn = document.getElementById('rejectedViewBtn');

        allViewBtn?.addEventListener('click', () => setView('all', allViewBtn));
        pendingViewBtn?.addEventListener('click', () => setView('pending', pendingViewBtn));
        approvedViewBtn?.addEventListener('click', () => setView('approved', approvedViewBtn));
        rejectedViewBtn?.addEventListener('click', () => setView('rejected', rejectedViewBtn));
    }

    // Set view
    function setView(status, button) {
        // Update active button
        document.querySelectorAll('#allViewBtn, #pendingViewBtn, #approvedViewBtn, #rejectedViewBtn').forEach(btn => {
            btn.classList.remove('active');
        });
        button.classList.add('active');

        // Filter data
        if (status === 'all') {
            filteredData = [...leaveRequestsData];
        } else {
            filteredData = leaveRequestsData.filter(leave => leave.status === status);
        }

        currentPage = 1;
        populateLeaveTable();
    }

    // Update pagination
    function updatePagination(totalRecords) {
        const totalPages = Math.ceil(totalRecords / recordsPerPage);
        const pagination = document.getElementById('pagination');
        const recordInfo = document.getElementById('recordInfo');
        
        if (!pagination || !recordInfo) return;

        // Update record info
        const startRecord = (currentPage - 1) * recordsPerPage + 1;
        const endRecord = Math.min(currentPage * recordsPerPage, totalRecords);
        recordInfo.textContent = `Showing ${startRecord}-${endRecord} of ${totalRecords} records`;

        // Clear existing pagination
        pagination.innerHTML = '';

        // Previous button
        const prevLi = document.createElement('li');
        prevLi.className = `page-item ${currentPage === 1 ? 'disabled' : ''}`;
        prevLi.innerHTML = `
            <a class="page-link" href="#" tabindex="-1" aria-disabled="${currentPage === 1}">
                <i class="fas fa-chevron-left"></i>
            </a>
        `;
        if (currentPage > 1) {
            prevLi.addEventListener('click', (e) => {
                e.preventDefault();
                changePage(currentPage - 1);
            });
        }
        pagination.appendChild(prevLi);

        // Page numbers
        const maxVisiblePages = 5;
        let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
        let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
        
        if (endPage - startPage < maxVisiblePages - 1) {
            startPage = Math.max(1, endPage - maxVisiblePages + 1);
        }

        for (let i = startPage; i <= endPage; i++) {
            const li = document.createElement('li');
            li.className = `page-item ${i === currentPage ? 'active' : ''}`;
            li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
            li.addEventListener('click', (e) => {
                e.preventDefault();
                changePage(i);
            });
            pagination.appendChild(li);
        }

        // Next button
        const nextLi = document.createElement('li');
        nextLi.className = `page-item ${currentPage === totalPages ? 'disabled' : ''}`;
        nextLi.innerHTML = `
            <a class="page-link" href="#" aria-disabled="${currentPage === totalPages}">
                <i class="fas fa-chevron-right"></i>
            </a>
        `;
        if (currentPage < totalPages) {
            nextLi.addEventListener('click', (e) => {
                e.preventDefault();
                changePage(currentPage + 1);
            });
        }
        pagination.appendChild(nextLi);
    }

    // Change page
    function changePage(page) {
        currentPage = page;
        populateLeaveTable();
    }

    // Setup pagination
    function setupPagination() {
        // Already handled in updatePagination
    }

    // Setup records per page
    function setupRecordsPerPage() {
        const recordsSelect = document.getElementById('recordsPerPage');
        if (!recordsSelect) return;

        recordsSelect.addEventListener('change', function() {
            recordsPerPage = parseInt(this.value);
            currentPage = 1; // Reset to first page
            populateLeaveTable();
        });
    }

    // Export leave data
    window.exportLeaveData = function() {
        const csvContent = "data:text/csv;charset=utf-8,Employee ID,Employee Name,Department,Leave Type,Start Date,End Date,Days,Reason,Applied On,Status\n";
        
        leaveRequestsData.forEach(leave => {
            csvContent += `${leave.employeeId},${leave.employeeName},${leave.department},${leave.leaveTypeDisplay},${leave.startDate},${leave.endDate},${leave.days},"${leave.reason}",${leave.appliedOn},${leave.status}\n`;
        });
        
        // Download the CSV
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", `leave_approvals_${new Date().toISOString().split('T')[0]}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showToast('Leave data exported successfully!', 'success');
    };

    // Show toast notification
    function showToast(message, type = 'info') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(toast);

        // Auto remove after 3 seconds
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    console.log('Leave Approval Management initialized successfully');
});