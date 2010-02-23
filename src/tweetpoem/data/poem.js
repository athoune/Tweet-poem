var last = null;
var poems;
var size = 0;
var MAX = 36;
var stack = [];
var best;

var position;
var Circle = function(width, height) {
  this.angle = 0;
  this.width = width;
  this.height = height;
  this.radius = 300;
};

Circle.prototype = {
  x: function() {
    return (this.radius * Math.cos(this.angle)) + (this.radius);
  },
  y: function() {
    return (this.radius * Math.sin(this.angle)) + (this.height/2);
  },
  next: function() {
    this.angle += Math.PI / 15;
  }
};

var Column = function(width, height) {
  this.col = 0;
  this.line = 0;
};

Column.prototype = {
  x: function() {
    return this.col * 350 + 10;
  },
  y: function() {
    return this.line * 35 + 150;
  },
  next: function() {
    this.line ++;
    if(this.line > MAX / 3) {
      this.line = 0;
      this.col++;
    }
    if(this.col >= 3) {
      this.col = 0;
    }
    
  }
};

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
        stack.unshift(data.poems[i]);
      }
    }
    setTimeout('fetch()', 1000);
    //fetch();
  },
  cache: false});
};

var display = function() {
  if(stack.length > 0) {
    var poem = stack.pop();
    poems.prepend($('<div>')
      .text(poem)
      .css('position', 'absolute')
      .css('left', position.x())
      .css('top' , position.y())
      .click(function() {
        best.append($('<li>').text(poem));
      })
      .animate({
      opacity:0
    }, 5000, function() {
        $(this).remove();
      }));
    position.next();
    if(size > MAX) {
      poems.children().last().remove();
    } else {
      size++;
    }
  }
  setTimeout('display()', 100);
}

$(function(){
  poems = $('#poems');
  best = $('#best');
  var body = $('body');
  position = new Column(body.width(), body.height());
  fetch();
  display();
});