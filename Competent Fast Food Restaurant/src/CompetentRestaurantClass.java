import java.util.Scanner;
public class CompetentRestaurantClass {
	static double[] menuCost = new double[5];//Declare Menu Cost, for use in other methods
	
	public static void printMenu() {
		//Constants
		final double HAMBURGER_COST=2.99;
		final double FRIES_COST=2.49;
		final double SALAD_COST=5.99;
		final double ICE_CREAM_COST=1.49;
		final double DRINK_COST=0.99;
		//Cost of items in menu
		menuCost[0] = HAMBURGER_COST;
		menuCost[1] = FRIES_COST;
		menuCost[2] = SALAD_COST;
		menuCost[3] = ICE_CREAM_COST;
		menuCost[4] = DRINK_COST;
		//Menu itself
		String[] menuString;
		menuString=new String[5];
		menuString[0] = "Hamburger: ";
		menuString[1] = "French Fries: ";
		menuString[2] = "Salad: ";
		menuString[3] = "Ice Cream: ";
		menuString[4] = "Drink: ";
		System.out.println("Menu:");
		for (int x=0; x<menuString.length;x++) {
			System.out.printf("%-20s$%5.2f\n", menuString[x], menuCost[x]);
		}
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner input= new Scanner(System.in);
		double total=0.00;
		int userOrder=0;
		printMenu();
		while(true) {//Order loop
			System.out.println("What do you want to buy? (Type 'None' if you're done)");
			String answer=(input.next()).toLowerCase();
			if (answer=="none") {
				break;
			}else if (answer=="hamburger") {
				userOrder=0;
			}else if (answer=="french fries" || answer=="fries") {
				userOrder=1;
			}else if (answer=="salad") {
				userOrder=2;
			}else if (answer=="ice cream") {
				userOrder=3;
			}else if (answer=="drink") {
				userOrder=4;
			}else{
				userOrder=-1;
			}
			if(userOrder!=-1) {
				total=total+ menuCost[userOrder];
				System.out.printf("%-7s$%5.2f\n", "Total= ",total);
			}else{
				System.out.println("Invalid Input, please try again.");
				System.out.println(answer);
			}
		}
		System.out.println("Done");
		
	}

}
