.source Person.java
.class public Person
.super java/lang/Object
	.field name Ljava/lang/String;
	.field age I
	.field height F

.method public <init>()V
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	aload_0
	ldc ""
	putfield Person/name Ljava/lang/String;
	aload_0
	iconst_0
	putfield Person/age I
	aload_0
	fconst_0
	putfield Person/height F
	return
Label1:
.limit stack 3
.limit locals 1
.end method

.method public <init>(Ljava/lang/String;IF)V
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	aload_0
	aload_1
	putfield Person/name Ljava/lang/String;
	aload_0
	iload_2
	putfield Person/age I
	aload_0
	fload_3
	putfield Person/height F
	return
Label1:
.limit stack 3
.limit locals 4
.end method
