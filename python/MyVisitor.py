# -------------------------------
# -*- coding: utf-8 -*- 
# @Time : 2019/5/17 15:03 
# @Author : monarch
# @Site :  
# @File : MyVisitor.py 
# @Software: PyCharm
# -------------------------------
from python.Prolog import Prolog
from python.cGrammer.CParser import CParser
from python.cGrammer.CVisitor import CVisitor


class MyVisitor(CVisitor):
    prolog_list = {}
    count = 1
    current_father_prolog = list()

    def visitCompilationUnit(self, ctx:CParser.CompilationUnitContext):
        prolog = Prolog(id=self.count, name='C程序', value='', father_id=0, children_id=set())
        self.count += 1
        self.current_father_prolog .append(prolog)
        self.visitChildren(ctx)
        cfp = self.current_father_prolog.pop()
        self.prolog_list[cfp.id] = cfp

    def visitDeclaration(self, ctx:CParser.DeclarationContext):
        cfp = self.current_father_prolog.pop()
        cfp.children_id.add(self.count)
        prolog = Prolog(id=self.count, name='变量声明', value='', father_id=cfp.id, children_id=set())
        self.count += 1
        self.current_father_prolog.append(cfp)
        self.current_father_prolog.append(prolog)
        self.visitChildren(ctx)
        cfp = self.current_father_prolog.pop()
        self.prolog_list[cfp.id] = cfp

    def visitDeclarationSpecifier(self, ctx:CParser.DeclarationSpecifierContext):
        cfp = self.current_father_prolog.pop()
        cfp.children_id.add(self.count)
        prolog = Prolog(id=self.count, name='类型名', value=ctx.getText(), father_id=cfp.id, children_id=set())
        self.count += 1
        self.current_father_prolog.append(cfp)
        self.current_father_prolog.append(prolog)
        cfp = self.current_father_prolog.pop()
        self.prolog_list[cfp.id] = cfp

    def visitInitDeclarator(self, ctx:CParser.InitDeclaratorContext):
        cfp = self.current_father_prolog.pop()
        cfp.children_id.add(self.count)
        if ctx.getChildCount() == 1:
            prolog = Prolog(id=self.count, name='变量名', value=ctx.getText(), father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.prolog_list[prolog.id] = prolog
        else:
            prolog = Prolog(id=self.count, name='初始化变量', value='',  father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)

            # self.visitDirectDeclarator(ctx)
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            directDeclarator_prolog = Prolog(id=self.count, name='变量名', value=ctx.declarator().getText(),  father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.prolog_list[directDeclarator_prolog.id] = directDeclarator_prolog

            # self.visitInitializer(ctx)
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            initializer_prolog = Prolog(id=self.count, name='初始值', value=ctx.initializer().getText(), father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.prolog_list[initializer_prolog.id] = initializer_prolog

            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp

    def visitFunctionDefinition(self, ctx:CParser.FunctionDefinitionContext):
        cfp = self.current_father_prolog.pop()
        cfp.children_id.add(self.count)
        prolog = Prolog(id=self.count, name='函数定义', value='', father_id=cfp.id, children_id=set())
        self.count += 1
        self.current_father_prolog.append(cfp)
        self.current_father_prolog.append(prolog)
        self.visitChildren(ctx)
        cfp = self.current_father_prolog.pop()
        self.prolog_list[cfp.id] = cfp

    def visitDirectDeclarator(self, ctx:CParser.DirectDeclaratorContext):
        if ctx.getChildCount() > 1:
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='函数名', value=ctx.directDeclarator().getText(), father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.prolog_list[prolog.id] = prolog
            if ctx.getChildCount() == 4:
                self.visitParameterTypeList(ctx.parameterTypeList())

    def visitParameterList(self, ctx:CParser.ParameterTypeListContext):
        cfp = self.current_father_prolog.pop()
        if cfp.name != '参数列表':
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='参数列表', value='', father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)
            self.visitChildren(ctx)
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        else:
            self.current_father_prolog.append(cfp)
            self.visitChildren(ctx)

    def visitParameterDeclaration(self, ctx:CParser.ParameterDeclarationContext):
        cfp = self.current_father_prolog.pop()
        cfp.children_id.add(self.count)
        prolog = Prolog(id=self.count, name='参数声明', value='', father_id=cfp.id, children_id=set())
        self.count += 1
        self.current_father_prolog.append(cfp)
        self.current_father_prolog.append(prolog)

        # visitDeclarationSpecifiers
        self.visitDeclarationSpecifiers(ctx.declarationSpecifiers())

        # visitDeclarator
        cfp = self.current_father_prolog.pop()
        cfp.children_id.add(self.count)
        declarator_prolog = Prolog(id=self.count, name='参数名', value=ctx.declarator().getText(), father_id=cfp.id, children_id=set())
        self.count += 1
        self.prolog_list[declarator_prolog.id] = declarator_prolog
        self.prolog_list[cfp.id] = cfp

    def visitArgumentExpressionList(self, ctx:CParser.ArgumentExpressionListContext):
        cfp = self.current_father_prolog.pop()
        if cfp.name != ctx.__class__.__name__[:-7]:
            cfp.children_id.add(self.count)
            argumentExpressionList_prolog = Prolog(id=self.count, name=ctx.__class__.__name__[:-7], value=ctx.__class__.__name__[:-7], father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(argumentExpressionList_prolog)
            self.visitChildren(ctx)
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        else:
            self.current_father_prolog.append(cfp)
            self.visitChildren(ctx)

    # statement
    def visitCompoundStatement(self, ctx:CParser.CompoundStatementContext):
        cfp = self.current_father_prolog.pop()
        cfp.children_id.add(self.count)
        compoundStatement_prolog = Prolog(id=self.count, name='程序块', value='', father_id=cfp.id, children_id=set())
        self.count += 1
        self.current_father_prolog.append(cfp)
        self.current_father_prolog.append(compoundStatement_prolog)
        self.visitChildren(ctx)
        cfp = self.current_father_prolog.pop()
        self.prolog_list[cfp.id] = cfp

    def visitLabeledStatement(self, ctx:CParser.LabeledStatementContext):
        if ctx.getChild(0).getText() == 'case':
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='case标记语句', value='', father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)

            #self.visitConstantExpression(ctx.constantExpression())
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            constantExpression_prolog= Prolog(id=self.count, name='case值', value=ctx.constantExpression().getText(), father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.prolog_list[constantExpression_prolog.id] = constantExpression_prolog

            self.visitStatement(ctx.statement())
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        elif ctx.getChild(0).getText() == 'default':
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='default标记语句', value='', father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)
            self.visitStatement(ctx.statement())
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp

    def visitExpressionStatement(self, ctx:CParser.ExpressionStatementContext):
        cfp = self.current_father_prolog.pop()
        if cfp.name != '表达式语句':
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='表达式语句', value='', father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)
            self.visitChildren(ctx)
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        else:
            self.current_father_prolog.append(cfp)
            self.visitChildren(ctx)

    def visitSelectionStatement(self, ctx:CParser.SelectionStatementContext):
        if ctx.getChild(0).getText() == 'if':
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='switch选择语句', value='', father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)
            self.visitChildren(ctx)
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        elif ctx.getChild(0).getText() == 'switch':
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='switch选择语句', value='', father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)
            self.visitChildren(ctx)
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp

    def visitIterationStatement(self, ctx:CParser.IterationStatementContext):
        if ctx.getChild(0).getText() == 'for':
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='for迭代语句', value='', father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)

            # visitExpression
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            forCondition_prolog = Prolog(id=self.count, name='for条件语句', value='', father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(forCondition_prolog)
            self.visitForCondition(ctx.forCondition())
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp

            self.visitStatement(ctx.statement())
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        elif ctx.getChild(0).getText() == 'while':
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='while迭代语句', value='', father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)
            self.visitStatement(ctx.statement())
            # visitExpression
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            expression_prolog = Prolog(id=self.count, name='while条件语句', value='', father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(expression_prolog)
            self.visitExpression(ctx.expression())
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp

            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        elif ctx.getChild(0).getText() == 'do':
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='do-while迭代语句', value='', father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)

            # visitForCondition
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            expression_prolog = Prolog(id=self.count, name='do-while条件语句', value='', father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(expression_prolog)
            self.visitExpression(ctx.expression())
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp

            self.visitStatement(ctx.statement())
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
    def visitJumpStatement(self, ctx:CParser.JumpStatementContext):
        cfp = self.current_father_prolog.pop()
        cfp.children_id.add(self.count)
        prolog = Prolog(id=self.count, name='跳转语句', value='', father_id=cfp.id, children_id=set())
        self.count += 1
        self.current_father_prolog.append(cfp)
        self.current_father_prolog.append(prolog)
        self.visitChildren(ctx)
        cfp = self.current_father_prolog.pop()
        self.prolog_list[cfp.id] = cfp

    # expression
    def visitAssignmentExpression(self, ctx:CParser.AssignmentExpressionContext):
        if ctx.getChildCount() == 3:
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='赋值表达式', value='', father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)

            # visitUnaryExpression
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            unaryExpression_prolog = Prolog(id=self.count, name='变量名', value=ctx.unaryExpression().getText(), father_id=cfp.id,children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.prolog_list[unaryExpression_prolog.id] = unaryExpression_prolog
            self.visitAssignmentOperator(ctx.assignmentOperator())
            self.visitAssignmentExpression(ctx.assignmentExpression())
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        else:
            return self.visitChildren(ctx)

    def visitConditionalExpression(self, ctx:CParser.ConditionalExpressionContext):
        if ctx.getChildCount() > 1:
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='条件表达式', value=ctx.getText(), father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)
            self.visitChildren(ctx)
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        else:
            return self.visitChildren(ctx)

    def visitLogicalOrExpression(self, ctx:CParser.LogicalOrExpressionContext):
        if ctx.getChildCount() > 1:
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='与表达式', value=ctx.getChild(1).getText(), father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)
            self.visitChildren(ctx)
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        else:
            return self.visitChildren(ctx)

    def visitLogicalAndExpression(self, ctx:CParser.LogicalAndExpressionContext):
        if ctx.getChildCount() > 1:
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='逻辑与表达式', value=ctx.getChild(1).getText(), father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)
            self.visitChildren(ctx)
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        else:
            return self.visitChildren(ctx)

    def visitInclusiveOrExpression(self, ctx:CParser.InclusiveOrExpressionContext):
        if ctx.getChildCount() > 1:
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='或表达式', value=ctx.getChild(1).getText(), father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)
            self.visitChildren(ctx)
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        else:
            return self.visitChildren(ctx)

    def visitExclusiveOrExpression(self, ctx:CParser.ExclusiveOrExpressionContext):
        if ctx.getChildCount() > 1:
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='异或表达式', value=ctx.getChild(1).getText(), father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)
            self.visitChildren(ctx)
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        else:
            return self.visitChildren(ctx)

    def visitAndExpression(self, ctx:CParser.AndExpressionContext):
        if ctx.getChildCount() > 1:
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='与表达式', value=ctx.getChild(1).getText(), father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)
            self.visitChildren(ctx)
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        else:
            return self.visitChildren(ctx)

    def visitEqualityExpression(self, ctx:CParser.EqualityExpressionContext):
        if ctx.getChildCount() > 1:
            if ctx.getChild(1).getText() == '==':
                cfp = self.current_father_prolog.pop()
                cfp.children_id.add(self.count)
                prolog = Prolog(id=self.count, name='相等表达式', value='', father_id=cfp.id, children_id=set())
                self.count += 1
                self.current_father_prolog.append(cfp)
                self.current_father_prolog.append(prolog)
                self.visitEqualityExpression(ctx.equalityExpression())
                cfp = self.current_father_prolog.pop()
                cfp.children_id.add(self.count)
                operate_prolog = Prolog(id=self.count, name='相等号', value='==', father_id=cfp.id, children_id=set())
                self.count += 1
                self.prolog_list[operate_prolog.id] = operate_prolog
                self.current_father_prolog.append(cfp)
                self.visitRelationalExpression(ctx.relationalExpression())
                cfp = self.current_father_prolog.pop()
                self.prolog_list[cfp.id] = cfp
            elif ctx.getChild(1).getText() == '!=':
                cfp = self.current_father_prolog.pop()
                cfp.children_id.add(self.count)
                prolog = Prolog(id=self.count, name='不等表达式', value='', father_id=cfp.id, children_id=set())
                self.count += 1
                self.current_father_prolog.append(cfp)
                self.current_father_prolog.append(prolog)
                self.visitEqualityExpression(ctx.equalityExpression())
                cfp = self.current_father_prolog.pop()
                cfp.children_id.add(self.count)
                operate_prolog = Prolog(id=self.count, name='不等号', value='!=', father_id=cfp.id, children_id=set())
                self.count += 1
                self.prolog_list[operate_prolog.id] = operate_prolog
                self.current_father_prolog.append(cfp)
                self.visitRelationalExpression(ctx.relationalExpression())
                cfp = self.current_father_prolog.pop()
                self.prolog_list[cfp.id] = cfp
        else:
            return self.visitChildren(ctx)

    def visitRelationalExpression(self, ctx:CParser.RelationalExpressionContext):
        if ctx.getChildCount() > 1:
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='关系表达式', value='', father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)
            self.visitRelationalExpression(ctx.relationalExpression())
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            operate_prolog = Prolog(id=self.count, name='关系符', value=ctx.getChild(1).getText(), father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.prolog_list[operate_prolog.id] = operate_prolog
            self.visitShiftExpression(ctx.shiftExpression())
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        else:
            return self.visitChildren(ctx)

    def visitShiftExpression(self, ctx:CParser.ShiftExpressionContext):
        if ctx.getChildCount() > 1:
            cfp = self.current_father_prolog.pop()
            cfp.children_id.add(self.count)
            prolog = Prolog(id=self.count, name='位移表达式', value=ctx.getChild(1).getText(), father_id=cfp.id, children_id=set())
            self.count += 1
            self.current_father_prolog.append(cfp)
            self.current_father_prolog.append(prolog)
            self.visitChildren(ctx)
            cfp = self.current_father_prolog.pop()
            self.prolog_list[cfp.id] = cfp
        else:
            return self.visitChildren(ctx)

    def visitAdditiveExpression(self, ctx:CParser.AdditiveExpressionContext):
        if ctx.getChildCount() > 1:
            if ctx.getChild(1).getText() == '+':
                cfp = self.current_father_prolog.pop()
                cfp.children_id.add(self.count)
                prolog = Prolog(id=self.count, name='加法语句', value='', father_id=cfp.id, children_id=set())
                self.count += 1
                self.current_father_prolog.append(cfp)
                self.current_father_prolog.append(prolog)
                self.visitAdditiveExpression(ctx.additiveExpression())
                cfp = self.current_father_prolog.pop()
                cfp.children_id.add(self.count)
                operate_prolog = Prolog(id=self.count, name='加号', value='+', father_id=cfp.id, children_id=set())
                self.count += 1
                self.prolog_list[operate_prolog.id] = operate_prolog
                self.current_father_prolog.append(cfp)
                self.visitMultiplicativeExpression(ctx.multiplicativeExpression())
                cfp = self.current_father_prolog.pop()
                self.prolog_list[cfp.id] = cfp
            elif ctx.getChild(1).getText() == '-':
                cfp = self.current_father_prolog.pop()
                cfp.children_id.add(self.count)
                prolog = Prolog(id=self.count, name='减法语句', value='', father_id=cfp.id, children_id=set())
                self.count += 1
                self.current_father_prolog.append(cfp)
                self.current_father_prolog.append(prolog)
                self.visitAdditiveExpression(ctx.additiveExpression())
                cfp = self.current_father_prolog.pop()
                cfp.children_id.add(self.count)
                operate_prolog = Prolog(id=self.count, name='减号', value='-', father_id=cfp.id, children_id=set())
                self.count += 1
                self.prolog_list[operate_prolog.id] = operate_prolog
                self.current_father_prolog.append(cfp)
                self.visitMultiplicativeExpression(ctx.multiplicativeExpression())
                cfp = self.current_father_prolog.pop()
                self.prolog_list[cfp.id] = cfp
        else:
            return self.visitChildren(ctx)

    def visitMultiplicativeExpression(self, ctx:CParser.MultiplicativeExpressionContext):
        if ctx.getChildCount() > 1:
            if ctx.getChild(1).getText() == '*':
                cfp = self.current_father_prolog.pop()
                cfp.children_id.add(self.count)
                prolog = Prolog(id=self.count, name='乘法语句', value='', father_id=cfp.id, children_id=set())
                self.count += 1
                self.current_father_prolog.append(cfp)
                self.current_father_prolog.append(prolog)
                self.visitMultiplicativeExpression(ctx.multiplicativeExpression())
                cfp = self.current_father_prolog.pop()
                cfp.children_id.add(self.count)
                operate_prolog = Prolog(id=self.count, name='乘号', value='*', father_id=cfp.id, children_id=set())
                self.count += 1
                self.prolog_list[operate_prolog.id] = operate_prolog
                self.current_father_prolog.append(cfp)
                self.visitCastExpression(ctx.castExpression())
                cfp = self.current_father_prolog.pop()
                self.prolog_list[cfp.id] = cfp
            elif ctx.getChild(1).getText() == '/':
                cfp = self.current_father_prolog.pop()
                cfp.children_id.add(self.count)
                prolog = Prolog(id=self.count, name='除法语句', value='', father_id=cfp.id, children_id=set())
                self.count += 1
                self.current_father_prolog.append(cfp)
                self.current_father_prolog.append(prolog)
                self.visitMultiplicativeExpression(ctx.multiplicativeExpression())
                cfp = self.current_father_prolog.pop()
                cfp.children_id.add(self.count)
                operate_prolog = Prolog(id=self.count, name='除号', value='/', father_id=cfp.id, children_id=set())
                self.count += 1
                self.prolog_list[operate_prolog.id] = operate_prolog
                self.current_father_prolog.append(cfp)
                self.visitCastExpression(ctx.castExpression())
                cfp = self.current_father_prolog.pop()
                self.prolog_list[cfp.id] = cfp
            elif ctx.getChild(1).getText() == '%':
                cfp = self.current_father_prolog.pop()
                cfp.children_id.add(self.count)
                prolog = Prolog(id=self.count, name='取余语句', value='', father_id=cfp.id, children_id=set())
                self.count += 1
                self.current_father_prolog.append(cfp)
                self.current_father_prolog.append(prolog)
                self.visitMultiplicativeExpression(ctx.multiplicativeExpression())
                cfp = self.current_father_prolog.pop()
                cfp.children_id.add(self.count)
                operate_prolog = Prolog(id=self.count, name='取余号', value='%', father_id=cfp.id, children_id=set())
                self.count += 1
                self.prolog_list[operate_prolog.id] = operate_prolog
                self.current_father_prolog.append(cfp)
                self.visitCastExpression(ctx.castExpression())
                cfp = self.current_father_prolog.pop()
                self.prolog_list[cfp.id] = cfp
        else:
            return self.visitChildren(ctx)

    def visitPrimaryExpression(self, ctx:CParser.PrimaryExpressionContext):
        cfp = self.current_father_prolog.pop()
        cfp.children_id.add(self.count)
        prolog = Prolog(id=self.count, name='值',value=ctx.getText(), father_id=cfp.id, children_id=set())
        self.count += 1
        self.current_father_prolog.append(cfp)
        self.current_father_prolog.append(prolog)
        self.visitChildren(ctx)
        cfp = self.current_father_prolog.pop()
        self.prolog_list[cfp.id] = cfp

    # operator
    def visitAssignmentOperator(self, ctx:CParser.AssignmentOperatorContext):
        cfp = self.current_father_prolog.pop()
        cfp.children_id.add(self.count)
        prolog = Prolog(id=self.count, name='赋值操作',value=ctx.getText(), father_id=cfp.id, children_id=set())
        self.count += 1
        self.current_father_prolog.append(cfp)
        self.current_father_prolog.append(prolog)
        self.visitChildren(ctx)
        cfp = self.current_father_prolog.pop()
        self.prolog_list[cfp.id] = cfp

