var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

const STONE_SIZE = 35;
const STAGE_SIZE = 8;

class Stone{
    constructor(x,y){
        this.x = x;
        this.y = y;
    }
    draw(){
        ctx.beginPath();
        ctx.arc(this.x,this.y,STONE_SIZE,0,Math.PI*2);
        ctx.fillStyle = "#555555";
        ctx.fill();
        ctx.closePath();
    }
}

// ここからmainだよ
var stones = []
for(var i=0; i<STAGE_SIZE;i++){
    stones[i] = [];
    for(var j=0;j<STAGE_SIZE;j++){
        stones[i][j] = new Stone(100*i+50,100*j+50);
    }
}
document.write("oiu")


for(var i=0; i<STAGE_SIZE;i++){
    for(var j=0;j<STAGE_SIZE;j++){
        stones[i][j].draw();
    }
}
