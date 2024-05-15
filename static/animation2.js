class Animation{
	constructor(){
		this.masterCanvas = document.getElementById("main").getContext("2d");//Шорткаты к html-элементам
		this.sliders = document.getElementById("stats");
		this.graphCanvas = document.getElementById("graph").getContext("2d");
		this.gx = 0;
		this.gy = 250;
		this.masterBackgroundStyle = "lightgrey";
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


        }
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

	drawGraph(){//кадр отрисовки графика
		this.graphCanvas.fillStyle = "white";
		this.graphCanvas.fillRect(0,0,500,500);
		this.graphCanvas.fillStyle = "black";
		this.graphCanvas.fillRect(0, 249, 500, 2);
		this.graphCanvas.fillRect(0, 0, 2, 500);
	}

	drawLine(y){
		this.masterCanvas.fillStyle = "green";
		this.masterCanvas.fillRect(0,y-1,1000,1);
	}

	graphLine(x, y){
		this.graphCanvas.beginPath();
		this.graphCanvas.strokeStyle = "red";
		this.graphCanvas.lineWidth = 2;
		this.graphCanvas.moveTo(this.gx, this.gy);
		this.graphCanvas.lineTo(x, -y + 250);
		this.graphCanvas.stroke();
		this.gx = x;
		this.gy = -y + 250;
	}

	vector(x, y, x2, y2, color, x3=0, y3=0, x4=0, y4=0){
		this.masterCanvas.beginPath();
		this.masterCanvas.strokeStyle = color;
		this.masterCanvas.lineWidth = 2;
		this.masterCanvas.moveTo(x, y);
		this.masterCanvas.lineTo(x + x2, y + y2);
		this.masterCanvas.lineTo(x + x3, y + y3);
		this.masterCanvas.moveTo(x + x2, y + y2);
		this.masterCanvas.lineTo(x + x4, y + y4);
		this.masterCanvas.stroke();
	}*/
}
