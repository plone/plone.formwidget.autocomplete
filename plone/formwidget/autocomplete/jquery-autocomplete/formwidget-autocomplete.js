(function ($) {
    "use strict"; /*global jQuery: true, document:true */

    function init_pfa_autocomplete() {
        $(".pfa_autocomplete").each(function () {
            var $this = $(this),
                options = $this.find(".autocomplete_options");
            $this.find(".submit-widget").remove();
            $this.find(".textline-field").autocomplete({
                source: options.attr('data-source'),
                minLength: options.attr('data-minLength')
            });
        });

    }
    $(document).on("onLoad", init_pfa_autocomplete);
    $(document).ready(init_pfa_autocomplete);
}(jQuery));