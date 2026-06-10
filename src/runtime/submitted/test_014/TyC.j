.source TyC.java
.class public TyC
.super java/lang/Object

.method public static foo()I
Label0:
Label2:
	iconst_1
	invokestatic io/printInt(I)V
	iconst_1
	ireturn
Label3:
	iconst_0
	ireturn
Label1:
.limit stack 1
.limit locals 0
.end method

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
	iconst_1
	dup
	ifgt Label4
	iconst_0
	goto Label5
Label4:
	invokestatic TyC/foo()I
Label5:
	iand
	invokestatic io/printInt(I)V
	iconst_1
	ifle Label6
	iconst_1
	goto Label7
	pop
Label6:
	invokestatic TyC/foo()I
Label7:
	invokestatic io/printInt(I)V
Label3:
	return
Label1:
.limit stack 3
.limit locals 1
.end method
