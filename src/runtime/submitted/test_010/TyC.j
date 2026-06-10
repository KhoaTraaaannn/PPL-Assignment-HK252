.source TyC.java
.class public TyC
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
.var 1 is x I from Label2 to Label3
	bipush 10
	istore_1
.var 2 is y I from Label2 to Label3
	bipush 20
	istore_2
	iload_1
	iload_2
	iadd
	invokestatic io/printInt(I)V
Label3:
	return
Label1:
.limit stack 2
.limit locals 3
.end method
