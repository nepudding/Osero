var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

const STONE_SIZE = 40;
const STAGE_SIZE = 8;
var COLOR = [128,120,120];

function getBlack(){
    var col = "#";
    for(var i=0;i<3;i++){
        col += ("0"+COLOR[i].toString(16)).slice(-2);
    }
    return col;
}
function getWhite(){
    var col = "#";
    for(var i=0;i<3;i++){
        col += ("0"+(255-COLOR[i]).toString(16)).slice(-2);
    }
    return col;
}
class Stone{
    constructor(x,y,side){
        this.x = x;
        this.y = y;
        this.side = side;
    }
    draw(){
        if(this.side == 0) return;
        ctx.beginPath();
        ctx.arc(this.x,this.y,STONE_SIZE,0,Math.PI*2);
        if(this.side == 1)ctx.fillStyle = getBlack();
        if(this.side == 2)ctx.fillStyle = getWhite();
        ctx.fill();
        ctx.closePath();
    }
}

class Board{
    constructor(){
        this.stones = []
        for(var i=0; i<STAGE_SIZE;i++){
            this.stones[i] = [];
            for(var j=0;j<STAGE_SIZE;j++){
                this.stones[i][j] = new Stone(100*i+50,100*j+50,(i+j)%3);
            }
        }
    }
    draw(){
        for(var i=0; i<STAGE_SIZE;i++){
            for(var j=0;j<STAGE_SIZE;j++){
                this.stones[i][j].draw();
            }
        }
    }
}

var board = new Board();


board.draw()

function draw(){
    board.draw()
    for(var i=0;i<3;i++){
        COLOR[i] = (COLOR[i]+i+3)%256
    }
}
setInterval(draw,10);
