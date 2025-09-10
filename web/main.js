// ...existing code...

document.addEventListener('DOMContentLoaded', function () {
    const collapseBtn = document.getElementById('collapseNavBtn');
    const navbarCollapse = document.getElementById('mainNavbar');
    let isCollapsed = false;

    // Searchbar logic
    const searchBtn = document.getElementById('searchBtn');
    const searchbarContainer = document.getElementById('searchbarContainer');
    const closeSearchBtn = document.getElementById('closeSearchBtn');

    if (searchBtn && searchbarContainer && closeSearchBtn) {
        searchBtn.addEventListener('click', () => {
            searchbarContainer.style.display = 'flex';
            searchbarContainer.querySelector('.searchbar-input').focus();
        });
        closeSearchBtn.addEventListener('click', () => {
            searchbarContainer.style.display = 'none';
        });
        document.addEventListener('click', (e) => {
            if (!searchbarContainer.contains(e.target) && !searchBtn.contains(e.target)) {
                searchbarContainer.style.display = 'none';
            }
        });
    }

    // Notification dropdown logic
    const notificationBtn = document.getElementById('notificationBtn');
    const notificationsDropdown = document.getElementById('notificationsDropdown');

    if (notificationBtn && notificationsDropdown) {
        notificationBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            notificationsDropdown.style.display = notificationsDropdown.style.display === 'block' ? 'none' : 'block';
        });
        document.addEventListener('click', (e) => {
            if (!notificationsDropdown.contains(e.target) && !notificationBtn.contains(e.target)) {
                notificationsDropdown.style.display = 'none';
            }
        });
    }

    // Profile dropdown logic
    const profileBtn = document.getElementById('profileBtn');
    const profileDropdown = document.getElementById('profileDropdown');

    if (profileBtn && profileDropdown) {
        profileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            profileDropdown.style.display = profileDropdown.style.display === 'block' ? 'none' : 'block';
        });
        document.addEventListener('click', (e) => {
            if (!profileDropdown.contains(e.target) && !profileBtn.contains(e.target)) {
                profileDropdown.style.display = 'none';
            }
        });
    }

    if (collapseBtn) {
        collapseBtn.addEventListener('click', function () {
            isCollapsed = !isCollapsed;
            if (isCollapsed) {
                navbarCollapse.classList.remove('show');
                collapseBtn.querySelector('span').classList.remove('fa-angle-up');
                collapseBtn.querySelector('span').classList.add('fa-angle-down');
            } else {
                navbarCollapse.classList.add('show');
                collapseBtn.querySelector('span').classList.remove('fa-angle-down');
                collapseBtn.querySelector('span').classList.add('fa-angle-up');
            }
        });
    }

    // Auto-collapse on small screens
    function autoCollapseNavbar() {
        if (window.innerWidth < 992) {
            navbarCollapse.classList.remove('show');
            isCollapsed = true;
            if (collapseBtn) {
                collapseBtn.querySelector('span').classList.remove('fa-angle-up');
                collapseBtn.querySelector('span').classList.add('fa-angle-down');
            }
        } else {
            navbarCollapse.classList.add('show');
            isCollapsed = false;
            if (collapseBtn) {
                collapseBtn.querySelector('span').classList.remove('fa-angle-down');
                collapseBtn.querySelector('span').classList.add('fa-angle-up');
            }
        }
    }
    window.addEventListener('resize', autoCollapseNavbar);
    autoCollapseNavbar();
});