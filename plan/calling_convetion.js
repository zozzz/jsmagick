/**
 * DEFINITIONS: 
 * ============================================
 * def test1()
 * 
 * def test2(arg1, arg2, arg3=None)
 * 
 * def test3(*args)
 * 
 * def test4(**kwargs)
 * 
 * def test5(arg1, arg2=None, *args, **kwargs)
 * 
 * class X:
 * 		def test1(self)
 * 
 * 		def test2(self, arg1)
 * 
 * 		@classmethod
 * 		def test3(cls)
 * 
 * 		@staticmethod
 * 		def test4()
 * 
 * CALL
 * ============================================
 * test1() -> ok
 * test2(1) -> error
 * test2(1,2) -> ok, and arg3 = null
 * test2(arg1=1, arg2=2) -> ok
 * test2(1,2,3) -> ok
 * test3() -> ok, and args = []
 * test3(1,2,3) -> ok, and args = [1,2,3]
 * test4(test=1, test=2, test=3) -> ok, and kwargs = {test:1, test:2, test:3}
 * test5(1, 2, 3, 4, test=2, test=3) -> ok, and arg1=1, arg2=2, args = [3,4], kwargs = {test:2, test:3}
 * 
 * CC_TYPES:
 * 		NORMAL: test() | test(1,2,3) ...
 * 		KW_ARGS: test(1,2, test=1) | test(test=2) ...
 * 		UNPACK_ARGS: test(*params)
 * 		UNPACK_KWARGS: test(**kwparams)
 * 		UNPACK_BOTH: test(*params, **kwparams)
 * 
 * az összes függvényt így hívja majd meg: func(CC_TYPE, KW_START, params...)
 */

Function.prototype._arg = function(){};

function calling_convention()
{
	var T = 1000000, i=0, j=0, k=0, l=0;
	
	function test(args, kwargs)
	{
		
	}
	
	function test2(test1, test2, test3, test4)
	{
		
	}
	
	function test3(cc_type, kw_start)
	{
		
	}
	
	new Timer("array")
	for( i=0 ; i<T ; ++i )
		var z = [1, 2, 3, 4];
	Timer.last()
	
	new Timer("object")
	for( i=0 ; i<T ; ++i )
		var z = {test1:1, test2:2, test3:3, test4:4};
	Timer.last()
	
	new Timer("call('test1', 1, ...)")
	for( i=0 ; i<T ; ++i )
		test3(1, 0, 'test1', 1, 'test2', 2, 'test3', 3, 'test4', 4);
	Timer.last()
	
	new Timer("call(array)")
	for( i=0 ; i<T ; ++i )
		test([1, 2, 3, 4]);
	Timer.last()
	
	new Timer("call(object)")
	for( i=0 ; i<T ; ++i )
		test([], {test1:1, test2:2, test3:3, test4:4});
	Timer.last()
		
	new Timer("call(1, 2, 3, 4)")
	for( i=0 ; i<T ; ++i )
		test2(1, 2, 3, 4);
	Timer.last()
	
	new Timer("call()")
	for( i=0 ; i<T ; ++i )
		test();
	Timer.last()
	
	function fb_up(args)
	{
		var l=args.length, ret = [];
		while( --l >= 0 ) 
			ret[l] = args[l]+5;
		/*for(var i=0 ; i<l ; ++i)
		{
			ret.push(args[i]+5);
		}*/
		return ret;
	}
	
	function for_based_unpack(test1, test2, test3)
	{
		var t = fb_up(arguments);
		test1 = t[0];
		test2 = t[1];
		test3 = t[2];
		//console.log(test1, test2, test3);
	}
	
	new Timer("for_based_unpack()")
	for( i=0 ; i<T ; ++i )
		for_based_unpack(1,2,3);
	Timer.last()
	
	function up2(args,i)
	{
		return args[i]+5;
	}
	
	function _call_based_up(test1, test2, test3)
	{
		/*test1 = up2(arguments, 0);
		test2 = up2(arguments, 1);
		test3 = up2(arguments, 2);*/
		//console.log(test1, test2, test3);
	}
	
	function call_based_up()
	{
		return _call_based_up(up2(arguments, 0), up2(arguments, 1), up2(arguments, 2));
	}
	
	// WINNER
	new Timer("call_based_up()")
	for( i=0 ; i<T ; ++i )
		call_based_up(1,2,3);
	Timer.last()
	
	function e_up(args, o, n)
	{
		var l=args.length; 
		for(var i=0 ; i<l ; ++i)
		{
			o[n[i]] = args[i]+5;
		}
	}
	
	var extreme = (function(test1, test2, test3)
	{
		//var o = {test1:null, test2:null, test3:null};
		var n = ['test1', 'test2', 'test3'];
		return function ()
		{
			e_up(arguments, o={}, n);
			test1 = o.test1; test2 = o.test2; test3 = o.test3;
			//console.log(test1, test2, test3);
		};
	})()
	
	/*new Timer("extreme()")
	for( i=0 ; i<T ; ++i )
		extreme(1,2,3);
	Timer.last()*/	
	
	
	for_based_unpack(1,2,3);
	call_based_up(1,2,3);
	extreme(1,2,3);
	
	/*function UNPACK(x)
	{
		x = 2;
	}
	
	function CALLER(test)
	{
		var z = 0;
		UNPACK(z)
		console.log(z);
	}
	
	CALLER();*/
}

