package session1.controlflow;

public class LargestNumber {

    public static int findLargest(int a, int b, int c) {
        if (a >= b && a >= c) return a;
        else if (b >= c) return b;
        else return c;
    }
}
