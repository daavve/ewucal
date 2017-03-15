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
        boxes: null,
        big_box_1: null,
        has_big_box : false

    });
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
            $image.css({
                width: Math.round($image.width),
                height: Math.round($image.width * $image.lw_ratio),
                left: Math.round($image.offset_left * $image.scale_factor + $viewport.middle_x),
                top: Math.round($image.offset_top * $image.scale_factor + $viewport.middle_y)
            });
            $viewport.middle_x = Math.round($viewport.width() / 2);
            $viewport.middle_y = Math.round($viewport.height() / 2);
            for (let boxPack of $viewport.boxes)
            {
                updateBoxPosition(boxPack.selectable);
                updateBoxPosition(boxPack.resizable);
            }
        }
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
                console.log(ui.value);
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
        scroll: false,
        addClasses: false
    });
    
    $( '.submit_button' ).button().click(submit_form);
    
    $( '.rotate_button' ).button().click(function() {
        do_rotation();
    });
    
    let num_rotates = iImg.rotation / 90; //Pretty Hacky, but works
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
    
    
    //Best bet is probably to hide box and place a draggable in the location in the spot
    function toggle_box_selection(boxPack){
        let $box = boxPack.selectable;
        let $r_box = boxPack.resizable;
        if($image.box_is_selected)
        {
            if($image.box_last_selected.charId != $box.charId)
            {
                $image.box_last_selected.toggleClass('char_box_select', false);
                $image.box_last_selected.toggleClass('char_box', true);
                $image.box_last_selected.selected = false;
            }
        }
        $box.selected = true;
        $image.box_is_selected = true;
        $image.box_last_selected = $box;
        $box.hide();
        $r_box.show();
            
    }
    
    function build_a_box(iChar){
        
        var $charBox = $('<div class="char_box"></div>').css({
            position: 'absolute'
            }).selectable({
                autoRefresh: false,
                stop: function(event, ui){
                    let boxPack = $(this).data('self');
                    let $box = boxPack.selectable;
                    toggle_box_selection(boxPack);
                    if($viewport.has_big_box)
                    {
                        $( '#big_img_1' ).attr('src', $box.URL);
                        $viewport.big_box_1.resize({
                                                    width: $box.x_thumb,
                                                    height: $box.y_thumb,
                                                    resize: 'content'}
                        ).headerTitle($box.mark);
                        $viewport.big_box_1.contentReload();
                    }
                    else
                    {
                        $viewport.has_big_box = true;
                        $viewport.big_box_1 = $.jsPanel({
                            headerTitle: $box.mark,
                            headerControls: {'controls': 'none'},
                            contentSize:    {width: $box.x_thumb, height: $box.y_thumb},
                            position: {
                                my:      "left-top",
                                at:      "left-top",
                                offsetY: 100,
                                offsetX: 800
                            },
                            content: $('<img src="' + $box.URL + '"id="big_img_1">').data('parentBox', $box)
                    }
                    );
                }
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
                collection: iChar.collection
            }).mouseenter(function(){
                let $box = $(this).data('self').selectable;
                if($box.selected)
                {
                    $box.toggleClass('char_box_select', false);
                    $box.toggleClass('char_box_hover2', true);
                }
                else
                {
                    $box.toggleClass('char_box', false);
                    $box.toggleClass('char_box_hover', true);
                }
            }).mouseleave(function(){
                let $box = $(this).data('self').selectable;
                if($box.selected)
                {
                    $box.toggleClass('char_box_hover2', false);
                    $box.toggleClass('char_box_select', true);
                }
                else
                {
                    $box.toggleClass('char_box_hover', false);
                    $box.toggleClass('char_box', true);
                }
            });
            
var $dragBox = $('<div class="char_box_resize"></div>').css({
            position: 'absolute'
            }).resizable().draggable().extend({
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
                collection: iChar.collection
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
        console.log('INS!');
        //TODO: Add new box feature
        return;
    }
    
    if (keyName === 'Delete') {
        $image.box_last_selected.deleted = true;
        $image.box_last_selected.hide();
        return;
    }
    
    console.log(`Key pressed ${keyName}`);

});
}

////////////////////////////////////////////////////////////////////////////////////////


function startMe( $ ){
    var  $dialog = $( "#dialog" ).dialog({autoOpen: false});
    var  $pages = $.getJSON('/ajax/get_to_verify_page').done(iWindow);
}


$(document).ready(startMe);
