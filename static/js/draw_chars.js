//
//
// Runs the dynamic part of the website for image
// This Find offsets also performs the task of validating them
//
////////////////////////////////////////////////////


function iWindow (iImg) {
    var settings = {
        longset_side: 500,
        zoom_max: 20, // 100X initial zoom
    };

    var $image = $('.draggable').extend({
        min_width: null,
        max_width: null,
        lw_ratio: null,
        scale_factor: null,
        zoom_factor: null,
        box_offset_top: null,
        offset_left: null,
        box_offset_left: null,
        position_left: null,
        middle_x: null,
        middle_y: null,
        page_id: iImg.pageId,
        src_length: iImg.height,
        src_width: iImg.width,
        update_boxes: true,
        update_box_visibility: true,
        rotation: 0,
        modified: false,
        box_last_selected: null,
        box_is_selected: false,
        draw_new_box_mode: false,
        x_start: null,
        y_start: null
    });

    
    if ($image.src_image_length > $image.src_image_width) {
        $image.min_width = $image.src_image_width * settings.longset_side / $image.src_image_length;
    }
    else {
        $image.min_width = settings.longset_side;
    }
    $image.width = $image.min_width;
    $image.max_width = $image.min_width * settings.zoom_max;
    $image.lw_ratio = $image.src_length / $image.src_width;
    $image.height = $image.min_width * $image.lw_ratio;
    $image.scale_factor = $image.min_width / $image.src_width;
    
    $image.attr('src', iImg.URL);
    $image.css({'position': 'absolute',
                'transform-origin': 'left bottom'}).wrap('<div class="page_viewport"></div>');


    var $viewport = $image.parent().resizable();
    $viewport.extend({
        middle_x: Math.round($viewport.width() / 2),
        middle_y: Math.round($viewport.height() / 2),
        x_start: null,
        y_start: null
    });

        $viewport.extend({
        draw_overlay: $('<div class="draw-overlay"></div>').selectable({
            start: function(e){
                $viewport.x_start = e.pageX;
                $viewport.y_start = e.pageY;
            },
            stop: function(e){
                let p1 = reverseCoordinates({x: Math.min($viewport.x_start, e.pageX) - 14,
                                             y: Math.min($viewport.y_start, e.pageY) - 14
                                        });
                let p2 = reverseCoordinates({x: Math.max($viewport.x_start, e.pageX) - 14,
                                             y: Math.max($viewport.y_start, e.pageY) - 14
                                        });
                console.log({
                    pageX: Math.min($viewport.x_start, e.pageX)
                });
                build_a_box({
                    x1: p1.x,
                    x2: p2.x,
                    y1: p1.y,
                    y2: p2.y
                });
                $image.update_boxes = true;
                }}).hide()
    });
    $viewport.append($viewport.draw_overlay);
    
    $image.offset_left = -$viewport.middle_x / $image.scale_factor;
    $image.box_offset_left = $image.offset_left;
    $image.offset_top = -$viewport.middle_y / $image.scale_factor;
    $image.box_offset_top = $image.offset_top;
    var $container = $viewport.parent();
    
    $viewport.boxes = new Set();
    
    for(i = 0; i < iImg.chars.length; ++i) {
        build_a_box(iImg.chars[i]);
    }
    
    var screenupdate = setInterval(updateZoom, 10);
    function updateZoom(){
        if ($image.update_boxes)
        {
            $image.update_boxes = false;
            $image.height = Math.round($image.width * $image.lw_ratio);
            $image.scale_factor = $image.width / $image.src_width;
            $viewport.middle_x = Math.round($viewport.width() / 2);
            $viewport.middle_y = Math.round($viewport.height() / 2);
            
            let im_left = Math.round($image.width * $image.lw_ratio);
            $image.css({
                width: Math.round($image.width),
                height: Math.round($image.width * $image.lw_ratio),
                left: Math.round($image.offset_left * $image.scale_factor + $viewport.middle_x),
                top: Math.round($image.offset_top * $image.scale_factor + $viewport.middle_y)
            });   
            if($image.draw_new_box_mode)
            {
                $viewport.draw_overlay.css({
                    width: Math.round($image.width),
                    height: Math.round($image.width * $image.lw_ratio),
                    left: Math.round($image.offset_left * $image.scale_factor + $viewport.middle_x),
                    top: Math.round($image.offset_top * $image.scale_factor + $viewport.middle_y)
                });
            }
            for (let boxPack of $viewport.boxes)
            {
                updateBoxPosition(boxPack.selectable);
                updateBoxPosition(boxPack.resizable);
            }
        }
    }
    
    function reverseCoordinates(xy) {
        return  {x: Math.round((xy.x - $viewport.middle_x) / $image.scale_factor - $image.box_offset_left),
                 y: Math.round((xy.y  - $viewport.middle_y) / $image.scale_factor - $image.box_offset_top)
                };
    }

    
    function updateBoxPosition($box) {
        $box.css({
            left: Math.round($image.scale_factor * ($box.x_top + $image.box_offset_left) + $viewport.middle_x),
            top: Math.round($image.scale_factor * ($box.y_top + $image.box_offset_top) + $viewport.middle_y),
            width: Math.round($image.scale_factor * $box.x_len),
            height: Math.round($image.scale_factor * $box.y_len)
        });
    }
    
    
    var $zoom_widget = $('<div class="ui-slider-handle"></div>')
        .slider({
            value: $image.min_width,
            min: $image.min_width,
            max: $image.max_width,
            slide: function (event, ui) {
                $image.update_boxes = true;
                $image.width = ui.value;
            }});
    $container.append($zoom_widget);

    function updateOffsetsForRotation(){
        if($image.rotation == 90)
        {
            $image.offset_left = $image.box_offset_left;
            $image.offset_top = $image.box_offset_top - $image.src_length;
        }
        else
        {
            if($image.rotation == 180)
            {
                $image.offset_left = $image.box_offset_left + $image.src_width;
                $image.offset_top = $image.box_offset_top - $image.src_length;
            }
            else
            {
                if($image.rotation == 270)
                {
                    $image.offset_left = $image.box_offset_left + $image.src_length;
                    $image.offset_top =  $image.box_offset_top - $image.src_width / 2;
                }
                else // $image.rotation == 360
                {
                    $image.rotation = 0;
                    $image.offset_top = $image.box_offset_top;
                    $image.offset_left = $image.box_offset_left;
                }
            }
        }
    }
    
    $image.draggable({  // Can correct image spazzing out using cursorAt for rotated images.
        drag: function (event, ui) {
            $image.box_offset_left = (ui.position.left - $viewport.middle_x) / $image.scale_factor;
            $image.box_offset_top = (ui.position.top - $viewport.middle_y) / $image.scale_factor;
            updateOffsetsForRotation();
            $image.update_boxes = true;
        },
        scroll: false
    });
    
    $( '.submit_button' ).button().click(submit_form);
    
    $( '.rotate_button' ).button().click(function() {
        do_rotation();
    });
    
    let num_rotates = iImg.rotation / 90;
    for(i = 0; i < num_rotates; ++i){
        do_rotation();
    }
    
    
    function do_rotation(){
        if(($image.rotation += 90) == 360)
        {
            $image.rotation = 0;
        }
        updateOffsetsForRotation();
        $image.css({'transform': 'rotate(' + $image.rotation + 'deg)'});
        $image.update_boxes = true;
    }
    
    function submit_form(){
        
        alert("NO-WORKY");
        return;
        
        for (let i = 0; i < 4; ++i)
        {
            if(false === $image.boxes_validated[i])
            {
                alert("Check all the sets before re-submitting");
                return;
            }
        }
        
        let xmults = [4];
        let ymults = [4];
        let boxes = [4];
        let hasStuff = [4];
        for (let i = 0; i < 4; ++i)
        {
            let scaleIndex = $image.box_scale_val_set[i] * (iImg.mult_max + 1 - iImg.mult_min) / 1000 + iImg.mult_min;
            xmults[i] = scaleIndex + $image.box_scale_x_offset_set[i] / 1000;
            ymults[i] = scaleIndex + $image.box_scale_y_offset_set[i] / 1000;
            boxes[i] = [];
        }
        for (let $box of $viewport.boxes)
        {
            boxes[$box.collection].push({'id': $box.charId});
            hasStuff[$box.collection] = true;
        }
        
        let scale_set = [];
        for (let i = 0; i < 3; ++i)
        {
            if (hasStuff[i])
            {
                scale_set.push({"Chars_valid": true, "Chars": boxes[i], "xmult": xmults[i], "ymult": ymults[i]});
            }
        }
        if (hasStuff[3])
        {
            scale_set.push({"Chars_valid": false, "Chars": boxes[3], "xmult": xmults[3], "ymult": ymults[3]});
        }
        let message = {"Char_sets": scale_set,
                       "rotation": $image.rotation,
                       "page_id": $image.page_id,
                       "modified": $image.modified,
                       "mult_id": $image.mult_id,
                       "choice_id": $image.choice_id};
                       
        let token = get_csrf_token();

        
        var ajaxcall = $.ajax({
            url: '/ajax/post_offsets',
            data: JSON.stringify(message),
            method: 'POST',
            dataType: 'json',
        }).done(function( data ) {
            location.reload();
            }).fail( function(){
                alert("Something went wrong  Call Dave");
            });
    }
    
    
    function update_box_selection(boxPack){
        let $box = boxPack.selectable;
        let $r_box = boxPack.resizable;
        if($image.box_is_selected && !$image.box_last_selected.selectable.deleted)
        {
                $image.box_last_selected.resizable.hide();
                $image.box_last_selected.selectable.show();
        }
        else
        {
            $image.box_is_selected = true;
        }
        $image.box_last_selected = boxPack;
        $box.hide();
        $r_box.show();
        $image.update_boxes = true;
        
    }
    
    function build_a_box(iChar){
        
        var $charBox = $('<div class="char_box"></div>').selectable({
                autoRefresh: false,
                stop: function(event, ui){
                    let boxPack = $(this).data('self');
                    let $box = boxPack.selectable;
                    update_box_selection(boxPack);
                }}).extend({
                charId : iChar.charId,
                URL : iChar.URL,
                mark : iChar.mark,
                x_top: iChar.x1,
                y_top: iChar.y1,
                x_len: iChar.x2 - iChar.x1,
                y_len: iChar.y2 - iChar.y1,
                x_thumb: iChar.x_thumb,
                y_thumb: iChar.y_thumb,
                selected: false,
                deleted: false,
                changed: false
            }).mouseenter(function(){
                $charBox.toggleClass('char_box', false);
                $charBox.toggleClass('char_box_hover', true);
            }).mouseleave(function(){
                $charBox.toggleClass('char_box_hover', false);
                $charBox.toggleClass('char_box', true);
            });
            
var $dragBox = $('<div class="char_box_resize"></div>').extend({
                charId : iChar.charId,
                x_top: iChar.x1,
                y_top: iChar.y1,
                x_len: iChar.x2 - iChar.x1,
                y_len: iChar.y2 - iChar.y1,
            }).resizable({
                stop: function( event, ui ){
                    $dragBox.x_len = Math.round( ui.size.width / $image.scale_factor);
                    $charBox.x_len = $dragBox.x_len;
                    $dragBox.y_len = Math.round( ui.size.height / $image.scale_factor);
                    $charBox.y_len = $dragBox.y_len;
                    $charBox.changed = true;
                }
            }).draggable({
                stop: function( event, ui ){
                    $dragBox.x_top = Math.round( (ui.position.left - $viewport.middle_x) / $image.scale_factor - $image.box_offset_left );
                    $charBox.x_top = $dragBox.x_top;
                    $dragBox.y_top = Math.round( (ui.position.top - $viewport.middle_y) / $image.scale_factor - $image.box_offset_top );
                    $charBox.y_top = $dragBox.y_top;
                    $charBox.changed = true;
                    console.log({ui: ui.position.left});
                }
            }).hide();
            
            var boxPack = {selectable:$charBox, resizable:$dragBox};

            $charBox.data('self', boxPack);
            $viewport.append($charBox).append($dragBox);
            $viewport.boxes.add(boxPack);
            
            
    }

////////////////////////////////////////////////////////////////////////////////////////

$(document).keydown(function(event) {
    event.preventDefault();
    const keyName = event.key;

  if (keyName === 'ArrowUp') {
        $image.box_offset_top += 50 / $image.scale_factor;
        updateOffsetsForRotation();
    $image.update_boxes = true;
    return;
  }
    if (keyName === 'ArrowDown') {
        $image.box_offset_top -= 50 / $image.scale_factor;
        updateOffsetsForRotation();
        $image.update_boxes = true;
    return;
  }
  
    if (keyName === 'ArrowRight') {
        $image.box_offset_left -= 50 / $image.scale_factor;
        updateOffsetsForRotation();
        $image.update_boxes = true;
        return;
    }
    if (keyName === 'ArrowLeft') {
        $image.box_offset_left += 50 / $image.scale_factor;
        updateOffsetsForRotation();
        $image.update_boxes = true;
    return;
  }
  
    if (keyName === '+') {
        $image.width += $image.width / 10;
        $image.update_boxes = true;
    return;
    }
    
    if (keyName === '-') {
        $image.width -= $image.width / 10;
        $image.update_boxes = true;
    return;
    }
    
   
    if (keyName === 'Insert') {
        if($image.draw_new_box_mode)
        {
            $viewport.draw_overlay.hide();
            $image.draw_new_box_mode = false;
        }
        else
        {
            if($image.box_is_selected)
            {
                $image.box_is_selected = false;
                $image.box_last_selected.resizable.hide();
                $image.box_last_selected.selectable.show();
            }
            $viewport.draw_overlay.show();
            $image.draw_new_box_mode = true;
            $image.update_boxes = true;
        }
        
        
        return;
    }
    if (keyName === 'Delete') {
        if($image.box_is_selected)
        {
            $image.box_is_selected = false;
            $image.box_last_selected.selectable.deleted = true;
            $image.box_last_selected.selectable.changed = true;
            $image.box_last_selected.resizable.hide();
        }
        return;
    }
    
//    console.log(`Key pressed ${keyName}`);

});
}

////////////////////////////////////////////////////////////////////////////////////////


function startMe( $ ){
    var  $dialog = $( "#dialog" ).dialog({autoOpen: false});
    var  $pages = $.getJSON('/ajax/get_to_verify_page').done(iWindow);
}


$(document).ready(startMe);
