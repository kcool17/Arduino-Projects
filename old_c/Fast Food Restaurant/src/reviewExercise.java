import java.util.Scanner;
public class reviewExercise {
	static Scanner input = new Scanner(System.in);
	public static void R2_15(){
		System.out.println("Enter a string:");
		String userInput=input.nextLine();
		System.out.printf("%-12s%1c\n", "First Char: ", userInput.charAt(0));
		System.out.printf("%-12s%1c\n", "Last Char: ", userInput.charAt(userInput.length()-1));
		System.out.printf("%-20s%"+userInput.length()+"s\n", "Removed First Char: ", userInput.substring(1));
		System.out.printf("%-20s%"+userInput.length()+"s\n", "Removed Last Char: ", userInput.substring(0, userInput.length()-1));
	}
	public static void R2_14() {
		System.out.println("Enter a string:");
		String str=input.nextLine();
		System.out.println("Enter a position:");
		int i=input.nextInt();
		System.out.println("Enter another position:");
		int j=input.nextInt();
		String first=str.substring(0,i);
		String middle=str.substring(i+1,j);
		String last=str.substring(j+1);
		System.out.println(first+str.charAt(i)+middle+str.charAt(j)+last);

	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("R2.15");
		R2_15();
		System.out.println("\nR2.14");
		R2_14();
		input.close();
	}

}
