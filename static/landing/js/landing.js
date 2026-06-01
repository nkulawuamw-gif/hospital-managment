document.addEventListener('DOMContentLoaded', function () {

    // AOS init
    AOS.init({ duration: 600, once: true, offset: 50 });

    // Navbar scroll effect
    window.addEventListener('scroll', function () {
        const nav = document.getElementById('mainNav');
        if (window.scrollY > 60) {
            nav.classList.add('navbar-scrolled');
        } else {
            nav.classList.remove('navbar-scrolled');
        }
    });

    // Back to top button
    const backToTop = document.getElementById('backToTop');
    window.addEventListener('scroll', function () {
        backToTop.classList.toggle('show', window.scrollY > 400);
    });
    backToTop.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Animated counters
    function animateCounters() {
        document.querySelectorAll('.counter').forEach(function (el) {
            var target = parseInt(el.getAttribute('data-target'));
            var current = parseInt(el.innerText.replace(/,/g, ''));
            if (current >= target) return;
            var increment = Math.ceil(target / 60);
            var interval = setInterval(function () {
                var val = parseInt(el.innerText.replace(/,/g, '')) + increment;
                if (val >= target) {
                    el.innerText = target.toLocaleString();
                    clearInterval(interval);
                } else {
                    el.innerText = val.toLocaleString();
                }
            }, 25);
        });
    }

    // Trigger counters when stats section is in view
    var countersTriggered = false;
    window.addEventListener('scroll', function () {
        if (countersTriggered) return;
        var stats = document.querySelector('.stats-section');
        if (!stats) return;
        var rect = stats.getBoundingClientRect();
        if (rect.top < window.innerHeight) {
            countersTriggered = true;
            animateCounters();
        }
    });

    // Testimonials Swiper
    new Swiper('.testimonialSwiper', {
        loop: true,
        autoplay: { delay: 4000, disableOnInteraction: false },
        pagination: { el: '.swiper-pagination', clickable: true },
        breakpoints: {
            0: { slidesPerView: 1 },
            768: { slidesPerView: 2 },
            992: { slidesPerView: 2 }
        }
    });

    // Health articles search
    var searchInput = document.getElementById('healthSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            var q = this.value.toLowerCase();
            document.querySelectorAll('.health-article').forEach(function (card) {
                card.style.display = card.textContent.toLowerCase().indexOf(q) > -1 ? '' : 'none';
            });
        });
    }

    // Navbar auto-close on mobile after click
    document.querySelectorAll('.navbar-nav .nav-link').forEach(function (link) {
        link.addEventListener('click', function () {
            var navbar = document.getElementById('mainNavbar');
            var bsCollapse = bootstrap.Collapse.getInstance(navbar);
            if (bsCollapse) bsCollapse.hide();
        });
    });

    // Appointment form submission
    var apptForm = document.getElementById('appointmentForm');
    if (apptForm) {
        apptForm.addEventListener('submit', function (e) {
            var btn = apptForm.querySelector('button[type="submit"]');
            var required = apptForm.querySelectorAll('[required]');
            var valid = true;
            required.forEach(function (el) {
                if (!el.value.trim()) valid = false;
            });
            if (!valid) return;
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Submitting...';
        });
    }

    // Active nav link highlighting on scroll
    var sections = document.querySelectorAll('section[id]');
    window.addEventListener('scroll', function () {
        var scrollPos = window.scrollY + 120;
        sections.forEach(function (section) {
            var top = section.offsetTop;
            var height = section.offsetHeight;
            var id = section.getAttribute('id');
            if (scrollPos >= top && scrollPos < top + height) {
                document.querySelectorAll('.navbar-nav .nav-link').forEach(function (link) {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + id) {
                        link.classList.add('active');
                    }
                });
            }
        });
    });

});
