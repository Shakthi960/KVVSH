document.addEventListener('DOMContentLoaded', function () {

    /* ===============================
   BUSINESS SLIDER
=============================== */

const slides = document.querySelectorAll('.bs-slide');
const thumbs = document.querySelectorAll('.bs-thumb');
const bar = document.querySelector('.bs-progress-bar');

if (slides.length > 0) {

    const INTERVAL = 4000;

    let current = 0;
    let timer = null;

    function goTo(n) {

        slides[current].classList.remove('active');
        thumbs[current].classList.remove('active');

        current = (n + slides.length) % slides.length;

        slides[current].classList.add('active');
        thumbs[current].classList.add('active');

        resetBar();

    }

    function resetBar() {

        if (!bar) return;

        bar.style.transition = 'none';
        bar.style.width = '0%';

        requestAnimationFrame(() => {

            requestAnimationFrame(() => {

                bar.style.transition =
                    `width ${INTERVAL}ms linear`;

                bar.style.width = '100%';

            });

        });

    }

    function startAuto() {

        stopAuto();

        timer = setInterval(() => {
            goTo(current + 1);
        }, INTERVAL);

        resetBar();

    }

    function stopAuto() {
        clearInterval(timer);
    }

    thumbs.forEach(thumb => {

        thumb.addEventListener('click', () => {

            goTo(parseInt(thumb.dataset.thumb));

            stopAuto();
            startAuto();

        });

    });

    const prevBtn = document.querySelector('.bs-prev');
    const nextBtn = document.querySelector('.bs-next');

    if (prevBtn) {

        prevBtn.addEventListener('click', () => {

            goTo(current - 1);

            stopAuto();
            startAuto();

        });

    }

    if (nextBtn) {

        nextBtn.addEventListener('click', () => {

            goTo(current + 1);

            stopAuto();
            startAuto();

        });

    }

    const section = document.querySelector(
        '.business-slider-section'
    );

    if (section) {

        section.addEventListener('mouseenter', stopAuto);

        section.addEventListener('mouseleave', startAuto);

        let touchX = 0;

        section.addEventListener(
            'touchstart',
            e => {
                touchX = e.touches[0].clientX;
            },
            { passive: true }
        );

        section.addEventListener('touchend', e => {

            const diff =
                touchX - e.changedTouches[0].clientX;

            if (Math.abs(diff) > 50) {

                goTo(
                    diff > 0
                        ? current + 1
                        : current - 1
                );

                stopAuto();
                startAuto();

            }

        });

    }

    startAuto();

}

/* ===============================
   HERO BACKGROUND SLIDER
=============================== */

const heroSlides =
    document.querySelectorAll('.hero-bg-slide');

if (heroSlides.length > 0) {

    let currentHero = 0;

    setInterval(() => {

        heroSlides[currentHero].classList.remove('active');

        currentHero =
            (currentHero + 1) % heroSlides.length;

        heroSlides[currentHero].classList.add('active');

    }, 5000);

}


});
