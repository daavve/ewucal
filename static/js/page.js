//
//
// Runs the dynamic part of the website for image
//
////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////////////////


function iWindow (iImg) {
    var settings = {
        'longset_side': 500,
        'zoom_max': 20, // 100X initial zoom
    }
    
    var $image = $('.draggable').extend({
        'start_width': parseInt(iImg.width),
        'min_width': null,
        'max_width': null,
        'lw_ratio': null,
        'scale_factor': null,
        'zoom_factor': null,
        'offset_top': null,
        'offset_left': null,
        'middle_x': null,
        'middle_y': null,
        'page_id': parseInt(iImg.pageId),
        'src_length': parseInt(iImg.height),
        'src_width': parseInt(iImg.width),
    })
    
    if ($image.src_image_length > $image.src_image_width) {
        $image.min_width = $image.src_image_width * settings.longset_side / $image.src_image_length
    }
    else {
        $image.min_width = settings.longset_side
    }
    $image.width = $image.min_width
    $image.max_width = $image.min_width * settings.zoom_max
    $image.lw_ratio = $image.src_length / $image.src_width
    $image.height = $image.min_width * $image.lw_ratio
    $image.scale_factor = $image.min_width / $image.start_width
    
    $image.attr("src", iImg.URL).delay("fast");
    $image.css('position', 'absolute').wrap('<div class="page_container"><div class="page_viewport"></div></div>').delay("fast");


    var $viewport = $image.parent().resizable()
    $viewport.extend({
        'middle_x': Math.round($viewport.width() / 2),
        'middle_y': Math.round($viewport.height() / 2),
        'last_selected': null,
        'boxes': null
    })
    $image.offset_left = -$viewport.middle_x / $image.scale_factor
    $image.offset_top = -$viewport.middle_y / $image.scale_factor
    var $container = $viewport.parent();
    
    $viewport.boxes = new Set()
    
    


    
    function updateZoom(){
        if ($zoom_widget.update)
        {
            $image.height = Math.round($image.width * $image.lw_ratio)
            $image.scale_factor = $image.width / $image.start_width
            $image.css({
                'width': Math.round($image.width),
                'height': Math.round($image.width * $image.lw_ratio),
                'left': Math.round($image.offset_left * $image.scale_factor + $viewport.middle_x),
                'top': Math.round($image.offset_top * $image.scale_factor + $viewport.middle_y)
            })
            $zoom_widget.update = false
        }
    };
    var screenupdate = setInterval(updateZoom, 250) 

    var $zoom_widget = $('<div class="jrac_zoom_slider"><div class="ui-slider-handle"></div></div>').extend({'update': true})
        .slider({
            value: $image.min_width,
            min: $image.min_width,
            max: $image.max_width,
            slide: function (event, ui) {
                $zoom_widget.update = true
                $image.width = ui.value
            }})
        
    
    $container.append($zoom_widget);

    $image.draggable({
        drag: function (event, ui) {
            $viewport.middle_x = Math.round($viewport.width() / 2)
            $viewport.middle_y = Math.round($viewport.height() / 2)
            $image.offset_left = (ui.position.left - $viewport.middle_x) / $image.scale_factor
            $image.offset_top = (ui.position.top - $viewport.middle_y) / $image.scale_factor
        },
        scroll: false,
        addClasses: false
    })
    
    function updateBoxPosition($box) {
        $box.css({
            'left': Math.round($image.scale_factor * ($box.x_top + $image.offset_left) + $viewport.middle_x),
            'top': Math.round($image.scale_factor * ($box.y_top + $image.offset_top) + $viewport.middle_y),
            'width': Math.round($image.scale_factor * $box.x_len),
            'height': Math.round($image.scale_factor * $box.y_len)
        })
    }
    function update_boxes() {
        for (let $box of boxes) updateBoxPosition($box);
    }
    function char_click( event, ui, me){
        $(me).toggleClass('char_box_select');    
        if($viewport.last_selected) {   
            $viewport.last_selected.removeClass('ui-selected');    
            $viewport.last_selected.toggleClass('char_box_select');  
            $viewport.last_selected = $(me);
        }
        $viewport.last_selected = $(me);   
    }
    function build_a_box(x1, y1, x2, y2){
        var $charBox = $('<div class="char_box"></div>').css({
            'position': 'absolute'
            }).selectable({
                autoRefresh: false,
                stop: function(event, ui){
                    char_click(event, ui, this);
                }
            }).extend({
                'x_top': x1,
                'y_top': y1,
                'x_len': x2 - x1,
                'y_len': y2 - y1,
                'related_chars': null,
                'selected': false
            }).hover(function(){
                if(!$(this).hasClass('ui-selected')) {
                    $(this).toggleClass('char_box_hover')
                }
            })
            updateBoxPosition($charBox)
            return $charBox;
        }
    }

////////////////////////////////////////////////////////////////////////////////////////


function doFailThing(jqXHR, textStatus, url){
  console.log("---- failure during request to: " + url + " ---------------");
  console.log("Request failed: " + textStatus);
};

function addRelatives(thisChar){
  var url = "/ajax/get_char_relatives";
  $.ajax({
    url: url,
    dataType: "json",
    method: "POST",
    data: {charId: thisChar.pk}
  }).done(function(relativesJSON){
    relatives = JSON.parse(relativesJSON);

    console.log("---------- Got Character Relatives ---------------");
    console.log("thisChar: " + thisChar.pk);
    console.log(relatives);

    if(!charRelativesMap[thisChar.pk])
      charRelativesMap[thisChar.pk] = [];

    relatives.forEach(function(thisRelative){
      // TODO: Implement this check if this relative is already in our map before
      //       inserting it
      // 9/25/2016
      // - Michael Peterson

      charRelativesMap[thisChar.pk].push(thisRelative);
    }, this);

    console.log("---------- Relatives map ---------------");
    console.log(charRelativesMap);
  }).fail(function(jqXHR, textStatus){
    doFailThing(jqXHR, textStatus, url);
  });;
}

// This function should render the bounding box around the characters on the
// as well as wire up any event handlers they need etc.
function buildCharInPage(thisChar){
  // TODO: Implement this function
  // 9/25/2016
  // - Michael Peterson

}

function getPage(pageId){ // get the page object from the server  DOES NOT HANDLE ERRORS!
    return $.getJSON("/ajax/get_page", {"pageId" : pageId})
}


function startMe( $ ){
    var pageId = parseInt(currentPageId = $( "#pageIdHolder" ).attr( "pageId" )) //Get the starting page
    getPage(pageId).done(iWindow)
}


$(document).ready(startMe);
