'''
Created on 2011.05.06.

@author: Zozzz
'''

# MISSING: Interactive, Expression, Suite
# Exec, IfExp, Set, ListComp, SetComp, DictComp, GeneratorExp, Yield
# comprehension, Ellipsis, ExtSlice

import ast
import os

from tree import *
from path import PathResolver

class Parser:
    CURRENT_FILE = None
    MODULES = {}

    @staticmethod
    def parseFile(file):
        if Parser.MODULES.has_key(file):
            Parser.SESSION.addModule(Parser.MODULES[file])
            return Parser.MODULES[file]

        Parser.CURRENT_FILE = file

        with open(file, "r") as fp:
            fp.seek(0, os.SEEK_END)
            size = fp.tell()
            fp.seek(0, os.SEEK_SET)

            Parser.MODULES[file] = Parser.parseString(fp.read(size))
            Parser.SESSION.addModule(Parser.MODULES[file])
            Parser.CURRENT_FILE = None
            return Parser.MODULES[file]

    @staticmethod
    def parseString(str):
        if Parser.CURRENT_FILE is not None:
            file = Parser.CURRENT_FILE
        else:
            file = "<String>"

        visitor = Visitor()
        visitor.visit(ast.parse(str, file))
        return visitor.root

    @staticmethod
    def setSession(sess):
        Parser.SESSION = sess



ImportModule._loadModule = lambda self: Parser.parseFile(self.file)


