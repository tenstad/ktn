$('.progress').progress();
i = 0;
interval = setInterval(function () {
    $('.progress').progress('increment');
    i += 1;
    if (i >= 100) {
        clearInterval(interval);
        $('.load_complete').css('display', 'block');
    }
}, 250);
