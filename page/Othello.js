var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

const STONE_SIZE = 40;
const STAGE_SIZE = 8;
var COLOR = 0.0

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
        var gradient = ctx.createLinearGradient(0,0,800,900);
        if(this.side == 1){
            gradient.addColorStop((COLOR+0)%1,'rgb(255,0,0)')
            gradient.addColorStop((COLOR+1/6)%1,'rgb(255,255,0)')
            gradient.addColorStop((COLOR+2/6)%1,'rgb(0,255,0)')
            gradient.addColorStop((COLOR+3/6)%1,'rgb(0,255,255)')
            gradient.addColorStop((COLOR+4/6)%1,'rgb(0,0,255)')
            gradient.addColorStop((COLOR+5/6)%1,'rgb(0,255,255)')
        }else{
            gradient.addColorStop((COLOR+0)%1,'rgb(0,255,255)')
            gradient.addColorStop((COLOR+1/6)%1,'rgb(0,0,255)')
            gradient.addColorStop((COLOR+2/6)%1,'rgb(255,0,255)')
            gradient.addColorStop((COLOR+3/6)%1,'rgb(255,0,0)')
            gradient.addColorStop((COLOR+4/6)%1,'rgb(255,255,0)')
            gradient.addColorStop((COLOR+5/6)%1,'rgb(255,0,0)')
        }
        ctx.fillStyle = gradient
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

function draw(){
    board.draw()
    COLOR += 0.01
    COLOR %= 1
}
setInterval(draw,10);
