.source A.java
.class public A
.super java/lang/Object
	.field x I

.method public <init>()V
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	aload_0
	iconst_0
	putfield A/x I
	return
Label1:
.limit stack 3
.limit locals 1
.end method

.method public <init>(I)V
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	aload_0
	iload_1
	putfield A/x I
	return
Label1:
.limit stack 3
.limit locals 2
.end method
