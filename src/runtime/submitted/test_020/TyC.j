.source TyC.java
.class public TyC
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
.var 1 is x I from Label2 to Label3
	iconst_3
	istore_1
	iload_1
	iconst_1
	if_icmpne Label10
	iconst_1
	goto Label11
Label10:
	iconst_0
Label11:
	ifgt Label6
	iload_1
	iconst_3
	if_icmpne Label12
	iconst_1
	goto Label13
Label12:
	iconst_0
Label13:
	ifgt Label7
	iload_1
	iconst_5
	if_icmpne Label14
	iconst_1
	goto Label15
Label14:
	iconst_0
Label15:
	ifgt Label8
	goto Label9
Label6:
	iconst_1
	invokestatic io/printInt(I)V
Label7:
	iconst_3
	invokestatic io/printInt(I)V
Label8:
	iconst_5
	invokestatic io/printInt(I)V
Label9:
	bipush 7
	invokestatic io/printInt(I)V
Label5:
Label3:
	return
Label1:
.limit stack 4
.limit locals 2
.end method
