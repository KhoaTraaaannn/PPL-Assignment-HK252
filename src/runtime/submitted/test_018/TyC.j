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
	iconst_5
	if_icmpge Label7
	iconst_1
	goto Label8
Label7:
	iconst_0
Label8:
	ifle Label5
Label9:
	iload_1
	iconst_1
	iadd
	dup
	istore_1
	pop
	iload_1
	iconst_2
	if_icmpne Label11
	iconst_1
	goto Label12
Label11:
	iconst_0
Label12:
	ifle Label13
Label15:
	goto Label4
Label16:
	goto Label14
Label13:
Label14:
	iload_1
	iconst_4
	if_icmpne Label17
	iconst_1
	goto Label18
Label17:
	iconst_0
Label18:
	ifle Label19
Label21:
	goto Label5
Label22:
	goto Label20
Label19:
Label23:
	iload_1
	invokestatic io/printInt(I)V
Label24:
Label20:
Label10:
Label4:
	goto Label6
Label5:
Label3:
	return
Label1:
.limit stack 4
.limit locals 2
.end method
