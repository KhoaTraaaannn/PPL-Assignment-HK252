from utils import Tokenizer

## python3 -m pytest -vv --timeout=3 tests/test_lexer.py
def test_001():
    source = """\t\r\n
    /* This is a block comment so // has no meaning here */
    // VOTIEN
"""
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_002():
    source = "@"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False, "Expected ErrorToken but no exception was raised"
    except Exception as e:
        assert str(e) == "Error Token @"

def test_003():
    source = "auto auto1"
    expected = "auto,auto1,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_004():
    source = "+ ++"
    expected = "+,++,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_005():
    source = "votien123"
    expected = "votien123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_006():
        source = "0   100   255   2500   -45"
        expected = "0,100,255,2500,-,45,EOF"
        assert Tokenizer(source).get_tokens_as_string() == expected

def test_007():
        source = "0.0   3.14   -2.5   1.23e4   5.67E-2   1.   .5"
        expected = "0.0,3.14,-,2.5,1.23e4,5.67E-2,1.,.5,EOF"
        assert Tokenizer(source).get_tokens_as_string() == expected

def test_008():
    source = """
    "This is a string containing tab \\t"
    "He asked me: \\"Where is John?\\""
"""
    expected = "This is a string containing tab \\t,He asked me: \\\"Where is John?\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_009():
        source = """
        "This is a string \n containing tab \\t"
    """
        try:
            Tokenizer(source).get_tokens_as_string()
            assert False, "Expected ErrorToken but no exception was raised"
        except Exception as e:
            assert str(e) == "Unclosed String: This is a string "
def test_010():
    source = """
    "This is a string \\z containing tab \\t"
"""
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False, "Expected ErrorToken but no exception was raised"
    except Exception as e:
        assert str(e) == "Illegal Escape In String: This is a string \\z"
def test_011():
        source = '.e-2'
        expected = '.,e,-,2,EOF'
        assert Tokenizer(source).get_tokens_as_string() == expected
def test_012():
    source = "int float string void"
    expected = "int,float,string,void,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_013():
    source = "if else while for return break continue"
    expected = "if,else,while,for,return,break,continue,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_014():
    source = "struct switch case default"
    expected = "struct,switch,case,default,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_015():
    source = "&& || ! == != <= >= < > ="
    expected = "&&,||,!,==,!=,<=,>=,<,>,=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_016():
    source = "+ - * / % ++ --"
    expected = "+,-,*,/,%,++,--,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_017():
    source = "{ } ( ) ; , : ."
    expected = "{,},(,),;,,,:,.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_018():
    source = "_a _A a_1 A1_2"
    expected = "_a,_A,a_1,A1_2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_019():
    source = "___ __123 abc_123"
    expected = "___,__123,abc_123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
def test_020():
    source = "0 00 0123"
    expected = "0,00,0123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_021():
    source = "1e4 2E3 3e-2 4E+5"
    expected = "1e4,2E3,3e-2,4E+5,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_022():
    source = "1.0 .0 0. .5"
    expected = "1.0,.0,0.,.5,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_023():
    source = "10.5e2 3.14E-2"
    expected = "10.5e2,3.14E-2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_024():
    source = "\"\""
    expected = ",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_025():
    source = "\"abc\" \"123\""
    expected = "abc,123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_026():
    source = "\"\\\\ \\\"\""
    expected = "\\\\ \\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_027():
    source = "\"\\n\\t\\r\""
    expected = "\\n\\t\\r,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_028():
    source = "\"Unclosed string"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Unclosed String: Unclosed string"

def test_029():
    source = "\"Illegal \\q escape\""
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Illegal Escape In String: Illegal \\q"
def test_030():
    source = "/* block comment */ 123"
    expected = "123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_031():
    source = "// line comment\n456"
    expected = "456,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_032():
    source = "/* comment */ // comment \n auto"
    expected = "auto,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_033():
    source = "a/*c*/b"
    expected = "a,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_034():
        source = "/* outer /* inner */ still comment */ boolean c"
        expected = "still,comment,*,/,boolean,c,EOF"
        assert Tokenizer(source).get_tokens_as_string() == expected

def test_035():
    source = "@@"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Error Token @"

def test_036():
    source = "#"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Error Token #"

