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
        update_boxes: false
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
        last_selected: null,
        boxes: null,
        has_big_box: false,
        big_box_1: null,
        big_box_2: null,
        big_box_3: null
    });
    $image.offset_left = -$viewport.middle_x / $image.scale_factor;
    $image.offset_top = -$viewport.middle_y / $image.scale_factor;
    var $container = $viewport.parent();
    
    $viewport.boxes = new Set();
    
    for(i = 0; i < iImg.chars.length; ++i) {
        build_a_box(iImg.chars[i]);
    }
    
    var screenupdate = setInterval(updateZoom, 250); // this value is a bit lagy, but it keeps the thing from glitching out
    function updateZoom(){
        if ($zoom_widget.update)
        {
            $image.height = Math.round($image.width * $image.lw_ratio);
            $image.scale_factor = $image.width / $image.start_width;
            $image.css({
                width: Math.round($image.width),
                height: Math.round($image.width * $image.lw_ratio),
                left: Math.round($image.offset_left * $image.scale_factor + $viewport.middle_x),
                top: Math.round($image.offset_top * $image.scale_factor + $viewport.middle_y)
            });
            updateBoxes();
            $zoom_widget.update = false;
        }
        else
        {
            if ($image.update_boxes)
            {
                $viewport.middle_x = Math.round($viewport.width() / 2);
                $viewport.middle_y = Math.round($viewport.height() / 2);
                $image.offset_left = ($image.position_left - $viewport.middle_x) / $image.scale_factor;
                $image.offset_top = ($image.position_top - $viewport.middle_y) / $image.scale_factor;
                updateBoxes();
                $image.update_boxes = false;
            }
        }
    }
    
    function updateBoxes(){
        for (let $box of $viewport.boxes)
            updateBoxPosition($box);
    }
    
    function updateBoxPosition($box) {
        $box.css({
            left: Math.round($image.scale_factor * ($box.x_top + $image.offset_left) + $viewport.middle_x),
            top: Math.round($image.scale_factor * ($box.y_top + $image.offset_top) + $viewport.middle_y),
            width: Math.round($image.scale_factor * $box.x_len),
            height: Math.round($image.scale_factor * $box.y_len)
        });
    }

    var $zoom_widget = $('<div class="jrac_zoom_slider"><div class="ui-slider-handle"></div></div>').extend({'update': true})
        .slider({
            value: $image.min_width,
            min: $image.min_width,
            max: $image.max_width,
            slide: function (event, ui) {
                $zoom_widget.update = true;
                $image.width = ui.value;
            }});
    $container.append($zoom_widget);


    $image.draggable({
        drag: function (event, ui) {
            $image.position_top  = ui.position.top;
            $image.position_left = ui.position.left;
            $image.update_boxes = true;
        },
        scroll: false,
        addClasses: false
    });
    

    
    function toggle_box_colors($box){
        $box.toggleClass('char_box_select');
        if($viewport.last_selected) {   
            $viewport.last_selected.removeClass('ui-selected');
            $viewport.last_selected.toggleClass('char_box_select');
            $viewport.last_selected = $box;
        }
        $viewport.last_selected = $box; 
    }
    
    var $big_char = $('<img src="">');
    function build_a_box(iChar){
        var $charBox = $('<div class="char_box"></div>').css({
            position: 'absolute'
            }).selectable({
                autoRefresh: false,
                stop: function(event, ui){
                    let $box = $(this);
                    toggle_box_colors($box);
                    $big_char.attr('src', $box.data('URL'));
                    if($viewport.has_big_box)
                    {
                        $viewport.big_box_1.resize({
                                                        width: $box.data('width'),
                                                        height: $box.data('height'),
                                                        resize: 'content'});
                    }
                    else
                    {
                        $viewport.has_big_box = true;
                        $viewport.big_box_1 = $.jsPanel({
                            contentSize:    {width: $box.data('width'), height: $box.data('height')},
                            resizable: false,
                            position: {
                                my:      "left-top",
                                at:      "left-top",
                                offsetY: 200,
                                offsetX: 10
                            },
                            headerTitle: $box.data('mark') + ' by ' + $box.data('authName'),
                            onclosed: function(){
                                $viewport.has_big_box = false;
                                $viewport.big_box_2.close();
                            },
                            headerControls: {'controls': 'closeonly'},
                            content: $big_char
                        });
                        $viewport.big_box_2 = $.jsPanel({
                            headerTitle:    'Other ' + $box.data('mark') + ' by ' + $box.data('authName'),
                            contentSize:    {width: '500px', height: '500px'},
                            contentAjax:    {
                                url:        '/ajax/get_char_relatives',
                                method:     'GET',
                                dataType:   'JSON',
                                data:       {charId: $box.data('charId')},
                                done: function( data, textStatus, jqXHR, panel ){
                                    var $container = $('<div class="container"></div>');
                                    $.each(data, function(i, item) {
                                        $container.append('<div class="item"> <img src="' + item.thumb + '" width="' + item.width + '" height="'  + item.height + '" /> </div>');
                                    });
                                    this.content.append($container);
                                    rowGrid($container, {
                                        itemSelector: '.item',
                                        minMargin: 10,
                                        maxMargin: 25,
                                        firstItemClass: 'first-item',
                                        lastRowClass: 'last-row',
                                        resize: true,
                                        minWidth: 500
                                    });
                                },
                            position: {
                                my:      "right-bottom",
                                at:      "right-bottom",
                                offsetY: -10,
                                offsetX: -10
                            },
                            onclosed:   function(){
                                $viewport.has_big_box = false;
                                $viewport.big_box_1.close();
                            },
                        }
                    });
                }
            }
            }).extend({
                charId : iChar.charId,
                pageId : iChar.pageId,
                authorId : iChar.authorId,
                workId : iChar.workId,
                URL : iChar.URL,
                mark : iChar.mark,
                x_top: iChar.x1,
                y_top: iChar.y1,
                x_len: iChar.x2 - iChar.x1,
                y_len: iChar.y2 - iChar.y1,
                related_chars: null,
                selected: false
            }).hover(function(){
                if(!$(this).hasClass('ui-selected')) {
                    $(this).toggleClass('char_box_hover');
                }
            }).data('authName', iChar.authorName
            ).data('mark', iChar.mark
            ).data('URL', iChar.URL
            ).data('charId', iChar.charId
            ).data('height', iChar.y2 - iChar.y1
            ).data('width', iChar.x2 - iChar.x1);

            updateBoxPosition($charBox);
            $viewport.append($charBox);
            $viewport.boxes.add($charBox);
    }
}

////////////////////////////////////////////////////////////////////////////////////////


function getPage(pageId){ // get the page object from the server
    return $.getJSON('/ajax/get_page', {'pageId' : pageId});
}

function getRelChars(charId){
    return $.getJSON('/ajax/get_char_relatives', {'charId': charId});
}

function startMe( $ ){
    var pageId = parseInt(currentPageId = $( '#pageIdHolder' ).attr( 'pageId' ));
    getPage(pageId).done(iWindow);
}


$(document).ready(startMe);
