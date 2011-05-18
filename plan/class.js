/**
 * Ezeket kell tudnia:
 * 	- kell ilyen tulajdonság neki: 
 * 		__name__	: osztály neve
 * 		__module__	: module neve, amiben definiálva van
 * 		__doc__		: dokumentáció ha van 
 */

/*var TestClass = JSM_Class(function()
{
	//this.STATIC = 20;
});*/

function property(fget, fset, fdel, deoc)
{
	function inst()
	{
		if( this.inst )
		{
			inst.inst = this;
			inst.cls = this.__class__;
		}
		else
		{
			inst.inst = null;
			inst.cls = this;
		}
			
		return inst;
	};
	
	inst.$get = function(){ return fget(this, this.inst, this.cls); };
	inst.$set = function(val){ fset(this, this.inst || this.cls, val); return val; };
	inst.$del = function(){ fdel(this, this.inst || this.cls); };
	
	/*inst.__get__ = function(){}
	inst.__set__ = function(){}
	inst.__del__ = function(){}*/
	
	return inst;
}

function TestClass()
{
	this.inst = true;
	this.STATIC = TestClass.STATIC;
	this.STATIC().$set(TestClass.STATIC().$get());
	
	this.hello = function(){ console.log(this.STATIC().$get()); }
}

TestClass.prototype.__class__ = TestClass;

TestClass.inst = false;
TestClass.STATIC = property(
	function(self, inst, cls){ return (inst || cls)._STATIC; }, 
	function(self, inst, val){ inst._STATIC = val; }, 
	function(self, inst){ delete inst._STATIC; }
);

TestClass.STATIC().$set(10);


/**
 * INHERITANCE
 */

function Pointer(val)
{
	return {$:val};
}

function A(){};
A.A = A.prototype.A = Pointer(1);
A.prototype.methodA = function(){};

function B(){};
B.A = B.prototype.A = A.prototype.A;
B.prototype.methodB = function(){};


var CLS = (function()
{
	function ret()
	{
		var inst = ret.__new__();
		ret.__extend_with__(inst);
		return inst;
	};
	
	ret.__new__ = function()
	{
		return function x(){ x.__call__(); };
	};
	
	ret.__call__ = function()
	{
		console.log('__call__');
	};
	
	ret.A = Pointer(10);
	
	ret.__extend_with__ = function(t)
	{
		for( var k in this )
			t[k] = this[k];
	};
	
	return ret;
})();

CLS.test = function(){ console.log('test'); }

var c = CLS();
c();
console.log(c.A.$);
c.test();

function class_time()
{
	function cls1()
	{
		this.__lookup__ = [];
		this.x = 10;
		this.y = cls1.y;
	}
	cls1.y = 200;
	
	function cls2()
	{
		this.__lookup__ = [cls1];
		//this.__dict__ = {};
		//this.__dict__['x'] = 10;
		this.x = 10;
		//this.__getattr__ = function(a){ return this.__dict__[a]; }
	}
	
	function cls3()
	{
		this.__lookup__ = [cls3, cls2, cls1];
		//this.__dict__ = {};
		//this.__dict__['x'] = 10;
		this.x = 10;
		this.__getattr__ = function(a)
		{ 
			if( !(a in this) )
			{
				for(var i=0, l=this.__lookup__, c ; c = l[i] ; i++)
				{
					if( !(a in c) ) continue;						
						return c[a];
				}
			}
			else
				return this[a];
			
			throw "AttributeError" 
		}
	}
	cls3.prototype.__getattr__2 = new Function('a', 'return this[a];');
	
	function getattr(o, n)
	{
		if(o.__getattr__ instanceof Function)
		{
			return o.__getattr__(n);
		}
		else
		{
			if( typeof o[n] != 'undefined' )
				return o[n];
			
			for(var i=0, l=o.__lookup__, c=l.length, v ; v = l[i][n] ; ++i)
			{
				if( typeof v != 'undefined' )
					return v;
			}
			
			throw "AttributeError";
		}
	}
	
	var CLS1 = new cls1();
	var CLS2 = new cls2();
	var CLS3 = new cls3();
	
	var T = 1000000, c;
	
	new Timer("cls1.x")
	for( i=0 ; i<T ; ++i )
		c = CLS1.x;
	Timer.last()
	
	new Timer("cls2.x getattr")
	for( i=0 ; i<T ; ++i )
		c = getattr(CLS2, 'x');
	Timer.last()
	
	new Timer("cls2.y getattr")
	for( i=0 ; i<T ; ++i )
		c = getattr(CLS2, 'y');
	Timer.last()
	
	new Timer("cls3.x")
	for( i=0 ; i<T ; ++i )
		c = CLS3.__getattr__('x');
	Timer.last()
	
	new Timer("cls3.y")
	for( i=0 ; i<T ; ++i )
		c = CLS3.__getattr__('y');
	Timer.last()
	
	//console.log('x', CLS3.__getattr__('x'));
	//console.log('y', CLS3.__getattr__('y'));
}
