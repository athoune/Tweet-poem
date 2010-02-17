var last = null;

var fetch = function() {
  $.ajax({
  url: (last == null) ? 'poem': 'poem?since=' + last,
  success: function(data, textStatus, XMLHttpRequest){
    console.log(data);
    last = data.tick;
    setTimeout('fetch()', 5000);
  },
  cache: false});
}
$(function(){
  console.log('plop');
  fetch();
});