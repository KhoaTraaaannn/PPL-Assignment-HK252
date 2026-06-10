.source TyC.java
.class public TyC
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
.var 1 is p LB; from Label2 to Label3
	new B
	dup
	invokespecial B/<init>()V
	astore_1
	aload_1
	getfield B/a LA;
	getfield A/x I
	iconst_1
	iadd
	invokestatic io/printInt(I)V
Label3:
	return
Label1:
.limit stack 2
.limit locals 2
.end method