class Visitor(ast.NodeVisitor):

    def __init__(self, root=None):
        ast.NodeVisitor.__init__(self)
        if root is None:
            root = ScriptContainer()
        self.root = root
        self.current = None

    def visit(self, node):
        self.current = node
        return ast.NodeVisitor.visit(self, node)

    def visit_get(self, node):
        self.visit(node)
        if len(self.root.children):
            return self.root.children[0]
        return None


    def visit_Module(self, node):
        self.root = Module(Parser.CURRENT_FILE)
        self.root.astNode = node

        Scope.CURRENT = self.root

        for sub in node.body:
            Visitor(self.root).visit(sub)

    def visit_Import(self, node):
        _module = self.root.module

        for alias in node.names:
            moduleFile = self._moduleFile(alias.name)
            _child = ImportModule(Parser.parseFile(moduleFile), alias.name, [alias.name, alias.asname][bool(alias.asname)])
            _child.astNode = node
            _module.addChild(_child)
            _module.addSymbol(alias.asname, _child)

    def visit_ImportFrom(self, node):
        _module = self.root.module

        moduleFile = self._moduleFile(node.module)
        for alias in node.names:
            _child = ImportDefinition(Parser.parseFile(moduleFile), node.module, alias.name, [alias.name, alias.asname][bool(alias.asname)])
            _child.astNode = node
            _module.addChild(_child)
            _module.addSymbol(alias.asname, _child)

    def visit_ClassDef(self, node):

        baseList = []
        for base in node.bases:
            baseList.append(Visitor().visit_get(base))

        # TODO: Implement decorators
        # for decor in node.decorator_list:
        #    print decor

        _cls = Class(Identifier(node.name), baseList, [])
        _cls.astNode = node

        Scope.CURRENT.addSymbol(node.name, _cls)
        Scope.CURRENT = _cls

        for stm in node.body:
            Visitor(_cls).visit(stm)

        self.root.addChild(_cls)

    def visit_FunctionDef(self, node):
        _node = Function(Identifier(node.name), self._arguments(node.args), [])
        _node.astNode = node

        Scope.CURRENT.addSymbol(node.name, _node)
        Scope.CURRENT = _node

        for stm in node.body:
            Visitor(_node).visit(stm)

        self.root.addChild(_node)

    def visit_Assign(self, node):

        assert len(node.targets) == 1 , ("Multiple targets %s" % node.targets)

        _node = Assign(Visitor().visit_get(node.targets[0]), Visitor().visit_get(node.value))
        _node.astNode = node
        self.root.addChild(_node)

    def visit_AugAssign(self, node):
        _left = Visitor().visit_get(node.target)
        _right = Visitor().visit_get(node.value)
        opcls = self._getOpClass(node.op)

        _op = opcls.__new__(opcls)
        _op.__init__(_left, _right)
        _op.astNode = node

        _node = AugAssign(_left, _op, _right)
        _node.astNode = node
        self.root.addChild(_node)

    def visit_Pass(self, node):
        pass

    def visit_Global(self, node):
        _node = Global(node.names)
        _node.astNode = node
        self.root.addChild(_node)

    def visit_Break(self, node):
        _node = Break()
        _node.astNode = node
        self.root.addChild(_node)

    def visit_Continue(self, node):
        _node = Continue()
        _node.astNode = node
        self.root.addChild(_node)

    def visit_Dict(self, node):
        _node = ObjectLiteral()
        _node.astNode = node
        for i in range(0, len(node.keys)):
            _node.addChild(KeyValuePair(Visitor().visit_get(node.keys[i]), Visitor().visit_get(node.values[i])))

        self.root.addChild(_node)

    def visit_List(self, node, cls=ArrayLiteral):
        _node = cls()
        _node.astNode = node

        for child in node.elts:
            Visitor(_node).visit(child)

        self.root.addChild(_node)

    def visit_Tuple(self, node):
        self.visit_List(node, TupleLiteral)

    def visit_Num(self, node):
        _n = NumberLiteral(node.n)
        _n.astNode = node
        self.root.addChild(_n)

    def visit_Str(self, node):
        _n = StringLiteral(node.s)
        _n.astNode = node

        if (isinstance(self.root, Class) \
            or isinstance(self.root, Function) \
            or isinstance(self.root, Module)) and len(self.root.children) == 0:
            self.root.doc = _n
        else:
            self.root.addChild(_n)

    def visit_Name(self, node):
        name = node.id
        if ConstLiteral.MAP.has_key(name):
            _node = ConstLiteral(name)
        else:
            _node = Identifier(name)

        _node.astNode = node
        self.root.addChild(_node)

    def visit_Attribute(self, node):
        _node = Attribute(ExpContext.getCtxFromAstNode(node))
        _node.astNode = node
        Visitor(_node).visit(node.value)
        _node.addChild(Identifier(node.attr))
        self.root.addChild(_node)

    def visit_Expr(self, node):
        Visitor(self.root).visit(node.value)

    def visit_BinOp(self, node):
        opcls = self._getOpClass(node.op)

        _node = opcls.__new__(opcls)
        _node.__init__(Visitor().visit_get(node.left), Visitor().visit_get(node.right))
        _node.astNode = node
        self.root.addChild(_node)

    def visit_UnaryOp(self, node):
        opcls = self._getOpClass(node.op)

        _node = opcls.__new__(opcls)
        _node.__init__(Visitor().visit_get(node.operand))
        _node.astNode = node
        self.root.addChild(_node)

    def visit_Compare(self, node):
        _node = self._cmpTree(node, len(node.ops) - 1)
        _node.astNode = node
        self.root.addChild(_node)

    def visit_BoolOp(self, node):
        opcls = self._getOpClass(node.op)
        _node = opcls.__new__(opcls)
        _node.__init__(Visitor().visit_get(node.values[0]), Visitor().visit_get(node.values[1]))
        _node.astNode = node
        self.root.addChild(_node)

    def visit_Print(self, node):
        _vals = []

        for expr in node.values:
            _vals.append(Visitor().visit_get(expr))

        _node = Print(node.dest and Visitor().visit_get(node.dest) or None, _vals, node.nl)
        _node.astNode = node
        self.root.addChild(_node)

    def visit_Call(self, node):

        _args = []
        for arg in node.args:
            _args.append(Visitor().visit_get(arg))

        _kwargs = []
        for arg in node.keywords:
            _kwargs.append(Visitor().visit_get(arg))

        _node = Call(
            Visitor().visit_get(node.func),
            _args,
            _kwargs,
            node.starargs and Visitor().visit_get(node.starargs) or None,
            node.kwargs and Visitor().visit_get(node.kwargs) or None
        )
        _node.astNode = node
        self.root.addChild(_node)

    def visit_For(self, node):
        _body = self._codeBlock(node.body)
        _else = self._codeBlock(node.orelse)

        _for = For(
            Visitor().visit_get(node.target),
            Visitor().visit_get(node.iter),
            _body,
            _else
        )
        _for.astNode = node
        self.root.addChild(_for)

    def visit_While(self, node):
        _test = Visitor().visit_get(node.test)
        _body = self._codeBlock(node.body)
        _else = self._codeBlock(node.orelse)

        _node = While(_test, _body, _else)
        _node.astNode = node
        self.root.addChild(_node)

    def visit_If(self, node):
        _test = Visitor().visit_get(node.test)
        _body = self._codeBlock(node.body)
        _else = self._codeBlock(node.orelse)

        _node = If(_test, _body, _else)
        _node.astNode = node
        self.root.addChild(_node)

    def visit_With(self, node):

        _node = With(
            Visitor().visit_get(node.context_expr),
            node.optional_vars and Visitor().visit_get(node.optional_vars) or None,
            self._codeBlock(node.body)
        )
        _node.astNode = node
        self.root.addChild(_node)

    def visit_Return(self, node):
        _node = Return(node.value and Visitor().visit_get(node.value) or None)
        _node.astNode = node
        self.root.addChild(_node)

    def visit_Delete(self, node):
        _targets = []
        for exp in node.targets:
            _targets.append(Visitor().visit_get(exp))
        _node = Delete(_targets)
        _node.astNode = node
        self.root.addChild(_node)

    def visit_Raise(self, node):
        _node = Raise(
            node.type and Visitor().visit_get(node.type) or None,
            node.inst and Visitor().visit_get(node.inst) or None,
            node.tback and Visitor().visit_get(node.tback) or None
        )
        _node.astNode = node
        self.root.addChild(_node)

    def visit_TryExcept(self, node):
        _node = TryExcept(
            self._codeBlock(node.body),
            self._codeBlock(node.orelse)
        )
        _node.astNode = node

        for stm in node.handlers:
            Visitor(_node).visit(stm)

        self.root.addChild(_node)

    def visit_TryFinally(self, node):
        _node = TryFinally(self._codeBlock(node.body), self._codeBlock(node.finalbody))
        _node.astNode = node
        self.root.addChild(_node)

    def visit_ExceptHandler(self, node):

        _node = ExceptHandler(
            node.type and Visitor().visit_get(node.type) or None,
            node.name and Visitor().visit_get(node.name) or None,
            self._codeBlock(node.body)
        )

        _node.astNode = node
        self.root.addChild(_node)

    def visit_Assert(self, node):
        _node = Assert(Visitor().visit_get(node.test), Visitor().visit_get(node.msg))
        _node.astNode = node
        self.root.addChild(_node)

    def visit_Lambda(self, node):
        _node = Lambda(self._arguments(node.args), Visitor().visit_get(node.body))
        _node.astNode = node
        self.root.addChild(_node)

    def visit_Subscript(self, node):
        _node = Subscript(
            Visitor().visit_get(node.value),
            Visitor().visit_get(node.slice),
            ExpContext.getCtxFromAstNode(node.ctx)
        )
        _node.astNode = node
        self.root.addChild(_node)

    def visit_Slice(self, node):
        _node = Slice(
            node.lower and Visitor().visit_get(node.lower) or None,
            node.upper and Visitor().visit_get(node.upper) or None,
            node.step and Visitor().visit_get(node.step) or None
        )
        _node.astNode = node
        self.root.addChild(_node)

    def visit_Index(self, node):
        _node = Index(Visitor().visit_get(node.value))
        _node.astNode = node
        self.root.addChild(_node)

    def visit_Repr(self, node):
        print "REPR: %s" % (node.value)
        # TODO: implement

    def visit_keyword(self, node):
        _node = KeyValuePair(
            node.arg,
            Visitor().visit_get(node.value)
        )
        _node.astNode = node
        self.root.addChild(_node)

    def visit_identifier(self, node):
        print "ID: %s" % node;

    def generic_visit(self, node):
        raise NotImplementedError("%s, %s" % (node, node.__class__.__name__))

    def _arguments(self, args):
        result = []
        defs = args.defaults
        if defs:
            dl = len(defs)
        else:
            dl = 0

        c = len(args.args)
        for arg in args.args:
            _def = None
            _name = self._qName(arg)

            if dl and dl - c >= 0:
                _def = Visitor().visit_get(defs[dl - c])

            c -= 1
            result.append(FArgument(Identifier(_name), _def))

        if args.vararg:
            result.append(VarArg(Identifier(args.vararg)))

        if args.kwarg:
            result.append(KwArg(Identifier(args.kwarg)))

        return result

    def _codeBlock(self, list):
        if not list:
            return None

        _ret = CodeBlock()
        for stm in list:
            Visitor(_ret).visit(stm)

        if not _ret.children:
            return None

        return _ret

    def _moduleFile(self, name):
        moduleFile = PathResolver.getFilePathFromModuleName(name, self.root.module.file)
        if moduleFile is None:
            raise ImportError("Module not found: %s in %s" % (name, self._getLocation()))
        return moduleFile

    """def _findDefinition(self, astNode, must=False):
        qName = self._qName(astNode)
        ref = self.root.ctx.getDefinitionByName(qName)
        if must and not ref:
            raise NameError("Definition not found for: %s in %s" % (qName, self._getLocation(astNode)))
        return ref"""

    def _qName(self, n):

        if isinstance(n, ast.Name):
            return n.id
        elif isinstance(n, ast.Attribute):
            return self._qName(n.value) + "." + n.attr
        elif isinstance(n, str):
            return n

    def _getLocation(self, node=None):
        if not node:
            node = self.current
        return "[File: %s, line: %d, col: %d]" % (self.root.module.file, node.lineno, node.col_offset)

    def _cmpTree(self, n, i):
        if i == 0:
            return self._cmpNode(
                Visitor().visit_get(n.left),
                n.ops[i],
                Visitor().visit_get(n.comparators[i]))
        else:
            return self._cmpNode(
                self._cmpTree(n, i - 1),
                n.ops[i],
                Visitor().visit_get(n.comparators[i]))

    def _cmpNode(self, l, op, r):
        opcls = self._getOpClass(op)
        _node = opcls.__new__(opcls)
        _node.__init__(l, r)
        return _node

    OP_CLASS_MAP = {}

    @staticmethod
    def _getOpClass(node):
        return Visitor.OP_CLASS_MAP[node.__class__.__name__]
        #return globals()["op%s" % node.__class__.__name__]

# Add | Sub | Mult | Div | Mod | Pow | LShift | RShift | BitOr | BitXor | BitAnd | FloorDiv
# Invert | Not | UAdd | USub
# Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn
# And | Or
_GLOBALS_ = globals()
for cls in [ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd, ast.FloorDiv,
            ast.Invert, ast.Not, ast.UAdd, ast.USub,
            ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn,
            ast.And, ast.Or]:
    Visitor.OP_CLASS_MAP[cls.__name__] = _GLOBALS_["op%s" % cls.__name__]
