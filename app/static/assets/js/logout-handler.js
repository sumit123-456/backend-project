// Global logout handler function
function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        // Clear any session data
        localStorage.clear();
        sessionStorage.clear();
        
        // Show logout message
        alert('You have been logged out successfully!');
        
        // In a real application, you would redirect to login page
        // window.location.href = '/login.html';
        
        console.log('User logged out');
    }
}

// Add this to global scope
window.handleLogout = handleLogout;

// Optional: Auto-logout on page unload (commented out for demo)
// window.addEventListener('beforeunload', function() {
//     // Could log user activity or save state
// });