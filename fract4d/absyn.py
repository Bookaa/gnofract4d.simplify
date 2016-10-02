# Abstract Syntax Tree produced by parser

#from __future__ import generators
import types
import string
import fracttypes
import re

class Node1:
    def __init__(self, dict_):
        self.dict_ = dict_

        self.type = dict_['type']
        self.leaf = dict_['leaf']
        self.pos = dict_['pos']
        self.datatype = dict_['datatype']
        if 'symmetry' in dict_:
            self.symmetry = dict_['symmetry']
        if 'last_line' in dict_:
            self.last_line = dict_['last_line']
        if 'text' in dict_:
            self.text = dict_['text']
        if 'deepmod' in dict_:
            self.deepmod = dict_['deepmod']

        self.children = [Node1(v) for v in dict_['children']]

    def childByName(self,name):
        'find a child with leaf == name'
        for child in self.children:
            if child.leaf == name:
                return child
        return None

class Node:
    def __init__(self,type,pos,children=None,leaf=None,datatype=None):
         self.type = type
         if children:
              self.children = children
         else:
              self.children = [ ]
         self.leaf = leaf
         self.datatype = datatype
         self.pos = pos

    def __str__(self):
        return "[%s : %s]" % (self.type , self.leaf)

    def pretty(self,depth=0):
        str = " " * depth + "[%s : %s" % (self.type , self.leaf)
        if self.datatype != None:
            str += "(%s)" % fracttypes.strOfType(self.datatype)
        if self.children:
            str += "\n"
            for child in self.children:
                assert(isinstance(child,Node))
                str += child.pretty(depth+1) + "\n"
            str += " " * depth + "]"
        else:
            str += "]"
        return str

    def __iter__(self):
        return NodeIter(self)

    def childByName(self,name):
        'find a child with leaf == name'
        for child in self.children:
            if child.leaf == name:
                return child
        return None

    def DeepCmp(self,other):
        if self.type < other.type: return -1
        if self.type > other.type: return 1

        if self.leaf < other.leaf: return -1
        if self.leaf > other.leaf: return 1

        #if len(self.children) < len(other.children): return -1
        #if len(self.children) > len(other.children): return 1

        if not self.children and not other.children: return 0

        for (child, otherchild) in zip(self.children,other.children):
            eql = child.DeepCmp(otherchild)
            if eql: return eql
        return eql

    def SerialOut(self):
        # self.type is str
        # self.leaf is str
        # self.pos is int
        # self.datatype is None or int
        lst = []
        for nod in self.children:
            s = nod.SerialOut()
            lst.append(s)

        dict_ = {'type' : self.type, 'leaf' : self.leaf, 'pos' : self.pos, 'datatype' : self.datatype,}
        if hasattr(self, 'symmetry'):
            dict_['symmetry'] = self.symmetry
        if hasattr(self, 'last_line'):
            dict_['last_line'] = self.last_line
        import json
        if not lst:
            dict_['children'] = []
            s = json.dumps(dict_)
        else:
            s = json.dumps(dict_)
            s2 = ', '.join(lst)
            assert s[-1] == '}'
            s = s[:-1] + (', "children": [%s]}' % s2)
        return s
    def SerialIn(self, dict_):
        self.type = dict_['type']
        self.leaf = dict_['leaf']
        self.pos = dict_['pos']
        self.datatype = dict_['datatype']
        if 'symmetry' in dict_:
            self.symmetry = dict_['symmetry']
        if 'last_line' in dict_:
            self.last_line = dict_['last_line']
        if 'text' in dict_:
            self.text = dict_['text']
        if 'deepmod' in dict_:
            self.deepmod = dict_['deepmod']
        lst = dict_['children']
        if lst:
            for dict1 in lst:
                m = Node(0,0)
                m.SerialIn(dict1)
                self.children.append(m)
# def preorder(t):
#     if t:
#         print "pre",t
#         yield t
#         for child in t.children:
#             print "prechild", child
#             preorder(child)

class NodeIter:
    def __init__(self,node):
        self.nodestack = [(node,-1)]

    def __iter__(self):
        return self

    def getNode(self,node,child):
        if child == -1:
            return node
        else:
            return node.children[child]

    def next(self):
        #print map(lambda (n,x) :"%s %s" % (n,x), self.nodestack)
        if self.nodestack == []:
            raise StopIteration

        (node,child) = self.nodestack.pop()
        ret = self.getNode(node,child)
        child+= 1
        while len(node.children) <= child:
            if self.nodestack == []:
                return ret
            (node,child) = self.nodestack.pop()

        self.nodestack.append((node,child+1))
        self.nodestack.append((node.children[child],-1))

        return ret

