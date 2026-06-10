from utils import Parser


def test_001():
    source = """
void main() {
    printString("Hello, World!");
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

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
    expected = "success"
    assert Parser(source).parse() == expected

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
    expected = "success"
    assert Parser(source).parse() == expected

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
    expected = "success"
    assert Parser(source).parse() == expected

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
    
    // Note: String concatenation is NOT supported
    // This is because + operator applies to int or float, not string
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_006():
    source ="""
struct Point {
    int x;
    int y;
};

struct Person {
    string name;
    int age;
    float height;
};

void main() {
    // Struct variable declaration without initialization
    Point p1;
    p1.x = 10;
    p1.y = 20;
    
    // Struct variable declaration with initialization
    Point p2 = {30, 40};
    
    // Access and modify struct members
    printInt(p2.x);
    printInt(p2.y);
    
    // Struct assignment
    p1 = p2;  // Copy all members
    
    // Person struct usage
    Person person1 = {"John", 25, 1.75};
    printString(person1.name);
    printInt(person1.age);
    printFloat(person1.height);
    
    // Modify struct members
    person1.age = 26;
    person1.height = 1.76;
    
    // Using struct with auto
    auto p3 = p2;  // p3: Point (inferred from assignment)
    printInt(p3.x);
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_007():
    source = """
void main() {
"""
    expected = "Error on line 3 col 0: <EOF>"
    assert Parser(source).parse() == expected

def test_008():
    source = """
void main {}
"""
    expected = "Error on line 2 col 10: {"
    assert Parser(source).parse() == expected
def test_009():
        source = """
    void main () {
        return a = b = 3;
        return (a = b) + 7;
    }
    """
        expected = "success"
        assert Parser(source).parse() == expected
def test_010():
        source = """
    void main () {
        return ++--++a;
        return !++a;
    }
    """
        expected = "success"
        assert Parser(source).parse() == expected
def test_011():
        source = """
    void main () {
        return a++--++--;
        return ++--++--a++--++--;
    }
    """
        expected = "success"
        assert Parser(source).parse() == expected
def test_012():
        source = """
    void main () {
    foo().b = 2;
    }
    """
        expected = "success"
        assert Parser(source).parse() == expected
def test_013():
        source = """
    void main () {
        return ++(+a) * (a / (c));
    }
    """
        expected = "success"
        assert Parser(source).parse() == expected
def test_014():
        source = """
    void main () {
    return ++!a;
    }
    """
        expected = "Error on line 3 col 13: !"
        assert Parser(source).parse() == expected
def test_015():
        source = """
    void main () {
    return +++a;
    }
    """
        expected = "Error on line 3 col 13: +"
        assert Parser(source).parse() == expected
def test_016():
        source = """
    void main () {
    ++a = 1;
    }
    """
        expected = "Error on line 3 col 8: ="
        assert Parser(source).parse() == expected
def test_017():
        source = """
    void main () {
        switch (1 *3 / 4) {
            default:
                1;
            case 2:
                 2;
        }
    
        switch (1 *3 / 4) {
            case 3:1;
            default:1;
            case 2: 2;
        }
    }
    """
        expected = "success"
        assert Parser(source).parse() == expected
def test_018():
        source = """
auto main(){}
    """
        expected = "Error on line 2 col 0: auto"
        assert Parser(source).parse() == expected
def test_019():
        source = """
    AAAA main (int a, int b) {return;}
    void main3 () {}
    ID main2 (int a) {return;}
    """
        expected = "success"
        assert Parser(source).parse() == expected
def test_020():
        source = """
    main(){}
    void main () {}
    """
        expected = "success"
        assert Parser(source).parse() == expected
def test_021():
        source = """
    void main () {
        auto x = readInt();
        switch (x) {
            default:
                printInt(0);
        default:
                printInt(0);
        }
    }
    """
        expected = "Error on line 7 col 8: default"
        assert Parser(source).parse() == expected
def test_022():
        source = """
    void main () {
   for(; ;a.b);
    }
    """
        expected = "Error on line 3 col 13: )"
        assert Parser(source).parse() == expected
def test_023():
    source = """
void main() {
    {
        {
        }
    }
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_024():
    source = """
void main() {
    if (a)
        if (b)
            c;
        else
            d;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_025():
    source = """
void main() {
    else a;
}
"""
    expected = "Error on line 3 col 4: else"
    assert Parser(source).parse() == expected
def test_026():
    source = """
void main() {
    return;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_027():
    source = """
void main() {
    return 1;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_028():
    source = """
void main() {
    a = 1
}
"""
    expected = "Error on line 4 col 0: }"
    assert Parser(source).parse() == expected
def test_029():
    source = """
void main() {
    for (i = 0 i < 10; i = i + 1) {
        i;
    }
}
"""
    expected = "Error on line 3 col 15: i"
    assert Parser(source).parse() == expected
def test_030():
        source = """
    void main () {
        foo().a;
        +a++;
    }
    """
        expected = "success"
        assert Parser(source).parse() == expected
def test_031():
    source = """
int foo() {
    return 1;
}

void main() {
    foo();
}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_032():
    source = """
int foo(int) {
    return 1;
}

void main() {}
"""
    expected = "Error on line 2 col 11: )"
    assert Parser(source).parse() == expected
def test_033():
    source = """
int foo(int a int b) {
    return a + b;
}

void main() {}
"""
    expected = "Error on line 2 col 14: int"
    assert Parser(source).parse() == expected
def test_034():
    source = """
void foo() {}

void main() {
    foo();
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_035():
    source = """
void foo(int a) {}

void main() {
    foo(1;
}
"""
    expected = "Error on line 5 col 9: ;"
    assert Parser(source).parse() == expected
def test_036():
    source = """
int add(int a, int b) {
    return a + b;
}

void main() {
    printInt(add(1, add(2, 3)));
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_037():
    source = """
void main() {
    foo(a = 1, b);
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_038():
        source = """
    void main () {
       foo().a;
    }
    """
        expected = "success"
        assert Parser(source).parse() == expected
def test_039():
        source = """
    void main () {
        foo() = 1;
    }
    """
        expected = "Error on line 3 col 14: ="
        assert Parser(source).parse() == expected
def test_040():
    source = """
void main() {
    a. = 1;
}
"""
    expected = "Error on line 3 col 7: ="
    assert Parser(source).parse() == expected
def test_041():
        source = """
    void main () {
    if (1);
    }
    """
        expected = "Error on line 3 col 10: ;"
        assert Parser(source).parse() == expected
def test_042():
    source = """
void main() {
    (a + b)++;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_043():
    source = """
void main() {
    break;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_044():
    source = """
void main() {
    continue;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_045():
    source = """
void main() {
    return
}
"""
    expected = "Error on line 4 col 0: }"
    assert Parser(source).parse() == expected
def test_046():
    source = """
void main() {
    switch (x) {
        case 1: x;
        case 2: y;
    }
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_047():
    source = """
void main() {
    switch (x) {
        default: x;
        case 1: y;
    }
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_048():
    source = """
void main() {
    switch (x) {
        case 1 x;
    }
}
"""
    expected = "Error on line 4 col 15: x"
    assert Parser(source).parse() == expected
def test_049():
    source = """
void main() {
    while x {
        x;
    }
}
"""
    expected = "Error on line 3 col 10: x"
    assert Parser(source).parse() == expected
def test_050():
    source = """
void main() {
    for (;;) {
    }
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_051():
        source = """
    void main () {
       for(int a = 1 + 2; i > 2; a++) continue;
       for(a = a.b = 1; ; --a) a++;
       for(auto a = 1; i * 2; a = 2) {return ;}
       for(; ; ) {}
       for({1,2}.a = 1; ; (a+2).b = 2) a++;
    }
    """
        expected = "success"
        assert Parser(source).parse() == expected

def test_052():
    source = """
void main() {
    a = (b = c) + 1;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_053():
    source = """
void main() {
    a = b + c * d / e - f;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_054():
    source = """
void main() {
    a = (b + c) * (d - e);
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_055():
    source = """
void main() {
    a = !-+-b;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_056():
    source = """
void main() {
    a = !(b + c) * d;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_057():
        source = """
    void main () {
       for(; ; -a) continue;
    }
    """
        expected = "Error on line 3 col 15: -"
        assert Parser(source).parse() == expected

def test_058():
    source = """
void main() {
    foo(bar(1), baz(2, 3));
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_059():
    source = """
void main() {
    foo((a + b), (c * d));
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_060():
    source = """
void main() {
    a.b.c.d = 1;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_061():
    source = """
void main() {
    a = b.c.d.e;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_062():
    source = """
void main() {
    (a + b)++;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_063():
    source = """
void main() {
    ++(a + b);
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_064():
    source = """
void main() {
    a = ++--++b;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_065():
    source = """
void main() {
    a = b++--++--;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_066():
    source = """
void main() {
    for (a = 0; a < 10; a = a + 1) ;
}
"""
    expected = "Error on line 3 col 35: ;"
    assert Parser(source).parse() == expected


def test_067():
    source = """
void main() {
    for (;;)
        ;
}
"""
    expected = "Error on line 4 col 8: ;"
    assert Parser(source).parse() == expected


def test_068():
    source = """
void main() {
    while (a < b)
        while (b < c)
            a;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_069():
    source = """
void main() {
    if (a)
        if (b)
            c;
        else
            d;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_070():
    source = """
void main() {
    switch (x) {
        case 1:
        case 2:
        default:
            x;
    }
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_071():
    source = """
void main() {
    ;
}
"""
    expected = "Error on line 3 col 4: ;"
    assert Parser(source).parse() == expected


def test_072():
    source = """
void main() {
    ;;;
}
"""
    expected = "Error on line 3 col 4: ;"
    assert Parser(source).parse() == expected


def test_073():
    source = """
void main() {
    if (a) ;
}
"""
    expected = "Error on line 3 col 11: ;"
    assert Parser(source).parse() == expected


def test_074():
    source = """
void main() {
    if (a) ;
    else ;
}
"""
    expected = "Error on line 3 col 11: ;"
    assert Parser(source).parse() == expected


def test_075():
    source = """
void main() {
    while (a) ;
}
"""
    expected = "Error on line 3 col 14: ;"
    assert Parser(source).parse() == expected


def test_076():
    source = """
void main() {
    for (;;) ;
}
"""
    expected = "Error on line 3 col 13: ;"
    assert Parser(source).parse() == expected


def test_077():
    source = """
void main() {
    if (a)
        for (;;)
            ;
}
"""
    expected = "Error on line 5 col 12: ;"
    assert Parser(source).parse() == expected


def test_078():
    source = """
void main() {
    for (;;)
        if (a)
            ;
        else
            ;
}
"""
    expected = "Error on line 5 col 12: ;"
    assert Parser(source).parse() == expected


def test_079():
    source = """
void main() {
    switch (a) {
        case 1:;
        case 2:;
        default:;
    }
}
"""
    expected = "Error on line 4 col 15: ;"
    assert Parser(source).parse() == expected


def test_080():
    source = """
void main() {
    switch (a) {
        case 1:
        case 2:
            ;
    }
}
"""
    expected = "Error on line 6 col 12: ;"
    assert Parser(source).parse() == expected


def test_081():
    source = """
void main() {
    a = (b = (c = 1));
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_082():
    source = """
void main() {
    a = (((b)));
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_083():
    source = """
void main() {
    a = !!!!!!!b;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_084():
    source = """
void main() {
    a = +++++b;
}
"""
    expected = "Error on line 3 col 12: +"
    assert Parser(source).parse() == expected

def test_085():
    source = """
void main() {
    a = b+++++c;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_086():
    source = """
void main() {
    a = (b++)++;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_087():
    source = """
void main() {
    return (a = b = c = 2);
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_088():
    source = """
void main() {
    return;
    ;
    ;
}
"""
    expected = "Error on line 4 col 4: ;"
    assert Parser(source).parse() == expected


def test_089():
    source = """
void main() {
    {{{;;}}}
}
"""
    expected = "Error on line 3 col 7: ;"
    assert Parser(source).parse() == expected


def test_090():
    source = """
void main() {
    for (a = 0;;)
        for (;;)
            ;
}
"""
    expected = "Error on line 5 col 12: ;"
    assert Parser(source).parse() == expected

def test_091():
    source = """
void main() {
    a = (b + c) * d / e % f;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_092():
    source = """
void main() {
    a = b < c && c < d || d < e;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_093():
    source = """
void main() {
    a = b == c != d;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_094():
    source = """
void main() {
    a = (b < c) == (d > e);
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_095():
    source = """
void main() {
    a = b = c < d;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_096():
    source = """
void main() {
    a = !b && !!c || !!!d;
}
"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_097():
        source = """
    main(){for(a * 3; i * 2; a++ = 2 = 3) {return ;}}
    """
        expected = "Error on line 2 col 17: *"
        assert Parser(source).parse() == expected

def test_098():
        source = """
    void main () {
       a++.c;
    }
    """
        expected = "Error on line 3 col 10: ."
        assert Parser(source).parse() == expected


def test_099():
    source = """
void main() {
    {
        for (;;)
            ;
        ;
    }
}
"""
    expected = "Error on line 5 col 12: ;"
    assert Parser(source).parse() == expected


def test_100():
        source = """
    void main () {
        a = foo().a = (a).b = "string".c.d.e = 1;
    }
    """
        expected = "success"
        assert Parser(source).parse() == expected