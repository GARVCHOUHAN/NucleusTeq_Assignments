

package session1.controlflow;

public class SumOfEven {

    public static int sumOfEven(int start, int end) {
        int sum = 0;
        for (int i = start; i <= end; i++) {
            if (i % 2 == 0) {
                sum += i;
            }
        }
        return sum;
    }

    public static void main(String[] args) {
        int start = 1;
        int end = 10;
        System.out.println("Sum of even numbers from " + start + " to " + end + " is " + sumOfEven(start, end));
    }
}


