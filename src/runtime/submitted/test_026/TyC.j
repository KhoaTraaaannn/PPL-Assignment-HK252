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
.var 2 is b F from Label2 to Label3
	fconst_0
	fstore_2
.var 3 is c Ljava/lang/String; from Label2 to Label3
	ldc ""
	astore_3
	iload_1
	invokestatic io/printInt(I)V
	fload_2
	invokestatic io/printFloat(F)V
	aload_3
	invokestatic io/printString(Ljava/lang/String;)V
Label3:
	return
Label1:
.limit stack 1
.limit locals 4
.end method
