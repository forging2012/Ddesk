$(document).ready(function() {
    $("[aria-label='loading']").click(function() {
        $(this).addClass('is-loading');
    });
    $("button.delete").click(function() {
        $(".notification").hide();
    });
    $("#nav-toggle").click(function() {
        $("#nav-toggle").toggleClass("is-active");
        $("#nav-menu").toggleClass("is-active");
    });
    $(document).activeNavigation("aside");

    // Modal card
    $('.modal-button').click(function() {
        var target = $(this).data('target');
        var href = $(this).data('href');
        $('html').addClass('is-clipped');
        $(target).addClass('is-active');
        $('#confirm').attr("href", href);
    });

    $('.modal-background, .modal-close').click(function() {
        $('html').removeClass('is-clipped');
        $(this).parent().removeClass('is-active');
    });

    $('.modal-card-head .delete, .modal-card-foot .button').click(function() {
        $('html').removeClass('is-clipped');
        $('#modal-ter').removeClass('is-active');
    });
    // Modal card End
});

(function($) {
    $.fn.activeNavigation = function(selector) {
        var pathname = window.location.pathname
        var extension_position;
        var href;
        var hrefs = []
        $(selector).find("a").each(function() {
            // Remove href file extension
            if ($(this).attr("href")) {
                extension_position = $(this).attr("href").lastIndexOf('.');
            }
            href = (extension_position >= 0) ? $(this).attr("href").substr(0, extension_position) : $(this).attr("href");

            if (pathname.indexOf(href) > -1) {
                hrefs.push($(this));
            }
        })
        if (hrefs.length) {
            hrefs.sort(function(a, b) {
                return b.attr("href").length - a.attr("href").length
            })
            hrefs[0].closest('a').addClass("is-active");
            hrefs[0].closest("[aria-haspopup='true']").addClass("active")
        }
    };
})(jQuery);
(jQuery);
(jQuery);
