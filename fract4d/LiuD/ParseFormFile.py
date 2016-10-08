import Ast_GFF
from Ast_GFF import GFF_sample_visitor_01

class mywalk(GFF_sample_visitor_01):
    def visit_Module(self, node):
        lst = []
        for v in node.vlst:
            leaf = v.walkabout(self)
            if leaf:
                lst.append(leaf)
        return new_dict(leaf='',type='formlist',children=lst)
    def visit_commentblk(self, node):
        return None
    def visit_formu_deep(self, node):
        leaf = node.n.strip()
        text = PrtOneNode(node)
        symm = None
        if node.vq is not None:
            symm = node.vq.n
        lst = []
        for v in node.vlst:
            if isinstance(v, Ast_GFF.GFF_anotherfmt):
                lst_init = v.v1.walkabout(self)
                lst.append(new_dict(type='stmlist', leaf='nameless', children=lst_init))

                lst_loop = v.v2.walkabout(self)

                condi_value = v.v3.walkabout(self)
                lst_loop.append(condi_value)

                lst.append(new_dict(type='stmlist', leaf='', children=lst_loop))
                continue
            sb = v.walkabout(self)
            if sb:
                lst.append(sb)
        return new_dict(leaf=leaf, children=lst, type='formula', text=text, symmetry=symm, deepmod=node)

    def visit_formu(self, node):
        leaf = node.n.strip()
        text = PrtOneNode(node)
        symm = None
        if node.vq is not None:
            symm = node.vq.n
        lst = []
        return new_dict(leaf=leaf, children=lst, type='formula', text=text, symmetry=symm)
    def visit_stmtblk(self, node):
        lst = []
        for v in node.vlst:
            a = v.walkabout(self)
            lst.append(a)
        return lst
    def _sub_blk(self, vlst, name):
        lst = []
        for v in vlst:
            sb = v.walkabout(self)
            if sb:
                lst.append(sb)
        return new_dict(leaf=name, type='stmlist', children=lst)
    def visit_init_blk(self, node):
        return self._sub_blk(node.vlst, 'init')
    def visit_loop_blk(self, node):
        return self._sub_blk(node.vlst, 'loop')
    def visit_bailout_blk(self, node):
        return self._sub_blk([node.v], 'bailout')
    def visit_default_blk(self, node):
        dict_ =  self._sub_blk(node.vlst, 'default')
        dict_['type'] = 'setlist'
        return dict_
    def visit_final_blk(self, node):
        return self._sub_blk(node.vlst, 'final')
    def visit_stmt(self, node):
        return node.v.walkabout(self)
    def visit_declare(self, node):
        dt = getdt(node.v1.s)
        a2 = node.v2.walkabout(self)
        name = a2['leaf']
        return new_dict(type='decl', leaf=name, datatype=dt)
    def visit_assign(self, node):

        assert len(node.vlst) == 1
        a1 = node.vlst[0].walkabout(self)
        a2 = node.v.walkabout(self)
        if a1 is None or a2 is None:
            a1 = node.vlst[0].walkabout(self)
            a2 = node.v.walkabout(self)

        if node.vq is not None:
            dt = getdt(node.vq.s)
            name = a1['leaf']
            return new_dict(type='decl', leaf=name, datatype=dt, children=[a2])

        return new_dict(type='assign', children=[a1,a2])
    def visit_EnclosedValue(self, node):
        return node.v.walkabout(self)
    def visit_AbsSigned(self, node):
        a = node.v.walkabout(self)
        return {"datatype": None, "leaf": "cmag", "type": "unop", "pos": 0, "children":[a]}
    def visit_bool_value(self, node):
        if node.s == 'true':
            flg = True
        elif node.s == 'false':
            flg = False
        else:
            assert False
        return {"datatype": 0, "leaf": flg, "type": "const", "pos": 0, "children": []}
    def visit_Num_Complex(self, node):
        a1 = node.v1.walkabout(self)
        a2 = node.v2.walkabout(self)
        if a1 is None:
            a1 = node.v1.walkabout(self)
        if a2 is None:
            a2 = node.v2.walkabout(self)
        return new_dict(leaf='complex', type='binop', children=[a1,a2])
    def visit_Num_Hyper(self, node):
        a1 = node.v1.walkabout(self)
        a2 = node.v2.walkabout(self)
        a3 = node.v3.walkabout(self)
        a4 = node.v4.walkabout(self)
        return new_dict(type='funcall', leaf='hyper', children=[a1,a2,a3,a4])
    def visit_neg_value(self, node):
        a = node.v.walkabout(self)
        return new_dict(leaf='t__neg',type='unop', children=[a])
    def visit_Numi(self, node):
        return {"datatype": 1, "leaf": node.i, "type": "const", "pos": 0, "children": []}
    def visit_nameq(self, node):
        return node.v.walkabout(self)
    def visit_Name0(self, node):
        name = node.n
        if name == 'true':
            return new_dict(leaf=True, datatype=0, type='const')
        if name == 'false':
            return new_dict(leaf=False, datatype=0, type='const')
        return new_dict(leaf=name, type='id')
    def visit_Name1(self, node):
        name = '#' + node.n
        dict_ = {'datatype' : None, 'pos' : 0, 'leaf' : name, 'children' : [], 'type' : 'id'}
        return dict_
    def visit_Name2(self, node):
        name = '@' + node.n
        dict_ = {'datatype' : None, 'pos' : 0, 'leaf' : name, 'children' : [], 'type' : 'id'}
        return dict_
    def visit_String(self, node):
        return new_dict(datatype=5, leaf=node.s[0], type="string")
    def visit_value2(self, node):
        a1 = node.v1.walkabout(self)
        a2 = node.v3.walkabout(self)
        name = node.s
        dict_ = {'datatype' : None, 'pos' : 0, 'leaf' : name, 'children' : [a1, a2], 'type' : 'binop'}
        return dict_
    def visit_funccall(self, node):
        name_dict = node.v.walkabout(self)
        name = name_dict['leaf']
        lst = []
        if node.vq is not None:
            for v in node.vq.vlst:
                a = v.walkabout(self)
                lst.append(a)
        dict_ = {'datatype' : None, 'pos' : 0, 'leaf' : name, 'children' : lst, 'type' : 'funcall'}
        return dict_
    def visit_general_param(self, node):
        name = node.n
        lst = []
        for v in node.vlst:
            a = v.walkabout(self)
            lst.append(a)
        return new_dict(leaf=name, children=lst, type='param')
    def visit_dt_param(self, node):
        dt = getdt(node.v1.s)
        name = node.v2.n
        lst = []
        for v in node.vlst:
            a = v.walkabout(self)
            if a is None:
                a = v.walkabout(self)

            lst.append(a)
        return new_dict(leaf=name, children=lst, type='param', datatype=dt)
    def visit_df_default(self, node):
        dict1 = {'datatype' : None, 'pos' : 0, 'leaf' : 'default', 'children' : [], 'type' : 'id'}
        dict2 = node.v.walkabout(self)
        if dict2 is None:
            dict2 = node.v.walkabout(self)

        lst = [dict1, dict2]
        return new_dict(type='set', children=lst)
    def visit_Number(self, node):
        dict_ = {'datatype' : 2, 'pos' : 0, 'leaf' : float(node.f), 'children' : [], 'type' : 'const'}
        return dict_
    def visit_dt_func(self, node):
        name = node.n
        dt = getdt(node.v.s)
        lst = []
        for v in node.vlst:
            a = v.walkabout(self)
            if a is None:
                a = v.walkabout(self)

            lst.append(a)
        return new_dict(datatype=dt, leaf=name, children=lst, type='func')
    def visit_df_enum(self, node):
        lst = []
        for s in node.slst:
            lst.append(new_dict(datatype=5, leaf=s[0], type="string"))
        first = lst.pop(0)
        first['children'] = lst

        a_enum = new_dict(leaf="enum", type="id")

        a_set = new_dict(type="set", children=[a_enum, first])
        return a_set

    def visit_df_hint(self, node):
        a1 = new_dict(leaf="hint", type="id")
        s = node.s[0]
        s = s.replace('\\\n','')
        a2 = new_dict(datatype=5, leaf=s, type="string")
        return new_dict(type='set', children=[a1,a2])
    def visit_df_caption(self, node):
        a1 = new_dict(leaf="caption", type="id")
        a2 = new_dict(datatype=5, leaf=node.s[0], type="string")
        return new_dict(type='set', children=[a1,a2])
    def visit_df_title(self, node):
        a1 = new_dict(leaf="title", type="id")
        a2 = new_dict(datatype=5, leaf=node.s[0], type="string")
        return new_dict(type='set', children=[a1,a2])
    def visit_df_argtype(self, node):
        dt = getdt(node.v.s)

        a1 = new_dict(type='id', leaf='argtype')
        a2 = new_dict(type='empty', leaf='')
        return new_dict(datatype=dt, type='set', children=[a1,a2])
    def visit_if_stmt(self, node):
        condi = node.v1.walkabout(self)
        if condi is None:
            condi = node.v1.walkabout(self)
        stmt_1 = node.v2.walkabout(self)
        stmt = new_dict(leaf='', type='stmlist', children=stmt_1)
        lst = []
        elseblk = new_dict(type='stmlist', leaf='', children=lst)
        if0 = new_dict(type='if', leaf='', children=[condi, stmt, elseblk])
        if True:
            for tem1 in node.vlst:
                condi2, stmt2 = tem1.walkabout(self)
                lst2 = []
                elseblk2 = new_dict(type='stmlist', leaf='', children=lst2)
                if2 = new_dict(type='if', leaf='', children=[condi2, stmt2, elseblk2])
                lst.append(if2)
                lst = lst2
            if node.vq is not None:
                elselst = node.vq.walkabout(self)
                lst.extend(elselst)
        if not lst:
            lst.append(new_dict(type='empty',leaf=''))
        return if0
    def visit_elseifblk(self, node):
        condi = node.v1.walkabout(self)
        stmt_1 = node.v2.walkabout(self)
        stmt = new_dict(leaf='', type='stmlist', children=stmt_1)
        return condi, stmt
    def visit_elseblk(self, node):
        stmt_1 = node.v.walkabout(self)
        return stmt_1 # new_dict(leaf='', type='stmlist', children=stmt_1)
    def visit_not_value(self, node):
        a = node.v.walkabout(self)
        return new_dict(type='unop',leaf='t__not',children=[a])
