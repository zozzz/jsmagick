
from jsmagick.decor import JavaScript

@JavaScript(doc=True)
def importFrom(target, module, aliases):
    """
    for( var alias in aliases )
        target[alias] = module[aliases[alias]];
    """
    pass

@JavaScript(doc=True)
def importModule(target, module, ns):
    """
    for( var _ns in ns )
        if( typeof target[_ns] == 'undefined' )
            target = target[_ns] = {};
        else
            target = target[_ns];
    
    module.importAll(target)
    """
    pass
