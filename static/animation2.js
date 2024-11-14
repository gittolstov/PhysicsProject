class Animation{
	constructor(){
		this.masterCanvas = document.getElementById("main").getContext("2d");//Шорткаты к html-элементам
		this.slidersCanvas = document.getElementById("sliderCanvas").getContext("2d");
		this.sliders = document.getElementById("stats");
		this.pauseButton = document.getElementById("pause");
		this.playbackButton = document.getElementById("playback");
		this.graphCanvas = document.getElementById("graph").getContext("2d");
		this.gx = 0;
		this.gy = 250;
		this.masterBackgroundStyle = "white";
		this.drawingFunctions = ["circle", "line", "vector", "scheme", "pause", "playingBack", "planet", "ship", "pendulum", "shipBoom", "semicircle", "laser", "angle"];
		this.schimage = new Image;
	    this.schimage.src = "/static/Scheme.png";
		this.earth = new Image;
	    this.earth.src = "/static/Planet.png";
		this.spaceship = new Image;
	    this.spaceship.src = "/static/Spaceship.png";
		this.pointer = new Image;
	    this.pointer.src = "/static/laser.png";
		this.dial = new Image;
	    this.dial.src = "/static/Dial.png";
		this.goldenball = new Image;
	    this.goldenball.src = "/static/Pendulum.png";
		this.expl = [new Image, new Image, new Image, new Image, new Image, new Image];
	    for (let a in this.expl){
	        this.expl[a].src = "/static/explosion_frames/frame" + a + ".png";
	    }
	}

	pause(isPaused){
	    if (parseInt(isPaused[1])){
			//this.pauseButton.innerHTML = "⏵︎";
			this.pauseButton.src = "/static/Play.svg";
		} else {
			//this.pauseButton.innerHTML = "⏸︎";
			this.pauseButton.src = "/static/Pause.svg";
		}
	}

	playingBack(args){
	    if (parseInt(args[1])){
			this.playbackButton.innerHTML = "Выключить запись";
		} else {
			this.playbackButton.innerHTML = "Включить.. запись";
		}
	}

	circle(args){
		this.masterCanvas.beginPath();
		this.masterCanvas.arc(args[1], args[2], args[3], 0, 2 * Math.PI);
		this.masterCanvas.strokeStyle = args[5];
		this.masterCanvas.lineWidth = parseInt(args[4]);
		this.masterCanvas.stroke();
	}

	line(args){
		this.masterCanvas.beginPath();
		if (args[6].startsWith("rgb")){
		    let a = args[6].split(":");
		    args[6] = a.join(", ");
		}
		this.masterCanvas.moveTo(parseFloat(args[1]), parseFloat(args[2]));
		this.masterCanvas.lineTo(parseFloat(args[3]), parseFloat(args[4]));
		this.masterCanvas.strokeStyle = args[6];
		this.masterCanvas.lineWidth = parseInt(args[5]);
		this.masterCanvas.stroke();
	}

	vector(args){//x1 y1 x2 y2
	    let magicArrowLength = 10;
	    let a = projections(args[1]-args[3], args[2]-args[4], magicArrowLength);
		this.masterCanvas.beginPath();
		this.masterCanvas.moveTo(args[1], args[2]);
		this.masterCanvas.lineTo(args[3], args[4]);
		this.masterCanvas.moveTo(parseFloat(args[3]) + 2 * a.x + a.y, parseFloat(args[4]) + 2 * a.y - a.x);
		this.masterCanvas.lineTo(parseFloat(args[3]), parseFloat(args[4]));
		this.masterCanvas.moveTo(parseFloat(args[3]) + 2 * a.x - a.y, parseFloat(args[4]) + 2 * a.y + a.x);
		this.masterCanvas.lineTo(parseFloat(args[3]), parseFloat(args[4]));
		this.masterCanvas.strokeStyle = args[6];
		this.masterCanvas.lineWidth = parseInt(args[5]);
		this.masterCanvas.stroke();
	}

	scheme(args){
	    this.masterCanvas.drawImage(this.schimage, 0, 0, 1000, 1000);
	}

	planet(args){
	    this.masterCanvas.drawImage(this.earth, args[1] - args[3] * 2, args[2] - args[3] * 2, args[3] * 4, args[3] * 4);
	}

	ship(args){
	    this.modifyContextMatrix(Math.atan(args[4] / args[3]) + Math.PI * (args[3] < 0) + Math.PI/2, args[1], args[2]);
	    this.masterCanvas.drawImage(this.spaceship, -30, -30, 60, 60);
	    this.masterCanvas.restore();
	}

	pendulum(args){
	    this.masterCanvas.drawImage(this.goldenball, args[1] - args[3] * 2, args[2] - args[3] * 2, args[3] * 4, args[3] * 4);
	}

	shipBoom(args){
	    this.masterCanvas.drawImage(this.expl[args[5]], args[1], args[2], args[3], args[4]);
	}

	semicircle(args){
		this.masterCanvas.beginPath();
		this.masterCanvas.arc(args[1], args[2], args[3], (parseFloat(args[4]) - 0.25) * 2 * Math.PI, (parseFloat(args[4]) + 0.25) * 2 * Math.PI);
		this.masterCanvas.fillStyle = "rgb(" + (255 - (parseFloat(args[5]) - 1) * 150) + ", " + (255 - (parseFloat(args[5]) - 1) * 150) + ", 255)";
		this.masterCanvas.fill();
	}

	laser(args){
	    args[4] = parseFloat(args[4])
	    args[3] = parseFloat(args[3])
	    this.masterCanvas.restore();
	    this.modifyContextMatrix(-args[3] + Math.PI/2, args[1], args[2]);
	    this.masterCanvas.drawImage(this.pointer, -args[4] / 2, -args[4] / 2, args[4], args[4]);
	    this.masterCanvas.restore();
	}

	angle(args){
	    this.masterCanvas.drawImage(this.dial, args[1] - args[3] / 2, args[2] - args[3] / 2, args[3], args[3]);
	    this.modifyContextMatrix(-Math.PI / 2, 0, 1000);
	}

	refresh(){
		this.masterCanvas.fillStyle = this.masterBackgroundStyle;
		this.masterCanvas.fillRect(0,0,1000,1000);
	}

    receiveData(){
        let url = '/get_data';
        fetch(url)
        .then(function(response) {
            return response.text();
        })
        .then(function(text) {
            animation.drawReceivedData(text);
        })
    }

    drawReceivedData(data){
        this.refresh();
        let parsedData = data.split(";")
        for (let a in parsedData){
            if (parsedData[a] === ""){continue}
            let figureData = parsedData[a].split(" ");
            this[this.drawingFunctions[figureData[0]]](figureData);
        }
    }

    drawGraph1(){
        let url = '/get_kinetic';
        fetch(url)
        .then(function(response) {
            return response.text();
        })
        .then(function(data) {
            let parsedData = data.split(";")
            for (let a in parsedData){
                if (parsedData[a] === ""){continue}
                let figureData = parsedData[a].split(" ");
                animation.graphLine(20, parseInt(figureData[0]) * 3);
            }
        })
    }

    drawGraph2(){
        let url = '/get_potential';
        fetch(url)
        .then(function(response) {
            return response.text();
        })
        .then(function(data) {
            let parsedData = data.split(";")
            for (let a in parsedData){
                if (parsedData[a] === ""){continue}
                let figureData = parsedData[a].split(" ");
                animation.graphLine(20, parseInt(figureData[0]) * 3);
            }
        })
    }

	/*drawPendulum(x, y, size){
		this.masterCanvas.beginPath();
		this.masterCanvas.strokeStyle = "grey";
		this.masterCanvas.lineWidth = 3;
		this.masterCanvas.moveTo(x, y);
		this.masterCanvas.lineTo(500, 0);
		this.masterCanvas.stroke();
		this.masterCanvas.beginPath();
		this.masterCanvas.arc(x, y, size, 0, 2 * Math.PI);
		this.masterCanvas.strokeStyle = "red";
		this.masterCanvas.lineWidth = 8;
		this.masterCanvas.stroke();

	}

	*/drawGraph(){//кадр отрисовки графика
		this.graphCanvas.fillStyle = "rgba(214, 235, 242)";
		this.graphCanvas.fillRect(0,0,500,500);
		this.graphCanvas.fillStyle = "black";
		this.graphCanvas.fillRect(0, 249, 500, 2);
		this.graphCanvas.fillStyle = "rgba(255, 255, 255, 0.5)";
		for (let a = 0; a < 20; a++){
		    this.graphCanvas.fillRect(a * 25, 0, 2, 500);
		}
		for (let a = 0; a < 20; a++){
		    this.graphCanvas.fillRect(0, a * 25, 500, 2);
		}
	}

	graphValues(scale){
		this.graphCanvas.fillStyle = 'black';
		this.graphCanvas.font = "15px Arial";
		for (let a = 1; a <= 4; a++){
    		this.graphCanvas.fillText(a / scale * 100 + "", 0, 250 - a * 50);
	    	this.graphCanvas.fillText(-a / scale * 100 + "", 0, 250 + a * 50);
		}
	}/*

	drawLine(y){
		this.masterCanvas.fillStyle = "green";
		this.masterCanvas.fillRect(0,y-1,1000,1);
	}

	*/graphLine(x, y){
		this.graphCanvas.beginPath();
		this.graphCanvas.lineWidth = 3;
		this.graphCanvas.moveTo(this.gx, this.gy);
		this.graphCanvas.lineTo(x, -y + 250);
		this.graphCanvas.stroke();
		this.gx = x;
		this.gy = -y + 250;
	}


	modifyContextMatrix(angle, xShift, yShift, xTurn = 1, yTurn = 1){
		this.masterCanvas.save();
		this.masterCanvas.setTransform(xTurn, 0, 0, yTurn, xShift, yShift);
		this.masterCanvas.rotate(angle);
	}
}
