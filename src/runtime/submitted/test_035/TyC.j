.source TyC.java
.class public TyC
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
Label0:
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label2:
.var 1 is p1 LPoint; from Label2 to Label3
	new Point
	dup
	invokespecial Point/<init>()V
	astore_1
	aload_1
	bipush 10
	dup_x1
	putfield Point/x I
	pop
	aload_1
	bipush 20
	dup_x1
	putfield Point/y I
	pop
.var 2 is p2 LPoint; from Label2 to Label3
	new Point
	dup
	bipush 30
	bipush 40
	invokespecial Point/<init>(II)V
	astore_2
	aload_2
	getfield Point/x I
	invokestatic io/printInt(I)V
	aload_2
	getfield Point/y I
	invokestatic io/printInt(I)V
	aload_2
	dup
	astore_1
	pop
.var 3 is person1 LPerson; from Label2 to Label3
	new Person
	dup
	ldc "John"
	bipush 25
	ldc 1.7500
	invokespecial Person/<init>(Ljava/lang/String;IF)V
	astore_3
	aload_3
	getfield Person/name Ljava/lang/String;
	invokestatic io/printString(Ljava/lang/String;)V
	aload_3
	getfield Person/age I
	invokestatic io/printInt(I)V
	aload_3
	getfield Person/height F
	invokestatic io/printFloat(F)V
	aload_3
	bipush 26
	dup_x1
	putfield Person/age I
	pop
	aload_3
	ldc 1.7600
	dup_x1
	putfield Person/height F
	pop
.var 4 is p3 LPoint; from Label2 to Label3
	aload_2
	astore 4
	aload 4
	getfield Point/x I
	invokestatic io/printInt(I)V
Label3:
	return
Label1:
.limit stack 5
.limit locals 5
.end method
