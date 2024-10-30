let animation = new Animation();
counter = 0
setInterval(() => {
	animation.receiveData();
	receiveSliders();
	if (counter >= 20){
	    counter = 0;
	    graphRequest = ""
    	for (let a in slidersList){
    	    if (slidersList[a].isChecked){
    	        graphRequest += a;
    	    }
	    }
	    graph(graphRequest);
	}
	counter++;
	for (let a in slidersList){
		slidersList[a].setter();
	}
	timeSlider.setter();
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
let lastGraph = 0;
let slidersReceived = {time: 0}
let lookupColors = ["red", "orange", "green", "blue", "magenta", "black", "brown", "pink"];
timeSlider = new TimeSlider();

function receiveSliders(){
	let url = '/get_sliders';
	fetch(url)
	.then(function(response) {
		return response.text();
	})
	.then(function(text) {
		let a = text.split(";");
		slidersReceived.time = a.shift();
		for (let i in a){
			let b = a[i].split(" ");
			slidersReceived[b[0]] = parseFloat(b[1]);
		}
	})
}

function graph(num){
    if (num == ""){
        animation.drawGraph();
        return;
    }
	let url = '/graph/' + num;
	fetch(url)
	.then(function(response) {
		return response.text();
	})
	.then(function(text) {
		let parsed = text.split(";");
        animation.drawGraph();
        animation.graphValues(slidersList[parseFloat(lastGraph)].modifieR);
	    timeSlider.draw();
        for (let a in parsed){
            animation.graphCanvas.strokeStyle = lookupColors[num[a]]
            b = parsed[parseFloat(a)].split(" ")
            for (let i in b){
				animation.graphLine(i / 10, parseFloat(b[i]) / 2);
            }
            animation.gx = 0
            animation.gy = 500
		}
	})
}

function postClick(){
    let x = event.offsetX
    let y = event.offsetY
	let url = '/click/' + x + "_" + y;
	fetch(url)
	.then(function(response) {
		return response.text();
	})
	.then(function(text) {
	    //nothing
	})
}

function playRecording(name){
	sendMyData("recording " + name);
}

function requestRecording(){
    if (animation.playbackButton.innerHTML === "Выключить запись"){
		sendMyData("playforth")
        return;
    }
	let url = '/playback_names';
	fetch(url)
	.then(function(response) {
		return response.text();
	})
	.then(function(text) {
	    let data = text.split("\n");
	    let list = "";
	    for (let a in data){
	        if (data[a] === ""){continue}
	        list += '<p onclick="playRecording(' + "'" + data[a] + "'" + ')">' + data[a] + '</p>';
	    }
	    document.getElementById("playbackDropdown").innerHTML = list;
	})
}

function switchPendulum(){
    sendMyData("model_pendulum")
    sendMyData("only_pause")
    setTimeout(requestSliders, 500)
}

function switchCosmic(){
    sendMyData("model_cosmic")
    sendMyData("only_pause")
    setTimeout(requestSliders, 500)
}

function switchElectro(){
    sendMyData("model_electro")
    sendMyData("only_pause")
    setTimeout(requestSliders, 500)
}

function tryResetting(){
	a = prompt("Введите название записи для сохранения (без пробелов латиницей)")
	if (a !== null){
		sendMyData("save_record " + a)
		requestSliders();
    } else {
		sendMyData('reset');
		setTimeout(requestSliders, 500)
	}
}

function reset(){
	sendMyData('reset');
}

requestSliders();
requestRecording();

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
