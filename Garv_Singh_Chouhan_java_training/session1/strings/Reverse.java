package session1.strings;
// here i have used StringBuilder to reverse the string, which is more efficient than using a loop to concatenate characters in reverse order.
public class Reverse {
    public static String reverse(String str) {
        return new StringBuilder(str).reverse().toString();
    }

    public static void main(String[] args) {
        String str = "Hello, World!";
        System.out.println(reverse(str));
    }
}
