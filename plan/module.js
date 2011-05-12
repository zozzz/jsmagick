// __builtin__
function JSM_import(m){return m;}

function JSM_def(o,n,v){return (o[n]=v);}

function JSM_import_def(m, n)
{
	for(var i=0, l=n.length ; i<l ; ++i)
		this[n[1]] = m[n[0]];
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
	 */
	
	var TOP_LEVEL = JSM_def(globals, "TOP_LEVEL", "TOP_LEVEL");
	 
	globals.ClassName = function(){}; /*Class decl...*/
	globals.func = function(){};
	return globals;	
})();

var module2 = (function()
{
	function globals(){ return globals; };
	JSM_import_def.call(globals, moduleName, [['TOP_LEVEL', 'TL'], ['func', 'funcAlias']]);
	globals.xyz = JSM_import(moduleName);
})();
