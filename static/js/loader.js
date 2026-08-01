document.addEventListener('DOMContentLoaded', function () {

    var loader = document.getElementById('kvvsh-loader');
    if (!loader) return;

    var navType = 'navigate';
    try {
        var entries = performance.getEntriesByType('navigation');
        if (entries.length) navType = entries[0].type;
    } catch (e) { /* older browsers */ }

    var firstOpen = false;
    try {
        if (!sessionStorage.getItem('kvvsh_seen')) {
            firstOpen = true;
            sessionStorage.setItem('kvvsh_seen', '1');
        }
    } catch (e) {
        firstOpen = true;
    }

    var shouldShow = (navType === 'reload') || firstOpen;

    if (!shouldShow) return;

    document.body.classList.add('loader-lock');
    loader.classList.add('active');

    setTimeout(function () {
        loader.classList.add('zoom');
    }, 1600);

    setTimeout(function () {
        loader.classList.add('done');
        document.body.classList.remove('loader-lock');
    }, 2300);

    setTimeout(function () {
        loader.style.display = 'none';
    }, 3000);

});
