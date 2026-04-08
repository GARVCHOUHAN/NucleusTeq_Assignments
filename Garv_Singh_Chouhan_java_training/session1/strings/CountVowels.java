package session1.strings;

public class CountVowels {
    public static int countVowels(String str) {
    int count = 0;
    for (char c : str.toLowerCase().toCharArray()) {
        if ("aeiou".indexOf(c) != -1) count++;
    }
    return count;
}

    public static void main(String[] args) {
        String input = "Hello World";
        System.out.println("Number of vowels in \"" + input + "\": " + countVowels(input));
    }
}
