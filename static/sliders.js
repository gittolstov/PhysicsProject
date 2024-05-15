class Slider{
	constructor(modify, set, text, modifier = 10){
		/*this.id = PENDULUM.sliders.push(this) - 1;
		this.modify = modify;
		this.modifieR = modifier;
		this.set = set;
		this.value = 0;
		this.active = false;
		document.getElementById(this.id + "b").innerText = text;*/
	}

	react(num){
		if (this.active){
			this.modifier(num / 10 / this.modifieR);
			return;
		}
	}

	modifier(num){
		PENDULUM[this.modify](num);
		PENDULUM.draw();
		for (let a in PENDULUM.sliders){
			PENDULUM.sliders[a].setter();
		}
	}

	setter(){
		document.getElementById("" + this.id).style.left = PENDULUM[this.set]() * this.modifieR + 5;
	}
}


function mouseMoveHandler(id){
	if (PENDULUM.sliders[id] === undefined){return}
	PENDULUM.sliders[id].react(Math.abs(event.offsetX) * 10);
}

function keyUp(){
	for (let a in PENDULUM.sliders){
		PENDULUM.sliders[a].active = false;
	}
	//PENDULUM.start();
}

function keyDown(id){
	PENDULUM.sliders[id].active = true;
	PENDULUM.stop();
}
