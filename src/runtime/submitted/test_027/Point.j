.source Point.java
.class public Point
.super java/lang/Object
	.field x I
	.field y F
	.field z Ljava/lang/String;

.method public <init>()V
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	aload_0
	iconst_0
	putfield Point/x I
	aload_0
	fconst_0
	putfield Point/y F
	aload_0
	ldc ""
	putfield Point/z Ljava/lang/String;
	return
Label1:
.limit stack 3
.limit locals 1
.end method

.method public <init>(IFLjava/lang/String;)V
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	aload_0
	iload_1
	putfield Point/x I
	aload_0
	fload_2
	putfield Point/y F
	aload_0
	aload_3
	putfield Point/z Ljava/lang/String;
	return
Label1:
.limit stack 3
.limit locals 4
.end method
