function checkAuthStatus() {
    const currentUser = localStorage.getItem('currentUser');
    if (!currentUser) {
        window.location.href = 'landing.html';
    } else {
        const userData = JSON.parse(localStorage.getItem(currentUser));
        const userName = document.getElementById('userName');
        if (userName) {
            userName.textContent = `Hello, ${userData.firstname} ${userData.lastname}`;
        }
    }
}

function logout() {
    localStorage.removeItem('currentUser');
    window.location.href = 'landing.html';
}

function signin() {
    const username = document.getElementById('signin-username').value;
    const password = document.getElementById('signin-password').value;

    // Get the full user data object from localStorage
    const storedUserData = localStorage.getItem(username);

    if (!username || !password) {
        showModal('Error', 'Please fill in all fields', 'error');
        return;
    }

    if (!storedUserData) {
        showModal('Error', 'User not found', 'error');
        return;
    }

    // Parse the stored user data
    const userData = JSON.parse(storedUserData);

    if (userData.password === password) {
        localStorage.setItem('currentUser', username);
        const modal = document.getElementById('modal');
        modal.dataset.redirect = '../index.html';
        showModal('Success', 'Sign in successful! Redirecting to home...');
    } else {
        showModal('Error', 'Invalid credentials', 'error');
    }
}

function signup() {
    const userData = {
        firstName: document.getElementById('signup-firstname').value,
        lastName: document.getElementById('signup-lastname').value,
        email: document.getElementById('signup-email').value,
        phone: document.getElementById('signup-phone').value,
        username: document.getElementById('signup-username').value,
        password: document.getElementById('signup-password').value
    };

    // Validate all fields
    if (Object.values(userData).some(value => !value)) {
        showModal('Error', 'Please fill in all fields', 'error');
        return;
    }

    // Validate email format
    if (!validateEmail(userData.email)) {
        showModal('Error', 'Please enter a valid email address', 'error');
        return;
    }

    // Check if username exists
    if (localStorage.getItem(userData.username)) {
        showModal('Error', 'Username already exists', 'error');
        return;
    }

    // Store user data
    localStorage.setItem(userData.username, JSON.stringify(userData));
    const modal = document.getElementById('modal');
    modal.dataset.redirect = 'signin.html';
    showModal('Success', 'Account created successfully! Redirecting to sign in...');
}

function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
