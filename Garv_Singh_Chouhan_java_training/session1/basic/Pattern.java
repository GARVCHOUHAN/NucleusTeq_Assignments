package session1.basic;

public class Pattern {

    public static void main(String[] args) {

        // Simple triangle pattern
        for (int i = 1; i <= 5; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print("* ");
            }
            System.out.println();
        }
    }
}
// this will be the output of the above program
/*
*
* *
* * *
* * * *
* * * * *
*/