def CheckTree(tree, nullOK=0):
    if nullOK and tree == None:
        return 1
    if not isinstance(tree,Node):
        raise Exception, "bad node type %s" % tree
    if tree.children:
        if not isinstance(tree.children, types.ListType):
            raise Exception, ("children not a list: %s instead" % tree.children)
        for child in tree.children:
            CheckTree(child,0)
    return 1

# shorthand named ctors for specific node types
def Formlist(list, pos):
    return Node("formlist", pos, list, "")

def Set(id, s, pos):
    return Node("set", pos, [id,s], None)

def SetType(id,t,pos):
    type = fracttypes.typeOfStr(t)
    return Node("set", pos, [id, Empty(pos)], None, type)

def Number(n,pos):
    if re.search('[.eE]',n):
        assert False
        from ffloat import Float

        t = fracttypes.Float
        n = Float(n)
    else:
        t = fracttypes.Int
        n = string.atoi(n)

    return Node("const", pos, None, n, t)

def Const(n,pos):
    if isinstance(n,types.StringType):
        n = n.lower()
    return Node("const", pos, None, n=="true" or n=="yes", fracttypes.Bool)

def Binop(op, left, right,pos):
    return Node("binop", pos, [left, right], op)

def ID(id,pos):
    return Node("id", pos, None, id)

def Mag(exp,pos):
    return Node("unop", pos, [exp], "cmag")

def Negate(exp,pos):
    return Node("unop", pos, [exp], "t__neg")

def Not(exp, pos):
    return Node("unop", pos, [exp], "t__not")

def String(s,list,pos):
    return Node("string", pos, list, s, fracttypes.String)

def Funcall(id,arglist,pos):
    return Node("funcall", pos, arglist, id)

def Assign(id,exp,pos):
    return Node("assign", pos, [id, exp], None)

def Decl(type, id, pos, exp=None):
    if exp == None:
        l = None
    else:
        l = [exp]
    return Node("decl", pos, l , id, fracttypes.typeOfStr(type))

def DeclArray(type, id, indexes, pos):
    return Node("declarray", pos, indexes, id, fracttypes.typeOfStr(type))

def ArrayLookup(id, indexes, pos):
    return Node("arraylookup", pos, indexes, id)

def Stmlist(id, list,pos):
    return Node("stmlist", pos,list, string.lower(id))

def Setlist(id, list,pos):
    return Node("setlist", pos, list, string.lower(id))

def Empty(pos):
    return Node("empty", pos, None, "")

def Formula(id, stmlist, pos):
    # rather gruesome: we re-lex the formula ID to extract the symmetry spec
    # if any. Then we smuggle it into the top-level node
    m = re.match(".*?(\s*\(\s*(\w+)\s*\))", id)
    if m:
        symmetry = m.group(2)
        id = id[:m.start(1)]
    else:
        symmetry = None

    n = Node("formula", pos, stmlist, id)
    n.symmetry = symmetry

    return n

def Param(id,settinglist,type,pos):
    return Node("param", pos, settinglist, id, fracttypes.typeOfStr(type))

def Func(id,settinglist,type, pos):
    return Node("func", pos, settinglist, id, fracttypes.typeOfStr(type))

def Heading(settinglist,pos):
    return Node("heading", pos, settinglist)

def Repeat(body, test, pos):
    return Node("repeat", pos, [test, Stmlist("",body,pos)], "")

def While(test, body, pos):
    return Node("while", pos, [test, Stmlist("", body,pos)], "")

def If(test, left, right, pos):
    return Node("if", pos,
                [test, Stmlist("",left,pos), Stmlist("",right,pos)], "")

def Error2(str, pos):
    if str == "$":
        return Node(
            "error", pos, None,
            "%d: Error: unexpected preprocessor directive" % pos)
    return Node("error", pos, None,
                "%d: Syntax error: unexpected '%s' " % (pos,str))

def Error(type, value, pos):
    # get complaints about NEWLINE tokens on right line
    if type == "NEWLINE":
        pos -= 1
        return Node("error", pos, None,
                    "%d: Syntax error: unexpected newline" % pos)

    return Node("error", pos, None,
                "%d: Syntax error: unexpected %s '%s'" %
                (pos, string.lower(type), value))

def PreprocessorError(value,pos):
    return Node("error", pos, None, value)
