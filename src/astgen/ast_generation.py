"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""
#haiya so hard this assignment
from functools import reduce
from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser # type: ignore
from src.utils.nodes import *

class ASTGeneration(TyCVisitor):

    # Visit a parse tree produced by TyCParser#literal.
   def visitLiteral(self, ctx: TyCParser.LiteralContext):
      if ctx.INT_LITERAL():
         return IntLiteral(int(ctx.INT_LITERAL().getText()))
      if ctx.FLOAT_LITERAL():
         return FloatLiteral(float(ctx.FLOAT_LITERAL().getText()))
      if ctx.STRING_LITERAL():
         return StringLiteral(ctx.STRING_LITERAL().getText())


    # Visit a parse tree produced by TyCParser#expression.
   def visitPrimary_expression(self, ctx: TyCParser.Primary_expressionContext):
      if ctx.literal():
         return self.visit(ctx.literal())

      if ctx.ID():
         return Identifier(ctx.ID().getText())

      if ctx.expression():
         return self.visit(ctx.expression())

      if ctx.function_call():
         return self.visit(ctx.function_call())

      if ctx.struct_init():
         return self.visit(ctx.struct_init())


    # Visit a parse tree produced by TyCParser#assignment_expression.
   def visitAssignment_expression(self, ctx):
      if ctx.ASS():
         lhs = self.visit(ctx.assign_lhs())
         rhs = self.visit(ctx.assignment_expression())
         return AssignExpr(lhs, rhs)

      return self.visit(ctx.logical_or_expression())


    # Visit a parse tree produced by TyCParser#logical_or_expression.
   def visitLogical_or_expression(self, ctx):
      expr = self.visit(ctx.logical_and_expression(0))

      for i in range(1, len(ctx.logical_and_expression())):
         right = self.visit(ctx.logical_and_expression(i))
         expr = BinaryOp(expr, "||", right)

      return expr


    # Visit a parse tree produced by TyCParser#logical_and_expression.
   def visitLogical_and_expression(self, ctx):
      expr = self.visit(ctx.equality_expression(0))

      for i in range(1, len(ctx.equality_expression())):
         right = self.visit(ctx.equality_expression(i))
         expr = BinaryOp(expr, "&&", right)

      return expr


    # Visit a parse tree produced by TyCParser#equality_expression.
   def visitEquality_expression(self, ctx):
      expr = self.visit(ctx.relational_expression(0))

      for i in range(1, len(ctx.relational_expression())):
         op = ctx.getChild(2*i - 1).getText()
         right = self.visit(ctx.relational_expression(i))
         expr = BinaryOp(expr, op, right)

      return expr


    # Visit a parse tree produced by TyCParser#relational_expression.
   def visitRelational_expression(self, ctx):
      exprs = list(map(self.visit, ctx.additive_expression()))
      ops = [ctx.getChild(2*i - 1).getText() for i in range(1, len(exprs))]
      return reduce(lambda acc, t: BinaryOp(acc, t[0], t[1]), zip(ops, exprs[1:]), exprs[0])



    # Visit a parse tree produced by TyCParser#additive_expression.
   def visitAdditive_expression(self, ctx):
      exprs = list(map(self.visit, ctx.multiplicative_expression()))
      ops = [ctx.getChild(2*i - 1).getText() for i in range(1, len(exprs))]
      return reduce(lambda acc, t: BinaryOp(acc, t[0], t[1]), zip(ops, exprs[1:]), exprs[0])


    # Visit a parse tree produced by TyCParser#multiplicative_expression.
   def visitMultiplicative_expression(self, ctx):
      exprs = list(map(self.visit, ctx.unary_expression()))
      ops = [ctx.getChild(2*i - 1).getText() for i in range(1, len(exprs))]
      return reduce(lambda acc, t: BinaryOp(acc, t[0], t[1]), zip(ops, exprs[1:]), exprs[0])


    # Visit a parse tree produced by TyCParser#unary_expression.
   def visitUnary_expression(self, ctx):
      if ctx.getChildCount() == 2:
         op = ctx.getChild(0).getText()
         operand = self.visit(ctx.unary_expression())
         return PrefixOp(op, operand)
      return self.visit(ctx.incdec_expression())


    # Visit a parse tree produced by TyCParser#non_prefix_unary.
   def visitNon_prefix_unary(self, ctx: TyCParser.Non_prefix_unaryContext):
      return self.visit(ctx.incdec_expression())


    # Visit a parse tree produced by TyCParser#prefix_incdec.
   def visitPrefix_incdec(self, ctx: TyCParser.Prefix_incdecContext):
      op = ctx.getChild(0).getText()
      operand = self.visit(ctx.non_prefix_unary())
      return PrefixOp(op, operand)


    # Visit a parse tree produced by TyCParser#incdec_expression.
   def visitIncdec_expression(self, ctx: TyCParser.Incdec_expressionContext):

      if ctx.prefix_incdec():
         expr = self.visit(ctx.prefix_incdec())

         if ctx.postfix_tail():
               ops = self.visit(ctx.postfix_tail())
               expr = reduce(lambda acc, op: PostfixOp(op, acc), ops, expr)

         return expr

      return self.visit(ctx.postfix_expression())


    # Visit a parse tree produced by TyCParser#postfix_tail.
   def visitPostfix_tail(self, ctx: TyCParser.Postfix_tailContext):
      return list(map(lambda child: child.getText(), ctx.getChildren()))


    # Visit a parse tree produced by TyCParser#postfix_expression.
   def visitPostfix_expression(self, ctx):
      expr = self.visit(ctx.primary_postfix())

      member_parts = list(map(lambda p: lambda e: MemberAccess(e, p.ID().getText()), ctx.member_part()))
      incdec_parts = list(map(lambda p: lambda e: PostfixOp(p.getText(), e), ctx.incdec_part()))

      return reduce(lambda acc, f: f(acc), member_parts + incdec_parts, expr)

    # Visit a parse tree produced by TyCParser#member_part.
   def visitMember_part(self, ctx):
      return ctx.ID().getText()


    # Visit a parse tree produced by TyCParser#incdec_part.
   def visitIncdec_part(self, ctx):
      return ctx.getChild(0).getText()


    # Visit a parse tree produced by TyCParser#primary_postfix.
   def visitPrimary_postfix(self, ctx):

      if ctx.function_call():
         return self.visit(ctx.function_call())

      if ctx.ID():
         return Identifier(ctx.ID().getText())

      if ctx.literal():
         return self.visit(ctx.literal())

      if ctx.struct_init():
         return self.visit(ctx.struct_init())

      if ctx.expression():
         return self.visit(ctx.expression())


    # Visit a parse tree produced by TyCParser#non_call_primary.
   def visitNon_call_primary(self, ctx):

      if ctx.ID():
         return Identifier(ctx.ID().getText())

      if ctx.literal():
         return self.visit(ctx.literal())

      if ctx.struct_init():
         return self.visit(ctx.struct_init())

      if ctx.expression():
         return self.visit(ctx.expression())


    # Visit a parse tree produced by TyCParser#lvalue.
   def visitLvalue(self, ctx):
      ids = ctx.ID()      
      expr = Identifier(ids[0].getText())
      for i in range(1, len(ids)):
         expr = MemberAccess(expr, ids[i].getText())
      return expr


    # Visit a parse tree produced by TyCParser#function_call.
   def visitFunction_call(self, ctx):
      name = ctx.ID().getText()

      args = []
      if ctx.argument_list():
         args = self.visit(ctx.argument_list())

      return FuncCall(name, args)


    # Visit a parse tree produced by TyCParser#primary_expression.
   def visitPrimary_expression(self, ctx: TyCParser.Primary_expressionContext):

      # function call
      if ctx.function_call():
         return self.visit(ctx.function_call())

      # identifier
      if ctx.ID():
         return Identifier(ctx.ID().getText())

      # literal
      if ctx.literal():
         return self.visit(ctx.literal())

      # struct literal
      if ctx.struct_init():
         return self.visit(ctx.struct_init())

      # parenthesized expression
      if ctx.expression():
         return self.visit(ctx.expression())


    # Visit a parse tree produced by TyCParser#argument_list.
   def visitArgument_list(self, ctx):
      return [self.visit(expr) for expr in ctx.expression()]


    # Visit a parse tree produced by TyCParser#type.
   def visitType(self, ctx):

      if ctx.INT():
         return IntType()

      if ctx.FLOAT():
         return FloatType()

      if ctx.STRING():
         return StringType()

      return StructType(ctx.ID().getText())


    # Visit a parse tree produced by TyCParser#return_type.
   def visitReturn_type(self, ctx):

      if ctx.type_():
         return self.visit(ctx.type_())

      return VoidType()


    # Visit a parse tree produced by TyCParser#statement.
   def visitStatement(self, ctx):
      if ctx.var_statement():
         return self.visit(ctx.var_statement())

      if ctx.assign_statement():
         return self.visit(ctx.assign_statement())

      if ctx.postfix_expression():
         return ExprStmt(self.visit(ctx.postfix_expression()))

      if ctx.if_statement():
         return self.visit(ctx.if_statement())

      if ctx.while_statement():
         return self.visit(ctx.while_statement())

      if ctx.for_statement():
         return self.visit(ctx.for_statement())

      if ctx.switch_statement():
         return self.visit(ctx.switch_statement())

      if ctx.break_statement():
         return BreakStmt()

      if ctx.continue_statement():
         return ContinueStmt()

      if ctx.return_statement():
         return self.visit(ctx.return_statement())

      if ctx.block_statement():
         return self.visit(ctx.block_statement())


    # Visit a parse tree produced by TyCParser#block_statement.
   def visitBlock_statement(self, ctx):
      stmts = [self.visit(stmt) for stmt in ctx.statement()]
      return BlockStmt(stmts)


    # Visit a parse tree produced by TyCParser#var_statement.
   def visitVar_statement(self, ctx):
      if ctx.AUTO():
         name = ctx.ID().getText()
         init = None
         if ctx.ASS():
               if ctx.expression():
                  init = self.visit(ctx.expression())
               else:
                  init = self.visit(ctx.struct_init())
         return VarDecl(None, name, init)
      var_type = self.visit(ctx.type_())
      name = ctx.ID().getText()
      init = None

      if ctx.ASS():
         if ctx.expression():
               init = self.visit(ctx.expression())
         else:
               init = self.visit(ctx.struct_init())
      return VarDecl(var_type, name, init)


    # Visit a parse tree produced by TyCParser#assign_statement.
   def visitAssign_statement(self, ctx):
      expr = self.visit(ctx.assignment_expression())
      return ExprStmt(expr)


    # Visit a parse tree produced by TyCParser#member_base.
   def visitMember_base(self, ctx):

      if ctx.ID():
         return Identifier(ctx.ID().getText())

      if ctx.function_call():
         return self.visit(ctx.function_call())

      if ctx.literal():
         return self.visit(ctx.literal())

      if ctx.struct_init():
         return self.visit(ctx.struct_init())


    # Visit a parse tree produced by TyCParser#member_access.
   def visitMember_access(self, ctx):

      expr = self.visit(ctx.member_base())

      ids = ctx.ID()
      for name_token in ids:
         expr = MemberAccess(expr, name_token.getText())

      return expr


    # Visit a parse tree produced by TyCParser#assign_lhs.
   def visitAssign_lhs(self, ctx):

      if ctx.ID():
         ids = ctx.ID()
         expr = Identifier(ids[0].getText())

         for i in range(1, len(ids)):
               expr = MemberAccess(expr, ids[i].getText())

         return expr

      expr = self.visit(ctx.primary_postfix())

      for part in ctx.member_part():
         expr = MemberAccess(expr, part.ID().getText())

      return expr


    # Visit a parse tree produced by TyCParser#if_statement.
   def visitIf_statement(self, ctx):

      condition = self.visit(ctx.expression())
      then_stmt = self.visit(ctx.statement(0))

      else_stmt = None
      if len(ctx.statement()) > 1:
         else_stmt = self.visit(ctx.statement(1))

      return IfStmt(condition, then_stmt, else_stmt)


    # Visit a parse tree produced by TyCParser#while_statement.
   def visitWhile_statement(self, ctx):

      condition = self.visit(ctx.expression())
      body = self.visit(ctx.statement())

      return WhileStmt(condition, body)


    # Visit a parse tree produced by TyCParser#for_statement.
   def visitFor_statement(self, ctx):

      init = None
      condition = None
      update = None

      if ctx.for_init():
         init = self.visit(ctx.for_init())

      if ctx.expression():
         condition = self.visit(ctx.expression())

      if ctx.for_update():
         update = self.visit(ctx.for_update())

      body = self.visit(ctx.statement())

      return ForStmt(init, condition, update, body)


    # Visit a parse tree produced by TyCParser#for_init.
   def visitFor_init(self, ctx):
      if ctx.var_statement():
         return self.visit(ctx.var_statement())

      # second alternative
      lhs = self.visit(ctx.assign_lhs())
      rhs = self.visit(ctx.assignment_expression())
      return ExprStmt(AssignExpr(lhs, rhs))


   # Visit a parse tree produced by TyCParser#incdec_only.
   def visitIncdec_only(self, ctx):
      if ctx.prefix_incdec():
         expr = self.visit(ctx.prefix_incdec())

         if ctx.postfix_tail():
               ops = self.visit(ctx.postfix_tail())
               for op in ops:
                  expr = PostfixOp(op, expr)
         return expr
      expr = self.visit(ctx.postfix_expression())
      tokens = ctx.INCRE() + ctx.DECRE()
      for token in tokens:
         expr = PostfixOp(token.getText(), expr)
      return expr


    # Visit a parse tree produced by TyCParser#for_update.
   def visitFor_update(self, ctx):

      if ctx.assign_lhs():
         lhs = self.visit(ctx.assign_lhs())
         rhs = self.visit(ctx.assignment_expression())
         return AssignExpr(lhs, rhs)

      return self.visit(ctx.incdec_only())


    # Visit a parse tree produced by TyCParser#switch_statement.
   def visitSwitch_statement(self, ctx):

      expr = self.visit(ctx.expression())
      cases, default_case = self.visit(ctx.switch_body())

      return SwitchStmt(expr, cases, default_case)


    # Visit a parse tree produced by TyCParser#switch_body.
   def visitSwitch_body(self, ctx):
      cases = []
      default_case = None
      for case_ctx in ctx.case_clause():
         cases.append(self.visit(case_ctx))
      if ctx.default_clause():
         default_case = self.visit(ctx.default_clause())
      return cases, default_case


    # Visit a parse tree produced by TyCParser#case_clause.
   def visitCase_clause(self, ctx):

      expr = self.visit(ctx.expression())
      stmts = [self.visit(s) for s in ctx.statement()]

      return CaseStmt(expr, stmts)


    # Visit a parse tree produced by TyCParser#default_clause.
   def visitDefault_clause(self, ctx):

      stmts = [self.visit(s) for s in ctx.statement()]
      return DefaultStmt(stmts)


    # Visit a parse tree produced by TyCParser#break_statement.
   def visitBreak_statement(self, ctx):
      return BreakStmt()


    # Visit a parse tree produced by TyCParser#continue_statement.
   def visitContinue_statement(self, ctx):
      return ContinueStmt()


    # Visit a parse tree produced by TyCParser#return_statement.
   def visitReturn_statement(self, ctx):

      if ctx.expression():
         return ReturnStmt(self.visit(ctx.expression()))

      return ReturnStmt()


    # Visit a parse tree produced by TyCParser#program.
   def visitProgram(self, ctx):
      decls = []

      for s in ctx.struct_decl():
         decls.append(self.visit(s))

      for f in ctx.function_decl():
         decls.append(self.visit(f))

      return Program(decls)

    # Visit a parse tree produced by TyCParser#struct_init.
   def visitStruct_init(self, ctx):

      values = []
      if ctx.expression():
         values = [self.visit(e) for e in ctx.expression()]

      return StructLiteral(values)
   # Visit a parse tree produced by TyCParser#struct_member.
   def visitStruct_member(self, ctx):
      member_type = self.visit(ctx.type_())
      name = ctx.ID().getText()
      return MemberDecl(member_type, name)

    # Visit a parse tree produced by TyCParser#struct_decl.
   def visitStruct_decl(self, ctx):
      name = ctx.ID().getText()
      members = [self.visit(m) for m in ctx.struct_member()]
      return StructDecl(name, members)


    # Visit a parse tree produced by TyCParser#function_decl.
   def visitFunction_decl(self, ctx):

      return_type = self.visit(ctx.return_type()) if ctx.return_type() else None
      name = ctx.ID().getText()

      params = self.visit(ctx.param_list()) if ctx.param_list() else []

      body = self.visit(ctx.block_statement())

      return FuncDecl(return_type, name, params, body)


    # Visit a parse tree produced by TyCParser#param_list.
   def visitParam_list(self, ctx):
      return [self.visit(p) for p in ctx.param()]


    # Visit a parse tree produced by TyCParser#param.
   def visitParam(self, ctx):

      param_type = self.visit(ctx.type_())
      name = ctx.ID().getText()

      return Param(param_type, name)




