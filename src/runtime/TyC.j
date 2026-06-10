.source TyC.java
.class public TyC
.super java/lang/Object

.method public static change(LPoint;)V
Label0:
.var 0 is p LPoint; from Label0 to Label1
	aload_0
	dup
	bipush 99
	dup_x1
	putfield Point/x I
	pop
	return
Label1:
.limit stack 4
.limit locals 1
.end method

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
.var 1 is a LPoint; from Label0 to Label1
	new Point
	dup
	invokespecial Point/<init>()V
	dup
	iconst_0
	putfield Point/x I
	astore_1
	aload_1
	dup
	bipush 10
	dup_x1
	putfield Point/x I
	pop
	aload_1
	astore_2
	new Point
	dup
	invokespecial Point/<init>()V
	dup
	iconst_0
	putfield Point/x I
	dup
	aload_2
	getfield Point/x I
	putfield Point/x I
	invokestatic TyC/change(LPoint;)V
	aload_1
	getfield Point/x I
	invokestatic io/printInt(I)V
	return
Label1:
.limit stack 4
.limit locals 3
.end method
