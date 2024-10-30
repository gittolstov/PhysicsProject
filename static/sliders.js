/*let x = document.getElementById("stats");
for (let a = 0; a < 9; a++){
	x.innerHTML += '<div style="height: 50; margin-top: 5; background-color: darkgray;" onmousedown="keyDown(' + a + ');" onmousemove="mouseMoveHandler(' + a + ');"><button style="background-color: crimson; display: block; position: relative; left: 0; height: 25; width: 25;" id="' + a + '"></button><i id="' + a + 'b"></i></div>';
}*/


function switchGraph(id){
    slidersList[id].switchGraph(document.getElementById(id + "a").checked);
}


function react(id){
    slidersList[id].reactAnyway(parseFloat(document.getElementById(id + "b").value));
}


class Slider{
	constructor(modify, set, text, modifier = 10, shift = 0){
		this.id = slidersList.push(this) - 1;
		this.modify = modify;
		this.modifieR = modifier;
		this.set = set;
		this.text = text;
		this.shift = shift;
		this.value = 0;//legacy?
		this.active = false;
		this.offset = 0;
		this.isChecked = false;
		this.canvas = animation.slidersCanvas;
		let id1 = this.id + "a";
		let id2 = this.id + "b";
		document.getElementById("checkboxes").innerHTML += "<div class='box-wrapper'><input id='" + id1 + "' type='checkbox' onchange='switchGraph(" + this.id + ")'></input><input id='" + id2 + "' type='text' onchange='react(" + this.id + ")'></input></div>";
	}

	draw(){
		let x1 = 0;
		let y1 = this.id * 60 + 20;
		let x2 = 500;
		let y2 = 30;
		let x = this.offset
		let zeroX = this.shift
		let can = this.canvas;//background
		can.fillStyle = "white";
		can.fillRect(x1, y1, x2, y2);
		can.fillStyle = "DeepSkyBlue";
		can.fillRect(x1 + y2 * 0.5, y1, x2 - y2, y2);
		can.beginPath();
		can.arc(x1 + y2 * 0.5, y1 + y2 * 0.5, y2 * 0.5, 0, 2 * Math.PI, false);
		can.arc(x1 + x2 - y2 * 0.5, y1 + y2 * 0.5, y2 * 0.5, 0, 2 * Math.PI, false);
		can.fill();
		can.fillStyle = "Bisque";//pale line
		can.beginPath();
		can.arc(x1 + x2 - y2 * 0.3, y1 + y2 * 0.5, y2 * 0.1, 0, 2 * Math.PI, false);
		can.fill();
		can.fillRect(x1 + x, y1 + y2 * 0.4, x2 - x - y2 * 0.3, y2 * 0.2);
		can.fillStyle = "MidnightBlue";//dark line
		can.beginPath();
		can.arc(x1 + y2 * 0.3, y1 + y2 * 0.5, y2 * 0.1, 0, 2 * Math.PI, false);
		can.arc(x1 + x, y1 + y2 * 0.5, y2 * 0.4, 0, 2 * Math.PI, false);
		can.fill();
		can.fillRect(x1 + y2 * 0.3, y1 + y2 * 0.4, x - y2 * 0.3, y2 * 0.2);
		can.beginPath();//pale dot
		can.fillStyle = "Bisque";
		can.arc(x1 + x, y1 + y2 * 0.5, y2 * 0.15, 0, 2 * Math.PI, false);
		can.fill()
		can.fillStyle = "DarkMagenta";//zero marker
		can.strokeStyle = 'indigo';
		//can.fillRect(zeroX, y1, 2, y2);
		can.font = "bold 30px Arial";
		can.fillText("0", zeroX, y1 + y2 * 0.85);
		can.strokeText("0", zeroX, y1 + y2 * 0.85);
		can.fillStyle = "indigo";//text
		can.font = "22px Arial";
		can.fillText(this.text, Math.ceil(x1 + x2 / 4), Math.floor(y1 - y2 * 0.15));
		can.fillStyle = lookupColors[this.id];//color marker
		can.fillRect(x1 + x2 / 4 - 15, y1 - y2 * 0.15 - 10, 10, 10);
	}

	switchGraph(bool){
	    console.log(bool);
	    if (bool){
	        lastGraph = this.id;
	    } else if (lastGraph === this.id){
	        for (let a in slidersList){
	            if (slidersList[a].isChecked){
	                lastGraph = a;
	            }
	        }
	    }
	    this.isChecked = bool;
	}

