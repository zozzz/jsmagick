function module_plan()
{

	// __builtin__
	function JSM_import(m){return m;}
	
	function JSM_def(o,n,v){return (o[n]=v);}
	
	function JSM_import_def(m, n)
	{
		for(var i=0, l=n.length ; i<l ; ++i)
			this[n[i][1]] = m[n[i][0]];
	}
	
	// MODULES
	var moduleName = (function()
	{
		function globals(){ return globals; };
		
		/* lehet gondot fog okozni ha így szerepel:
		 * def func():
		 * 		TestClass().xy()
		 * 
		 * class TestClass:
		 * 		def xy(self): pass
		 * 
		 * func() 
		 * 
		 */
		
		JSM_def(globals, "TOP_LEVEL", "TOP_LEVEL");
		JSM_def(globals, "GLOBAL_VAR", 5)
		
		globals.printGV = function()
		{
			console.log(globals.GLOBAL_VAR);
		}
		 
		globals.ClassName = function(){}; /*Class decl...*/
		globals.func = function(){};
		return globals;	
	})();
	
	var __builtin__str = function(){};
	
	var module2 = (function()
	{
		function globals(){ return globals; };
		JSM_import_def.call(globals, moduleName, [['printGV', 'printGV'], ['GLOBAL_VAR', 'GLOBAL_VAR']]);
		globals.xyz = JSM_import(moduleName);
		
		console.dir(globals);
		
		globals.printGV();
		
		globals.GLOBAL_VAR = 10;
		
		globals.printGV();	
		globals.str = function(){};
		
		
		
		var T = 10000000, tmp;
		
		new Timer("__builtin__str")
		for( i=0 ; i<T ; ++i )
			tmp = __builtin__str;
		Timer.last()
		
		new Timer("globals.str")
		for( i=0 ; i<T ; ++i )
			tmp = globals.str;
		Timer.last()
		
	})();

}
