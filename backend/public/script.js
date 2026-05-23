document.addEventListener('DOMContentLoaded', () => {
    const authSection = document.getElementById('auth-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const loginBtn = document.getElementById('login-btn');
    const registerBtn = document.getElementById('register-btn');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const alertBox = document.getElementById('alert-box');

    // Check if already logged in (for simplicity, just checking if token exists)
    if (localStorage.getItem('token')) {
        showDashboard();
    }

    function showAlert(msg, isError = false) {
        alertBox.textContent = msg;
        alertBox.className = 'alert ' + (isError ? 'error' : 'success');
        alertBox.style.display = 'block';
        setTimeout(() => { alertBox.style.display = 'none'; }, 4000);
    }

    function showDashboard() {
        authSection.classList.add('hidden');
        dashboardSection.classList.remove('hidden');
    }

    loginBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        const email = emailInput.value;
        const password = passwordInput.value;

        if (!email || !password) return showAlert('Please enter email and password', true);

        // Fallback admin logic for testing without database
        if (email === 'admin@admin.com' && password === 'admin') {
            localStorage.setItem('token', 'fake-admin-token');
            showAlert('Login successful!');
            setTimeout(showDashboard, 1000);
            return;
        }

        try {
            const res = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const data = await res.json();

            if (res.ok) {
                localStorage.setItem('token', data.token);
                showAlert('Login successful!');
                setTimeout(showDashboard, 1000);
            } else {
                showAlert(data.message || 'Login failed', true);
            }
        } catch (err) {
            showAlert('Error connecting to server. Is it running?', true);
        }
    });

    registerBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        const email = emailInput.value;
        const password = passwordInput.value;

        if (!email || !password) return showAlert('Please enter email and password', true);

        try {
            const res = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const data = await res.json();

            if (res.ok) {
                showAlert('Registration successful! Please login.');
            } else {
                showAlert(data.message || 'Registration failed', true);
            }
        } catch (err) {
            showAlert('Error connecting to server.', true);
        }
    });
});
