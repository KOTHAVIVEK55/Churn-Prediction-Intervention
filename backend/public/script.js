document.addEventListener('DOMContentLoaded', () => {
    const authSection = document.getElementById('auth-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const enterBtn = document.getElementById('enter-btn');

    async function loadConfig() {
        try {
            const res = await fetch('/api/config');
            if (res.ok) {
                const config = await res.json();
                const churnLink = document.getElementById('churn-link');
                const growthLink = document.getElementById('growth-link');
                const futureLink = document.getElementById('future-link');
                if (churnLink && config.churnUrl) churnLink.href = config.churnUrl;
                if (growthLink && config.growthUrl) growthLink.href = config.growthUrl;
                if (futureLink && config.futureUrl) futureLink.href = config.futureUrl;
            }
        } catch (err) {
            console.error('Failed to load configuration:', err);
        }
    }
    loadConfig();

    function showDashboard() {
        authSection.classList.add('hidden');
        dashboardSection.classList.remove('hidden');
    }

    if (enterBtn) {
        enterBtn.addEventListener('click', () => {
            showDashboard();
        });
    }
});
