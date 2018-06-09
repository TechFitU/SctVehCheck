(function($) {
    $("input[type='text']").keyup(function() {
    	// store current positions in variables
    	var start = this.selectionStart,
        	end = this.selectionEnd;

	    // do your stuff
	    $(this).val( $(this).val().toUpperCase() );

	    // restore from variables...
	    this.setSelectionRange(start, end);


    });

    $("textarea").keyup(function() {
        var start = this.selectionStart,
        end = this.selectionEnd;

	    // do your stuff
	    $(this).val( $(this).val().toUpperCase() );

	    // restore from variables...
	    this.setSelectionRange(start, end);

    });
})(django.jQuery);