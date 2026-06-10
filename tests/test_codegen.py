"""
Test cases for TyC code generation.
"""

from src.utils.nodes import *
from utils import CodeGenerator

# ! ## java -jar jasmin.jar *.j && java -noverify TyC
def test_001():
    source = """
    void main() {
        printString("Hello World");
    }
    """
    assert CodeGenerator().generate_and_run(source) == "Hello World"


def test_002():
    source = """
    void main() {
        printInt(42);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "42"


def test_003():
    source = """
    void main() {
        printFloat(3.14);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "3.14"


def test_004():
    source = """
    void main() {
        int x = 10;
        printInt(x);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "10"


def test_005():
    source = """
    void main() {
        printInt(5 + 3);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "8"


def test_006():
    source = """
    void main() {
        printInt(6 * 7);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "42"


def test_007():
    source = """
    void main() {
        if (1 < 2)
            printString("yes");
        else
            printString("no");
    }
    """
    assert CodeGenerator().generate_and_run(source) == "yes"


def test_008():
    source = """
    void main() {
        int i = 0;
        while (i < 3) {
            printInt(i);
            i = i + 1;
        }
    }
    """
    assert CodeGenerator().generate_and_run(source) == "012"


def test_009():
    source = """
    int add(int a, int b) {
        return a + b;
    }

    void main() {
        printInt(add(20, 22));
    }
    """
    assert CodeGenerator().generate_and_run(source) == "42"


def test_010():
    source = """
    void main() {
        int x = 10;
        int y = 20;
        printInt(x + y);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "30"

def test_011():
    source = """
    void main() {
        printFloat(1 + 1.2);
        printFloat(1.1 * 2);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "2.22.2"

def test_012():
    source = """
    void main() {
        printInt(1 <= 1.2);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "1"

def test_013():
    source = """
    int foo() {
        printInt(1);
        return 1;
    }
    void main() {
        printInt(1 && foo());
        printInt(1 || foo());
    }
    """
    assert CodeGenerator().generate_and_run(source) == "111"

def test_014():
    source = """
    int foo() {
        printInt(1);
        return 1;
    }
    void main() {
        printInt(1 && foo());
        printInt(1 || foo());
    }
    """
    assert CodeGenerator().generate_and_run(source) == "111"


def test_015():
    source = """
    void main() {
        printInt(!0);
        printInt(- - - 2);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "1-2"

def test_016():
    source = """
    void main() {
        int a = 2;
        printInt(++a);
        printInt(a);
        printInt(-- a);
        printInt(a);        
    }
    """
    assert CodeGenerator().generate_and_run(source) == "3322"

def test_017():
    source = """
    void main() {
        int a = 2;
        printInt(a++);
        printInt(a);
        printInt(a--);
        printInt(a);        
    }
    """
    assert CodeGenerator().generate_and_run(source) == "2332"

def test_018():
    source = """
    void main() {
        int i = 0;
        while (i < 5) {
            i = i + 1;

            if (i == 2) {
                continue;
            }

            if (i == 4) {
                break;
            } else {
                printInt(i);
            }
        }
    }
    """
    assert CodeGenerator().generate_and_run(source) == "13"


def test_019():
    source = """
    void main() {
        for(int i = 0; i <= 10; i++){
            printInt(i);
        }
        printInt(i);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "01234567891011"

def test_020():
    source = """
    void main() {
        int x = 3;
        switch (x) {
            case 1: printInt(1);
            case 3: printInt(3);
            case 5: printInt(5);
            default: printInt(7);
        }
    }
    """
    assert CodeGenerator().generate_and_run(source) == "357"

def test_021():
    source = """
    void main() {
        int x = 3;
        {
            int x = 2;
        }
        printInt(x);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "3"

def test_022():
    source = """
    void main() {
        int x = 5;
        switch (x) {
            case 1: printInt(1);
            case 3: printInt(3);
            case 5: int b = 2; printInt(b);
            default: b = 3; printInt(b);
        }
    }
    """
    assert CodeGenerator().generate_and_run(source) == "23"

def test_023():
    source = """
    struct Point {
        int x;
        int y;
    };
    void main(){
        Point p;
        p.x = 2;
        printInt(p.x);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "2"

def test_024():
    source = """
    struct Point {
        int x;
        int y;
    };
    void main(){
        Point p;
        int a;
        a = p.y = 3;
        printInt(a);
        printInt(p.y);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "33"

def test_025():
    source = """
    void main(){
        printInt(readInt());
        printFloat(readFloat());
        printString(readString());
    }
    """
    assert CodeGenerator().generate_and_run(source) == "22.2votien"

def test_026():
    source = """
    void main(){
        int a;
        float b;
        string c;
        printInt(a);
        printFloat(b);
        printString(c);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "00.0"

def test_027():
    source = """
    struct Point {
        int x;
        float y;
        string z;
    };
    void main(){
        Point p;
        printInt(p.x);
        printFloat(p.y);
        printString(p.z);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "00.0"

def test_028():
    source = """
    struct A {int x;};
    struct B {A a;};
    void main(){
        B p;
        printInt(p.a.x + 1);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "1"

def test_029():
    source = """
    struct Point {
        int x;
        float y;
        string z ;
    };
    void main(){
        Point p = {1,2.2,"votien"};
        printInt(p.x);
        printFloat(p.y);
        printString(p.z);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "12.2votien"

def test_030():
    source = """
    void main(){
        auto a; auto b;
        {a = b = 1;}
        printInt(a + b);
    }
    """
    assert CodeGenerator().generate_and_run(source) == "2"

def test_031():
    source = """
foo(int a, int b) {return a + b;}
void main(){
    auto a; auto b;
    printInt(foo(a, b));
}
    """
    assert CodeGenerator().generate_and_run(source) == "0"


def test_032():
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
    assert CodeGenerator().generate_and_run(source) == "44"

def test_033():
    source = """
void main() {
    auto n = 10;
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
    assert CodeGenerator().generate_and_run(source) == "012345678902468"


def test_034():
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
    assert CodeGenerator().generate_and_run(source) == "4.2Hello, votien"

def test_035():
    source = """
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
    assert CodeGenerator().generate_and_run(source) == "3040John251.7530"

def test_036():
    source = """
int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

void main() {
    auto num = 10;
    auto result = factorial(num);
    printInt(result);
}
    """
    assert CodeGenerator().generate_and_run(source) == "3628800"

def test_056():
        source = """
        void main() {
            for (int i = 0; i < 6; i++) {
                if (i == 3) continue;
                printInt(i);
            }
        }
        """
        assert CodeGenerator().generate_and_run(source) == "01245"
def test_061():
        source = """
        void main() {
            int i = 0;
            for (; i < 5; i++) {
                printInt(i);
            }
        }
        """
        assert CodeGenerator().generate_and_run(source) == "01234"
def test_076():
        source = """
        void main() {
            int x = 3;
            switch (x) {
                case 1: printInt(1); break;
                case 3: printInt(3); break;
                case 5: printInt(5);
                default: printInt(9);
            }
        }
        """
        assert CodeGenerator().generate_and_run(source) == "3"
def test_081():
        source = """
        void main() {
            int i = 0;
            while (i < 5) {
                i = i + 1;
                switch (i) {
                    case 2: continue;
                    case 4: break;
                    default: printInt(i);
                }
                printInt(i);
            }
        }
        """
        assert CodeGenerator().generate_and_run(source) == "1133455"
def test_084():
        source = """
        void main() {
            int i = 2;
            switch (i) {
                default: int i = 3;
            }
            printInt(i);
        }
        """
        assert CodeGenerator().generate_and_run(source) == "2"
def test_123():
        source = """
        void main() {
            int a = 5;
    
            printInt(++a);  // 6
            printInt(a);    // 6
    
            printInt(--a);  // 5
            printInt(a);    // 5
    
            printInt(+ + +a);   // 5
            printInt(- - -a);   // -5
        }
        """
        assert CodeGenerator().generate_and_run(source) == "66555-5"
def test_131():
        source = """
        struct Point {
            int x;
            int y;
        };
    
        void main() {
            Point p1;
            Point p2;
    
            p2.x = 10;
            p2.y = 20;
    
            p1 = p2;   // copy struct
    
            p2.x = 99;
            p2.y = 88;
    
            printInt(p1.x);
            printInt(p1.y);
            printInt(p2.x);
            printInt(p2.y);
        }
        """
        assert CodeGenerator().generate_and_run(source) == "10209988"
def test_134():
        source = """
        struct Point {
            int x;
            int y;
        };
    
        void main() {
            Point a;
            Point b;
    
            a = b = {1, 2};
    
            printInt(a.x);
            printInt(a.y);
            printInt(b.x);
            printInt(b.y);
        }
        """
        assert CodeGenerator().generate_and_run(source) == "1212"
def test_135():
        source = """
        struct A { int x; };
        struct B { A a; };
        struct C { B b; };
        struct D { C c; };
    
        void main() {
            D d1;
            D d2;
    
            d2.c.b.a.x = 10;
    
            d1 = d2 = d2;
    
            printInt(d1.c.b.a.x);
            printInt(d2.c.b.a.x);
    
            d2.c.b.a.x = d2.c.b.a.x + d2.c.b.a.x - 10 + 10;
    
            printInt(d1.c.b.a.x);
            printInt(d2.c.b.a.x);
        }
        """
        assert CodeGenerator().generate_and_run(source) == "10101020"

def test_151():
        source = """
        struct Point {
            int x;
            int y;
            int c;
            int d;
        };
        void main(){
            Point p;
            p.d = 2;
            Point p1 = p;
            p1.d = 3;
            printInt(p.d);
        }
        """
        assert CodeGenerator().generate_and_run(source) == "2"
def test_154():
        source = """
        struct Point {
            int x;
        };
    
        void change(Point p){
            p.x = 99;
        }
    
        void main(){
            Point a;
            a.x = 10;
    
            change(a);
    
            printInt(a.x);
        }
        """
        assert CodeGenerator().generate_and_run(source) == "10"
