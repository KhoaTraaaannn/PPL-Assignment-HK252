from utils import ASTGenerator
from src.utils.nodes import *



def test_001():
    source = """
void main() {
    printString("Hello, World!");
}
"""
    expected = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(
                    FuncCall("printString", [StringLiteral("Hello, World!")])
                )
            ])
        )
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_002():
    source = """
int add(int x, int y) {
    return x + y;
}

int multiply(int x, int y) {
    return x * y;
}

void main() {
    auto a = readInt();
    auto b = readInt();
    
    auto sum = add(a, b);
    auto product = multiply(a, b);
    
    printInt(sum);
    printInt(product);
}
"""
    expected = Program([
        FuncDecl(
            IntType(),
            "add",
            [Param(IntType(), "x"), Param(IntType(), "y")],
            BlockStmt([
                ReturnStmt(
                    BinaryOp(Identifier("x"), "+", Identifier("y"))
                )
            ])
        ),
        FuncDecl(
            IntType(),
            "multiply",
            [Param(IntType(), "x"), Param(IntType(), "y")],
            BlockStmt([
                ReturnStmt(
                    BinaryOp(Identifier("x"), "*", Identifier("y"))
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "a", FuncCall("readInt", [])),
                VarDecl(None, "b", FuncCall("readInt", [])),
                VarDecl(None, "sum", FuncCall("add", [Identifier("a"), Identifier("b")])),
                VarDecl(None, "product", FuncCall("multiply", [Identifier("a"), Identifier("b")])),
                ExprStmt(FuncCall("printInt", [Identifier("sum")])),
                ExprStmt(FuncCall("printInt", [Identifier("product")]))
            ])
        )
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_003():
    source = """
void main() {
    auto n = readInt();
    auto i = 0;
    
    while (i < n) {
        printInt(i);
        ++i;
    }
    
    for (auto j = 0; j < n; ++j) {
        if (j % 2 == 0) {
            printInt(j);
        }
    }
}
"""
    expected = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "n", FuncCall("readInt", [])),
                VarDecl(None, "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", Identifier("n")),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(PrefixOp("++", Identifier("i")))
                    ])
                ),
                ForStmt(
                    VarDecl(None, "j", IntLiteral(0)),
                    BinaryOp(Identifier("j"), "<", Identifier("n")),
                    PrefixOp("++", Identifier("j")),
                    BlockStmt([
                        IfStmt(
                            BinaryOp(
                                BinaryOp(Identifier("j"), "%", IntLiteral(2)),
                                "==",
                                IntLiteral(0)
                            ),
                            BlockStmt([
                                ExprStmt(FuncCall("printInt", [Identifier("j")]))
                            ]),
                            None
                        )
                    ])
                )
            ])
        )
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_004():
    source = """
int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

void main() {
    auto num = readInt();
    auto result = factorial(num);
    printInt(result);
}
"""
    expected = Program([
        FuncDecl(
            IntType(),
            "factorial",
            [Param(IntType(), "n")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("n"), "<=", IntLiteral(1)),
                    BlockStmt([
                        ReturnStmt(IntLiteral(1))
                    ]),
                    BlockStmt([
                        ReturnStmt(
                            BinaryOp(
                                Identifier("n"),
                                "*",
                                FuncCall(
                                    "factorial",
                                    [BinaryOp(Identifier("n"), "-", IntLiteral(1))]
                                )
                            )
                        )
                    ])
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "num", FuncCall("readInt", [])),
                VarDecl(None, "result", FuncCall("factorial", [Identifier("num")])),
                ExprStmt(FuncCall("printInt", [Identifier("result")]))
            ])
        )
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_005():
        source = """
    void main() {
        // With auto and initialization
        auto x = readInt();
        auto y = readFloat();
        auto name = readString();
    
        // With auto without initialization
        auto sum;
        sum = x + y;              // sum: float (inferred from first usage - assignment)
    
        // With explicit type and initialization
        int count = 0;
        float total = 0.0;
        string greeting = "Hello, ";
    
        // With explicit type without initialization
        int i;
        float f;
        i = readInt();            // assignment to int
        f = readFloat();          // assignment to float
    
        printFloat(sum);
        printString(greeting);
        printString(name);
    }
    """
        expected = Program([
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt([
                    VarDecl(None, "x", FuncCall("readInt", [])),
                    VarDecl(None, "y", FuncCall("readFloat", [])),
                    VarDecl(None, "name", FuncCall("readString", [])),
    
                    VarDecl(None, "sum", None),
                    ExprStmt(
                        AssignExpr(
                            Identifier("sum"),
                            BinaryOp(Identifier("x"), "+", Identifier("y"))
                        )
                    ),
    
                    VarDecl(IntType(), "count", IntLiteral(0)),
                    VarDecl(FloatType(), "total", FloatLiteral(0.0)),
                    VarDecl(StringType(), "greeting", StringLiteral("Hello, ")),
    
                    VarDecl(IntType(), "i", None),
                    VarDecl(FloatType(), "f", None),
                    ExprStmt(
                        AssignExpr(Identifier("i"), FuncCall("readInt", []))
                    ),
                    ExprStmt(
                        AssignExpr(Identifier("f"), FuncCall("readFloat", []))
                    ),
    
                    ExprStmt(FuncCall("printFloat", [Identifier("sum")])),
                    ExprStmt(FuncCall("printString", [Identifier("greeting")])),
                    ExprStmt(FuncCall("printString", [Identifier("name")]))
                ])
            )
        ])
        assert str(ASTGenerator(source).generate()) == str(expected)
