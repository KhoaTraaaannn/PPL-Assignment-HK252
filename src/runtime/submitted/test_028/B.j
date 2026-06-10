.source B.java
.class public B
.super java/lang/Object
	.field a LA;

.method public <init>()V
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	aload_0
	new A
	dup
	invokespecial A/<init>()V
	putfield B/a LA;
	return
Label1:
.limit stack 3
.limit locals 1
.end method

.method public <init>(LA;)V
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	aload_0
	aload_1
	putfield B/a LA;
	return
Label1:
.limit stack 3
.limit locals 2
.end method
