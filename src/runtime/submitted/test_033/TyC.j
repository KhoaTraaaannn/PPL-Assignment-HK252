.source TyC.java
.class public TyC
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
.var 1 is n I from Label2 to Label3
	bipush 10
	istore_1
.var 2 is i I from Label2 to Label3
	iconst_0
	istore_2
Label6:
	iload_2
	iload_1
	if_icmpge Label7
	iconst_1
	goto Label8
Label7:
	iconst_0
Label8:
	ifle Label5
Label9:
	iload_2
	invokestatic io/printInt(I)V
iinc 2 1
	iload_2
	pop
Label10:
Label4:
	goto Label6
Label5:
.var 3 is j I from Label2 to Label3
	iconst_0
	istore_3
Label13:
	iload_3
	iload_1
	if_icmpge Label14
	iconst_1
	goto Label15
Label14:
	iconst_0
Label15:
	ifle Label12
Label16:
	iload_3
	iconst_2
	irem
	iconst_0
	if_icmpne Label18
	iconst_1
	goto Label19
Label18:
	iconst_0
Label19:
	ifle Label20
Label22:
	iload_3
	invokestatic io/printInt(I)V
Label23:
	goto Label21
Label20:
Label21:
Label17:
Label11:
iinc 3 1
	iload_3
	pop
	goto Label13
Label12:
Label3:
	return
Label1:
.limit stack 4
.limit locals 4
.end method
