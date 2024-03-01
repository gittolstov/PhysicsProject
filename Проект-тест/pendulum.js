class Pendulum{
	constructor(gravity = new Vector(0, 0.05, "red"), tension = new Vector(0, -0.05, "green"), frame = 20, speed = new Vector(5, 0, "red", 100), acc = new Vector(0, 0, "blue")){
		this.x = 500;
		this.y = 500;
		this.speed = speed;
		this.length = 500;
		this.acceleration = acc;
		this.size = 30;
		this.gravity = gravity;
		this.tension = tension;
		this.frame = frame;
		this.time = 0;
		this.previousTime = 0;
		this.logs = [];
		this.fullEnergy = this.fullE();//пока только вниз
		this.ymin = 500;
		this.ymax = 0;
		this.butn = this.start;
		this.sliders = [];
		this.stopped = true;
		this.direction = 1;
		this.speedCopy = this.speed.copy();
		this.xyCopy = {x: this.x, y: this.y};
	}

	start(){
		if (!this.stopped){return}
		this.runner = setInterval((obj) => {
			obj.tick();
		}, this.tick, this);
		document.getElementById("butn").innerHTML = "Остановить маятник";
		this.butn = this.stop;
		this.stopped = false;
	}

	stop(){
		if (this.stopped){return}
		clearInterval(this.runner);
		document.getElementById("butn").innerHTML = "Запустить маятник";
		this.butn = this.start;
		this.stopped = true;
	}

	tick(){
		if (this.time % 50 === 0){
			this.calibrateKinetics();
		}
		this.direction = -Math.sign(this.speed.x)
		this.log();
		this.snap(this.length);
		this.reviseTension();
		this.acceleration.x = this.gravity.x + this.tension.x;
		this.acceleration.y = this.gravity.y + this.tension.y;
		this.x += this.speed.x + this.acceleration.x;
		this.y += this.speed.y + this.acceleration.y;
		this.speed.x += this.acceleration.x;
		this.speed.y += this.acceleration.y;
		this.time++;
		this.draw();
		for (let a in this.sliders){
			this.sliders[a].setter();
		}
		animation.graphLine(this.time * 0.05, (this.x - 500) * 0.05);
		if (this.y < this.ymin){
			this.ymin = this.y;
		}
		if (this.y > this.ymax){
			this.ymax = this.y;
		}
		this.speedCopy = this.speed.copy();
		this.xyCopy = {x: this.x, y: this.y};
	}

	log(){
		for (let i in this.logs){
			this.logs[i].tick(this.copy());
		}
	}

	draw(){
		animation.refresh();
		animation.drawPendulum(this.x, this.y, this.size);
		this.speed.draw();
		this.acceleration.draw();
		this.gravity.draw();
		this.tension.draw();
		this.drawPlaceholder1();
	}

	drawPlaceholder1(){

	}

	drawPlaceholder2(){
		animation.drawLine(-this.fullEnergy / this.gravity.y + this.length);
	}

	copy(){
		let a = new Pendulum(this.gravity.copy(), this.tension.copy(), 10000, this.speed.copy(), this.acceleration.copy());
		a.x = this.x;
		a.y = this.y;
		a.time = this.time;
		a.fullEnergy = this.fullEnergy;
		return a;
	}

	speedTowardsNormal(){//направляет скорость вдоль вращения
		this.speed.point(this.x + this.tension.y * 10000 * this.direction, this.y - this.tension.x * 10000 * this.direction);
	}

	getSpeed(){
		return this.speed.length();
	}

	setSpeed(num){
		this.speed.x = this.speedCopy.x;
		this.speed.y = this.speedCopy.y;
		this.speed.multiply(num);
		this.fullEnergy = this.fullE();
	}

	getLength(){
		return this.length;
	}

	setLength(num){
		this.x = this.xyCopy.x;
		this.y = this.xyCopy.y;
		this.length = num;
		this.snap(num)
	}

	getGravity(){
		return this.gravity.length();
	}

	setGravity(num){
		this.gravity.y = num;
		this.fullEnergy = this.fullE();
		this.getGravity();
	}

	setKineticEnergy(num){
		this.speed.x = 1;
		this.speed.y = 1;
		this.speed.multiply((num * 2) ** 0.5);
		this.speedTowardsNormal();
		animation.masterCanvas.fillStyle = "black";
		animation.masterCanvas.fillRect(this.x + this.tension.y * 10000 * this.direction, this.y - this.tension.x * 10000 * this.direction, 10, 10);
		this.fullEnergy = this.fullE();
	}

	fullE(){
		return this.kineticEnergy() + this.potentialEnergy();
	}

	potentialEnergy(){
		return (this.length - this.y) * this.gravity.y;
	}

	kineticEnergy(){
		return this.speed.length() ** 2 / 2;
	}

	tp(x, y){
		this.x = x;
		this.y = y;
	}

	reviseTension(){
		this.tension.point(500, 0);
		this.tension.multiply(this.gravity.length() * -this.tension.y/(this.tension.y**2 + this.tension.x**2)**0.5 + this.speed.length() ** 2 / ((this.x - 500) ** 2 + this.y ** 2) ** 0.5);
	}

	snap(length){
		let a = projections(this.x - 500, this.y, length);
		this.tp(a.x + 500, a.y)
	}

	calibrateKinetics(){
		this.setKineticEnergy(this.fullEnergy - this.potentialEnergy());
	}
}


class Vector{
	constructor(x, y, color = "green", drawMultiplier = 500){
		this.x = x;
		this.y = y;
		this.color = color;
		this.drawMultiplier = drawMultiplier;
	}
	
	point(x, y){//направляет вектор в заданную координату с сохранением модуля
		let a = this.length();
		let b = projections(x - PENDULUM.x, y - PENDULUM.y, a);
		this.x = b.x;
		this.y = b.y;
	}

	multiply(resultingModule){//меняем модуль вектора
		let a = resultingModule;
		let b = projections(this.x, this.y, a);
		this.x = b.x;
		this.y = b.y;
	}

	length(){//возвращает модуль вектора
		return (this.x**2 + this.y**2)**0.5;
	}

	draw(){
		animation.vector(PENDULUM.x, PENDULUM.y, this.x * this.drawMultiplier, this.y * this.drawMultiplier, this.color);
	}

	copy(){
		return new Vector(this.x, this.y, this.color, this.drawMultiplier);
	}
}


class Log{
	constructor(multiplierX, multiplierY){
		this.multiplierX = multiplierX;
		this.multiplierY = multiplierY;
		this.id = PENDULUM.logs.push(this);
		this.log = [];
	}

	deactivate(){
		PENDULUM.logs.splice(this.id, 1);
	}

	drawSpeed(){
		for (let a in this.log){
			animation.graphLine(this.log[a].time * this.multiplierX, this.log[a].speed.length() * this.multiplierY);
		}
	}

	tick(a){
		this.log.push(a);
	}
}