def test_006():
        source = """
    struct A {};
    struct B {int a; ID b;};
    struct C {float a; string b;};
    struct D {Z a;};
    """
        expected = Program([
            StructDecl('A', []),
            StructDecl('B', [MemberDecl(IntType(), 'a'), MemberDecl(StructType('ID'), 'b')]),
            StructDecl('C', [MemberDecl(FloatType(), 'a'), MemberDecl(StringType(), 'b')]),
            StructDecl('D', [ MemberDecl(StructType('Z'), 'a')]),
        ])
        assert str(ASTGenerator(source).generate()) == str(expected)
def test_020():
        source = """
    void main() {
        -+!-+! 2;
        -a.b.c;
    }
    """
        expected = Program([
            FuncDecl(VoidType(), "main", [], BlockStmt([
                ExprStmt(
                    PrefixOp(
                        "-",
                        PrefixOp(
                            "+",
                            PrefixOp(
                                "!",
                                PrefixOp(
                                    "-",
                                    PrefixOp(
                                        "+",
                                        PrefixOp(
                                            "!",
                                            IntLiteral(2)
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                ExprStmt(
                    PrefixOp( "-",
                    MemberAccess(
                        MemberAccess( Identifier("a"), "b"),
                        "c"
                    ))
                )
            ]))
        ])
        assert str(ASTGenerator(source).generate()) == str(expected)
def test_030():
        source = """
    void main() {
        for (;;) continue;
        for (a.b=1;a.b;) {}
        for (auto a = 1; ; ) {return;}
    }
    """
        expected = Program([
            FuncDecl(VoidType(), "main", [], BlockStmt([
                ForStmt(
                    None,
                    None,
                    None,
                    ContinueStmt()
                ),
                ForStmt(
                     ExprStmt(AssignExpr(
                        MemberAccess(Identifier("a"), "b"),
                        IntLiteral(1)
                    ))
                    ,
                    MemberAccess(Identifier("a"), "b"),
                    None,
                    BlockStmt([])
                ),
                ForStmt(
                    VarDecl( None, "a", IntLiteral(1)),
                    None,
                    None,
                    BlockStmt([
                        ReturnStmt(None)
                    ])
                )
            ]))
        ])
        assert str(ASTGenerator(source).generate()) == str(expected)
def test_036():
        source = """
    void main() {
        switch(1) {
        }
    }
    """
        expected = Program([
            FuncDecl(VoidType(), "main", [], BlockStmt([
                SwitchStmt(
                    IntLiteral(1),
                    [],
                    None
                )
            ]))
        ])
        assert str(ASTGenerator(source).generate()) == str(expected)
def test_041():
        source = """
   void main() {
    {2,3,2};
    }
    """
        expected = Program([
    FuncDecl(VoidType(), "main", [], BlockStmt([
        ExprStmt(
            StructLiteral([
                IntLiteral(2),
                IntLiteral(3),
                IntLiteral(2)
            ])
        )
    ]))
]) 
        assert str(ASTGenerator(source).generate()) == str(expected)
def test_007():
        source = """
    void main() {}
    main(int a) {}
    int main(int a, ID b) {}
    float main(float b) {}
    string main(string b, int a, Z b) {}
    """
        expected = Program([
            FuncDecl(VoidType(), "main", [], BlockStmt([])),
            FuncDecl(None, "main",
                [Param(IntType(), "a")],
                BlockStmt([])
            ),
            FuncDecl(IntType(), "main",
                [Param(IntType(), "a"), Param(StructType("ID"), "b")],
                BlockStmt([])
            ),
            FuncDecl(FloatType(), "main",
                [Param(FloatType(), "b")],
                BlockStmt([])
            ),
            FuncDecl(StringType(), "main",
                [
                    Param(StringType(), "b"),
                    Param(IntType(), "a"),
                    Param(StructType("Z"), "b")
                ],
                BlockStmt([])
            ),
        ])
        assert str(ASTGenerator(source).generate()) == str(expected)
def test_031():
        source = """
    void main() {
        for(;;a++) {}
        for (;;++a) {}
        for (;;a.b=2) {}
        for (a=1;;a.b=2) {}
    }
    """
        expected = Program([
            FuncDecl(VoidType(), "main", [], BlockStmt([
                ForStmt(
                    None,
                    None,
                    PostfixOp('++', Identifier("a")),
                    BlockStmt([])
                ),
                ForStmt(
                    None,
                    None,
                    PrefixOp('++', Identifier("a")),
                    BlockStmt([])
                ),
                ForStmt(
                    None,
                    None,
                    AssignExpr(
                        MemberAccess(Identifier("a"), "b"),
                        IntLiteral(2)
                    ),
                    BlockStmt([])
                ),
                ForStmt(
                     ExprStmt(AssignExpr(
                       Identifier("a"),
                        IntLiteral(1)
                    )),
                    None,
                    AssignExpr(
                        MemberAccess(Identifier("a"), "b"),
                        IntLiteral(2)
                    ),
                    BlockStmt([])
                )
            ]))
        ])
        assert str(ASTGenerator(source).generate()) == str(expected)
def test_033():
        source = """
    void main() {
        switch(a) {
            case 1: b = 2;
            default: d = 4;
            case 2: c = 3;
        }
    }
    """
        expected = Program([
            FuncDecl(VoidType(), "main", [], BlockStmt([
                SwitchStmt(
                    Identifier("a"),
                    [
                        CaseStmt(
                            IntLiteral(1),
                            [ExprStmt(AssignExpr(Identifier("b"), IntLiteral(2)))]
                        ),
                        CaseStmt(
                            IntLiteral(2),
                            [ExprStmt(AssignExpr(Identifier("c"), IntLiteral(3)))]
                        )
                    ],
                    DefaultStmt([
                        ExprStmt(AssignExpr(Identifier("d"), IntLiteral(4)))
                    ])
                )
            ]))
        ])
        assert str(ASTGenerator(source).generate()) == str(expected)