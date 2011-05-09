'''
Created on 2011.05.06.

@author: Zozzz
'''

# MISSING: Interactive, Expression, Suite, While, If, With, Raise, TryExcept, TryFinally, Assert
# Exec, Global, Break, Continue, Lambda, IfExp, Set, ListComp, SetComp, DictComp, GeneratorExp, Yield, Repr
# Subscript, slice, comprehension, excepthandler 

import ast
from tree import *
import os

class Parser:
    CURRENT_FILE = None

    @staticmethod
    def parseFile(file):
        Parser.CURRENT_FILE = file

        fp = open(file, "r")
        fp.seek(0, os.SEEK_END)
        size = fp.tell()
        fp.seek(0, os.SEEK_SET)

        ret = Parser.parseString(fp.read(size))
        Parser.CURRENT_FILE = None
        return ret

    @staticmethod
    def parseString(str):
        if Parser.CURRENT_FILE is not None:
            file = Parser.CURRENT_FILE
        else:
            file = "<String>"

        visitor = Visitor()
        visitor.visit(ast.parse(str, file))
        return visitor.root


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

        for sub in node.body:
            Visitor(self.root).visit(sub)

    def visit_Import(self, node):
        _module = self.root.ctx.getCtx(CodeContext.Type.MODULE).node

        for alias in node.names:
            moduleFile = self._moduleFile(alias.name)
            _child = ImportModule(moduleFile, [alias.name, alias.asname][bool(alias.asname)])
            _child.astNode = node
            _module.addChild(_child)

    def visit_ImportFrom(self, node):
        _module = self.root.ctx.getCtx(CodeContext.Type.MODULE).node

        moduleFile = self._moduleFile(node.module)
        for alias in node.names:
            _child = ImportDefinition(moduleFile, node.module, alias.name, [alias.name, alias.asname][bool(alias.asname)])
            _child.astNode = node
            _module.addChild(_child)

    def visit_ClassDef(self, node):

        baseList = []
        for base in node.bases:
            baseList.append(self._findDefinition(base, True))

        # TODO: Implement decorators
        # for decor in node.decorator_list:
        #    print decor

        _cls = Class(node.name, baseList, [])
        _cls.astNode = node

        for stm in node.body:
            Visitor(_cls).visit(stm)
        self.root.addChild(_cls)

    def visit_FunctionDef(self, node):
        #print "Func: %s, args: %s" % (node.name, node.args.args)
        normalArgs = []
        defs = node.args.defaults
        if defs:
            dl = len(defs)
        else:
            dl = 0

        c = len(node.args.args)
        for arg in node.args.args:
            _def = None
            _name = self._qName(arg)

            if dl and dl - c >= 0:
                _def = Visitor().visit_get(defs[dl - c])

            c -= 1
            normalArgs.append(FArgument(Identifier(_name), _def))

        if node.args.vararg:
            normalArgs.append(VarArg(Identifier(node.args.vararg)))

        if node.args.kwarg:
            normalArgs.append(KwArg(Identifier(node.args.kwarg)))

        _node = Function(node.name, normalArgs, [])
        _node.astNode = node
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
        qname = self._qName(node)
        _node = None
        if ConstLiteral.MAP.has_key(qname):
            _node = ConstLiteral(qname)
        else:
            _node = Identifier(qname)

        _node.astNode = node
        self.root.addChild(_node)

    def visit_Attribute(self, node):
        _node = Attribute(Expression.Context.getCtxFromAstNode(node))
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
        _body = CodeBlock()
        for stm in node.body:
            Visitor(_body).visit_get(stm)

        _orelse = CodeBlock()
        for stm in node.orelse:
            Visitor(_orelse).visit(stm)
        else:
            _orelse = None

        _for = For(
            Visitor().visit_get(node.target),
            Visitor().visit_get(node.iter),
            _body,
            _orelse
        )
        _for.astNode = node
        self.root.addChild(_for)

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

    def visit_keyword(self, node):
        _node = KeyValuePair(
            node.arg,
            Visitor().visit_get(node.value)
        )
        _node.astNode = node
        self.root.addChild(_node)

    def generic_visit(self, node):
        print "genric_visit %s" % node
        pass

    def _moduleFile(self, name):
        moduleFile = PathResolver.getFilePathFromModuleName(name, self.root.ctx.getCtx(CodeContext.Type.MODULE).node.file)
        if moduleFile is None:
            raise ImportError("Module not found: %s in %s" % (name, self._getLocation()))
        return moduleFile

    def _findDefinition(self, astNode, must=False):
        qName = self._qName(astNode)
        ref = self.root.ctx.getDefinitionByName(qName)
        if must and not ref:
            raise NameError("Definition not found for: %s in %s" % (qName, self._getLocation(astNode)))
        return ref

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
        return "[File: %s, line: %d, col: %d]" % (self.root.ctx.getCtx(CodeContext.Type.MODULE).node.file, node.lineno, node.col_offset)

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

import jsmagick._tree.tree as TREE
# Add | Sub | Mult | Div | Mod | Pow | LShift | RShift | BitOr | BitXor | BitAnd | FloorDiv
# Invert | Not | UAdd | USub
# Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn
# And | Or
for cls in [ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd, ast.FloorDiv,
            ast.Invert, ast.Not, ast.UAdd, ast.USub,
            ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn,
            ast.And, ast.Or]:
    Visitor.OP_CLASS_MAP[cls.__name__] = getattr(TREE, "op%s" % cls.__name__)

