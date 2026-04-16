package session1.datatypes;

public class TemperatureConverter {

    public static double cToF(double c) {
        return (c * 9/5) + 32;
    }

    public static double fToC(double f) {
        return (f - 32) * 5/9;
    }
}
