
$(window).on('load', function () {
    $('.js-mega-menu').HSMegaMenu({
        event: 'hover',
        pageContainer: $('.container'),
        breakpoint: 767.98,
        hideTimeOut: 0
    });
});

$(document).on('ready', function () {
    $.HSCore.components.HSHeader.init($('#header'));
    $.HSCore.components.HSUnfold.init($('[data-unfold-target]'), {
        afterOpen: function () {
            //$(this).find('input[type="search"]').focus();
        }
    });
    var typed = new Typed(".u-text-animation--typing", {
        strings: ["more professional.", "perfect in every way.", "astonishing."],
        typeSpeed: 60,
        loop: true,
        backSpeed: 25,
        backDelay: 1500
    });
});


