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
