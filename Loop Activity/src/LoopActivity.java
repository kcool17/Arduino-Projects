import java.util.Scanner;
public class LoopActivity {

	public static void multTable() {
		int x=1;
		int y=1;
		int printVar;
		int printSpace;
		while (y<=10) {
			while (x<=10) {
				printVar=x*y;
				if (printVar<10) {
					printSpace = 2;
				} else if (printVar<100) {
					printSpace = 1;
				}else {
					printSpace = 0;
				}
				System.out.print(" ");
				while (printSpace>0) {
					System.out.print(" ");
					printSpace= printSpace-1;
				}
				System.out.print("" + printVar);
				x=x+1;
			}
			y=y+1;
			x=1;
			System.out.println();
		}
	}
	public static void primesBefore(int maxPrime) {
		boolean notPrime = false;
		for(int toTest=2; toTest<=maxPrime; toTest++) {
			notPrime = false;
			for(int tester=2; tester<=toTest/2; tester++) {
				if (toTest%tester==0) {
					notPrime = true;
					break;
				}
			}
			if(!notPrime) {
				System.out.print(toTest +", ");
			}
		}
	}
	public static void binPrint(int decimal) {
		while (decimal>0) {
			System.out.print(decimal%2);
			decimal = decimal / 2;
		}
	}
	public static void powerOf2(int maxPower) {
		for(int x = 0; x<=maxPower;x++) {
			System.out.print((int)Math.pow(2, x)+", ");
		}
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner input = new Scanner(System.in);
		System.out.println("What is the max value you want to test for prime numbers?");
		int userInput = input.nextInt();
		primesBefore(userInput);
		System.out.println("\n\nWhat do you want to convert to binary?");
		userInput = input.nextInt();
		binPrint(userInput);
		System.out.println("\n\nWhat is the max value you want to find the power of 2 for?");
		userInput = input.nextInt();
		powerOf2(userInput);
		System.out.println("\n\nHere's a multiplication table!\n");
		multTable();
		input.close();
	}

}
