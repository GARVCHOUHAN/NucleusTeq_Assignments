package session1.oop;

public class Student {

    // Encapsulation (private variables)
    private String name;
    private int rollNo;
    private double marks;

    public Student(String name, int rollNo, double marks) {
        this.name = name;
        this.rollNo = rollNo;
        this.marks = marks;
    }

    public void display() {
        System.out.println(name + " " + rollNo + " " + marks);
    }
}