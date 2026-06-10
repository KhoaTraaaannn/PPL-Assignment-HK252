.source TyC.java
.class public TyC
.super java/lang/Object

.method public static add(II)I
Label0:
.var 0 is a I from Label0 to Label1
.var 1 is b I from Label0 to Label1
Label2:
	iload_0
	iload_1
	iadd
	ireturn
Label3:
	iconst_0
	ireturn
Label1:
.limit stack 2
.limit locals 2
.end method

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
	bipush 20
	bipush 22
	invokestatic TyC/add(II)I
	invokestatic io/printInt(I)V
Label3:
	return
Label1:
.limit stack 2
.limit locals 1
.end method
