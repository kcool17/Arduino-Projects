import java.util.Scanner;
public class CompetentRestaurantClass {
	static double[] menuCost = new double[5];//Declare Menu Cost, for use in other methods
	public static int hundredBill=0;
	public static int twentyBill=0;
	public static int tenBill=0;
	public static int fiveBill=0;
	public static int oneBill=0;
	public static int quarterCoin=0;
	public static int dimeCoin=0;
	public static int nickelCoin=0;
	public static int pennyCoin=0;
	
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
	
	public static void payChange(double money){//Function to pay change
		System.out.printf("%-8s$%4.2f\n","Change: ", money);
		while (money>=100) {
			hundredBill=hundredBill+1;
			money=money-100;
		}
		while (money>=20) {
			twentyBill=twentyBill+1;
			money=money-20;
		}
		while (money>=10) {
			tenBill=tenBill+1;
			money=money-10;
		}
		while (money>=5) {
			fiveBill=fiveBill+1;
			money=money-5;
		}
		while (money>=1) {
			oneBill=oneBill+1;
			money=money-1;
		}
		while (money>=0.25) {
			quarterCoin=quarterCoin+1;
			money=money-0.25;
		}
		while (money>=0.1) {
			dimeCoin=dimeCoin+1;
			money=money-0.1;
		}
		while (money>=0.05) {
			nickelCoin=nickelCoin+1;
			money=money-0.05;
		}
		while (money>=0.01) {
			pennyCoin=pennyCoin+1;
			money=money-0.01;
		}
		System.out.printf("%-22s%2d\n", "Hundred Dollar Bills: ", hundredBill);
		System.out.printf("%-22s%2d\n", "Twenty Dollar Bills: ", twentyBill);
		System.out.printf("%-22s%2d\n", "Ten Dollar Bills: ", tenBill);
		System.out.printf("%-22s%2d\n", "Five Dollar Bills: ", fiveBill);
		System.out.printf("%-22s%2d\n", "One Dollar Bills: ", oneBill);
		System.out.printf("%-22s%2d\n", "Quarters: ", quarterCoin);
		System.out.printf("%-22s%2d\n", "Dimes: ", dimeCoin);
		System.out.printf("%-22s%2d\n", "Nickels: ", nickelCoin);
		System.out.printf("%-22s%2d\n", "Pennies: ", pennyCoin);
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner input= new Scanner(System.in);
		double total=0.00;
		int userOrder=0;
		int numFood=0;
		boolean loop2=false;//Used to see if this is your first time ordering
		System.out.println("Welcome to just your average fast food restaurant!");
		while(true) {//Order loop
			printMenu();
			numFood=0;
			if (loop2) {
				System.out.println("Anything else? (Type 'None'/'Done' if you're done, and replace spaces with '_')");
			}else {
				System.out.println("What do you want to buy? (Type 'None'/'Done' if you're done, and replace spaces with '_')");
			}
			loop2=true;
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
				System.out.println("How many of that item do you want?");
				numFood=input.nextInt();
				total=total+ (menuCost[userOrder])*numFood;
				System.out.printf("%-7s$%5.2f\n", "Current Total= ",total);
			}else{
				System.out.println("Invalid Input, please try again.");
				
			}
		}
		System.out.printf("Final Total: $%5.2f\n",(total*1.0625));
		System.out.println("How much money are you going to pay? (This will give change)");
		double userMoney=-1;
		while (userMoney<0) {
			userMoney=(input.nextDouble())-total;
			if (userMoney<0) {
				System.out.println("Not enough money! Please try again.");
			}else {
				break;
			}
		}
		payChange(userMoney);
		System.out.println("Thank you for shopping at your average fast food restaurant! Have an average day!");
		input.close();
	}

}
