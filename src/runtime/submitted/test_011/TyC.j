.source TyC.java
.class public TyC
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
	iconst_1
	i2f
	ldc 1.2000
	fadd
	invokestatic io/printFloat(F)V
	ldc 1.1000
	iconst_2
	i2f
	fmul
	invokestatic io/printFloat(F)V
Label3:
	return
Label1:
.limit stack 2
.limit locals 1
.end method
