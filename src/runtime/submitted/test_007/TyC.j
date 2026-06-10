.source TyC.java
.class public TyC
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
	iconst_1
	iconst_2
	if_icmpge Label4
	iconst_1
	goto Label5
Label4:
	iconst_0
Label5:
	ifle Label6
	ldc "yes"
	invokestatic io/printString(Ljava/lang/String;)V
	goto Label7
Label6:
	ldc "no"
	invokestatic io/printString(Ljava/lang/String;)V
Label7:
Label3:
	return
Label1:
.limit stack 2
.limit locals 1
.end method
