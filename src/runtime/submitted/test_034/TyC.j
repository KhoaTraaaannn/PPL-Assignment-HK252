.source TyC.java
.class public TyC
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
.var 1 is x I from Label2 to Label3
	invokestatic io/readInt()I
	istore_1
.var 2 is y F from Label2 to Label3
	invokestatic io/readFloat()F
	fstore_2
.var 3 is name Ljava/lang/String; from Label2 to Label3
	invokestatic io/readString()Ljava/lang/String;
	astore_3
.var 4 is sum F from Label2 to Label3
	fconst_0
	fstore 4
	iload_1
	i2f
	fload_2
	fadd
	dup
	fstore 4
	pop
.var 5 is count I from Label2 to Label3
	iconst_0
	istore 5
.var 6 is total F from Label2 to Label3
	fconst_0
	fstore 6
.var 7 is greeting Ljava/lang/String; from Label2 to Label3
	ldc "Hello, "
	astore 7
.var 8 is i I from Label2 to Label3
	iconst_0
	istore 8
.var 9 is f F from Label2 to Label3
	fconst_0
	fstore 9
	invokestatic io/readInt()I
	dup
	istore 8
	pop
	invokestatic io/readFloat()F
	dup
	fstore 9
	pop
	fload 4
	invokestatic io/printFloat(F)V
	aload 7
	invokestatic io/printString(Ljava/lang/String;)V
	aload_3
	invokestatic io/printString(Ljava/lang/String;)V
Label3:
	return
Label1:
.limit stack 2
.limit locals 10
.end method
