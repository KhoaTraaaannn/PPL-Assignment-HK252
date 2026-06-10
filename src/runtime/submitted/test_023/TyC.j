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
	aload_1
	iconst_2
	dup_x1
	putfield Point/x I
	pop
	aload_1
	getfield Point/x I
	invokestatic io/printInt(I)V
Label3:
	return
Label1:
.limit stack 3
.limit locals 2
.end method
