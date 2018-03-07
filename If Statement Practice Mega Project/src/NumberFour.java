import java.util.Scanner;
public class NumberFour {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner input = new Scanner(System.in);
		boolean overlap;
		
		System.out.println("Input the event 1 start time (24 Hour time):");
		double startOne = input.nextDouble();
		System.out.println("Input the event 1 end time (24 Hour time):");
		double endOne = input.nextDouble();
		System.out.println("Input the event 2 start time (24 Hour time):");
		double startTwo = input.nextDouble();
		System.out.println("Input the event 2 end time (24 Hour time):");
		double endTwo = input.nextDouble();
		
		if (startOne>startTwo && startOne<endTwo) {
			overlap = true;
		}else if (endOne>startTwo && endOne<endTwo) {
			overlap = true;
		}else if (startTwo>startOne && startTwo<endOne) {
			overlap = true;
		}else if (endTwo>startOne && endTwo<endOne) {
			overlap = true;
		}else {
			overlap = false;
		}
		
		if (overlap == true) {
			System.out.println("They overlap.");
		}else {
			System.out.println("They do not overlap.");
		}
		input.close();
	}

}
