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
	getfield Point/x I
	invokestatic io/printInt(I)V
	aload_1
	getfield Point/y F
	invokestatic io/printFloat(F)V
	aload_1
	getfield Point/z Ljava/lang/String;
	invokestatic io/printString(Ljava/lang/String;)V
Label3:
	return
Label1:
.limit stack 2
.limit locals 2
.end method
