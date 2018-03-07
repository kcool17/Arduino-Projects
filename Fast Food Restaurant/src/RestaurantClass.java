import java.util.Scanner;
public class RestaurantClass {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		final double HAMBURGER_COST=2.99;
		final double FRIES_COST=2.49;
		final double SALAD_COST=5.99;
		final double ICE_CREAM_COST=1.49;
		final double DRINK_COST=0.99;
		Scanner input= new Scanner(System.in);
		double numFood;
		double total=0.00;
		//Hamburgers
		System.out.print("How many hamburgers?  ");
		numFood= input.nextDouble();
		total=total+(numFood*HAMBURGER_COST);
		System.out.printf("%-15s%7.2f","Current Total: ", total);
		//Fries
		System.out.print("\nHow many french fries?  ");
		numFood= input.nextDouble();
		total=total+(numFood*FRIES_COST);
		System.out.printf("%-15s%7.2f","Current Total: ", total);
		//Salad
		System.out.print("\nHow many salads?  ");
		numFood= input.nextDouble();
		total=total+(numFood*SALAD_COST);
		System.out.printf("%-15s%7.2f","Current Total: ", total);
		//Ice Cream
		System.out.print("\nHow many ice creams?  ");
		numFood= input.nextDouble();
		total=total+(numFood*ICE_CREAM_COST);
		System.out.printf("%-15s%7.2f","Current Total: ", total);
		//Drink
		System.out.print("\nHow many drinks?  ");
		numFood= input.nextDouble();
		total=total+(numFood*DRINK_COST);
		System.out.printf("%-15s%7.2f","Final Total: ", total);
		
		input.close();
	}

}
