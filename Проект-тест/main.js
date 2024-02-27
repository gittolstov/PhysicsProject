let x = document.getElementById("stats");
for (let a = 0; a < 9; a++){
	x.innerHTML += '<div style="height: 50; margin-top: 5; background-color: darkgray;" onmousedown="keyDown(' + a + ');" onmousemove="mouseMoveHandler(' + a + ');"><button style="background-color: crimson; display: block; position: relative; left: 0; height: 25; width: 25;" id="' + a + '"></button><i id="' + a + 'b">adadadada</i></div>';
}

let animation = new Animation();
const PENDULUM = new Pendulum();
animation.drawGraph();

new Slider("setKineticEnergy", "kineticEnergy", "Кинетическая энергия");
new Slider("setSpeed", "getSpeed", "Скорость", 20);
new Slider("setLength", "getLength", "Длина", 0.9);