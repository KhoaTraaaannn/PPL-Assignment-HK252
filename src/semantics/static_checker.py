"""
Static Semantic Checker for TyC Programming Language

This module implements a comprehensive static semantic checker using visitor pattern
for the TyC procedural programming language. It performs type checking,
scope management, type inference, and detects all semantic errors as
specified in the TyC language specification.
"""

from functools import reduce
from typing import (
    Dict,
    List,
    Set,
    Optional,
    Any,
    Tuple,
    NamedTuple,
    Union,
    TYPE_CHECKING,
)
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode,
    Program,
    StructDecl,
    MemberDecl,
    FuncDecl,
    Param,
    VarDecl,
    IfStmt,
    WhileStmt,
    ForStmt,
    BreakStmt,
    ContinueStmt,
    ReturnStmt,
    BlockStmt,
    SwitchStmt,
    CaseStmt,
    DefaultStmt,
    Type,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    BinaryOp,
    PrefixOp,
    PostfixOp,
    AssignExpr,
    MemberAccess,
    FuncCall,
    Identifier,
    StructLiteral,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    ExprStmt,
    Expr,
    Stmt,
    Decl,
)

# Type aliases for better type hints
TyCType = Union[IntType, FloatType, StringType, VoidType, StructType]
from .static_error import (
    StaticError,
    Redeclared,
    UndeclaredIdentifier,
    UndeclaredFunction,
    UndeclaredStruct,
    TypeCannotBeInferred,
    TypeMismatchInStatement,
    TypeMismatchInExpression,
    MustInLoop,
)

class FuncSymbol:
    def __init__(self, name, param_types, return_type):
        self.name = name
        self.param_types = param_types
        self.return_type = return_type


class StructSymbol(NamedTuple):
    name: str
    members: Dict[str, TyCType]
