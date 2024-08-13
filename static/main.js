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
let slidersReceived = {time: 0}
let lookupColors = ["red", "orange", "yellow", "green", "blue", "magenta", "black", "brown", "pink"];
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

function graph(num){//legacy
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
	    timeSlider.draw();
        for (let a in parsed){
            animation.graphCanvas.strokeStyle = lookupColors[num[a]]
            b = parsed[parseFloat(a)].split(" ")
            for (let i in b){
                animation.graphLine(i / 20, parseFloat(b[i]));
            }
            animation.gx = 0
            animation.gy = 500
		}
	})
}

function playRecording(){
    if (animation.playbackButton.innerHTML === "Выключить запись"){
		sendMyData("playforth")
        return
    }
	let url = '/playback_names';
	fetch(url)
	.then(function(response) {
		return response.text();
	})
	.then(function(text) {
		let prmt = prompt("Выберите запись из списка сохранённых:" + text)
		if (prmt === null){
			return
		}
		sendMyData("recording " + prmt)
        setTimeout(requestSliders, 500)
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

requestSliders();

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