def test_037():
    source = "123abc"
    expected = "123,abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_038():
    source = "abc123.45"
    expected = "abc123,.45,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_039():
    source = "   \t \n  "
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
def test_040():
    source = "a=b=c"
    expected = "a,=,b,=,c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_041():
    source = "a==b=c"
    expected = "a,==,b,=,c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_042():
    source = "a<=b>=c"
    expected = "a,<=,b,>=,c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_043():
    source = "a<b>c"
    expected = "a,<,b,>,c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_044():
    source = "a&&b&&c"
    expected = "a,&&,b,&&,c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_045():
    source = "a||b||c"
    expected = "a,||,b,||,c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_046():
    source = "!a!!b"
    expected = "!,a,!,!,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_047():
    source = "++a--"
    expected = "++,a,--,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_048():
    source = "a+++b"
    expected = "a,++,+,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_049():
    source = "--a++"
    expected = "--,a,++,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_050():
    source = "a.b.c.d"
    expected = "a,.,b,.,c,.,d,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_051():
    source = "func(1,2,3)"
    expected = "func,(,1,,,2,,,3,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_052():
    source = "(a+b)*(c-d)"
    expected = "(,a,+,b,),*,(,c,-,d,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_053():
    source = "{a;b;c;}"
    expected = "{,a,;,b,;,c,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_054():
    source = "for(i=0;i<10;i++)"
    expected = "for,(,i,=,0,;,i,<,10,;,i,++,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_055():
    source = "while(x!=0)"
    expected = "while,(,x,!=,0,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_056():
    source = "switch(x){case 1:break;default:break;}"
    expected = "switch,(,x,),{,case,1,:,break,;,default,:,break,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_057():
    source = "return x+y*z;"
    expected = "return,x,+,y,*,z,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_058():
    source = "auto x=readInt();"
    expected = "auto,x,=,readInt,(,),;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_059():
    source = "printString(\"Hello\")"
    expected = "printString,(,Hello,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
def test_060():
    source = "a=b+--c"
    expected = "a,=,b,+,--,c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_061():
    source = "a---b"
    expected = "a,--,-,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_062():
    source = "a++++b"
    expected = "a,++,++,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_063():
    source = "!~"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Error Token ~"


def test_064():
    source = "123 45.67 8.9e10"
    expected = "123,45.67,8.9e10,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_065():
    source = ".e+3"
    expected = ".,e,+,3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_066():
    source = "0.e1"
    expected = "0.e1,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_067():
    source = "1..2"
    expected = "1.,.2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_068():
    source = "\"a\"\"b\"\"c\""
    expected = "a,b,c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_069():
    source = "\"abc"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Unclosed String: abc"

def test_070():
    source = "\"a\\\\b\""
    expected = "a\\\\b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_071():
    source = "\"a\\\"b\""
    expected = "a\\\"b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_072():
    source = "/* comment /* nested */ end */ 1"
    expected = "end,*,/,1,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_073():
    source = "/* comment // still comment */ 2"
    expected = "2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_074():
    source = "// comment /* block */\n3"
    expected = "3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_075():
    source = "/* unclosed comment"
    expected = "/,*,unclosed,comment,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_076():
    source = "____"
    expected = "____,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_077():
    source = "_1_2_3"
    expected = "_1_2_3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_078():
    source = "a@b"
    try:
        Tokenizer(source).get_tokens_as_string()
        assert False
    except Exception as e:
        assert str(e) == "Error Token @"


def test_079():
    source = "\n\t\r"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
def test_080():
    source = "auto x=1;"
    expected = "auto,x,=,1,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_081():
    source = "float y=1.23;"
    expected = "float,y,=,1.23,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_082():
    source = ".e-2"
    expected = ".,e,-,2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_083():
    source = "1e-2+3"
    expected = "1e-2,+,3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_084():
    source = "a=b*c+d/e-f%g"
    expected = "a,=,b,*,c,+,d,/,e,-,f,%,g,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_085():
    source = "++--a"
    expected = "++,--,a,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_086():
    source = "a--++"
    expected = "a,--,++,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_087():
    source = "\"\"\"\""
    expected = ",,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_088():
    source = "\"abc\"//comment"
    expected = "abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_089():
    source = "\"abc\"/*comment*/\"def\""
    expected = "abc,def,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_090():
    source = "struct A{int x;}"
    expected = "struct,A,{,int,x,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_091():
    source = "switch(x){case 1:break;}"
    expected = "switch,(,x,),{,case,1,:,break,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_092():
        source =  """ "a\\\n """
        try:
            Tokenizer(source).get_tokens_as_string()
            assert False, "Expected ErrorToken but no exception was raised"
        except Exception as e:
            assert str(e) == "Unclosed String: a\\"


def test_093():
    source = "continue;"
    expected = "continue,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_094():
    source = "return;"
    expected = "return,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_095():
    source = "main(){"
    expected = "main,(,),{,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_096():
    source = "x.y.z"
    expected = "x,.,y,.,z,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_097():
    source = "123/*comment*/456"
    expected = "123,456,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_098():
    source = "\"a\\tb\""
    expected = "a\\tb,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_099():
    source = "\"a\\fb\""
    expected = "a\\fb,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_100():
    source = " \n\t /* all ignored */ "
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
