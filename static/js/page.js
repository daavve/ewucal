//
//
// Runs the dynamic part of the website for image
//
////////////////////////////////////////////////////

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
  });
}

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
