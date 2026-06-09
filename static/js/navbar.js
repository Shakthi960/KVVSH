document.addEventListener('DOMContentLoaded', function () {

const nav = document.querySelector('.quicklinks');
const navLinks = document.querySelectorAll('.quicklinks > .ql > a');
const mobileToggle = document.querySelector('.mobile-menu-toggle');
const body = document.body;
const html = document.documentElement;

// Prevent errors on pages without mobile navbar
if (!nav || !mobileToggle) return;

/* Mobile Menu */

mobileToggle.addEventListener('click', function (e) {

    e.stopPropagation();

    this.classList.toggle('active');
    nav.classList.toggle('active');

    if (nav.classList.contains('active')) {
        body.classList.add('no-scroll');
        html.classList.add('no-scroll');
    } else {
        body.classList.remove('no-scroll');
        html.classList.remove('no-scroll');
    }

});

/* Mobile Links */

navLinks.forEach(link => {
    link.onclick = null;
});

/* Close Menu */

document.addEventListener('click', function (e) {

    if (
        window.innerWidth <= 767 &&
        !nav.contains(e.target) &&
        !mobileToggle.contains(e.target)
    ) {

        mobileToggle.classList.remove('active');
        nav.classList.remove('active');

        body.classList.remove('no-scroll');
        html.classList.remove('no-scroll');

    }

});

/* Resize */

function handleResize() {

    if (window.innerWidth > 767) {

        mobileToggle.classList.remove('active');
        nav.classList.remove('active');

        body.classList.remove('no-scroll');
        html.classList.remove('no-scroll');

    }

}

let resizeTimer;

window.addEventListener('resize', function () {

    clearTimeout(resizeTimer);

    resizeTimer = setTimeout(handleResize, 250);

});

/* Dropdown */

const dropdownTriggers = document.querySelectorAll('.ql');

dropdownTriggers.forEach(trigger => {

    const dropdown = trigger.querySelector('.dropdown-menu');

    if (!dropdown) return;

    trigger.addEventListener('mouseenter', function () {

        if (window.innerWidth > 767) {

            dropdown.style.display = 'block';

            setTimeout(() => {

                dropdown.style.opacity = '1';
                dropdown.style.visibility = 'visible';

            }, 10);

        }

    });

    trigger.addEventListener('mouseleave', function () {

        if (window.innerWidth > 767) {

            dropdown.style.opacity = '0';
            dropdown.style.visibility = 'hidden';

            setTimeout(() => {

                if (dropdown.style.opacity === '0') {
                    dropdown.style.display = 'none';
                }

            }, 300);

        }

    });

});

/* Close Dropdown */

document.addEventListener('click', function (e) {

    if (window.innerWidth > 767) {

        dropdownTriggers.forEach(trigger => {

            const dropdown = trigger.querySelector('.dropdown-menu');

            if (dropdown && !trigger.contains(e.target)) {

                dropdown.style.opacity = '0';
                dropdown.style.visibility = 'hidden';

                setTimeout(() => {
                    dropdown.style.display = 'none';
                }, 300);

            }

        });

    }

});

/* Scroll Effect */

window.addEventListener('scroll', function () {

    const scrollPosition =
        window.scrollY || document.documentElement.scrollTop;

    if (scrollPosition > 50) {

        nav.classList.add('scrolled');

        if (window.innerWidth <= 767) {

            mobileToggle.querySelectorAll('span').forEach(span => {
                span.style.background = '#000';
            });

        }

    } else {

        nav.classList.remove('scrolled');

        if (window.innerWidth <= 767) {

            mobileToggle.querySelectorAll('span').forEach(span => {
                span.style.background =
                    'linear-gradient(90deg,#000,#7D2AE8)';
            });

        }

    }

});

handleResize();

window.dispatchEvent(new Event('scroll'));


});
