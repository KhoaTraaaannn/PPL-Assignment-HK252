.source TyC.java
.class public TyC
.super java/lang/Object

.method public static add(II)I
Label0:
.var 0 is x I from Label0 to Label1
.var 1 is y I from Label0 to Label1
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

.method public static multiply(II)I
Label0:
.var 0 is x I from Label0 to Label1
.var 1 is y I from Label0 to Label1
Label2:
	iload_0
	iload_1
	imul
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
.var 1 is a I from Label2 to Label3
	invokestatic io/readInt()I
	istore_1
.var 2 is b I from Label2 to Label3
	invokestatic io/readInt()I
	istore_2
.var 3 is sum I from Label2 to Label3
	iload_1
	iload_2
	invokestatic TyC/add(II)I
	istore_3
.var 4 is product I from Label2 to Label3
	iload_1
	iload_2
	invokestatic TyC/multiply(II)I
	istore 4
	iload_3
	invokestatic io/printInt(I)V
	iload 4
	invokestatic io/printInt(I)V
Label3:
	return
Label1:
.limit stack 2
.limit locals 5
.end method
