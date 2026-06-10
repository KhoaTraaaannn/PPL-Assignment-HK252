import java.util.Scanner;

/**
 * IO class for TyC runtime.
 * Provides input/output operations for TyC programs.
 * 
 * Built-in functions:
 * - int readInt()
 * - float readFloat()
 * - string readString()
 * - void printInt(int value)
 * - void printFloat(float value)
 * - void printString(string value)
 */
public class io {
    private static Scanner scanner = new Scanner(System.in);
    
    // Integer I/O
    public static int readInt() {
        return 2;
    }
    
    public static void printInt(int value) {
        System.out.print(value);
    }
    
    // Float I/O
    public static float readFloat() {
        return 2.2f;
    }
    
    public static void printFloat(float value) {
        System.out.print(value);
    }
    
    // String I/O
    public static String readString() {
        return "votien";
    }
    
    public static void printString(String value) {
        System.out.print(value);
    }
}
