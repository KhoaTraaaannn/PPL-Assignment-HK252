.source Point.java
.class public Point
.super java/lang/Object
	.field x I
	.field y I

.method public <init>()V
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	aload_0
	iconst_0
	putfield Point/x I
	aload_0
	iconst_0
	putfield Point/y I
	return
Label1:
.limit stack 3
.limit locals 1
.end method

.method public <init>(II)V
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	aload_0
	iload_1
	putfield Point/x I
	aload_0
	iload_2
	putfield Point/y I
	return
Label1:
.limit stack 3
.limit locals 3
.end method
