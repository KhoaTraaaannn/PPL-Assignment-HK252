.source TyC.java
.class public TyC
.super java/lang/Object

.method public static factorial(I)I
Label0:
.var 0 is n I from Label0 to Label1
Label2:
	iload_0
	iconst_1
	if_icmpgt Label4
	iconst_1
	goto Label5
Label4:
	iconst_0
Label5:
	ifle Label6
Label8:
	iconst_1
	ireturn
Label9:
	goto Label7
Label6:
Label10:
	iload_0
	iload_0
	iconst_1
	isub
	invokestatic TyC/factorial(I)I
	imul
	ireturn
Label11:
Label7:
Label3:
	iconst_0
	ireturn
Label1:
.limit stack 4
.limit locals 1
.end method

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
.var 1 is num I from Label2 to Label3
	bipush 10
	istore_1
.var 2 is result I from Label2 to Label3
	iload_1
	invokestatic TyC/factorial(I)I
	istore_2
	iload_2
	invokestatic io/printInt(I)V
Label3:
	return
Label1:
.limit stack 1
.limit locals 3
.end method
