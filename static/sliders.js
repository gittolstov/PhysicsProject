class Slider{
	constructor(modify, set, text, modifier = 10){
		this.id = slidersList.push(this) - 1;
		this.modify = modify;
		this.modifieR = modifier;
		this.set = set;
		this.value = 0;
		this.active = false;
		document.getElementById(this.id + "b").innerText = text;
	}

	react(num){
		if (this.active){
			this.modifier(num / 10 / this.modifieR);
			return;
		}
	}

	modifier(num){
		sendMyData("slider " + this.modify + " " + num);
		for (let a in slidersList){
			//slidersList[a].setter();
		}
	}

	setter(){
		document.getElementById("" + this.id).style.left = slidersReceived[this.set] * this.modifieR + 5;
	}
}


function mouseMoveHandler(id){
	if (slidersList[id] === undefined){return}
	slidersList[id].react(Math.abs(event.offsetX) * 10);
}

function keyUp(){
	for (let a in slidersList){
		slidersList[a].active = false;
	}
	//PENDULUM.start();
}

function keyDown(id){
	slidersList[id].active = true;
	sendMyData('only_pause');
}
