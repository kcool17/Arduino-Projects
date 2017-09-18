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
		while(true) {//Order loop
			printMenu();
			System.out.println("What do you want to buy? (Type 'None'/'Done' if you're done, and replace spaces with '_')");
			String answer=(input.next()).toLowerCase();
			if (answer.equals("none")|| answer.equals("done")) {
				break;
			}else if (answer.equals("hamburger")) {
				userOrder=0;
			}else if (answer.equals("french fries") || answer.equals("fries")) {
				userOrder=1;
			}else if (answer.equals("salad")) {
				userOrder=2;
			}else if (answer.equals("ice_cream")) {
				userOrder=3;
			}else if (answer.equals("drink")) {
				userOrder=4;
			}else{
				userOrder=-1;
			}
			if(userOrder!=-1) {
				total=total+ menuCost[userOrder];
				System.out.printf("%-7s$%5.2f\n", "Current Total= ",total);
			}else{
				System.out.println("Invalid Input, please try again.");
				
			}
		}
		System.out.printf("Final Total: $%5.2f",(total*6.25));
		
	}

}
