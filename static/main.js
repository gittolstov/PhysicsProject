let x = document.getElementById("stats");
for (let a = 0; a < 9; a++){
	x.innerHTML += '<div style="height: 50; margin-top: 5; background-color: darkgray;" onmousedown="keyDown(' + a + ');" onmousemove="mouseMoveHandler(' + a + ');"><button style="background-color: crimson; display: block; position: relative; left: 0; height: 25; width: 25;" id="' + a + '"></button><i id="' + a + 'b">adadadada</i></div>';
}

let animation = new Animation();
//animation.drawGraph();
setInterval(() => {
	animation.receiveData();
	//animation.drawGraph1();
	receiveSliders();
	for (let a in slidersList){
		slidersList[a].setter();
	}
}, 50);

function sendMyData(something){
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
let slidersReceived = {}

function receiveSliders(){
	let url = '/get_sliders';
	fetch(url)
	.then(function(response) {
		return response.text();
	})
	.then(function(text) {
		let a = text.split(";");
		for (let i in a){
			let b = a[i].split(" ");
			slidersReceived[b[0]] = parseFloat(b[1]);
		}
	})
}

function speedGraph(){
	let url = '/speed_graph';
	fetch(url)
	.then(function(response) {
		return response.text();
	})
	.then(function(text) {
		let a = text.split(" ");
		animation.drawGraph();
		for (let i in a){
		    animation.graphLine(i / 5, parseFloat(a[i]) * 20);
		}
	})
}

new Slider("hardset_kinetic_energy", "get_kinetic_energy", "Кинетическая энергия");
new Slider("set_speed", "get_speed", "Скорость", 20);
new Slider("set_base_length", "get_base_length", "Длина", 0.9);
new Slider("set_gravity", "get_gravity", "Ускорение свободного падения", 2000);

/*let getMyData = function () {
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
