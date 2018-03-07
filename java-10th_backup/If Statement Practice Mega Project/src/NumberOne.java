import java.util.Scanner;
public class NumberOne {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		double y;
		Scanner input = new Scanner(System.in);
		System.out.println("Input a number:");
		double x = input.nextDouble();
		if (x<0) {
			y = x * -1;
		}else {
			y = x;
		}
		System.out.println("The absolute value is " + y);
		input.close();
	}

}
