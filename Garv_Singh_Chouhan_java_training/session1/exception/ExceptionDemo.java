package session1.exception;
// exception handling is done by using try-catch blocks. We can catch specific exceptions or use a generic Exception class to catch all exceptions.
public class ExceptionDemo {

    public static void main(String[] args) {
        try {
            int result = 10 / 0;
        } catch (ArithmeticException e) {
            System.out.println("Cannot divide by zero");
        } finally {
            System.out.println("Execution finished");
        }
    }
}