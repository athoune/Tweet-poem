var last = null;
var poems;
var size = 0;
var MAX = 25;

var fetch = function() {
  $.ajax({
  url: (last == null) ? 'poem': 'poem?since=' + last,
  dataType: 'json',
  success: function(data, textStatus, XMLHttpRequest){
    //console.log(data);
    //console.log(data.poems);
    last = data.tick;
    if(typeof data.poems != 'undefined') {
      for(var i=0; i < data.poems.length; i++) {
        poems.prepend($('<li>').text(data.poems[i]));
        if(size > MAX) {
          poems.children().last().remove();
        } else {
          size++;
        }
      }
    }
    setTimeout('fetch()', 1000);
    //fetch();
  },
  cache: false});
};
$(function(){
  poems = $('#poems');
  fetch();
});