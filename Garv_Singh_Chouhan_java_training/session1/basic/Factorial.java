package session1.basic;

public class Factorial {

    public static int factorial(int n) {
        if (n < 0) return -1; // validation
        int result = 1;

        for (int i = 1; i <= n; i++) {
            result *= i;
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(factorial(5));
    }
}
