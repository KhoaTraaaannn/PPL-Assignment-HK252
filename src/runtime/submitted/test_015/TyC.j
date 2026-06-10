.source TyC.java
.class public TyC
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
	iconst_0
	ifgt Label4
	iconst_1
	goto Label5
Label4:
	iconst_0
Label5:
	invokestatic io/printInt(I)V
	iconst_2
	ineg
	ineg
	ineg
	invokestatic io/printInt(I)V
Label3:
	return
Label1:
.limit stack 4
.limit locals 1
.end method
