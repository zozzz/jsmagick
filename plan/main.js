function Timer(name)
{
	this.name = name;
	this.start = new Date();
	this.end = null;
	this.result = 0;
	Timer._last = this;
}

Timer.last = function(){ Timer._last.print(); }

Timer.prototype.stop = function()
{ 
	if( this.end ) return this.result;
	
	this.end = new Date();
	this.result = (this.end.getTime() - this.start.getTime()) / 1000;
	return this.result;
}
Timer.prototype.print = function()
{
	var pre = document.createElement('pre');
	pre.innerHTML = '<b>'+this.name+':</b> '+this.stop();
	document.getElementsByTagName('body')[0].appendChild(pre);
}
