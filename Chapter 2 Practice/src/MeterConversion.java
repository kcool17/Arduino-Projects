import java.util.Scanner;
public class MeterConversion {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner scanner= new Scanner(System.in);
		double meters;
		System.out.print("How many meters do you want to convert? ");
		meters = scanner.nextDouble();
		System.out.printf("\n"+(meters*3.3)+" Feet");
		System.out.printf("\n"+(meters*0.00062)+" Miles");
		System.out.printf("\n"+(meters*39.37)+" Inches");
	}

}
