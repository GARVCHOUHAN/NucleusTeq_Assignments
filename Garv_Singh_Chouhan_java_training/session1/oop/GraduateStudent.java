package session1.oop;

public class GraduateStudent extends Student {

    private String specialization;

    public GraduateStudent(String name, int rollNo, double marks, String specialization) {
        super(name, rollNo, marks);
        this.specialization = specialization;
    }

    // Polymorphism (method overriding)
    @Override
    public void display() {
        super.display();
        System.out.println("Specialization: " + specialization);
    }
}