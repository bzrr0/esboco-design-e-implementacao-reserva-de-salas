function toggleDarkMode() {
    const body = document.body;
    body.classList.toggle('dark-mode');

    // Save the user's preference in local storage
    if (body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
}

// Apply saved theme on page load
window.onload = function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.body.classList.add(savedTheme === 'dark' ? 'dark-mode' : 'light-mode');
    }

    // Display any existing messages (errors, reservations, etc.)
    displayMessages();
}

// Function to collect and display messages (e.g., error messages or reservation confirmation)
function displayMessages() {
    const errorMessage = document.querySelector('.error-message');
    if (errorMessage) {
        alert(errorMessage.textContent); // Show an alert with the error message
    }

    const reservationMessage = document.querySelector('.reservation-message');
    if (reservationMessage) {
        alert(reservationMessage.textContent); // Show an alert with the reservation message
    }
}
