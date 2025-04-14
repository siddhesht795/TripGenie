// Toggle hamburger menu for mobile
function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}

// Toggle account dropdown
function toggleDropdown(event) {
    event.preventDefault();
    const dropdown = document.getElementById('dropdownMenu');
    dropdown.classList.toggle('show');
}

// Close dropdown if clicked outside
window.onclick = function (event) {
    const dropdown = document.getElementById('dropdownMenu');
    if (!event.target.matches('.auth-btn')) {
        if (dropdown && dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
    }
};

// --------- SIGN IN / SIGN UP Functionality --------- //
// Store user (Sign Up)
function signupUser() {
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    if (!email || !password) {
        alert('Please fill all fields');
        return;
    }
    localStorage.setItem(email, password);
    alert('Account created successfully!');
    window.location.href = 'signin.html'; // Redirect to Sign In
}

// Sign in user
function signinUser() {
    const email = document.getElementById('signin-email').value;
    const password = document.getElementById('signin-password').value;
    const storedPassword = localStorage.getItem(email);
    if (storedPassword && storedPassword === password) {
        alert('Sign in successful!');
        localStorage.setItem('currentUser', email); // Store session
        window.location.href = '../index.html'; // Redirect to Home after login
    } else {
        alert('Invalid email or password');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const signupBtn = document.getElementById('signup-btn');
    if (signupBtn) signupBtn.addEventListener('click', signupUser);

    const signinBtn = document.getElementById('signin-btn');
    if (signinBtn) signinBtn.addEventListener('click', signinUser);
});

// Reveal animations on scroll
window.addEventListener('scroll', function () {
    var reveals = document.querySelectorAll('.reveal');
    for (var i = 0; i < reveals.length; i++) {
        var windowHeight = window.innerHeight;
        var elementTop = reveals[i].getBoundingClientRect().top;
        var elementVisible = 150;
        if (elementTop < windowHeight - elementVisible) {
            reveals[i].classList.add('active');
        }
    }
});

// -------- Handle Get Suggestions Button -------- //
document.getElementById("getSuggestions").addEventListener("click", async () => {
    const source = document.querySelector('.source-input').value;
    const destination = document.querySelector('.destination-input').value;
    const style = document.querySelector('select[name="travelStyle"]').value;
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    if (!source || !destination || !style || !startDate || !endDate) {
        alert('Please fill in all fields to get suggestions!');
        return;
    }

    const currentUser = localStorage.getItem('currentUser');
    if (!currentUser) {
        alert('Please sign in to get AI suggestions!');
        window.location.href = 'auth/signin.html';
        return;
    }

    // Optional: Store user input in localStorage if needed later
    localStorage.setItem('tripData', JSON.stringify({ source, destination, style, startDate, endDate }));

    // Redirect to itinerary page (AI will generate there)
    window.location.href = 'itenary.html';
});