'''
type : unop leaf : t__not children : [
                     type : id leaf : @offset children : []
                ]
                '''

def new_dict(**ww):
    if ww.has_key('children'):
        for a in ww['children']:
            if a is None:
                pass
            assert a is not None
    a = {"datatype": None, "leaf": None, "type": None, "pos": 0, "children": []}
    a.update(ww)
    return a

'''
int param mode
    enum = "basin" "basin + iterations" "basin + potential"
    default = "basin + iterations"
endparam

            {"datatype": 1, "leaf": "mode", "type": "param", "pos": 26, "children": [
                {"datatype": null, "leaf": null, "type": "set", "pos": 27, "children": [
                    {"datatype": null, "leaf": "enum", "type": "id", "pos": 27, "children": []},
                    {"datatype": 5, "leaf": "basin", "type": "string", "pos": 27, "children": [
                        {"datatype": 5, "leaf": "basin + iterations", "type": "string", "pos": 27, "children": []},
                        {"datatype": 5, "leaf": "basin + potential", "type": "string", "pos": 27, "children": []}
                    ]}
                ]},
                {"datatype": null, "leaf": null, "type": "set", "pos": 28, "children": [
                    {"datatype": null, "leaf": "default", "type": "id", "pos": 28, "children": []},
                    {"datatype": 5, "leaf": "basin + iterations", "type": "string", "pos": 28, "children": []}
                ]}
            ]},
'''

