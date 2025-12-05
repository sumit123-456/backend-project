// Attendance Management JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Pagination state
    let currentPage = 1;
    let recordsPerPage = 10;
    let filteredData = [];
    
    // Empty attendance data - will be populated from server
    let attendanceData = [];

    // Function to load attendance data from server
    function loadAttendanceData() {
        // This function should be implemented to fetch data from server
        // For now, we'll use empty data
        attendanceData = [];
        populateTable();
    }

    // Populate the table with pagination
    function populateTable(data = attendanceData) {
        const tableBody = document.getElementById('attendanceTableBody');
        const paginationControls = document.getElementById('paginationControls');
        if (!tableBody) return;

        // Store filtered data and reset to first page
        filteredData = data;
        currentPage = 1;

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
        
        if (pageData.length === 0) {
            // Show no data message
            const row = document.createElement('tr');
            row.innerHTML = `
                <td colspan="8" class="text-center py-4">
                    <div class="text-muted">
                        <i class="fas fa-calendar-times fa-3x mb-3"></i>
                        <p class="mb-0">No attendance records found</p>
                        <small>Attendance data will appear here when available.</small>
                    </div>
                </td>
            `;
            tableBody.appendChild(row);
            return;
        }
        
        pageData.forEach(employee => {
            const row = document.createElement('tr');
            
            // Status badge styling
            let statusBadge = '';
            if (employee.status === 'Present') {
                statusBadge = '<span class="badge bg-success">Present</span>';
            } else {
                statusBadge = '<span class="badge bg-danger">Absent</span>';
            }

            // Action buttons
            let actionButtons = `
                <button class="btn btn-sm btn-outline-primary me-1" onclick="viewAttendanceDetails('${employee.empId}')">
                    <i class="fas fa-eye"></i> 
                </button>
            `;

            // Late arrival indicator
            if (employee.lateArrival) {
                actionButtons += `<span class="badge bg-warning text-dark ms-1">Late</span>`;
            }

            row.innerHTML = `
                <td class="px-4 py-3" style="font-size:14px; color:#333;">${employee.empId}</td>
                <td class="px-4 py-3" style="font-size:14px; color:#333;">${employee.name}</td>
                <td class="px-4 py-3" style="font-size:14px; color:#666;">${employee.department}</td>
                <td class="px-4 py-3" style="font-size:14px; color:#333;">${employee.date}</td>
                <td class="px-4 py-3" style="font-size:14px; color:#333;">${employee.checkIn}</td>
                <td class="px-4 py-3" style="font-size:14px; color:#333;">${employee.checkOut}</td>
                <td class="px-4 py-3">${statusBadge}</td>
                <td class="px-4 py-3">${actionButtons}</td>
            `;
            
            tableBody.appendChild(row);
        });

        // Update pagination
        updatePagination(data.length);
    }

    // Update pagination display
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

    // Change page function
    function changePage(page) {
        currentPage = page;
        populateTable(filteredData);
    }

    // Setup records per page selector
    function setupRecordsPerPage() {
        const recordsSelect = document.getElementById('recordsPerPage');
        if (!recordsSelect) return;

        recordsSelect.addEventListener('change', function() {
            recordsPerPage = parseInt(this.value);
            currentPage = 1; // Reset to first page
            populateTable(filteredData);
        });
    }

    // Chart.js Configuration and Initialization
    function initializeCharts() {
        initializeDailyAttendanceChart();
        initializeDepartmentAttendanceChart();
    }

    // Daily Attendance Status Chart
    function initializeDailyAttendanceChart() {
        const ctx = document.getElementById('dailyAttendanceChart');
        if (!ctx) return;

        // Sample data for the last 7 days
        const last7Days = [];
        const presentData = [];
        const absentData = [];
        const lateData = [];

        for (let i = 6; i >= 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            const dateStr = date.toISOString().split('T')[0];
            last7Days.push(date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' }));
            
            // Generate sample data
            const totalPresent = Math.floor(Math.random() * 20) + 440; // 440-460
            const totalAbsent = Math.floor(Math.random() * 10) + 20;  // 20-30
            const totalLate = Math.floor(Math.random() * 15) + 5;     // 5-20
            
            presentData.push(totalPresent);
            absentData.push(totalAbsent);
            lateData.push(totalLate);
        }

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: last7Days,
                datasets: [
                    {
                        label: 'Present',
                        data: presentData,
                        borderColor: '#28a745',
                        backgroundColor: 'rgba(40, 167, 69, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Absent',
                        data: absentData,
                        borderColor: '#dc3545',
                        backgroundColor: 'rgba(220, 53, 69, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Late',
                        data: lateData,
                        borderColor: '#ffc107',
                        backgroundColor: 'rgba(255, 193, 7, 0.1)',
                        tension: 0.4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                },
                elements: {
                    point: {
                        radius: 5,
                        hoverRadius: 7
                    }
                }
            }
        });
    }

    // Department-wise Attendance Chart
    function initializeDepartmentAttendanceChart() {
        const ctx = document.getElementById('departmentAttendanceChart');
        if (!ctx) return;

        // Calculate department-wise data from attendanceData
        const departmentData = {};
        attendanceData.forEach(employee => {
            if (!departmentData[employee.department]) {
                departmentData[employee.department] = { present: 0, absent: 0 };
            }
            if (employee.status === 'Present') {
                departmentData[employee.department].present++;
            } else {
                departmentData[employee.department].absent++;
            }
        });

        const labels = Object.keys(departmentData);
        const presentData = labels.map(dept => departmentData[dept].present);
        const absentData = labels.map(dept => departmentData[dept].absent);

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Present',
                        data: presentData,
                        backgroundColor: [
                            '#28a745',
                            '#17a2b8',
                            '#ffc107',
                            '#6f42c1',
                            '#e83e8c'
                        ],
                        borderWidth: 2,
                        borderColor: '#fff'
                    },
                    {
                        label: 'Absent',
                        data: absentData,
                        backgroundColor: [
                            '#dc3545',
                            '#fd7e14',
                            '#20c997',
                            '#6c757d',
                            '#495057'
                        ],
                        borderWidth: 2,
                        borderColor: '#fff'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.dataset.label || '';
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '50%'
            }
        });
    }

    // View attendance details in modal
    window.viewAttendanceDetails = function(empId) {
        try {
            const employee = attendanceData.find(emp => emp.empId === empId);
            if (!employee) {
                console.error('Employee not found:', empId);
                return;
            }

            const modalElement = document.getElementById('attendanceDetailsModal');
            const modalContent = document.getElementById('modalContent');
            
            if (!modalElement || !modalContent) {
                console.error('Modal elements not found');
                return;
            }

            // Generate detailed content
            modalContent.innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label class="form-label fw-bold text-dark">Employee Information</label>
                            <div class="bg-light p-3 rounded border">
                                <p class="mb-2"><strong>Employee ID:</strong> ${employee.empId}</p>
                                <p class="mb-2"><strong>Name:</strong> ${employee.name}</p>
                                <p class="mb-2"><strong>Department:</strong> ${employee.department}</p>
                                <p class="mb-0"><strong>Date:</strong> ${employee.date}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label class="form-label fw-bold text-dark">Attendance Details</label>
                            <div class="bg-light p-3 rounded border">
                                <p class="mb-2"><strong>Check In:</strong> ${employee.checkIn}</p>
                                <p class="mb-2"><strong>Check Out:</strong> ${employee.checkOut}</p>
                                <p class="mb-2"><strong>Total Hours:</strong> ${employee.totalHours}</p>
                                <p class="mb-0"><strong>Status:</strong> 
                                    <span class="badge ${employee.status === 'Present' ? 'bg-success' : 'bg-danger'}">
                                        ${employee.status}
                                    </span>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-12">
                        <div class="mb-3">
                            <label class="form-label fw-bold text-dark">Additional Information</label>
                            <div class="bg-light p-3 rounded border">
                                <div class="row">
                                    <div class="col-md-4">
                                        <p class="mb-2"><strong>Late Arrival:</strong> 
                                            <span class="badge ${employee.lateArrival ? 'bg-warning text-dark' : 'bg-secondary'}">
                                                ${employee.lateArrival ? 'Yes' : 'No'}
                                            </span>
                                        </p>
                                    </div>
                                    <div class="col-md-4">
                                        <p class="mb-2"><strong>Early Leave:</strong> 
                                            <span class="badge ${employee.earlyLeave ? 'bg-warning text-dark' : 'bg-secondary'}">
                                                ${employee.earlyLeave ? 'Yes' : 'No'}
                                            </span>
                                        </p>
                                    </div>
                                    <div class="col-md-4">
                                        <p class="mb-0"><strong>Attendance Rate:</strong> 
                                            <span class="badge bg-info">${employee.status === 'Present' ? '100%' : '0%'}</span>
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-12">
                        <div class="d-flex gap-2 flex-wrap">
                            <button class="btn btn-primary" onclick="editAttendance('${employee.empId}')">
                                <i class="fas fa-edit me-1"></i> Edit Record
                            </button>
                            <button class="btn btn-success" onclick="exportAttendance('${employee.empId}')">
                                <i class="fas fa-download me-1"></i> Export Data
                            </button>
                        </div>
                    </div>
                </div>
            `;

            // Initialize and show modal without backdrop
            const modal = new bootstrap.Modal(modalElement, {
                backdrop: false,
                keyboard: true
            });
            modal.show();
            
            console.log('Modal shown for employee:', empId);
            
        } catch (error) {
            console.error('Error showing modal:', error);
        }
    };

    // Edit attendance function
    window.editAttendance = function(empId) {
        alert('Edit functionality for employee: ' + empId);
        // Implementation would go here
    };

    // Export attendance function
    window.exportAttendance = function(empId) {
        const employee = attendanceData.find(emp => emp.empId === empId);
        if (!employee) return;
        
        // Create CSV content
        const csvContent = `data:text/csv;charset=utf-8,Employee ID,Name,Department,Date,Check In,Check Out,Status,Total Hours
${employee.empId},${employee.name},${employee.department},${employee.date},${employee.checkIn},${employee.checkOut},${employee.status},${employee.totalHours}`;
        
        // Download the CSV
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", `attendance_${employee.empId}_${employee.date}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    // Search functionality
    function setupSearch() {
        const searchInput = document.querySelector('input[placeholder="Search..."]');
        if (!searchInput) return;

        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const filteredData = attendanceData.filter(employee => 
                employee.empId.toLowerCase().includes(searchTerm) ||
                employee.name.toLowerCase().includes(searchTerm) ||
                employee.department.toLowerCase().includes(searchTerm)
            );
            populateTable(filteredData);
        });
    }

    // Department filter functionality
    function setupDepartmentFilter() {
        const departmentSelect = document.querySelector('select');
        if (!departmentSelect) return;

        departmentSelect.addEventListener('change', function() {
            const selectedDepartment = this.value;
            let filteredData = attendanceData;

            if (selectedDepartment !== 'All Departments') {
                filteredData = attendanceData.filter(employee => 
                    employee.department === selectedDepartment
                );
            }
            
            populateTable(filteredData);
        });
    }

    // Date filter functionality
    function setupDateFilter() {
        const dateInput = document.querySelector('input[type="date"]');
        if (!dateInput) return;

        dateInput.addEventListener('change', function() {
            const selectedDate = this.value;
            let filteredData = attendanceData;

            if (selectedDate) {
                filteredData = attendanceData.filter(employee => 
                    employee.date === selectedDate
                );
            }
            
            populateTable(filteredData);
        });
    }

    // Export all data
    function setupExportButtons() {
        // Export all button
        const exportButtons = document.querySelectorAll('button');
        exportButtons.forEach(button => {
            if (button.innerHTML.includes('fa-download')) {
                button.addEventListener('click', function() {
                    exportAllData();
                });
            }
        });
    }

    function exportAllData() {
        // Create CSV content for all data
        let csvContent = "data:text/csv;charset=utf-8,Employee ID,Name,Department,Date,Check In,Check Out,Status,Total Hours\n";
        
        attendanceData.forEach(employee => {
            csvContent += `${employee.empId},${employee.name},${employee.department},${employee.date},${employee.checkIn},${employee.checkOut},${employee.status},${employee.totalHours}\n`;
        });
        
        // Download the CSV
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", `attendance_report_${new Date().toISOString().split('T')[0]}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    // Initialize all functionality
    populateTable();
    setupSearch();
    setupDepartmentFilter();
    setupDateFilter();
    setupExportButtons();
    setupRecordsPerPage();
    initializeCharts();

    // Set current date as default
    const dateInput = document.querySelector('input[type="date"]');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
    }

    console.log('Attendance Management initialized successfully');
});