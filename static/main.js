let x = document.getElementById("stats");
for (let a = 0; a < 9; a++){
	x.innerHTML += '<div style="height: 50; margin-top: 5; background-color: darkgray;" onmousedown="keyDown(' + a + ');" onmousemove="mouseMoveHandler(' + a + ');"><button style="background-color: crimson; display: block; position: relative; left: 0; height: 25; width: 25;" id="' + a + '"></button><i id="' + a + 'b">adadadada</i></div>';
}

let animation = new Animation();
animation.drawGraph();
setInterval(() => {
    animation.receiveData();
    animation.drawGraph1();
}, 50);

let sendMyData = function (something) {
    let url = '/event';
    fetch(url, {
        method: "post",
        headers: {
        'Accept': 'text/html',
        'Content-Type': 'text/html'
        },
        body: something
    })
    .then( (response) => {
        //do something awesome that makes the world a better place
    });
}

let slidersList = [];

function receiveSliders(){
    let url = '/sliders';
    fetch(url)
    .then(function(response) {
        return response.text();
    })
    .then(function(text) {

    })
}

new Slider("hardset_kinetic_energy", "kineticEnergy", "Кинетическая энергия");
/*new Slider("setSpeed", "getSpeed", "Скорость", 20);
new Slider("setLength", "getLength", "Длина", 0.9);
new Slider("setGravity", "getGravity", "Ускорение свободного падения", 2000);

let getMyData = function () {
    let url = '/get_data';
    fetch(url)
    .then(function(response) {
        return response.json();
    })
    .then(function(json) {
        console.log('Request successful', json.funni_json);
    })
}

let elem = document.getElementById('aaa')

setTimeout(getMyData, 1000)*/
