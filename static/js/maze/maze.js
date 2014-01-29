var Keys = {
  pressed: [],
  empty: function() {
    return !!Keys.pressed;
  },
  isPressed: function(key) {
    for (var i = 0; i < Keys.pressed.length; ++i) {
      if (Keys.pressed[i] == key) {
        return true;
      }
    }
    return false;
  },
  pressKey: function(key) {
    if (!Keys.isPressed(key)) {
      Keys.pressed.push(key);
    }
  },
  unpressKey: function(key) {
    for (var i = 0; i < Keys.pressed.length; ++i) {
      if (Keys.pressed[i] == key) {
        Keys.pressed.splice(i, 1);
        break;
      }
    }
  },
  UP: 38,
  DOWN: 40,
  LEFT: 37,
  RIGHT: 39,
  C: 67
}

function Chamber(x, y, x2, y2) {
  this.x = x;
  this.y = y;
  this.x2 = x2;
  this.y2 = y2;
  this.toString = function() {
    return "(" + this.x + 
           ", " + this.y +
           ") , (" + this.x2 + 
           ", " + this.y2 + ")";
  }
}

const MARGIN_X = 100;
const MARGIN_Y = 100;
const CELLS_X = 20;
const CELLS_Y = 20;
const HOLE_SIZE = 20;
const LINE_WIDTH = 3;
const STEP_SIZE = 0.5;