class StaticChecker(ASTVisitor):

    def __init__(self):
        pass

    def check_program(self, node: "Program"):
        self.visit_program(node, None)

    def visit_program(self, node: Program, o=None):
        env = {
            "vars": [{}],
            "funcs": {
                "readInt": FuncSymbol("readInt", [], IntType()),
                "readFloat": FuncSymbol("readFloat", [], FloatType()),
                "readString": FuncSymbol("readString", [], StringType()),
                "printInt": FuncSymbol("printInt", [IntType()], VoidType()),
                "printFloat": FuncSymbol("printFloat", [FloatType()], VoidType()),
                "printString": FuncSymbol("printString", [StringType()], VoidType()),
            },
            "structs": {},
            "logic_vars": set(),
            "current_func": None,
            "in_loop": 0,
            "in_switch": 0
        }

        for decl in node.decls:
            if isinstance(decl, StructDecl):
                if decl.name in env["structs"]:
                    raise Redeclared("Struct", decl.name)
                self.visit(decl, env)

            elif isinstance(decl, FuncDecl):
                self.visit(decl, env)
     
            

    def visit_struct_decl(self, node: StructDecl, env):
        members = {}

        for mem in node.members:
            if mem.name in members:
                raise Redeclared("Member", mem.name)

            mem_type = self.visit(mem, env)
            members[mem.name] = mem_type

        env["structs"][node.name] = StructSymbol(node.name, members)
        
        
        
        
        
    def visit_member_decl(self, node: MemberDecl, env):
        typ = self.visit(node.member_type, env)

        if isinstance(typ, StructType):
            if typ.struct_name not in env["structs"]:
                raise UndeclaredStruct(typ.struct_name)

        return typ

    def visit_func_decl(self, node: FuncDecl, env):
        if node.name in env["funcs"]:
            raise Redeclared("Function", node.name)

        if node.return_type:
            ret_type = self.visit(node.return_type, env)
        else:
            ret_type = None

        param_types = []
        for p in node.params:
            param_types.append(self.visit(p.param_type, env))

        func = FuncSymbol(node.name, param_types, ret_type)

        env["funcs"][node.name] = func

        env["vars"].append({})
        env["params"] = set()

        old_func = env["current_func"]
        env["current_func"] = func

        for param in node.params:
            self.visit(param, env)

        if isinstance(node.body, BlockStmt):
            try:
                self.visit(node.body, env)
            except TypeMismatchInStatement as e:
                raise e
            except TypeCannotBeInferred as e:
                raise e
        else:
            for stmt in node.body:
                self.visit(stmt, env)
        
        scope = env["vars"][-1]

        if scope:
            all_none = all(typ is None for typ in scope.values())
            if all_none:
                if isinstance(node.body, BlockStmt):
                    raise TypeCannotBeInferred(node.body)
                else:
                    raise TypeCannotBeInferred(BlockStmt(node.body))
        env["vars"].pop()
        env["current_func"] = old_func

        
        
        
        

    def visit_param(self, node: Param, env):
        scope = env["vars"][-1]

        if node.name in scope:
            raise Redeclared("Parameter", node.name)

        typ = self.visit(node.param_type, env)

        if isinstance(typ, StructType):
            if typ.struct_name not in env["structs"]:
                raise UndeclaredStruct(typ.struct_name)

        scope[node.name] = typ
        env["params"].add(node.name)

    # Type system
    def visit_int_type(self, node: "IntType", o: Any = None):
        return node

    def visit_float_type(self, node: "FloatType", o: Any = None):
        return node 

    def visit_string_type(self, node: "StringType", o: Any = None):
        return node

    def visit_void_type(self, node: "VoidType", o: Any = None):
        return node

    def visit_struct_type(self, node: StructType, o=None):
        env = o
        if node.struct_name not in env["structs"]:
            raise UndeclaredStruct(node.struct_name)
        return node

    # Statements
    def visit_block_stmt(self, node: BlockStmt, o=None):
        env = o

        env["vars"].append({})

        for stmt in node.statements:
            try:
                self.visit(stmt, env)
            except (TypeCannotBeInferred, TypeMismatchInStatement, TypeMismatchInExpression) as e:
                raise e

        scope = env["vars"][-1]

        if scope:
            for stmt in node.statements:
                if isinstance(stmt, VarDecl) and stmt.init_value:
                    if isinstance(stmt.init_value, Identifier):
                        typ = self.visit(stmt.init_value, env)
                        if typ is None and isinstance(stmt.var_type, FloatType):
                            raise TypeMismatchInStatement(stmt)

            all_none = all(typ is None for typ in scope.values())
            if all_none:
                raise TypeCannotBeInferred(node)

        env["vars"].pop()

    def contains_float(self, node, env):
        if isinstance(node, FloatLiteral):
            return True

        if isinstance(node, Identifier):
            typ = self.visit(node, env)
            return isinstance(typ, FloatType)

        if isinstance(node, BinaryOp):
            return self.contains_float(node.left, env) or \
                self.contains_float(node.right, env)

        return False
    def will_be_inferred(self, name, env):
        for scope in env["vars"]:
            if name in scope and scope[name] is not None:
                return True
        return False
    def visit_var_decl(self, node: VarDecl, env):
        scope = env["vars"][-1]

        if node.name in scope:
            raise Redeclared("Variable", node.name)

        if node.name in env.get("params", set()):
            raise Redeclared("Variable", node.name)

        var_type = node.var_type
        init = node.init_value
        if init:
            init_type = self.visit(init, env)

            if var_type is None:
                var_type = init_type
        if var_type:
            var_type = self.visit(var_type, env)

            if isinstance(var_type, StructType):
                if var_type.struct_name not in env["structs"]:
                    raise UndeclaredStruct(var_type.struct_name)

        init_type = None
        if init:
            try:
                if isinstance(init, BinaryOp) and init.operator in ['&&', '||']:
                    def collect_ids(expr):
                        if isinstance(expr, Identifier):
                            env["logic_vars"].add(expr.name)
                        elif isinstance(expr, BinaryOp):
                            collect_ids(expr.left)
                            collect_ids(expr.right)

                    collect_ids(init)
                init_type = self.visit(init, env)
                if var_type is None and init_type is not None:
                    var_type = init_type
            except TypeCannotBeInferred as e:
                
                if var_type is None and isinstance(init, BinaryOp):
                    left = self.visit(init.left, env)
                    right = self.visit(init.right, env)

                    if left is None and right is None:
                        raise e

                    if left is None:
                        if isinstance(init.left, Identifier):
                            self.infer(init.left, right, env)
                        else:
                            self.infer_expr(init.left, right, env)

                    if right is None:
                        if isinstance(init.right, Identifier):
                            self.infer(init.right, left, env)
                        else:
                            self.infer_expr(init.right, left, env)

                    init_type = self.visit(init, env)
                if isinstance(init, BinaryOp) and var_type is not None:
                    left = self.visit(init.left, env)
                    right = self.visit(init.right, env)

                    if left is None and right is None:
                        raise e

                    if isinstance(var_type, FloatType):
                        if left is None and right is None:
                            raise TypeCannotBeInferred(init)

                        if left is None or right is None:
                            if self.contains_float(init, env):
                                raise TypeCannotBeInferred(init)
                            raise TypeMismatchInStatement(node)
                        else:
                            self.infer_expr(init, var_type, env)
                            init_type = self.visit(init, env)
                    elif isinstance(var_type, IntType):
                        if not self.contains_float(init, env):
                            self.infer_expr(init, var_type, env)
                            init_type = self.visit(init, env)
                        else:
                            raise e
                    else:
                        raise e
                else:
                    raise e
            if init_type is None and isinstance(init, Identifier):
                if init.name in env.get("logic_vars", set()):
                    raise TypeMismatchInStatement(node)

        if var_type is None:
            if isinstance(init, BinaryOp):
                op = init.operator

                left = self.visit(init.left, env)
                right = self.visit(init.right, env)
                if init_type is not None:
                    var_type = init_type
                else:
                    if op in ['&&', '||']:
                        if left is None:
                            self.infer(init.left, IntType(), env)
                        if right is None:
                            self.infer(init.right, IntType(), env)
                        init_type = IntType()
                    else:
                        if left is None and right is None:
                            raise TypeCannotBeInferred(init)

                        if left is None or right is None:
                            if left is None and right is None:
                                raise TypeCannotBeInferred(init)

                            unknown = init.left if left is None else init.right
                            known = init.right if left is None else init.left

                            if isinstance(known, (IntLiteral, FloatLiteral)):
                                scope[node.name] = None
                                return

                            raise TypeCannotBeInferred(init)

                        init_type = self.visit(init, env)

                var_type = init_type
                
        else:
            if init:
                if isinstance(init, StructLiteral):
                    if not isinstance(var_type, StructType):
                        raise TypeMismatchInExpression(init)

                    struct = env["structs"].get(var_type.struct_name)

                    if struct is None:
                        raise UndeclaredStruct(var_type.struct_name)

                    members = list(struct.members.values())
                    values = init.values

                    if len(values) != len(members):
                        raise TypeMismatchInExpression(init)

                    for val, mem_type in zip(values, members):
                        val_type = self.visit(val, env)

                        if val_type is None:
                            self.infer_expr(val, mem_type, env)
                            val_type = self.visit(val, env)

                        if not isinstance(val_type, type(mem_type)):
                            raise TypeMismatchInExpression(init)
                
                elif init_type is None:
                    if isinstance(init, FuncCall):
                        raise TypeMismatchInStatement(node)
                    if isinstance(init, BinaryOp):
                        if init.operator in ['<', '>', '<=', '>=', '==', '!=']:
                            left = self.visit(init.left, env)
                            right = self.visit(init.right, env)

                            if left is None and right is None:
                                raise TypeCannotBeInferred(init)

                            if left is None:
                                self.infer_expr(init.left, right, env)

                            if right is None:
                                self.infer_expr(init.right, left, env)

                            raise TypeCannotBeInferred(init)
                        left = self.visit(init.left, env)
                        right = self.visit(init.right, env)

                        if left is None and right is None:
                            raise TypeCannotBeInferred(init)

                        if left is None or right is None:
                            if self.contains_float(init, env):
                                raise TypeCannotBeInferred(init)
                            if isinstance(var_type, FloatType):
                                raise TypeCannotBeInferred(init)

                            if left is None:
                                self.infer_expr(init.left, right, env)

                            if right is None:
                                self.infer_expr(init.right, left, env)

                            init_type = self.visit(init, env)

                        self.infer_expr(init, var_type, env)
                        init_type = self.visit(init, env)
                    else:
                        
                        if isinstance(init, Identifier):
                            init_type = self.visit(init, env)

                            if init_type is None:
                                if isinstance(init, Identifier):
                                    self.infer(init, var_type, env)
                                    init_type = var_type
                                return
                elif isinstance(var_type, StructType) and isinstance(init_type, StructType):
                    if var_type.struct_name != init_type.struct_name:
                        raise TypeMismatchInStatement(node)
                elif type(var_type) != type(init_type):
                    raise TypeMismatchInStatement(node)
                

        scope[node.name] = var_type
        
    def visit_type(self, node: Type, env):
        return self.visit(node.typ, env)
    def visit_if_stmt(self, node: IfStmt, o=None):
        env = o

        cond_type = self.visit(node.condition, env)

        if cond_type is None:
            self.infer(node.condition, IntType(), env)
        elif not isinstance(cond_type, IntType):
            raise TypeMismatchInStatement(node)

        if not isinstance(node.then_stmt, BlockStmt):
            env["vars"].append({})
            self.visit(node.then_stmt, env)
            env["vars"].pop()
        else:
            self.visit(node.then_stmt, env)

        if node.else_stmt:
            if not isinstance(node.else_stmt, BlockStmt):
                env["vars"].append({})
                self.visit(node.else_stmt, env)
                env["vars"].pop()
            else:
                self.visit(node.else_stmt, env)

    def visit_while_stmt(self, node: WhileStmt, o=None):
        env = o

        cond_type = self.visit(node.condition, env)

        if cond_type is None:
            self.infer(node.condition, IntType(), env)
        elif not isinstance(cond_type, IntType):
            raise TypeMismatchInStatement(node)

        env["in_loop"] += 1

        if not isinstance(node.body, BlockStmt):
            env["vars"].append({})
            self.visit(node.body, env)
            env["vars"].pop()
        else:
            self.visit(node.body, env)

        env["in_loop"] -= 1
    def visit_for_stmt(self, node: ForStmt, o=None):
        env = o


        if node.init:
            if isinstance(node.init, VarDecl):
                self.visit(node.init, env)
            elif isinstance(node.init, ExprStmt):
                try:
                    self.visit(node.init.expr, env)
                except TypeMismatchInExpression:
                    raise TypeMismatchInStatement(node)

            else:
                self.visit(node.init, env)

        if node.condition:
            cond_type = self.visit(node.condition, env)

            if cond_type is None:
                self.infer(node.condition, IntType(), env)
            elif not isinstance(cond_type, IntType):
                raise TypeMismatchInStatement(node)

        if node.update:
            try:
                self.visit(node.update, env)
            except TypeMismatchInExpression:
                raise TypeMismatchInStatement(node)

        env["in_loop"] += 1

        if not isinstance(node.body, BlockStmt):
            env["vars"].append({})
            self.visit(node.body, env)
            env["vars"].pop()
        else:
            self.visit(node.body, env)

        env["in_loop"] -= 1

    def is_constant_expr(self, expr):
        if isinstance(expr, IntLiteral):
            return True

        if isinstance(expr, Identifier):
            return False

        if isinstance(expr, FuncCall):
            return False

        if isinstance(expr, PrefixOp):
            return self.is_constant_expr(expr.operand)

        if isinstance(expr, BinaryOp):
            return self.is_constant_expr(expr.left) and self.is_constant_expr(expr.right)

        return False
    def visit_switch_stmt(self, node: SwitchStmt, o=None):
        env = o

        expr_type = self.visit(node.expr, env)

        if expr_type is None:
            self.infer(node.expr, IntType(), env)
        elif not isinstance(expr_type, IntType):
            raise TypeMismatchInStatement(node)

        env["in_switch"] += 1

        env["vars"].append({})

        for case in node.cases:
            case_type = self.visit(case, env)

            if not self.is_constant_expr(case.expr):
                raise TypeMismatchInStatement(node)

            if case_type is None:
                raise TypeMismatchInStatement(node)
            elif not isinstance(case_type, IntType):
                raise TypeMismatchInStatement(node)
        if node.default_case:
            self.visit(node.default_case, env)
        
        
        for name, typ in env["vars"][-1].items():
            if typ is None:
                raise TypeCannotBeInferred(node)
        env["vars"].pop()
        env["in_switch"] -= 1
    def visit_case_stmt(self, node: CaseStmt, o=None):
        env = o

        case_type = self.visit(node.expr, env)

        for stmt in node.statements:
            self.visit(stmt, env)

        return case_type
    def visit_default_stmt(self, node: DefaultStmt, o=None):
        env = o

        for stmt in node.statements:
            self.visit(stmt, env)

    def visit_break_stmt(self, node: BreakStmt, o=None):
        env = o

        if env["in_loop"] == 0 and env["in_switch"] == 0:
            raise MustInLoop(node)

    def visit_continue_stmt(self, node: ContinueStmt, o=None):
        env = o

        if env["in_loop"] == 0:
            raise MustInLoop(node)
        
        
    def visit_return_stmt(self, node: ReturnStmt, o=None):
        env = o
        func = env["current_func"]

        if node.expr:
            expr_type = self.visit(node.expr, env)

            if expr_type is None:
                if isinstance(node.expr, BinaryOp):
                    raise TypeCannotBeInferred(node.expr)
                raise TypeCannotBeInferred(node)

            if func.return_type:
                if not isinstance(expr_type, type(func.return_type)):
                    raise TypeMismatchInStatement(node)
            else:
                if expr_type is None:
                    raise TypeCannotBeInferred(node)
                func.return_type = expr_type

        else:
            if func.return_type:
                if not isinstance(func.return_type, VoidType):
                    raise TypeMismatchInStatement(node)
            else:
                func.return_type = VoidType()

    def visit_expr_stmt(self, node: ExprStmt, o=None):
        env = o

        if isinstance(node.expr, BinaryOp) and node.expr.operator in ['&&', '||']:
            def collect_ids(expr):
                if isinstance(expr, Identifier):
                    env["logic_vars"].add(expr.name)
                elif isinstance(expr, BinaryOp):
                    collect_ids(expr.left)
                    collect_ids(expr.right)

            collect_ids(node.expr)

            left = self.visit(node.expr.left, env)

            try:
                right = self.visit(node.expr.right, env)
            except TypeCannotBeInferred as e:
                raise e

            if right is None and isinstance(node.expr.right, BinaryOp):
                raise TypeCannotBeInferred(node.expr.right)

            if left is not None and right is not None:
                if not isinstance(left, IntType) or not isinstance(right, IntType):
                    raise TypeMismatchInExpression(node.expr)
            return

        try:
            typ = self.visit(node.expr, env)

        except TypeMismatchInExpression as e:
            if isinstance(node.expr, AssignExpr) and not isinstance(node.expr.rhs, AssignExpr):
                raise TypeMismatchInStatement(node)
            raise e

        except TypeCannotBeInferred as e:
            raise e

        if typ is None:
            if isinstance(node.expr, BinaryOp):
                left = self.visit(node.expr.left, env)
                right = self.visit(node.expr.right, env)

                if left is None and right is None:
                    raise TypeCannotBeInferred(node.expr)

                unknown = node.expr.left if left is None else node.expr.right
                known = node.expr.right if left is None else node.expr.left

                if isinstance(known, (IntLiteral, FloatLiteral)):
                    return

                raise TypeCannotBeInferred(node.expr)

            raise TypeCannotBeInferred(node.expr)

    # Expressions
    def visit_binary_op(self, node: BinaryOp, o=None):
        env = o
        
        op = node.operator
        if op == '%':
            try:
                left = self.visit(node.left, env)
            except TypeCannotBeInferred:
                left = None

            try:
                right = self.visit(node.right, env)
            except TypeCannotBeInferred:
                right = None

            if (left is None and isinstance(node.left, BinaryOp)) or \
            (right is None and isinstance(node.right, BinaryOp)):
                raise TypeCannotBeInferred(node.left if left is None else node.right)

            if left is None:
                self.infer_expr(node.left, IntType(), env)
                left = self.visit(node.left, env)

            if right is None:
                self.infer_expr(node.right, IntType(), env)
                right = self.visit(node.right, env)

            if isinstance(left, IntType) and isinstance(right, IntType):
                return IntType()

            raise TypeMismatchInExpression(node)
        left = self.visit(node.left, env)
        right = self.visit(node.right, env)
        

        if op in ['+', '-', '*', '/']:
            if left is None and right is None:
                raise TypeCannotBeInferred(node)

            if left is None or right is None:
                if isinstance(left, FloatType) or isinstance(right, FloatType):
                    raise TypeCannotBeInferred(node)
                return None
            
            if not isinstance(left, (IntType, FloatType)) or \
            not isinstance(right, (IntType, FloatType)):
                raise TypeMismatchInExpression(node)

            if isinstance(left, FloatType) or isinstance(right, FloatType):
                return FloatType()
            return IntType()

        

        if op in ['<', '>', '<=', '>=', '==', '!=']:
            if left is None and right is None:
                return None

            if left is None and right is None:
                return None

            if left is None or right is None:
                return None

            if not isinstance(left, (IntType, FloatType)) or \
            not isinstance(right, (IntType, FloatType)):
                raise TypeMismatchInExpression(node)

            return IntType()

        if op in ['&&', '||']:
            if left is None and right is None:
                return IntType()

            if left is None:
                self.infer_expr(node.left, IntType(), env)
                left = self.visit(node.left, env)

            if right is None:
                self.infer_expr(node.right, IntType(), env)
                right = self.visit(node.right, env)

            if isinstance(left, IntType) and isinstance(right, IntType):
                return IntType()

            raise TypeMismatchInExpression(node)

           

    def visit_prefix_op(self, node: PrefixOp, o=None):
        env = o

        operand = self.visit(node.operand, env)
        op = node.operator

        if op in ['+', '-']:
            if operand is None:
                raise TypeCannotBeInferred(node)

            if isinstance(operand, (IntType, FloatType)):
                return operand

            raise TypeMismatchInExpression(node)

        if op == '!':
            if operand is None:
                self.infer(node.operand, IntType(), env)
                return IntType()

            if isinstance(operand, IntType):
                return IntType()

            raise TypeMismatchInExpression(node)

        if op in ['++', '--']:
            if not isinstance(node.operand, (Identifier, MemberAccess)):
                raise TypeMismatchInExpression(node)

            if operand is None:
                self.infer(node.operand, IntType(), env)
                return IntType()

            if isinstance(operand, IntType):
                return IntType()

            raise TypeMismatchInExpression(node)

    def visit_postfix_op(self, node: PostfixOp, o=None):
        env = o

        operand = self.visit(node.operand, env)
        op = node.operator

        if op in ['++', '--']:
            if not isinstance(node.operand, (Identifier, MemberAccess)):
                raise TypeMismatchInExpression(node)

            if operand is None:
                self.infer(node.operand, IntType(), env)
                return IntType()

            if isinstance(operand, IntType):
                return IntType()

            raise TypeMismatchInExpression(node)
        
    def infer(self, node, typ, env):
        if isinstance(node, Identifier):
            for scope in reversed(env["vars"]):
                if node.name in scope:
                    scope[node.name] = typ
                    return
    def infer_expr(self, node, typ, env):
        if isinstance(node, Identifier):
            self.infer(node, typ, env)

        elif isinstance(node, BinaryOp):
            if node.operator in ['+', '-', '*', '/']:
                self.infer_expr(node.left, typ, env)
                self.infer_expr(node.right, typ, env)

        elif isinstance(node, PrefixOp):
            if node.operator in ['+', '-', '++', '--']:
                self.infer_expr(node.operand, typ, env)
            elif node.operator == '!':
                self.infer_expr(node.operand, IntType(), env)

        elif isinstance(node, AssignExpr):
            self.infer_expr(node.lhs, typ, env)
            self.infer_expr(node.rhs, typ, env)
            
    def visit_assign_expr(self, node: AssignExpr, o=None):
        env = o

        try:
            lhs_type = self.visit(node.lhs, env)
        except TypeCannotBeInferred as e:
            raise e

        try:
            rhs_type = self.visit(node.rhs, env)
        except TypeCannotBeInferred as e:
            raise e

        if lhs_type is None and rhs_type is None:
            if isinstance(node.rhs, AssignExpr):
                raise TypeCannotBeInferred(node.rhs)

            if isinstance(node.rhs, BinaryOp):
                left = self.visit(node.rhs.left, env)
                right = self.visit(node.rhs.right, env)

                if left is None and right is None:
                    raise TypeCannotBeInferred(node.rhs)

                if left is not None and right is not None:
                    rhs_type = FloatType() if isinstance(left, FloatType) or isinstance(right, FloatType) else IntType()

            return None

        if lhs_type is None:
            if rhs_type is None:
                return None

            self.infer(node.lhs, rhs_type, env)
            lhs_type = rhs_type
        if rhs_type is None:
            if isinstance(node.rhs, BinaryOp):
                left = self.visit(node.rhs.left, env)
                right = self.visit(node.rhs.right, env)

                if left is not None and right is not None:
                    rhs_type = FloatType() if isinstance(left, FloatType) or isinstance(right, FloatType) else IntType()
                else:
                    return None
            else:
                self.infer_expr(node.rhs, lhs_type, env)
                rhs_type = self.visit(node.rhs, env)
            self.infer_expr(node.rhs, lhs_type, env)
            rhs_type = self.visit(node.rhs, env)
            if isinstance(node.rhs, BinaryOp) and rhs_type is None:
                left = self.visit(node.rhs.left, env)
                right = self.visit(node.rhs.right, env)

                if left is not None and right is not None:
                    rhs_type = FloatType() if isinstance(left, FloatType) or isinstance(right, FloatType) else IntType()

        if lhs_type is None and rhs_type is None:
            
            raise TypeCannotBeInferred(node)

        if type(lhs_type) != type(rhs_type):
            raise TypeMismatchInExpression(node)

        if isinstance(node.lhs, Identifier):
            if node.lhs.name in env.get("logic_vars", set()):
                if isinstance(rhs_type, FloatType):
                    raise TypeMismatchInExpression(node)

        return lhs_type

    def visit_member_access(self, node: MemberAccess, o=None):
        env = o

        obj_type = self.visit(node.obj, env)

        if not isinstance(obj_type, StructType):
            raise TypeMismatchInExpression(node)

        struct = env["structs"].get(obj_type.struct_name)

        if struct is None:
            raise UndeclaredStruct(obj_type.struct_name)

        if node.member not in struct.members:
            raise TypeMismatchInExpression(node)

        return struct.members[node.member]

    def visit_func_call(self, node: FuncCall, o=None):
        env = o

        if node.name not in env["funcs"]:
            raise UndeclaredFunction(node.name)

        func = env["funcs"][node.name]

        if len(node.args) != len(func.param_types):
            raise TypeMismatchInExpression(node)

        for arg, param_type in zip(node.args, func.param_types):
            arg_type = self.visit(arg, env)

            if arg_type is None:
                if isinstance(arg, BinaryOp):
                    raise TypeCannotBeInferred(arg)
                self.infer(arg, param_type, env)
                continue

            if isinstance(param_type, StructType) and isinstance(arg_type, StructType):
                if param_type.struct_name != arg_type.struct_name:
                    raise TypeMismatchInExpression(node)
            elif not isinstance(arg_type, type(param_type)):
                raise TypeMismatchInExpression(node)

        if func.return_type is None:
            if env["current_func"] is not None and node.name == env["current_func"].name:
                raise TypeCannotBeInferred(node)
            return None

        return func.return_type

    def visit_identifier(self, node: Identifier, o=None):
        env = o

        for scope in reversed(env["vars"]):
            if node.name in scope:
                typ = scope[node.name]
                if typ is None:
                    return None
                return typ

        raise UndeclaredIdentifier(node.name)

    def visit_struct_literal(self, node: StructLiteral, o=None):
        env = o

        for val in node.values:
            self.visit(val, env)

        return StructType("__anonymous__")

    # Literals
    def visit_int_literal(self, node: IntLiteral, o=None):
        return IntType()
    
    def visit_float_literal(self, node: "FloatLiteral", o: Any = None):
        return FloatType()

    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        return StringType()