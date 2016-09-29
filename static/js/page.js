//TODO: jCarrotCell works with Jquery2, but not Jquery3
//TODO: jCarrotCell chops off image edges on rectangular images
/*
  function iWindow ( $ ) {
      //Helper-Functions
      function reload() {
          relatedChars = $("#relatedChars").carrotCell({
          navi: true,
          makeNavi: true})
          relatedCharsAPI = $(relatedChars).data("carrotCell")
      }
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
        relatedCharsAPI.reloadWith($(me).attr("related_chars"));

        var thisCharacterId = $(me).attr('id');
        var thisCharacterImage = $(me).attr('image');

        console.log("clicked: { id: " + thisCharacterId + ", image: " + thisCharacterImage + "}");
        $("#leftThumbnail").attr("src", thisCharacterImage);

        reload();
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



      $( "button" ).button().click(function( event ) {
          event.preventDefault();
          alert("clicked!");
      })

      var relatedChars = $("#relatedChars").carrotCell({
          navi: true,
          makeNavi: true
      })
      var relatedCharsAPI = $(relatedChars).data("carrotCell")

    var settings = {
      'longset_side': 500,
      'zoom_max': 20, // 100X initial zoom
    }

    var src_image_length = {{ page.image_length }}
    var src_image_width = {{ page.image_width }}

    var $image = $('.pane img').extend({
      'start_width': null,
      'min_width': null,
      'max_width': null,
      'lw_ratio': null,
      'scale_factor': null,
      'zoom_factor': null,
      'offset_top': null,
      'offset_left': null,
      'middle_x': null,
      'middle_y': null
    })

    if (src_image_length > src_image_width) {
      $image.min_width = src_image_width * settings.longset_side / src_image_length
    }
    else {
      $image.min_width = settings.longset_side
    }
    $image.start_width = src_image_width
    $image.max_width = $image.min_width * settings.zoom_max
    $image.lw_ratio = src_image_length / src_image_width
    $image.scale_factor = $image.min_width / $image.start_width

    $image.width($image.min_width).height($image.min_width * $image.lw_ratio)
    $image.css({'left': 0, 'top': 0});
    $image.css('position', 'absolute').wrap('<div class="page_container"><div class="page_viewport"></div></div>');

    var $viewport = $image.parent().resizable()
    $viewport.extend({
      'middle_x': Math.round($viewport.width() / 2),
      'middle_y': Math.round($viewport.height() / 2),
      'last_selected': null
    })
    $image.offset_left = -$viewport.middle_x / $image.scale_factor
    $image.offset_top = -$viewport.middle_y / $image.scale_factor
    var $container = $viewport.parent();
    var boxes = new Set()

    var $zoom_widget = $('<div class="jrac_zoom_slider"><div class="ui-slider-handle"></div></div>')
        .slider({
          value: $image.longest_side,
          min: $image.min_width,
          max: $image.max_width,
          slide: function (event, ui) {
            $image.width(ui.value).height(Math.round(ui.value * $image.lw_ratio))
            $image.scale_factor = ui.value / $image.start_width
            $image.css({
              'left': Math.round($image.offset_left * $image.scale_factor + $viewport.middle_x),
              'top': Math.round($image.offset_top * $image.scale_factor + $viewport.middle_y)
            });
            update_boxes()
          }
        });
    $container.append($zoom_widget);

    $image.draggable({
      drag: function (event, ui) {
        $viewport.middle_x = Math.round($viewport.width() / 2)
        $viewport.middle_y = Math.round($viewport.height() / 2)
        $image.offset_left = (ui.position.left - $viewport.middle_x) / $image.scale_factor
        $image.offset_top = (ui.position.top - $viewport.middle_y) / $image.scale_factor
        update_boxes()
      },
      scroll: false,
      addClasses: false
    })


     {% for char in a_chars %}
      var char_x1 = {{ char.mainchar.x1 }}
      var char_y1 = {{ char.mainchar.y1 }}
      var char_x2 = {{ char.mainchar.x2 }}
      var char_y2 = {{ char.mainchar.y2 }}
      var $gotbox = build_a_box(char_x1, char_y1, char_x2, char_y2)
      $gotbox.attr("id",    '{{ char.mainchar.id }}');
      $gotbox.attr("image", '{{ char.mainchar.image }}');
      $gotbox.attr("related_chars", ' \
          {% for char_rel in char.relatedChars %} \
              <li> \
                  <a href="{{  char_rel.parent_page.get_absolute_url }}" target="_blank"> \
                    <img id="{{ char_rel.id }}" src="{% static char_rel.get_image %}" /> \
                  </a> \
              </li> \
          {% endfor %} \
      ');
      boxes.add($gotbox)
      $viewport.append($gotbox)
    {% endfor %}
  }
$(document).ready( iWindow )
*/

var pageObject;
var charObjects;
var charRelativesMap = {};

function doFailThing(jqXHR, textStatus, url){
  console.log("---- failure during request to: " + url + " ---------------");
  console.log("Request failed: " + textStatus);
};

function getPageCharacters(){
  var url = "/ajax/get_page_chars";
  $.ajax({
    url: url,
    dataType: "json",
    method: "POST",
    data: {pageId: pageObject.pk}
  }).done(function(charJSON){
    charObjects = JSON.parse(charJSON);

    console.log("---------- Got Char Objects ---------------");
    console.log("thisPage: " + pageObject.pk);
    console.log(charObjects);

    charObjects.forEach(function(thisChar){
      buildCharInPage(thisChar);
      addRelatives(thisChar);
    }, this);
  }).fail(function(jqXHR, textStatus){
    doFailThing(jqXHR, textStatus, url);
  });;
}

function addRelatives(thisChar){
  var url = "/ajax/get_char_relatives";
  $.ajax({
    url: url,
    dataType: "json",
    method: "POST",
    data: {charId: thisChar.pk}
  }).done(function(relativesJSON){
    relatives = JSON.parse(relatives);

    console.log("---------- Got Character Relatives ---------------");
    console.log("thisChar: " + thisChar.id);
    console.log(relatives);

    if(!charRelativesMap[thisChar.pk])
      charRelativesMap[thisChar.pk] = [];

    relatives.forEach(function(thisRelative){
      // TODO: Implement this check if this relative is already in our map before
      //       inserting it
      // 9/25/2016
      // - Michael Peterson

      charRelativesMap[thisChar.id].append(thisRelative);
    });
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



$(document).ready(function(){
  pageId = parseInt(currentPageId = $("#pageIdHolder").attr("pageId"));

  // get the page object from the server
  var url = "/ajax/get_page";
  $.ajax({
    url: url,
    dataType: "json",
    method: "POST",
    data: {pageId: pageId}
  }).done(function(pageJSON){
    pageObject = JSON.parse(pageJSON)[0];
    console.log("---------- Got page Object ---------------");
    console.log(pageObject);
    // TODO: update page image with the source url found in pageObject
    // 9/25/2016
    // - Michael Peterson

    // get the pages chacacter objects
    getPageCharacters();
  }).fail(function(jqXHR, textStatus){
    doFailThing(jqXHR, textStatus, url);
  });
});
