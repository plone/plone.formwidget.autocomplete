    function htmlDecode(input){
        var e = document.createElement('div');
        e.innerHTML = input;
        return e.childNodes[0];
    }

    function formwidget_autocomplete_ready(event, data, formatted) {
        var input_box = $(event.target);
        var base_id = input_box[0].id.replace(/-widgets-query$/,"");
        var widget_base = $('#'+base_id+"-input-fields");

        var all_fields = widget_base.find('input:radio, input:checkbox');
        
        // Clear query box and uncheck any radio boxes
        input_box.val("");
        widget_base.find('input:radio').attr('checked', '');
        
        // If a radio/check box for this value already exists, check it.
        var selected_field = $('#'+base_id+'-input-fields input[value="' + data[0] + '"]');
        if(selected_field.length) {
            selected_field.each(function() { this.checked = true; });
            return;
        }

        // Create the box for this value
        var idx = all_fields.length;
        var klass = widget_base.data('klass');
        var title = widget_base.data('title');
        var type = widget_base.data('input_type');
        var name = input_box[0].name.replace(/\.widgets\.query$/,":list"); //TODO: Is this safe?
        var span = $('<span/>').attr("id",base_id+"-"+idx+"-wrapper").attr("class","option");
        span.append($("<label/>").attr("for",base_id+"-"+idx)
                                 .append($('<input>').attr("type",type)
                                                     .attr("id",base_id+"-"+idx)
                                                     .attr("name",name)
                                                     .attr("class",klass)
                                                     .attr("title",title)
                                                     .attr("checked","checked")
                                                     .attr("value",data[0])
                                                     )
                                 .append($("<span>").attr("class","label").text(data[1]))
                                 );
        $('#'+base_id+'-input-fields').append(span);
    }
