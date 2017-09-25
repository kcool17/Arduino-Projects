
public class GeometryJoe {

	public static void main(String[] args) { 
		// TODO Auto-generated method stub
		/*Costs of different pizza sizes*/
		final double LARGE_PIZZA_DIAMETER = 14; //Note: these are doubles so they won't be rounded when calculating radius, etc.
		final double MEDIUM_PIZZA_DIAMETER = 12;
		final double SMALL_PIZZA_DIAMETER = 10;
		
		/*Customer's order choices*/
		final double CUSTOMER_PIZZA_DIAMETER_1 = SMALL_PIZZA_DIAMETER; //Change these for different customer orders
		final double REGULAR_TOPPINGS_AMOUNT_1 = 4;
		final double PREMIUM_TOPPINGS_AMOUNT_1 = 2;
		
		/*Calculates needed values for receipt (Pizza #1)*/
		double pizzaCost1 = 0.05* Math.PI * Math.pow((CUSTOMER_PIZZA_DIAMETER_1/2), 2);
		double regularToppingCost1 = REGULAR_TOPPINGS_AMOUNT_1 * Math.sqrt(0.49 * CUSTOMER_PIZZA_DIAMETER_1);
		double premiumToppingCost1 = PREMIUM_TOPPINGS_AMOUNT_1 * Math.sqrt(0.79 * CUSTOMER_PIZZA_DIAMETER_1);
		double pizzaSubtotal1 = pizzaCost1 + regularToppingCost1  + premiumToppingCost1;
		
		/*Calculates needed values for receipt (Pizza #2)*/
		double pizzaCost2 = 0.05* Math.PI * Math.pow((CUSTOMER_PIZZA_DIAMETER_2/2), 2);
		double regularToppingCost2 = REGULAR_TOPPINGS_AMOUNT_2 * Math.sqrt(0.49 * CUSTOMER_PIZZA_DIAMETER_2);
		double premiumToppingCost2 = PREMIUM_TOPPINGS_AMOUNT_2 * Math.sqrt(0.79 * CUSTOMER_PIZZA_DIAMETER_2);
		double pizzaSubtotal2 = pizzaCost2 + regularToppingCost2  + premiumToppingCost2;
		
		/*Calculates needed values for receipt (Pizza #3)*/
		double pizzaCost3 = 0.05* Math.PI * Math.pow((CUSTOMER_PIZZA_DIAMETER_3/2), 2);
		double regularToppingCost3 = REGULAR_TOPPINGS_AMOUNT_3 * Math.sqrt(0.49 * CUSTOMER_PIZZA_DIAMETER_3);
		double premiumToppingCost3 = PREMIUM_TOPPINGS_AMOUNT_3 * Math.sqrt(0.79 * CUSTOMER_PIZZA_DIAMETER_3);
		double pizzaSubtotal3 = pizzaCost3 + regularToppingCost3  + premiumToppingCost3;
		
		/*Calculates needed values for receipt (Pizza #4)*/
		double pizzaCost4 = 0.05* Math.PI * Math.pow((CUSTOMER_PIZZA_DIAMETER_4/2), 2);
		double regularToppingCost4 = REGULAR_TOPPINGS_AMOUNT_4 * Math.sqrt(0.49 * CUSTOMER_PIZZA_DIAMETER_4);
		double premiumToppingCost4 = PREMIUM_TOPPINGS_AMOUNT_4 * Math.sqrt(0.79 * CUSTOMER_PIZZA_DIAMETER_4);
		double pizzaSubtotal4 = pizzaCost4 + regularToppingCost4  + premiumToppingCost4;
		
		
		double tax = subtotal * 0.07;
		double shippingCost = Math.min(((tax + subtotal) * 0.1), 5);
		double finalTotal =subtotal + tax + shippingCost;
		
		/*Prints out formatted receipt*/
		System.out.printf("%-27s","Geometry Joe's Pizza Parlor");
		System.out.printf("\n%-18s","Customer G. Hopper");
		System.out.printf("", "", );

	}

}
