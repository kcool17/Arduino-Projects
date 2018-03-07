import java.util.Scanner;
public class MeterConversion {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner scanner= new Scanner(System.in);//Creates a scanner object
		double meters;
		System.out.print("How many meters do you want to convert? ");
		meters = scanner.nextDouble();//Scans for user input for the meters to convert
		System.out.printf("\n"+(meters*3.3)+" Feet");//Converts to feet, and prints
		System.out.printf("\n"+(meters*0.00062)+" Miles");//Converts to miles, and prints
		System.out.printf("\n"+(meters*39.37)+" Inches");//Converts to Inches, and prints
		scanner.close();//Closes the scanner
	}

}