function calling_convention_2()
{
	var T=1000000;
	
	function jsm_arg(fn, args, idx, name, start){}
	
	// def cct(a1, a2, a3=None, a4=4)
	function _cct(args, kwargs)
	{
		
	}	
	
	function cct(type, kw_start, a1, a2, a3, a4)
	{
		if( type == 0 )
			return _cct(a1, a2, a3, a4);
		else
		{
			var fn, A=jsm_arg; 
			(fn=cct).__i = 0; 
			if( type == 1 )
			{
				return _cct(
					jsm_arg(fn, arguments, 0, 'a1'),
					jsm_arg(fn, arguments, 2, 'a2'),
					jsm_arg(fn, arguments, 3, 'a3'),
					jsm_arg(fn, arguments, 4, 'a4'),
					jsm_arg(fn, arguments, 5, 'a4'),
					jsm_arg(fn, arguments, 6, 'a4'),
					jsm_arg(fn, arguments, 7, 'a4'),
					jsm_arg(fn, arguments, 8, 'a4'),
					jsm_arg(fn, arguments, 9, 'a4'),
					jsm_arg(fn, arguments, 10, 'a4'),
					jsm_arg(fn, arguments, 11, 'a4'),
					jsm_arg(fn, arguments, 12, 'a4'),
					jsm_arg(fn, arguments, 13, 'a4'),
					jsm_arg(fn, arguments, 14, 'a4'),
					jsm_arg(fn, arguments, 15, 'a4'),
					jsm_arg(fn, arguments, 16, 'a4'),
					jsm_arg(fn, arguments, 17, 'a4'),
					jsm_arg(fn, arguments, 18, 'a4'),
					jsm_arg(fn, arguments, 19, 'a4'),
					jsm_arg(fn, arguments, 20, 'a4'),
					jsm_arg(fn, arguments, 21, 'a4'),
					jsm_arg(fn, arguments, 22, 'a4'),
					jsm_arg(fn, arguments, 23, 'a4'),
					jsm_arg(fn, arguments, 24, 'a4'),
					jsm_arg(fn, arguments, 25, 'a4'),
					jsm_arg(fn, arguments, 26, 'a4'),
					jsm_arg(fn, arguments, 27, 'a4'),
					jsm_arg(fn, arguments, 28, 'a4'),
					jsm_arg(fn, arguments, 29, 'a4'),
					jsm_arg(fn, arguments, 30, 'a4'),
					jsm_arg(fn, arguments, 31, 'a4'),
					jsm_arg(fn, arguments, 32, 'a4')
				);
			}
		}
		
	}
	cct.__original__ = _cct;
	
	function cct2(type, kw_start, a1, a2, a3, a4)
	{
		if( type == 0 )
		{
			return _cct(a1, a2, a3, a4);
		}
		else
		{
			if( type == 1 )
			{
				for( var i=0, l=arguments.length, x=[] ; i<l ; ++i )
					x[i] = arguments[i];
				
				return _cct.apply(null, x);	
			}
		}
	}
	
	// WINNER
	function cct3(l, args, kwargs, self, a1, a2)
	{
		var c = 0, a3=10, a4=15, isMethod;
		
		if( isMethod = (this != window) )
		{
			self = this;
		}
		else
		{
			if( l > c ){ self = args[c]; ++c; }
			else if( !(self = kwargs['self']) )
				throw "Unbound method vagy valami...";
		}
		
		if( args )
		{
			
			//var l=args.length;
			if( l > c ){ a1 = args[c++];
				if( l > c ){ a2 = args[c++]; 
					if( l > c ){ a3 = args[c++];
						if( l > c ){ a4 = args[c++]; } } } }
						
		}
		
		if( kwargs )
		{
			if( c < 2 ) a1 = kwargs.a1;
			if( c < 3 ) a2 = kwargs.a2;
			if( c < 4 ) a3 = kwargs.a3;
			if( c < 5 ) a4 = kwargs.a4;
		}
		
		/*if( typeof a3 == 'undefined' )
			a3 = 10;
			
		if( typeof a4 == 'undefined' )
			a4 = 15;*/
		
		//console.log(self, a1, a2, a3, a4);
		
		
	}
	
	
	
	function cct4(a1, a2, a3, a4)
	{
		//console.log(a1, a2, a3, a4);
	}
	cct4.__args__ = ['a1', 'a2', 'a3', 'a4'];
	
	
	Function.prototype.cc = function(args)
	{
		var i, l;
		/*for( i=0, l=args.length ; i<l ; ++i )
			x[i] = args[i];
		
		for( var i=1, l=arguments.length, c ; i<l ; i+=2 )
			if( ( c = this.__args__.indexOf(arguments[i]) ) > -1 )
				x[c] = arguments[i+1]*/
		
		return this.apply(null, args);	
	}
	
	function cct5(a1, a2, a3, a4)
	{
		if( a3 == undefined )
			a3 = 10;
			
		if( a4 == undefined )
			a4 = 15;
		//console.log(a1, a2, a3, a4);
	}
	
	cct5.$A = {a1:0, a2:1, a3:2, a4:3}; 
	cct5.$B = ['a1', 'a2', 'a3', 'a4'];
	
	function JSM_args(k, args, kwargs)
	{
		/*var kw = args.splice(k, args.length);
		
		for(var i=0, l=kw.length, a=cct5.$A ; i<l ; i+=2)
			args[a[kw[i]]] = kw[i+1];*/
		
		var a=cct5.$A;
		for(var k in kwargs)
			args[a[k]] = kwargs[k];
		
		return args;
	}
	
	cct5.$CALL = function(k, args, kwargs)
	{
		var a=this.$A;
		for(var k in kwargs)
			args[a[k]] = kwargs[k];
		
		return this(args[0], args[1], args[2], args[3]);
	}
	
	cct5.$CAL2 = new Function('k', 'args', 'kwargs', 'var a=this.$A; for(var k in kwargs) args[a[k]] = kwargs[k]; return this(args[0], args[1], args[2], args[3]);');
	
	var PUSH = Array.prototype.push;
	function JSM_args_x(a1, a2)
	{
		PUSH.apply(a1, a2);
		return a1;
	}
	
	x = {};
	
	//T = 1;
	new Timer("cct3()")
	for( i=0 ; i<T ; ++i )
		cct3(4, [x, 1, 2, 3], {a4:4});
	Timer.last()
	
	
	new Timer("cct4()")
	for( i=0 ; i<T ; ++i )
		cct4(1,2,3,4);
	Timer.last()
	
	new Timer("cct4.cc()")
	for( i=0 ; i<T ; ++i )
		cct4.cc([1, 2, 3, 'a4', 4]);
	Timer.last()
	
	var _args = [3, 4];
	var US = Array.prototype.concat;
	
	new Timer("cct5()")
	for( i=0 ; i<T ; ++i )
		cct5.apply(null, JSM_args(3, [1, 2, 3], {'a4':4}));
	Timer.last()
	
	new Timer("cct5.$CALL()")
	for( i=0 ; i<T ; ++i )
		cct5.$CALL(3, [1, 2, 3], {'a4':4});
	Timer.last()
	
	new Timer("cct5.$CAL2()")
	for( i=0 ; i<T ; ++i )
		cct5.$CAL2(3, [1, 2, 3], {'a4':4});
	Timer.last()
	
	T = 10000;
	new Timer("new.Func")
	for( i=0 ; i<T ; ++i )
		new Function('k', 'args', 'kwargs', 'var a=this.$A; for(var k in kwargs) args[a[k]] = kwargs[k]; return this(args[0], args[1], args[2], args[3]);');
	Timer.last()
	 
	
	/*
	new Timer("cct_call()")
	for( i=0 ; i<T ; ++i )
		cct2(1, 0, 'a1', 1, 'a2', 2, 'a3', 3);
	Timer.last()
	
	new Timer("cct.cc()")
	for( i=0 ; i<T ; ++i )
		_cct.cc('a1', 1, 'a2', 2, 'a3', 3);
	Timer.last()*/
	
	
	// cct(1,2)
	cct(0, 0, 1,2);
	
	// cct(a1=1, a2=2, a3=3)
	cct(1, 0, 'a1', 1, 'a2', 2, 'a3', 3);
	
	// cct(1, 2, a4=5);
	cct(1, 2, 1, 2, 'a4', 5);
}
