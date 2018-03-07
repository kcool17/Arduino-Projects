import java.util.Scanner;
public class MathPractice {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner input=new Scanner(System.in);
		System.out.println("Please input 2 values.");
		double userInput1=input.nextDouble();
		double userInput2=input.nextDouble();
		System.out.println("Sum: "+(userInput1+userInput2));
		System.out.println("Difference: "+(userInput1-userInput2));
		System.out.println("Product: "+(userInput1*userInput2));
		System.out.println("Average: "+((userInput1+userInput2)/2));
		System.out.println("Distance: "+(Math.abs(userInput1-userInput2)));
		System.out.println("Minumum: "+(Math.min(userInput1,userInput2)));
		System.out.println("Maximum: "+(Math.max(userInput1,userInput2)));
	}

}
