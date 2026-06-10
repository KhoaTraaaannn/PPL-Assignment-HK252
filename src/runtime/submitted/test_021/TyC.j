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
Label4:
.var 2 is x I from Label4 to Label5
	iconst_2
	istore_2
Label5:
	iload_1
	invokestatic io/printInt(I)V
Label3:
	return
Label1:
.limit stack 1
.limit locals 3
.end method
