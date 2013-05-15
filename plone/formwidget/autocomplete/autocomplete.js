function formwidget_autocomplete_new_value(input_box, value, label) {
	//console.log(input_box, value, label);
	
    (function($) {	
	/* Hack around bug as described on
	 * http://stackoverflow.com/questions/15651455/plone-dexterity-relationchoice-widget-clashes-with-jqueryui/16516223#16516223
	 * 
	 * Fortunately, the autocomplete widget is easy to detect, because it 
	 * leaves the "label" argument undefined.
	 * */ 
    if (!label) {
		label = value["item"]["label"];
		value = value["item"]["value"];
		input_box = $(input_box.target);
	}

        var base_id = input_box[0].id.replace(/-widgets-query$/,"");
        var base_name = input_box[0].name.replace(/\.widgets\.query$/,"");
        var widget_base = $('#'+base_id+"-input-fields");

        var all_fields = widget_base.find('input:radio, input:checkbox');
        
        // Clear query box and uncheck any radio boxes
        input_box.val("");
        widget_base.find('input:radio').attr('checked', '');
        
        // If a radio/check box for this value already exists, check it.
        var selected_field = widget_base.find('input[value="' + value + '"]');
        if(selected_field.length) {
            selected_field.each(function() { this.checked = true; });
            return;
        }

        widget_base, base_name, base_id
        // Create the box for this value
        var idx = all_fields.length;
        var klass = widget_base.data('klass');
        var title = widget_base.data('title');
        var type = widget_base.data('input_type');
        var span = $('<span/>').attr("id",base_id+"-"+idx+"-wrapper").attr("class","option");
        span.append($("<label/>").attr("for",base_id+"-"+idx)
                                 .append($('<input>').attr("type",type)
                                                     .attr("id",base_id+"-"+idx)
                                                     .attr("name",base_name+":list")
                                                     .attr("class",klass)
                                                     .attr("title",title)
                                                     .attr("checked","checked")
                                                     .attr("value",value)
                                                     )
                                 .append(" ")
                                 .append($("<span>").attr("class","label").text(label))
                                 );
        widget_base.append(span);
        // In respect of the source. Does that (still) make sence?
        if (!label) {
           // data["item"]["value"] = ""	
	   label = "";
	}
	
    }(jQuery));
}
