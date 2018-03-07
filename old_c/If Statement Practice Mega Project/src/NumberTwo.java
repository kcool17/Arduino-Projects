import java.util.Scanner;
public class NumberTwo {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner input = new Scanner(System.in);
		System.out.println("Input a number:");
		double x = input.nextDouble();
		System.out.println("Input another number:");
		double y = input.nextDouble();
		System.out.println("Input yet another number:");
		double z = input.nextDouble();
		if (x+y>z || x+z>y || y+z>x) {
			System.out.println("These could be sides to a Triangle!");
		}else {
			System.out.println("Error NaT (Not a Triangle)");
		}
		input.close();
	}

}
