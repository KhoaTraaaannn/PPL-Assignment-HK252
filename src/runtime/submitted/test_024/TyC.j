.source TyC.java
.class public TyC
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
.var 1 is p LPoint; from Label2 to Label3
	new Point
	dup
	invokespecial Point/<init>()V
	astore_1
.var 2 is a I from Label2 to Label3
	iconst_0
	istore_2
	aload_1
	iconst_3
	dup_x1
	putfield Point/y I
	dup
	istore_2
	pop
	iload_2
	invokestatic io/printInt(I)V
	aload_1
	getfield Point/y I
	invokestatic io/printInt(I)V
Label3:
	return
Label1:
.limit stack 3
.limit locals 3
.end method