	react(num){
		if (this.active){
			this.modifier((num / 10 - this.shift) / this.modifieR);
			return;
		}
	}

	reactAnyway(num){
		this.modifier(num);
	}

	modifier(num){
		sendMyData("slider " + this.modify + " " + num);
		/*for (let a in slidersList){
			//slidersList[a].setter();
		}*/
	}

	setter(){
		this.offset = slidersReceived[this.set] * this.modifieR + this.shift;
		if (document.activeElement !== document.getElementById(this.id + "b")){
		    document.getElementById(this.id + "b").value = slidersReceived[this.set];
		}
		this.draw()
	}
}


class TimeSlider{
    constructor(){
        this.canvas = animation.graphCanvas;
        this.active = false;
    }

    draw(){
		let x1 = 0;
		let y1 = 450;
		let x2 = 500;
		let y2 = 50;
		let x = this.offset
		let zeroX = this.shift
		let can = this.canvas;//background
		can.fillStyle = "DeepSkyBlue";
		can.fillRect(x1 + y2 * 0.5, y1, x2 - y2, y2);
		can.beginPath();
		can.arc(x1 + y2 * 0.5, y1 + y2 * 0.5, y2 * 0.5, 0, 2 * Math.PI, false);
		can.arc(x1 + x2 - y2 * 0.5, y1 + y2 * 0.5, y2 * 0.5, 0, 2 * Math.PI, false);
		can.fill();
		can.fillStyle = "Bisque";//pale line
		can.beginPath();
		can.arc(x1 + x2 - y2 * 0.3, y1 + y2 * 0.5, y2 * 0.1, 0, 2 * Math.PI, false);
		can.fill();
		can.fillRect(x1 + x, y1 + y2 * 0.4, x2 - x - y2 * 0.3, y2 * 0.2);
		can.fillStyle = "MidnightBlue";//dark line
		can.beginPath();
		can.arc(x1 + y2 * 0.3, y1 + y2 * 0.5, y2 * 0.1, 0, 2 * Math.PI, false);
		can.arc(x1 + x, y1 + y2 * 0.5, y2 * 0.4, 0, 2 * Math.PI, false);
		can.fill();
		can.fillRect(x1 + y2 * 0.3, y1 + y2 * 0.4, x - y2 * 0.3, y2 * 0.2);
		can.beginPath();//pale dot
		can.fillStyle = "Bisque";
		can.arc(x1 + x, y1 + y2 * 0.5, y2 * 0.15, 0, 2 * Math.PI, false);
		can.fill()
	}

	react(num){
		if (this.active){
			this.modifier(num);// * 20 / 10
			return;
		}
	}

	modifier(num){
		sendMyData("rewind " + num);
	}

	setter(){
		this.offset = slidersReceived.time / 10;
		this.draw()
	}
}


function requestSliders(){
	slidersList = []
	let url = '/request_sliders';
	fetch(url)
	.then(function(response) {
		return response.text();
	})
	.then(function(text) {
		let a = text.split(";");
		animation.slidersCanvas.fillStyle = "white";
		animation.slidersCanvas.fillRect(0, 0, 1000, 1000);
		document.getElementById("checkboxes").innerHTML = "";
		for (let i in a){
			let b = a[i].split("/");
			new Slider(b[0], b[1], b[2], parseFloat(b[3]), parseFloat(b[4]))//setter, getter, name, multiplier of range
		}
	})
}

function mouseMoveHandler(canvas = 0){
    if (canvas == 1){
    	timeSlider.react(Math.abs(event.offsetX) * 10);
        return
    }
    let id = Math.floor(event.offsetY / 60);
	if (slidersList[id] === undefined){return}
	slidersList[id].react(Math.abs(event.offsetX) * 10);
}

function keyUp(canvas = 0){
    if (canvas == 1){
    	timeSlider.active = false;
        return
    }
	for (let a in slidersList){
		slidersList[a].active = false;
	}
}

function keyDown(canvas = 0){
    if (canvas == 1){
    	timeSlider.active = true;
	    sendMyData('only_pause');
        return
    }
    let id = Math.floor(event.offsetY / 60);
	slidersList[id].active = true;
	sendMyData('only_pause');
}