def getdt(s):
    if s == 'bool':
        return 0
    if s == 'int':
        return 1
    if s == 'float':
        return 2
    if s == 'complex':
        return 3
    if s == 'color':
        return 4
    if s == 'hyper':
        return 6
    return 0

class myprt(Ast_GFF.GFF_out_visitor_01):
    pass
    #def visit_AssignDT(self, node):
    #    self.outp.puts(node.s)
    #def visit_value2(self, node):
    #    node.v1.walkabout(self)
    #    self.outp.puts(node.s)
    #    node.v3.walkabout(self)

def PrtOneNode(node):
    outlst = []
    outp = Ast_GFF.OutPrt(outlst)
    the = myprt(outp)
    node.walkabout(the)
    outp.newline()
    return '\n'.join(outlst)

def func1(deepin):
    if True:
        fname = 'formulas/gf4d.frm'
        fname = 'formulas/fractint-g4.frm'
        sfile = open(fname).read()
        sfile = '''Angles {
; delta total, total, min, delta min, max, delta max, avg, delta avg
; iter @ min, iter @ max, iter @ delta min, iter @ delta max
init:
float angle = 0.0
complex lastz = (0,0)
float temp_angle
int itermin = 0
int itermax = 0
if @angle_type == "delta min" || @angle_type == "min" || @angle_type == "iter @ min"
    angle = #pi
endif
loop:
if @angle_type == "delta total"
    angle = angle + abs(atan2(z-lastz))
elseif @angle_type == "delta max"
    temp_angle = abs(atan2(z-lastz))
    if temp_angle > angle
	angle = temp_angle
    endif
elseif @angle_type == "delta min"
    temp_angle = abs(atan2(z-lastz))
    if temp_angle < angle
	angle = temp_angle
    endif
elseif @angle_type == "min" || @angle_type == "iter @ min"
    temp_angle = abs(atan2(z))
    if temp_angle < angle
	angle = temp_angle
	itermin = #numiter
    endif
elseif @angle_type == "max" || @angle_type == "iter @ max"
    temp_angle = abs(atan2(z))
    if temp_angle > angle
	angle = temp_angle
	itermax = #numiter
    endif
elseif @angle_type == "total"
    angle = angle + abs(atan2(z))
endif
lastz = z
final:
if @angle_type == "iter @ min"
    #index = itermin/256.0
elseif @angle_type == "iter @ max"
    #index = itermax/256.0
else
    #index = angle/#pi
endif
default:
param angle_type
	default = 0
	enum = "delta total" "delta max" "delta min" "min" "max" "total" "iter @ min" "iter @ max"
endparam
}
        '''
        if deepin:
            parser = Ast_GFF.Parser(sfile)
            mod = parser.handle_formu_deep()
            if mod is None:
                lastpos, lastlineno, lastcolumn, lastline = parser.GetLast()
                print 'parse error, last pos = %d' % lastpos
                print 'last lineno = %d, column = %d' % (lastlineno, lastcolumn)
                print 'last line :', lastline
            else:
                print 'parse success'
        else:
            mod = Ast_GFF.Test_Parse_GFF(sfile)

    else:
        mod = Ast_GFF.Test_Parse_GFF(Ast_GFF.s_sample_GFF)
    if not mod :
        return
    the = mywalk()
    dict_ = mod.walkabout(the)
    print dict_

