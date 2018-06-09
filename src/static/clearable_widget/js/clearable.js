(function ($, undefined) {
    $.fn.clearable = function () {
        var $this = this;
        $(".clear-helper", $this.parent()).on('click', function(){
            $(this).addClass('hidden'); $this.val("").focus();
            var form = $this.closest('form');
            if (form) { $(form).trigger('cleared.clearable', [$this]); }
        });
        $this.on('keyup change input', function() {
            if ($(this).val()) {
                $(".clear-helper", $this.parent()).removeClass('hidden');
            } else {
                $(".clear-helper", $this.parent()).addClass('hidden');
            }
        });
    };
})(jQuery);


