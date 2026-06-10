"""
Code generator for TyC.
"""

from typing import Any

from ..utils.nodes import *
from ..utils.visitor import BaseVisitor
from .emitter import *
from .frame import *
from .io import IO_SYMBOL_LIST
from .utils import *
from functools import *

class StringArrayType:
    """Marker type for JVM main(String[] args)."""
    pass


class CodeGenerator(BaseVisitor):
    """Minimal AST -> Jasmin code generator."""

    def __init__(self):
        self.emit = None
        self.functions = {}
        self.current_return_type = VoidType()
        self.class_name = "TyC"
        self.loop_stack = []
        self.structs = {}

    def _lookup_symbol(self, name: str, sym_list: list[Symbol]) -> Symbol:
        for sym in reversed(sym_list):
            if sym.name == name:
                return sym
        raise RuntimeError(f"Undeclared symbol: {name}")

    def _infer_type(self, node: Expr, o: Access):
        if isinstance(node, IntLiteral):
            return IntType()
        if isinstance(node, FloatLiteral):
            return FloatType()
        if isinstance(node, StringLiteral):
            return StringType()
        if isinstance(node, Identifier):
            return self._lookup_symbol(node.name, o.sym).type
        if isinstance(node, AssignExpr):
            return self._infer_type(node.rhs, o)
        if isinstance(node, FuncCall):
            return self.functions[node.name].type.return_type
        if isinstance(node, BinaryOp):
            if node.operator in ["+", "-", "*", "/", "%"]:
                left_type = self._infer_type(node.left, o)
                right_type = self._infer_type(node.right, o)
                if is_float_type(left_type) or is_float_type(right_type):
                    return FloatType()
                return IntType()
            if node.operator in ["<", "<=", ">", ">=", "==", "!="]:
                return IntType()
        return IntType()

    def visit_program(self, node: Program, o: Any = None):
        self.emit = Emitter(f"{self.class_name}.j")
        self.emit.print_out(self.emit.emit_prolog(self.class_name))

        for io_sym in IO_SYMBOL_LIST:
            self.functions[io_sym.name] = io_sym

        for decl in node.decls:
            if isinstance(decl, StructDecl):
                self.visit(decl, None)

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                return_type = decl.return_type if decl.return_type else self._infer_func_return(decl)
                param_types = [p.param_type for p in decl.params]
                self.functions[decl.name] = Symbol(
                    decl.name, FunctionType(param_types, return_type), CName(self.class_name)
                )

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                self.visit(decl, None)

        self.emit.emit_epilog()
    def _infer_func_return(self, node: FuncDecl):
        param_syms = [
            Symbol(p.name, p.param_type, None)
            for p in node.params
        ]

        def find_return(stmt):
            if isinstance(stmt, ReturnStmt):
                if stmt.expr:
                    return self._infer_type(
                        stmt.expr,
                        Access(Frame("tmp", VoidType()), param_syms)
                    )
                return VoidType()

            if isinstance(stmt, BlockStmt):
                for s in stmt.statements:
                    t = find_return(s)
                    if t:
                        return t

            if isinstance(stmt, IfStmt):
                t1 = find_return(stmt.then_stmt)
                t2 = find_return(stmt.else_stmt) if stmt.else_stmt else None
                return t1 or t2

            return None

        body = node.body if isinstance(node.body, BlockStmt) else BlockStmt(node.body)
        t = find_return(body)
        return t if t else VoidType()
    def visit_func_decl(self, node: FuncDecl, o: Any = None):
        if node.return_type:
            self.current_return_type = node.return_type
        else:
            self.current_return_type = self._infer_func_return(node)
        frame = Frame(node.name, self.current_return_type)
        frame.enter_scope(True)

        if node.name == "main":
            mtype = FunctionType([StringArrayType()], VoidType())
        else:
            mtype = FunctionType([p.param_type for p in node.params], self.current_return_type)

        self.emit.print_out(self.emit.emit_method(node.name, mtype, True))

        start_label = frame.get_start_label()
        end_label = frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))

        local_syms: list[Symbol] = []
        if node.name == "main":
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", StringArrayType(), start_label, end_label
                )
            )

        for param in node.params:
            idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(idx, param.name, param.param_type, start_label, end_label)
            )
            local_syms.append(Symbol(param.name, param.param_type, Index(idx)))

        sub_body = SubBody(frame, local_syms)
        if isinstance(node.body, BlockStmt):
            sub_body = self.visit(node.body, sub_body)
        else:
            for stmt in node.body:
                sub_body = self.visit(stmt, sub_body)

        if is_void_type(self.current_return_type):
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))

        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_scope()
        self.emit.print_out(self.emit.emit_end_method(frame))

    def visit_block_stmt(self, node: BlockStmt, o: SubBody = None):
        frame = o.frame

        frame.enter_scope(False)

        start = frame.get_start_label()
        end = frame.get_end_label()

        self.emit.print_out(self.emit.emit_label(start, frame))

        base_len = len(o.sym)

        sub = SubBody(frame, o.sym.copy())

        for stmt in node.statements:
            sub = self.visit(stmt, sub)

        self.emit.print_out(self.emit.emit_label(end, frame))

        frame.exit_scope()

        sub.sym = sub.sym[:base_len]

        return sub
    def _is_terminal(self, stmt):
        if isinstance(stmt, ReturnStmt):
            return True
        if isinstance(stmt, BlockStmt):
            return any(self._is_terminal(s) for s in stmt.statements)
        if isinstance(stmt, IfStmt):
            if stmt.else_stmt:
                return self._is_terminal(stmt.then_stmt) and self._is_terminal(stmt.else_stmt)
        return False
    def _init_struct(self, struct_type, frame):
        code = ""
        code += self.emit.emit_new_instance(struct_type.struct_name, frame)
        members = self.structs[struct_type.struct_name]
        for mem in members:
            field_name = f"{struct_type.struct_name}/{mem.name}"
            code += self.emit.emit_dup(frame)
            if isinstance(mem.member_type, IntType):
                code += self.emit.emit_push_iconst(0, frame)
            elif isinstance(mem.member_type, FloatType):
                code += self.emit.emit_push_fconst("0.0", frame)
            elif isinstance(mem.member_type, StringType):
                code += self.emit.emit_push_const("", StringType(), frame)
            elif is_struct_type(mem.member_type):
                code += self._init_struct(mem.member_type, frame)
            code += self.emit.emit_put_field(field_name, mem.member_type, frame)
        return code
    def visit_var_decl(self, node, o):
        frame = o.frame
        sym = o.sym
        emit = self.emit

        var_name = node.name
        var_type = node.var_type

        if var_type is None:
            if node.init_value:
                var_type = self._infer_type(node.init_value, Access(frame, o.sym))
            else:
                var_type = IntType()

        index = frame.get_new_index()

        start = frame.get_start_label()
        end = frame.get_end_label()

        emit.print_out(
            emit.emit_var(
                index,
                var_name,
                var_type,
                start,
                end
            )
        )

        sym.append(Symbol(var_name, var_type, Index(index)))

        if node.init_value:
            acc = Access(frame, sym)
            acc.expected_type = var_type

            code, typ = self.visit(node.init_value, acc)

            if is_struct_type(var_type):
                code += self._clone_struct(var_type, frame)

            emit.print_out(code)
            emit.print_out(
                emit.emit_write_var(var_name, var_type, index, frame)
            )

            return o

        if is_struct_type(var_type):
            code = self._init_struct(var_type, frame)
            emit.print_out(code)
            emit.print_out(emit.emit_write_var(var_name, var_type, index, frame))
        else:
            if isinstance(var_type, IntType):
                emit.print_out(emit.emit_push_iconst(0, frame))
                emit.print_out(emit.emit_write_var(var_name, var_type, index, frame))

            elif isinstance(var_type, FloatType):
                emit.print_out(emit.emit_push_fconst("0.0", frame))
                emit.print_out(emit.emit_write_var(var_name, var_type, index, frame))

            elif isinstance(var_type, StringType):
                emit.print_out(emit.emit_push_const("", StringType(), frame))
                emit.print_out(emit.emit_write_var(var_name, var_type, index, frame))

        return o
    def visit_expr_stmt(self, node: ExprStmt, o: SubBody = None):
        code, expr_type = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        if not is_void_type(expr_type) and not isinstance(node.expr, FuncCall):
            self.emit.print_out(self.emit.emit_pop(o.frame))
        return o

    def visit_if_stmt(self, node: IfStmt, o: SubBody = None):
        frame = o.frame

        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        else_label = frame.get_new_label()
        end_label = frame.get_new_label()

        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(else_label, frame))
        self.visit(node.then_stmt, o)
        if not self._is_terminal(node.then_stmt):
            self.emit.print_out(self.emit.emit_goto(end_label, frame))
        self.emit.print_out(self.emit.emit_label(else_label, frame))
        if node.else_stmt:
            self.visit(node.else_stmt, o)
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_while_stmt(self, node: WhileStmt, o: SubBody = None):
        frame = o.frame
        start_label = frame.get_new_label()
        end_label = frame.get_new_label()

        self.loop_stack.append((start_label, end_label))

        self.emit.print_out(self.emit.emit_label(start_label, frame))

        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(end_label, frame))

        self.visit(node.body, o)

        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))

        self.loop_stack.pop()

        return o

    def visit_return_stmt(self, node: ReturnStmt, o: SubBody = None):
        if node.expr is None:
            self.emit.print_out(self.emit.emit_return(VoidType(), o.frame))
            return o
        code, ret_type = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        self.emit.print_out(self.emit.emit_return(ret_type, o.frame))
        return o

    def visit_binary_op(self, node: BinaryOp, o: Access = None):
        left_code, left_type = self.visit(node.left, o)
        right_code, right_type = self.visit(node.right, o)
        frame = o.frame

        if node.operator in ["+", "-"]:
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            if is_float_type(result_type):
                if is_int_type(left_type):
                    left_code += self.emit.emit_i2f(frame)
                if is_int_type(right_type):
                    right_code += self.emit.emit_i2f(frame)
            return (
                left_code
                + right_code
                + self.emit.emit_add_op(node.operator, result_type, frame),
                result_type,
            )
        if node.operator in ["*", "/"]:
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            if is_float_type(result_type):
                if is_int_type(left_type):
                    left_code += self.emit.emit_i2f(frame)
                if is_int_type(right_type):
                    right_code += self.emit.emit_i2f(frame)
            return (
                left_code
                + right_code
                + self.emit.emit_mul_op(node.operator, result_type, frame),
                result_type,
            )
        if node.operator == "%":
            return left_code + right_code + self.emit.emit_mod(frame), IntType()
        if node.operator in ["<", "<=", ">", ">=", "==", "!="]:
            op_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()

            if is_float_type(op_type):
                if is_int_type(left_type):
                    left_code += self.emit.emit_i2f(frame)
                if is_int_type(right_type):
                    right_code += self.emit.emit_i2f(frame)

            return (
                left_code
                + right_code
                + self.emit.emit_re_op(node.operator, op_type, frame),
                IntType(),
            )
        if node.operator == "&&":
            frame = o.frame

            label_false = frame.get_new_label()
            label_end = frame.get_new_label()

            code = left_code
            code += self.emit.emit_if_false(label_false, frame)

            code += right_code
            code += self.emit.emit_if_false(label_false, frame)

            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_goto(label_end, frame)

            code += self.emit.emit_label(label_false, frame)
            code += self.emit.emit_push_iconst(0, frame)

            code += self.emit.emit_label(label_end, frame)

            return code, IntType()
        if node.operator == "||":
            frame = o.frame

            label_true = frame.get_new_label()
            label_end = frame.get_new_label()

            code = left_code
            code += self.emit.emit_if_true(label_true, frame)

            code += right_code
            code += self.emit.emit_if_true(label_true, frame)

            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_goto(label_end, frame)

            code += self.emit.emit_label(label_true, frame)
            code += self.emit.emit_push_iconst(1, frame)

            code += self.emit.emit_label(label_end, frame)

            return code, IntType()
        raise RuntimeError(f"Unsupported operator: {node.operator}")

    
    
    def _clone_struct(self, struct_type, frame):
        temp_idx = frame.get_new_index()

        code = ""

        # save source struct ref
        code += self.emit.emit_write_var(
            "__clone_src",
            struct_type,
            temp_idx,
            frame
        )

        # create destination struct
        code += self._init_struct(struct_type, frame)

        members = self.structs[struct_type.struct_name]

        for mem in members:
            field_name = f"{struct_type.struct_name}/{mem.name}"

            # duplicate destination object
            code += self.emit.emit_dup(frame)

            # load source object
            code += self.emit.emit_read_var(
                "__clone_src",
                struct_type,
                temp_idx,
                frame
            )

            # get source field
            code += self.emit.emit_get_field(
                field_name,
                mem.member_type,
                frame
            )

            # deep copy nested struct
            if is_struct_type(mem.member_type):
                code += self._clone_struct(mem.member_type, frame)

            # store field
            code += self.emit.emit_put_field(
                field_name,
                mem.member_type,
                frame
            )

        return code
    
    
    
    
    
    
    
    def visit_assign_expr(self, node: AssignExpr, o: Access = None):
        frame = o.frame

        if isinstance(node.lhs, Identifier):
            lhs_sym = self._lookup_symbol(node.lhs.name, o.sym)
            idx = lhs_sym.value.value
            lhs_type = lhs_sym.type

            acc = Access(frame, o.sym)
            acc.expected_type = lhs_type

            rhs_code, rhs_type = self.visit(node.rhs, acc)

            if lhs_sym.type is None or isinstance(lhs_sym.type, IntType):
                lhs_sym.type = rhs_type

            if is_struct_type(lhs_sym.type):
                temp_idx = frame.get_new_index()

                code = rhs_code
                code += self.emit.emit_dup(frame)
                code += self.emit.emit_write_var("__tmp_struct", rhs_type, temp_idx, frame)

                code += self._init_struct(rhs_type, frame)

                members = self.structs[rhs_type.struct_name]

                for mem in members:
                    field_name = f"{rhs_type.struct_name}/{mem.name}"

                    code += self.emit.emit_dup(frame)

                    code += self.emit.emit_read_var("__tmp_struct", rhs_type, temp_idx, frame)
                    code += self.emit.emit_get_field(field_name, mem.member_type, frame)

                    if is_struct_type(mem.member_type):
                        # recursively clone nested struct
                        code += self._clone_struct(mem.member_type, frame)

                    code += self.emit.emit_put_field(field_name, mem.member_type, frame)

                code += self.emit.emit_dup(frame)
                code += self.emit.emit_write_var(node.lhs.name, lhs_sym.type, idx, frame)

                return code, rhs_type

            code = rhs_code
            code += self.emit.emit_dup(frame)
            code += self.emit.emit_write_var(node.lhs.name, lhs_sym.type, idx, frame)

            return code, rhs_type

        elif isinstance(node.lhs, MemberAccess):
            obj_code, obj_type = self.visit(node.lhs.obj, o)

            members = self.structs[obj_type.struct_name]
            field = next(m for m in members if m.name == node.lhs.member)
            field_type = field.member_type

            acc = Access(frame, o.sym)
            acc.expected_type = field_type

            rhs_code, rhs_type = self.visit(node.rhs, acc)

            field_name = f"{obj_type.struct_name}/{node.lhs.member}"

            code = obj_code
            code += self.emit.emit_dup(frame)
            code += rhs_code
            code += self.emit.emit_dup_x1(frame)
            code += self.emit.emit_put_field(field_name, rhs_type, frame)

            return code, rhs_type

        else:
            raise RuntimeError("Unsupported assignment target")

    def visit_func_call(self, node: FuncCall, o: Access = None):
        frame = o.frame
        fn_sym = self.functions[node.name]
        fn_type = fn_sym.type

        code = ""

        for arg, param_type in zip(node.args, fn_type.param_types):
            arg_access = Access(frame, o.sym)

            before = frame.get_stack_size()

            arg_code, arg_type = self.visit(arg, arg_access)
            if is_struct_type(arg_type):
                arg_code += self._clone_struct(arg_type, frame)
        
            after = frame.get_stack_size()
            if after == before:
                if is_int_type(param_type):
                    arg_code += self.emit.emit_push_iconst(0, frame)
                elif is_float_type(param_type):
                    arg_code += self.emit.emit_push_fconst("0.0", frame)
                elif is_string_type(param_type):
                    arg_code += self.emit.emit_push_const("", StringType(), frame)

            if is_int_type(arg_type) and is_float_type(param_type):
                arg_code += self.emit.emit_i2f(frame)

            code += arg_code

        code += self.emit.emit_invoke_static(
            f"{fn_sym.value.value}/{node.name}", fn_type, frame
        )

        return code, fn_type.return_type

    def visit_identifier(self, node: Identifier, o: Access = None):
        sym = self._lookup_symbol(node.name, o.sym)
        typ = sym.type
        frame = o.frame

        if isinstance(sym.value, Index):
            idx = sym.value.value

            if typ is None:
                return self.emit.emit_push_iconst(0, frame), IntType()

            return self.emit.emit_read_var(node.name, typ, idx, frame), typ

    def visit_int_literal(self, node: IntLiteral, o: Access = None):
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: FloatLiteral, o: Access = None):
        return self.emit.emit_push_fconst(str(node.value), o.frame), FloatType()

    def visit_string_literal(self, node: StringLiteral, o: Access = None):
        return self.emit.emit_push_const(node.value, StringType(), o.frame), StringType()

    def visit_struct_decl(self, node: StructDecl, o: Any = None):
        self.structs[node.name] = node.members
        emitter = Emitter(f"{node.name}.j")

        emitter.print_out(emitter.emit_prolog(node.name))

        for mem in node.members:
            field_type = emitter.get_jvm_type(mem.member_type)
            emitter.print_out(f".field public {mem.name} {field_type}\n")

        emitter.print_out(".method public <init>()V\n")
        emitter.print_out("\taload_0\n")
        emitter.print_out("\tinvokespecial java/lang/Object/<init>()V\n")
        emitter.print_out("\treturn\n")
        emitter.print_out(".end method\n")

        emitter.emit_epilog()
    def visit_member_decl(self, node: MemberDecl, o: Any = None):
        return None

    def visit_param(self, node: Param, o: Any = None):
        return None

    def visit_int_type(self, node: IntType, o: Any = None):
        return node

    def visit_float_type(self, node: FloatType, o: Any = None):
        return node

    def visit_string_type(self, node: StringType, o: Any = None):
        return node

    def visit_void_type(self, node: VoidType, o: Any = None):
        return node

    def visit_struct_type(self, node: StructType, o: Any = None):
        return node

    def visit_for_stmt(self, node: ForStmt, o: SubBody):
        frame = o.frame
        if node.init:
            o = self.visit(node.init, o)
        start_label = frame.get_new_label()
        update_label = frame.get_new_label()
        end_label = frame.get_new_label()
        self.loop_stack.append((update_label, end_label))
        self.emit.print_out(self.emit.emit_label(start_label, frame))
        if node.condition:
            cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
            self.emit.print_out(cond_code)
            self.emit.print_out(self.emit.emit_if_false(end_label, frame))
        self.visit(node.body, o)
        self.emit.print_out(self.emit.emit_label(update_label, frame))
        if node.update:
            update_code, _ = self.visit(node.update, Access(frame, o.sym))
            self.emit.print_out(update_code)
            self.emit.print_out(self.emit.emit_pop(frame))
        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        self.loop_stack.pop()
        return o
    
    
    
    def visit_switch_stmt(self, node: SwitchStmt, o: SubBody):
        frame = o.frame
        start = frame.get_new_label()
        end = frame.get_new_label()
        self.emit.print_out(self.emit.emit_label(start, frame))
        base_len = len(o.sym)
        sub = SubBody(frame, o.sym.copy())
        if self.loop_stack:
            continue_label, _ = self.loop_stack[-1]
        else:
            continue_label = None
        self.loop_stack.append((continue_label, end))
        expr_code, _ = self.visit(node.expr, Access(frame, sub.sym))
        case_labels = [frame.get_new_label() for _ in node.cases]
        default_label = frame.get_new_label()
        for i, case in enumerate(node.cases):
            self.emit.print_out(expr_code)
            case_code, _ = self.visit(case.expr, Access(frame, sub.sym))
            self.emit.print_out(case_code)
            self.emit.print_out(self.emit.emit_re_op("==", IntType(), frame))
            self.emit.print_out(self.emit.emit_if_true(case_labels[i], frame))
        self.emit.print_out(self.emit.emit_goto(default_label, frame))
        for i, case in enumerate(node.cases):
            self.emit.print_out(self.emit.emit_label(case_labels[i], frame))
            for stmt in case.statements:
                self.visit(stmt, sub)
        self.emit.print_out(self.emit.emit_label(default_label, frame))
        if node.default_case:
            for stmt in node.default_case.statements:
                self.visit(stmt, sub)
        self.emit.print_out(self.emit.emit_label(end, frame))
        self.loop_stack.pop()
        sub.sym = sub.sym[:base_len]
        return o
    
    
    
    def visit_case_stmt(self, node: CaseStmt, o: Any = None):
        raise RuntimeError("CaseStmt not supported in minimal codegen")

    def visit_default_stmt(self, node: DefaultStmt, o: Any = None):
        raise RuntimeError("DefaultStmt not supported in minimal codegen")

    def visit_break_stmt(self, node, o):
        _, end_label = self.loop_stack[-1]
        self.emit.print_out(self.emit.emit_goto(end_label, o.frame))
        return o

    def visit_continue_stmt(self, node, o):
        start_label, _ = self.loop_stack[-1]
        self.emit.print_out(self.emit.emit_goto(start_label, o.frame))
        return o

    def visit_prefix_op(self, node: PrefixOp, o: Access = None):
        frame = o.frame

        expr_code, expr_type = self.visit(node.operand, o)
        if node.operator == "+":
            return expr_code, expr_type
        if node.operator == "!":
            label_true = frame.get_new_label()
            label_end = frame.get_new_label()

            code = expr_code
            code += self.emit.emit_if_false(label_true, frame)

            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_goto(label_end, frame)

            code += self.emit.emit_label(label_true, frame)
            code += self.emit.emit_push_iconst(1, frame)

            code += self.emit.emit_label(label_end, frame)

            return code, IntType()

        if node.operator == "-":
            return expr_code + self.emit.emit_neg_op(expr_type, frame), expr_type
        if node.operator in ["++", "--"]:
            if not isinstance(node.operand, Identifier):
                raise RuntimeError("++/-- only supports identifier")

            sym = self._lookup_symbol(node.operand.name, o.sym)
            idx = sym.value.value
            var_type = sym.type

            code = self.emit.emit_read_var(node.operand.name, var_type, idx, frame)

            code += self.emit.emit_push_iconst(1, frame)

            if node.operator == "++":
                code += self.emit.emit_add_op("+", var_type, frame)
            else:
                code += self.emit.emit_add_op("-", var_type, frame)

            code += self.emit.emit_dup(frame)

            code += self.emit.emit_write_var(node.operand.name, var_type, idx, frame)

            return code, var_type
        raise RuntimeError(f"Unsupported prefix operator: {node.operator}")

    def visit_postfix_op(self, node: PostfixOp, o: Access = None):
        frame = o.frame

        if not isinstance(node.operand, Identifier):
            raise RuntimeError("postfix only supports identifier")

        sym = self._lookup_symbol(node.operand.name, o.sym)
        idx = sym.value.value
        var_type = sym.type

        code = self.emit.emit_read_var(node.operand.name, var_type, idx, frame)

        code += self.emit.emit_dup(frame)

        code += self.emit.emit_push_iconst(1, frame)

        if node.operator == "++":
            code += self.emit.emit_add_op("+", var_type, frame)
        else:
            code += self.emit.emit_add_op("-", var_type, frame)

        code += self.emit.emit_write_var(node.operand.name, var_type, idx, frame)

        return code, var_type

    def visit_member_access(self, node: MemberAccess, o: Access = None):
        frame = o.frame

        obj_code, obj_type = self.visit(node.obj, o)

        members = self.structs[obj_type.struct_name]

        field = next(m for m in members if m.name == node.member)

        field_type = field.member_type

        field_name = f"{obj_type.struct_name}/{node.member}"

        code = obj_code + self.emit.emit_get_field(field_name, field_type, frame)

        return code, field_type

    def visit_struct_literal(self, node: StructLiteral, o: Access = None):
        frame = o.frame

        struct_type = o.expected_type

        members = self.structs[struct_type.struct_name]

        code = ""

        code += self.emit.emit_new_instance(struct_type.struct_name, frame)

        for i, value in enumerate(node.values):
            field_name = struct_type.struct_name + "/" + members[i].name

            code += self.emit.emit_dup(frame)

            val_code, val_type = self.visit(value, o)
            code += val_code

            code += self.emit.emit_put_field(field_name, val_type, frame)

        return code, struct_type