def ParseFormuFile_nodeep(s_formufile):
    mod = Ast_GFF.Test_Parse_GFF(s_formufile)
    if not mod:
        return
    formulas = {}
    for v in mod.vlst:
        if isinstance(v, Ast_GFF.GFF_formu):
            leaf = v.n.strip()
            text = PrtOneNode(v)
            formulas[leaf] = text
    return formulas

def ParseFormuFile_deep(s_formufile):
    if True:
        parser = Ast_GFF.Parser(s_formufile)
        mod = parser.handle_formu_deep()
        if mod.n.strip() == 'CGNewton3':
            # replace with I support format
            src = '''CGNewton3 {
    init:
        z = (1.0, 1.0)
    loop:
        z2 = z * z
        z3 = z * z2
        z = z - @p1 * (z3 - #pixel) / (3.0 * z2)
    bailout:
        0.0001 < |z3 - #pixel|

    default:
    complex param p1
        default = (0.66253178213589414, -0.22238807443609804)
    endparam
    }'''
            parser = Ast_GFF.Parser(src)
            mod = parser.handle_formu_deep()
    else:
        mod = Ast_GFF.Test_Parse_GFF(s_formufile)
    if not mod:
        return
    the = mywalk()
    dict_ = mod.walkabout(the)
    return new_dict(leaf='',type='formlist',children=[dict_])

if __name__ == '__main__':
    func1(True)
