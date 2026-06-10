.source TyC.java
.class public TyC
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
.var 1 is a I from Label2 to Label3
	iconst_0
	istore_1
.var 2 is b I from Label2 to Label3
	iconst_0
	istore_2
Label4:
	iconst_1
	dup
	istore_2
	dup
	istore_1
	pop
Label5:
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
