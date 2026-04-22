document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function() {
        // Avval hammasidan 'active'ni olib tashlaymiz
        document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
        // Bosilganiga 'active' qo'shamiz
        this.classList.add('active');
    });
});