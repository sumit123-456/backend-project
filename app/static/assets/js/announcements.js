// Announcements Management JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Sample announcements data
    const announcementsData = [
        {
            id: 'ANN001',
            title: 'Company Holiday Schedule for 2025',
            category: 'Company News',
            priority: 'High',
            date: '2025-11-15',
            views: 234,
            status: 'Active',
            expiryDate: '2025-12-31',
            content: 'We are pleased to announce the official holiday schedule for the year 2025. Please review the calendar and plan your leave accordingly.',
            audience: 'All Employees',
            author: 'HR Department'
        },
        {
            id: 'ANN002',
            title: 'New Office Dress Code Policy',
            category: 'Policy Changes',
            priority: 'High',
            date: '2025-11-14',
            views: 189,
            status: 'Active',
            expiryDate: '2025-12-31',
            content: 'Effective immediately, we have updated our dress code policy to ensure a professional workplace environment. Please read the attached document for details.',
            audience: 'All Employees',
            author: 'Management'
        },
        {
            id: 'ANN003',
            title: 'Monthly Team Building Event',
            category: 'Events',
            priority: 'Medium',
            date: '2025-11-13',
            views: 156,
            status: 'Active',
            expiryDate: '2025-11-30',
            content: 'Join us for our monthly team building event on November 25th. Activities include team sports, lunch, and networking opportunities.',
            audience: 'All Employees',
            author: 'HR Team'
        },
        {
            id: 'ANN004',
            title: 'Employee Benefits Update',
            category: 'HR Updates',
            priority: 'Medium',
            date: '2025-11-12',
            views: 201,
            status: 'Active',
            expiryDate: '2025-12-31',
            content: 'We are excited to announce new employee benefits including improved health insurance options and wellness programs.',
            audience: 'All Employees',
            author: 'HR Department'
        },
        {
            id: 'ANN005',
            title: 'IT System Maintenance Notice',
            category: 'General',
            priority: 'Low',
            date: '2025-11-11',
            views: 145,
            status: 'Expired',
            expiryDate: '2025-11-15',
            content: 'Scheduled maintenance for our IT systems will take place this weekend. Some services may be temporarily unavailable.',
            audience: 'All Employees',
            author: 'IT Department'
        },
        {
            id: 'ANN006',
            title: 'Quarterly Performance Reviews',
            category: 'HR Updates',
            priority: 'High',
            date: '2025-11-10',
            views: 312,
            status: 'Active',
            expiryDate: '2025-11-30',
            content: 'Q4 performance reviews will begin next week. Managers should schedule one-on-one meetings with their team members.',
            audience: 'Management',
            author: 'HR Department'
        },
        {
            id: 'ANN007',
            title: 'Office Relocation Update',
            category: 'Company News',
            priority: 'Medium',
            date: '2025-11-09',
            views: 178,
            status: 'Active',
            expiryDate: '2025-12-31',
            content: 'The office relocation to the new building is progressing well. Expected move-in date is January 15, 2025.',
            audience: 'All Employees',
            author: 'Administration'
        },
        {
            id: 'ANN008',
            title: 'New Employee Onboarding Program',
            category: 'HR Updates',
            priority: 'Medium',
            date: '2025-11-08',
            views: 98,
            status: 'Draft',
            expiryDate: '2025-12-31',
            content: 'We have launched a comprehensive onboarding program to help new employees integrate smoothly into our team.',
            audience: 'HR Department',
            author: 'HR Team'
        }
    ];

    let filteredData = [...announcementsData];
    let currentView = 'list'; // 'list' or 'card'

    // Populate the table or cards
    function populateAnnouncements(data = filteredData) {
        if (currentView === 'list') {
            populateTable(data);
        } else {
            populateCards(data);
        }
    }

    // Populate table view
    function populateTable(data) {
        const tableBody = document.getElementById('announcementTableBody');
        if (!tableBody) return;

        tableBody.innerHTML = '';
        
        data.forEach(announcement => {
            const row = document.createElement('tr');
            
            // Priority badge styling
            let priorityBadge = '';
            if (announcement.priority === 'High') {
                priorityBadge = '<span class="badge bg-danger">High</span>';
            } else if (announcement.priority === 'Medium') {
                priorityBadge = '<span class="badge bg-warning text-dark">Medium</span>';
            } else {
                priorityBadge = '<span class="badge bg-secondary">Low</span>';
            }

            // Status badge styling
            let statusBadge = '';
            if (announcement.status === 'Active') {
                statusBadge = '<span class="badge bg-success">Active</span>';
            } else if (announcement.status === 'Draft') {
                statusBadge = '<span class="badge bg-warning text-dark">Draft</span>';
            } else {
                statusBadge = '<span class="badge bg-secondary">Expired</span>';
            }

            row.innerHTML = `
                <td class="px-4 py-3" style="font-size:14px; color:#333; font-weight:600;">${announcement.title}</td>
                <td class="px-4 py-3" style="font-size:14px; color:#666;">${announcement.category}</td>
                <td class="px-4 py-3">${priorityBadge}</td>
                <td class="px-4 py-3" style="font-size:14px; color:#333;">${formatDate(announcement.date)}</td>
                <td class="px-4 py-3" style="font-size:14px; color:#333;">${announcement.views}</td>
                <td class="px-4 py-3">${statusBadge}</td>
                <td class="px-4 py-3">
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="viewAnnouncementDetails('${announcement.id}')">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-success me-1" onclick="editAnnouncement('${announcement.id}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteAnnouncement('${announcement.id}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            
            tableBody.appendChild(row);
        });
    }

    // Populate card view
    function populateCards(data) {
        const cardsContainer = document.getElementById('announcementCards');
        if (!cardsContainer) return;

        cardsContainer.innerHTML = '';
        
        data.forEach(announcement => {
            const cardCol = document.createElement('div');
            cardCol.className = 'col-lg-6 col-md-12';
            
            // Priority badge styling
            let priorityBadge = '';
            if (announcement.priority === 'High') {
                priorityBadge = 'border-danger';
            } else if (announcement.priority === 'Medium') {
                priorityBadge = 'border-warning';
            } else {
                priorityBadge = 'border-secondary';
            }

            // Status badge styling
            let statusBadge = '';
            if (announcement.status === 'Active') {
                statusBadge = '<span class="badge bg-success">Active</span>';
            } else if (announcement.status === 'Draft') {
                statusBadge = '<span class="badge bg-warning text-dark">Draft</span>';
            } else {
                statusBadge = '<span class="badge bg-secondary">Expired</span>';
            }

            cardCol.innerHTML = `
                <div class="card h-100 ${priorityBadge}" style="border-left: 4px solid;">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h6 class="card-title fw-bold mb-0" style="color:#333; font-size:16px;">${announcement.title}</h6>
                            ${statusBadge}
                        </div>
                        <div class="mb-2">
                            <span class="badge bg-light text-dark me-2">${announcement.category}</span>
                            <span class="badge bg-light text-dark">Priority: ${announcement.priority}</span>
                        </div>
                        <p class="card-text text-muted" style="font-size:14px; line-height:1.4;">
                            ${announcement.content.substring(0, 100)}...
                        </p>
                        <div class="d-flex justify-content-between align-items-center mt-3">
                            <small class="text-muted">
                                <i class="fas fa-calendar me-1"></i>${formatDate(announcement.date)}
                            </small>
                            <small class="text-muted">
                                <i class="fas fa-eye me-1"></i>${announcement.views} views
                            </small>
                        </div>
                    </div>
                    <div class="card-footer bg-transparent border-0 pt-0">
                        <div class="btn-group w-100" role="group">
                            <button type="button" class="btn btn-outline-primary btn-sm" onclick="viewAnnouncementDetails('${announcement.id}')">
                                <i class="fas fa-eye me-1"></i>View
                            </button>
                            <button type="button" class="btn btn-outline-success btn-sm" onclick="editAnnouncement('${announcement.id}')">
                                <i class="fas fa-edit me-1"></i>Edit
                            </button>
                            <button type="button" class="btn btn-outline-danger btn-sm" onclick="deleteAnnouncement('${announcement.id}')">
                                <i class="fas fa-trash me-1"></i>Delete
                            </button>
                        </div>
                    </div>
                </div>
            `;
            
            cardsContainer.appendChild(cardCol);
        });
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

    // View announcement details
    window.viewAnnouncementDetails = function(announcementId) {
        const announcement = announcementsData.find(ann => ann.id === announcementId);
        if (!announcement) return;

        const modalContent = document.getElementById('announcementModalContent');
        const modal = new bootstrap.Modal(document.getElementById('announcementDetailsModal'));

        modalContent.innerHTML = `
            <div class="row">
                <div class="col-md-8">
                    <h4 class="fw-bold text-dark mb-3">${announcement.title}</h4>
                    <div class="mb-3">
                        <span class="badge bg-light text-dark me-2">${announcement.category}</span>
                        <span class="badge bg-light text-dark me-2">Priority: ${announcement.priority}</span>
                        <span class="badge bg-light text-dark">Status: ${announcement.status}</span>
                    </div>
                    <div class="border rounded p-3 mb-3" style="background:#f8f9fa;">
                        <p style="line-height:1.6; color:#333; margin:0;">${announcement.content}</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="bg-light rounded p-3">
                        <h6 class="fw-bold text-dark mb-3">Announcement Details</h6>
                        <p class="mb-2"><strong>Published:</strong> ${formatDate(announcement.date)}</p>
                        <p class="mb-2"><strong>Expires:</strong> ${formatDate(announcement.expiryDate)}</p>
                        <p class="mb-2"><strong>Views:</strong> ${announcement.views}</p>
                        <p class="mb-2"><strong>Audience:</strong> ${announcement.audience}</p>
                        <p class="mb-0"><strong>Author:</strong> ${announcement.author}</p>
                    </div>
                </div>
            </div>
        `;

        modal.show();
    };

    // Edit announcement
    window.editAnnouncement = function(announcementId) {
        const announcement = announcementsData.find(ann => ann.id === announcementId);
        if (!announcement) return;

        // Populate the create modal with existing data for editing
        document.getElementById('announcementTitle').value = announcement.title;
        document.getElementById('announcementCategory').value = announcement.category;
        document.getElementById('announcementPriority').value = announcement.priority;
        document.getElementById('announcementExpiry').value = announcement.expiryDate;
        document.getElementById('announcementContent').value = announcement.content;

        // Show the modal
        const modal = new bootstrap.Modal(document.getElementById('createAnnouncementModal'));
        modal.show();

        // Update modal title to indicate editing
        document.getElementById('createAnnouncementModalLabel').innerHTML = 
            '<i class="fas fa-edit me-2"></i>Edit Announcement';
    };

    // Delete announcement
    window.deleteAnnouncement = function(announcementId) {
        if (confirm('Are you sure you want to delete this announcement?')) {
            // Remove from data array
            const index = announcementsData.findIndex(ann => ann.id === announcementId);
            if (index > -1) {
                announcementsData.splice(index, 1);
                filteredData = [...announcementsData];
                populateAnnouncements();
                showToast('Announcement deleted successfully!', 'success');
            }
        }
    };

    // Create announcement
    window.createAnnouncement = function() {
        const form = document.getElementById('createAnnouncementForm');
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        // Get form data
        const title = document.getElementById('announcementTitle').value;
        const category = document.getElementById('announcementCategory').value;
        const priority = document.getElementById('announcementPriority').value;
        const expiryDate = document.getElementById('announcementExpiry').value || '2025-12-31';
        const content = document.getElementById('announcementContent').value;

        // Generate new ID
        const newId = 'ANN' + String(announcementsData.length + 1).padStart(3, '0');

        // Create new announcement
        const newAnnouncement = {
            id: newId,
            title: title,
            category: category,
            priority: priority,
            date: new Date().toISOString().split('T')[0],
            views: 0,
            status: 'Active',
            expiryDate: expiryDate,
            content: content,
            audience: 'All Employees',
            author: 'HR Department'
        };

        // Add to data array
        announcementsData.unshift(newAnnouncement);
        filteredData = [...announcementsData];
        populateAnnouncements();

        // Close modal and reset form
        const modal = bootstrap.Modal.getInstance(document.getElementById('createAnnouncementModal'));
        modal.hide();
        form.reset();

        // Reset modal title
        document.getElementById('createAnnouncementModalLabel').innerHTML = 
            '<i class="fas fa-bullhorn me-2"></i>Create New Announcement';

        showToast('Announcement created successfully!', 'success');
    };

    // Setup search functionality
    function setupSearch() {
        const searchInput = document.querySelector('input[placeholder="Search announcements..."]');
        if (!searchInput) return;

        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const categoryFilter = document.querySelector('select').value;
            const priorityFilter = document.querySelectorAll('select')[1].value;
            const dateFilter = document.querySelector('input[type="date"]').value;

            filterAnnouncements(searchTerm, categoryFilter, priorityFilter, dateFilter);
        });
    }

    // Setup filters
    function setupFilters() {
        const filters = document.querySelectorAll('select');
        
        filters[0]?.addEventListener('change', function() {
            applyFilters();
        });

        filters[1]?.addEventListener('change', function() {
            applyFilters();
        });

        const dateInput = document.querySelector('input[type="date"]');
        dateInput?.addEventListener('change', function() {
            applyFilters();
        });
    }

    // Apply filters
    function applyFilters() {
        const searchTerm = document.querySelector('input[placeholder="Search announcements..."]').value.toLowerCase();
        const categoryFilter = document.querySelector('select').value;
        const priorityFilter = document.querySelectorAll('select')[1].value;
        const dateFilter = document.querySelector('input[type="date"]').value;

        filterAnnouncements(searchTerm, categoryFilter, priorityFilter, dateFilter);
    }

    // Filter announcements
    function filterAnnouncements(searchTerm, categoryFilter, priorityFilter, dateFilter) {
        filteredData = announcementsData.filter(announcement => {
            const matchesSearch = !searchTerm || 
                announcement.title.toLowerCase().includes(searchTerm) ||
                announcement.content.toLowerCase().includes(searchTerm);
            
            const matchesCategory = !categoryFilter || categoryFilter === 'All Categories' ||
                announcement.category === categoryFilter;
            
            const matchesPriority = !priorityFilter || priorityFilter === 'All Priorities' ||
                announcement.priority === priorityFilter;
            
            const matchesDate = !dateFilter || announcement.date === dateFilter;

            return matchesSearch && matchesCategory && matchesPriority && matchesDate;
        });

        populateAnnouncements();
    }

    // Setup view switching
    function setupViewSwitching() {
        const listViewBtn = document.getElementById('listViewBtn');
        const cardViewBtn = document.getElementById('cardViewBtn');
        const listView = document.getElementById('listView');
        const cardView = document.getElementById('cardView');

        listViewBtn?.addEventListener('click', function() {
            currentView = 'list';
            listViewBtn.classList.add('active');
            cardViewBtn.classList.remove('active');
            listView.style.display = 'block';
            cardView.style.display = 'none';
            populateAnnouncements();
        });

        cardViewBtn?.addEventListener('click', function() {
            currentView = 'card';
            cardViewBtn.classList.add('active');
            listViewBtn.classList.remove('active');
            cardView.style.display = 'block';
            listView.style.display = 'none';
            populateAnnouncements();
        });
    }

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

    // Reset modal when closed
    document.getElementById('createAnnouncementModal')?.addEventListener('hidden.bs.modal', function () {
        const form = document.getElementById('createAnnouncementForm');
        form.reset();
        document.getElementById('createAnnouncementModalLabel').innerHTML = 
            '<i class="fas fa-bullhorn me-2"></i>Create New Announcement';
    });

    // Initialize everything
    populateAnnouncements();
    setupSearch();
    setupFilters();
    setupViewSwitching();

    console.log('Announcements Management initialized successfully');
});