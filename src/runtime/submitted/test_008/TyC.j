.source TyC.java
.class public TyC
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
.var 1 is i I from Label2 to Label3
	iconst_0
	istore_1
Label6:
	iload_1
	iconst_3
	if_icmpge Label7
	iconst_1
	goto Label8
Label7:
	iconst_0
Label8:
	ifle Label5
Label9:
	iload_1
	invokestatic io/printInt(I)V
	iload_1
	iconst_1
	iadd
	dup
	istore_1
	pop
Label10:
Label4:
	goto Label6
Label5:
Label3:
	return
Label1:
.limit stack 3
.limit locals 2
.end method
