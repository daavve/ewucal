//
//
// Runs the dynamic part of the website for image
//
////////////////////////////////////////////////////


function iWindow (iImg) {
    var settings = {
        longset_side: 500,
        zoom_max: 20, // 100X initial zoom
    };

   
    var $image = $('.draggable').extend({
        start_width: parseInt(iImg.width),
        min_width: null,
        max_width: null,
        lw_ratio: null,
        scale_factor: null,
        zoom_factor: null,
        offset_top: null,
        position_top: null,
        offset_left: null,
        position_left: null,
        middle_x: null,
        middle_y: null,
        page_id: parseInt(iImg.pageId),
        src_length: parseInt(iImg.height),
        src_width: parseInt(iImg.width),
        update_boxes: true,
        update_box_visibility: true,
        box_scale_val_set: [0, 0, 0, 0],
        box_scale_x_offset_set: [0, 0, 0, 0],
        box_scale_y_offset_set: [0, 0, 0, 0],
        box_scale_val: 0,
        box_scale_x_offset: 0,
        box_scale_y_offset: 0,
        active_set: 0
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
    $image.scale_factor = $image.min_width / $image.start_width;
    
    $image.attr('src', iImg.URL);
    $image.css('position', 'absolute').wrap('<div class="page_viewport"></div>');


    var $viewport = $image.parent().resizable();
    $viewport.extend({
        middle_x: Math.round($viewport.width() / 2),
        middle_y: Math.round($viewport.height() / 2),
        boxes: null,
        big_box_1: null,
        has_big_box : false

    });
    $image.offset_left = -$viewport.middle_x / $image.scale_factor;
    $image.offset_top = -$viewport.middle_y / $image.scale_factor;
    var $container = $viewport.parent();
    
    $viewport.boxes = new Set();
    
    for(i = 0; i < iImg.chars.length; ++i) {
        build_a_box(iImg.chars[i]);
    }
    
    var screenupdate = setInterval(updateZoom, 50); // this value is a bit lagy, but it keeps the thing from glitching out
    function updateZoom(){
        if ($image.update_boxes)
        {
            $image.height = Math.round($image.width * $image.lw_ratio);
            $image.scale_factor = $image.width / $image.start_width;
            $image.css({
                width: Math.round($image.width),
                height: Math.round($image.width * $image.lw_ratio),
                left: Math.round($image.offset_left * $image.scale_factor + $viewport.middle_x),
                top: Math.round($image.offset_top * $image.scale_factor + $viewport.middle_y)
            });
            $image.update_boxes = false;
            $viewport.middle_x = Math.round($viewport.width() / 2);
            $viewport.middle_y = Math.round($viewport.height() / 2);
            for (let $box of $viewport.boxes)
            {
                updateBoxPosition($box);
            }
        }
        else
        {
            if ($image.update_box_visibility)
            {
                for (let $box of $viewport.boxes)
                {
                    if ($box.collection == $image.active_set)
                    {
                        $box.show();
                    }
                    else
                    {
                        $box.hide();
                    }
                }
                $image.update_box_visibility = false;
            }
        }
        }
    
    function updateBoxPosition($box) {
        let scaleIndex = $image.box_scale_val * (iImg.mult_max + 1 - iImg.mult_min) / 1000 + iImg.mult_min;
        let xmult = scaleIndex + parseFloat($image.box_scale_x_offset / 1000);
        let ymult = scaleIndex + parseFloat($image.box_scale_y_offset / 1000);
        $box.css({
            left: Math.round($image.scale_factor * ($box.x_top * xmult + $image.offset_left) + $viewport.middle_x),
            top: Math.round($image.scale_factor * ($box.y_top * ymult + $image.offset_top) + $viewport.middle_y),
            width: Math.round($image.scale_factor * $box.x_len * xmult),
            height: Math.round($image.scale_factor * $box.y_len * ymult)
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

    var $scale_widget = $('<div class="ui-slider-handle"></div>')
        .slider({
            value: 0,
            min: 0,
            max: 1000,
            slide: function (event, ui) {
                $image.update_boxes = true;
                $image.box_scale_val = ui.value;
            }});
    $container.append($scale_widget);
    
    var $x_offset_widget = $('<div class="ui-slider-handle"></div>')
        .slider({
            value: 0,
            min: -500,
            max: 500,
            slide: function (event, ui) {
                $image.update_boxes = true;
                $image.box_scale_x_offset = ui.value;
            }});
    $container.append($x_offset_widget);
    
    var $y_offset_widget = $('<div class="ui-slider-handle"></div>')
        .slider({
            value: 0,
            min: -500,
            max: 500,
            slide: function (event, ui) {
                $image.update_boxes = true;
                $image.box_scale_y_offset = ui.value;
            }});
    $container.append($y_offset_widget);

    function updateBoxes(){
        for (let $box of $viewport.boxes)
            updateBoxPosition($box);
    }
    
    $image.draggable({
        drag: function (event, ui) {
            $image.position_top  = ui.position.top;
            $image.position_left = ui.position.left;
            $image.offset_left = ($image.position_left - $viewport.middle_x) / $image.scale_factor;
            $image.offset_top = ($image.position_top - $viewport.middle_y) / $image.scale_factor;
            $image.update_boxes = true;
        },
        scroll: false,
        addClasses: false
    });
    
    $( "input" ).checkboxradio();
    $( ".active_bar" ).controlgroup();
    $( "[name='active']").on( "change", switch_active_set );
    
    $( 'button' ).button().click(move_active_set);
    
    function switch_active_set( e ){
        for (let $box of $viewport.boxes)
        {
            if ($box.selected)
            {
                toggle_box_selection($box);
            }
        }
        $image.box_scale_val_set[$image.active_set] = $image.box_scale_val;
        $image.box_scale_x_offset_set[$image.active_set] = $image.box_scale_x_offset;
        $image.box_scale_y_offset_set[$image.active_set] = $image.box_scale_y_offset;
        $image.active_set = parseInt(e.currentTarget.attributes.data.value);
        $image.box_scale_val = $image.box_scale_val_set[$image.active_set];
        $image.box_scale_x_offset = $image.box_scale_x_offset_set[$image.active_set];
        $image.box_scale_y_offset = $image.box_scale_y_offset_set[$image.active_set];
        $scale_widget.slider( "value", $image.box_scale_val);
        $x_offset_widget.slider( "value", $image.box_scale_x_offset);
        $y_offset_widget.slider( "value", $image.box_scale_y_offset);
        $image.update_boxes = true;
        $image.update_box_visibility = true;
    }
    
    function move_active_set(){
        let buttonID = parseInt($(this)[0].attributes.data.value);
        $image.box_scale_val_set[buttonID] = $image.box_scale_val;
        $image.box_scale_x_offset_set[buttonID] = $image.box_scale_x_offset;
        $image.box_scale_y_offset_set[buttonID] = $image.box_scale_y_offset;
        
        for (let $box of $viewport.boxes)
        {
            if ($box.selected)
            {
                toggle_box_selection($box);
                $box.collection = buttonID;
            }
        }
        $image.update_box_visibility = true;
    }
    
    function toggle_box_selection($box){
        if($box.selected)
        {
            $box.toggleClass('char_box_select', false);
            $box.toggleClass('char_box', true);
            $box.selected = false;
        }
        else
        {
            $box.toggleClass('char_box'. false);
            $box.toggleClass('char_box_select', true);
            $box.selected = true;
        }
    }
    
    function build_a_box(iChar){
        var $charBox = $('<div class="char_box"></div>').css({
            position: 'absolute'
            }).selectable({
                autoRefresh: false,
                stop: function(event, ui){
                    let $box = $(this).data('self');
                    toggle_box_selection($box);
                    if($viewport.has_big_box)
                    {
                        $( '#big_img_1' ).attr('src', $box.URL);
                        $viewport.big_box_1.resize({
                                                    width: $box.x_len + 25,
                                                    height: $box.y_len + 25,
                                                    resize: 'content'}
                        ).headerTitle($box.mark);
                        $viewport.big_box_1.contentReload();
                    }
                    else
                    {
                        $viewport.has_big_box = true;
                        $viewport.big_box_1 = $.jsPanel({
                            headerTitle: $box.mark,
                            headerControls: {'controls': 'closeonly'},
                            contentSize:    {width: $box.x_len + 25, height: $box.y_len + 25},
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
                selected: false,
                collection: iChar.collection
            }).mouseenter(function(){
                let $box = $(this).data('self');
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
                let $box = $(this).data('self');
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

            $charBox.data('self', $charBox);
            $viewport.append($charBox);
            $viewport.boxes.add($charBox);
    }
}

////////////////////////////////////////////////////////////////////////////////////////


function startMe( $ ){
    var  $pages = $.getJSON('/ajax/get_todo').done(iWindow);
}


$(document).ready(startMe);
