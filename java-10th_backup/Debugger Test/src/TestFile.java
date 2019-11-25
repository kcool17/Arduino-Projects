import java.util.Scanner;

public class TestFile {

    public static void main(String[] args)
    {
    	Scanner myScanner = new Scanner("I love noodles haha\nBitch");
    	System.out.println(myScanner.next()); // "I"
    	System.out.println(myScanner.next()); // "love"
    	System.out.println(myScanner.nextLine() + "444"); // "noodles haha"?
    	System.out.println(myScanner.next());
    	myScanner.close();
    }    
    
    public static String getFlag() {
        StringBuilder stringBuilder1 = new StringBuilder("aaa");
        StringBuilder stringBuilder2 = new StringBuilder("aaa");
        StringBuilder stringBuilder3 = new StringBuilder("aaa");
        StringBuilder stringBuilder4 = new StringBuilder("aaa");
        stringBuilder1.setCharAt(0, (char)(stringBuilder1.charAt(0) + '\004'));
        stringBuilder1.setCharAt(1, (char)(stringBuilder1.charAt(1) + '\023'));
        stringBuilder1.setCharAt(2, (char)(stringBuilder1.charAt(2) + '\022'));
        stringBuilder2.setCharAt(0, (char)(stringBuilder2.charAt(0) + '\007'));
        stringBuilder2.setCharAt(1, (char)(stringBuilder2.charAt(1) + Character.MIN_VALUE));
        stringBuilder2.setCharAt(2, (char)(stringBuilder2.charAt(2) + '\001'));
        stringBuilder3.setCharAt(0, (char)(stringBuilder3.charAt(0) + Character.MIN_VALUE));
        stringBuilder3.setCharAt(1, (char)(stringBuilder3.charAt(1) + '\013'));
        stringBuilder3.setCharAt(2, (char)(stringBuilder3.charAt(2) + '\017'));
        stringBuilder4.setCharAt(0, (char)(stringBuilder4.charAt(0) + '\016'));
        stringBuilder4.setCharAt(1, (char)(stringBuilder4.charAt(1) + '\024'));
        stringBuilder4.setCharAt(2, (char)(stringBuilder4.charAt(2) + '\017'));
        return "".concat(stringBuilder3.toString()).concat(stringBuilder2.toString()).concat(stringBuilder1.toString()).concat(stringBuilder4.toString());
    }
}