window.onload = function() {
  window.addEventListener('keydown', handleKeyDown, false);
  window.addEventListener('keyup', handleKeyUp, false);
  window.addEventListener("resize", doResize, false);
  var canvas = document.getElementById("canvas");
  var c = canvas.getContext("2d");
  var cellSizeX, cellSizeY;
  var lastX = 0, lastY = 0;
  var timer = new Timer();
  var hero = new Sprite("/static/img/maze/peon_sprite.png", 
                        32, 34, 0, 34, 4, 0);
  doResize();

  function isWall(data) {
    for (var i = 0; i < data.length; i+= 4) {
      if (data[i + 2] > 2) {
        return true;
      }
    }
    return false;
  }

  function handleKeyUp(e) {
    switch (e.keyCode) {
      case Keys.LEFT:
        Keys.unpressKey(Keys.LEFT);
        break;
      case Keys.RIGHT:
        Keys.unpressKey(Keys.RIGHT);
        break;
      case Keys.UP:
        Keys.unpressKey(Keys.UP);
        break;
      case Keys.DOWN:
        Keys.unpressKey(Keys.DOWN);
        break;
    }
    if (Keys.empty()) {
      hero.setFrames(1);
    }
    //drawUnit();
    /*
    setTimeout(function() {
     // drawUnit(timer.getSeconds()); 
      drawUnit();
      }, 500);
      */
  }

  function handleKeyDown(e) {
    var tmpLastX = hero.posX;
    var tmpLastY = hero.posY;
    if (hero.frames != 4)
      hero.setFrames(4);

    switch (e.keyCode) {
      case Keys.LEFT:
        Keys.pressKey(Keys.LEFT);
        hero.setOffset(0, 0);
        if(isWall(c.getImageData(xToPixel(hero.posX) - 1, 
                                 yToPixel(hero.posY) + LINE_WIDTH, 
                                 1, cellSizeY - LINE_WIDTH*2).data)) {
          hero.setFrames(1);
          drawUnit();
          return;
        }
        hero.posX -= STEP_SIZE;
        break;
      case Keys.RIGHT:
        Keys.pressKey(Keys.RIGHT);
        hero.setOffset(0, 34);
        if(isWall(c.getImageData(xToPixel(hero.posX) + cellSizeX + 1, 
                                 yToPixel(hero.posY) + LINE_WIDTH, 
                                 1, cellSizeY - LINE_WIDTH*2).data)) {
          hero.setFrames(1);
          drawUnit();
          return;
        }
        hero.posX += STEP_SIZE;
        break;
      case Keys.UP:
        Keys.pressKey(Keys.UP);
        hero.setOffset(0, 102);
        if(isWall(c.getImageData(xToPixel(hero.posX) + LINE_WIDTH, 
                                 yToPixel(hero.posY) - 1, 
                                 cellSizeX - LINE_WIDTH*2, 1).data)) {
          hero.setFrames(1);
          drawUnit();
          return;
        }
        hero.posY -= STEP_SIZE;
        break;
      case Keys.DOWN:
        Keys.pressKey(Keys.DOWN);
        hero.setOffset(0, 68);
        if(isWall(c.getImageData(xToPixel(hero.posX) + LINE_WIDTH, 
                                 yToPixel(hero.posY) + cellSizeY + 1, 
                                 cellSizeX - LINE_WIDTH*2, 1).data)) {

          hero.setFrames(1);
          drawUnit();
          return;
        }
        hero.posY += STEP_SIZE;
        break;
    }

    lastX = tmpLastX;
    lastY = tmpLastY;
    drawUnit();
    setTimeout(function() {
     // drawUnit(timer.getSeconds()); 
      drawUnit();
      }, 25);

  }

  function rand(from, to){
    return Math.floor(Math.random() * (to - from + 1) + from);
  }

  function doResize() {
    canvas.width = document.body.clientWidth;
    canvas.height = document.body.clientHeight;
    cellSizeX = (canvas.width - MARGIN_X * 2) / CELLS_X;
    cellSizeY = (canvas.height - MARGIN_Y * 2) / CELLS_Y;
    draw();
  }

  function xToPixel(x) {
    return x * cellSizeX + MARGIN_X;
  }

  function yToPixel(y) {
    return y * cellSizeY + MARGIN_Y;
  }

  function drawVerticalLine(x, y, y2) {
    var hole = rand(y + 1, y2);
    c.beginPath();
    c.moveTo(xToPixel(x), yToPixel(y));
    c.lineTo(xToPixel(x), yToPixel(hole - 1));
    c.moveTo(xToPixel(x), yToPixel(hole));
    c.lineTo(xToPixel(x), yToPixel(y2));
    c.stroke();
  }
  
  function drawHorizontalLine(x, x2, y) {
    var hole = rand(x + 1, x2);
    c.beginPath();
    c.moveTo(xToPixel(x), yToPixel(y));
    c.lineTo(xToPixel(hole - 1), yToPixel(y));
    c.stroke();
    c.moveTo(xToPixel(hole),  yToPixel(y));
    c.lineTo(xToPixel(x2), yToPixel(y));
    c.stroke();
  }

  function drawTicks(chamber) {
    var oldLineWidth = c.lineWidth;
    var oldStrokeStyle = c.strokeStyle;

    c.lineWidth = 1;
    c.strokeStyle = "#f00";
    c.beginPath();
    for (var x = 0; x <= CELLS_X; ++x) {
      c.moveTo(xToPixel(x), yToPixel(0) - 5);
      c.lineTo(xToPixel(x), yToPixel(0) + 5);
      c.stroke();
    }
    c.beginPath();
    for (var y = 0; y <= CELLS_Y; ++y) {
      c.moveTo(xToPixel(0) - 5, yToPixel(y));
      c.lineTo(xToPixel(0) + 5, yToPixel(y));
      c.stroke();
    }

    c.lineWidth = oldLineWidth;
    c.strokeStyle = oldStrokeStyle;
  }

  function drawUnit() {
    timer.update();
    hero.setDuration(500);
    hero.animate(c, timer);
    c.fillStyle = "#000";
    c.fillRect(xToPixel(lastX) + LINE_WIDTH - 1, 
               yToPixel(lastY) + LINE_WIDTH - 1, 
               cellSizeX - LINE_WIDTH * 2 + 2, 
               cellSizeY - LINE_WIDTH * 2 + 2);
    c.fillRect(xToPixel(hero.posX) + LINE_WIDTH - 1, 
               yToPixel(hero.posY) + LINE_WIDTH - 1, 
               cellSizeX - LINE_WIDTH * 2 + 2, 
               cellSizeY - LINE_WIDTH * 2 + 2);
    hero.draw(c, 
              xToPixel(hero.posX) + LINE_WIDTH,
              yToPixel(hero.posY) + LINE_WIDTH,
              cellSizeX - LINE_WIDTH * 2, 
              cellSizeY - LINE_WIDTH * 2);
  }

  function drawChamber(chamber, horizontal, recursionLevel) {
    if (chamber.x + 1 >= chamber.x2)
      return;
    if (chamber.y + 1 >= chamber.y2)
      return;

    /*
    // For bigger rooms instead of a full maze
    if (recursionLevel > 4)
      return;
    */

    if (!horizontal) {
      var randX = rand(chamber.x + 1, chamber.x2 - 1);
      drawVerticalLine(randX, chamber.y, chamber.y2);
      drawChamber(new Chamber(chamber.x, chamber.y, randX, chamber.y2), 
                  !horizontal, recursionLevel + 1);
      drawChamber(new Chamber(randX, chamber.y, chamber.x2, chamber.y2), 
                  !horizontal, recursionLevel + 1);
    } else {
      var randY = rand(chamber.y + 1, chamber.y2 - 1);
      drawHorizontalLine(chamber.x, chamber.x2, randY);
      drawChamber(new Chamber(chamber.x, chamber.y, chamber.x2, randY), 
                  !horizontal, recursionLevel + 1);
      drawChamber(new Chamber(chamber.x, randY, chamber.x2, chamber.y2), 
                  !horizontal, recursionLevel + 1);
    }
  }

  function draw() {
    c.fillStyle = "#000";
    c.strokeStyle = "#aaf";
    c.lineWidth = LINE_WIDTH;
    c.fillRect(0, 0, canvas.width, canvas.height);

    var chamber = new Chamber(0, 0, CELLS_X, CELLS_Y);
    c.strokeRect(xToPixel(chamber.x), 
                 yToPixel(chamber.y), 
                 xToPixel(chamber.x2) - xToPixel(chamber.x), 
                 yToPixel(chamber.y2) - yToPixel(chamber.y));


    c.strokeStyle = "#000";
    c.fillStyle = "#000";
    c.lineWidth = LINE_WIDTH + 1;
    c.beginPath();
    c.moveTo(xToPixel(0), yToPixel(-1));
    c.lineTo(xToPixel(0), yToPixel(1));
    c.stroke();
    c.beginPath();
    c.moveTo(xToPixel(CELLS_X), yToPixel(CELLS_Y - 1));
    c.lineTo(xToPixel(CELLS_X), yToPixel(CELLS_Y + 1));
    c.stroke();

    c.lineWidth = LINE_WIDTH;
    c.fillStyle = "#000";
    c.strokeStyle = "#aaf";
    drawChamber(chamber, true, 0);
    drawUnit();
    /*setTimeout(function() {
        drawUnit();
    }, 500);*/
  }






}
