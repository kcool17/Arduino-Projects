/***********************************************************************************\
 * Java Programming Class Unit 1 Project
 * By: Kyle Sawicki
 * 
 * For each pizza, change the constants to what the customer ordered:
 * -The size of the pizza (0 if they ordered les than 4 pizzas, for Pizza #4
 * -The amount of regular toppings
 * -The amount of premium toppings
 * Then, change the printf statements to change what the receipt says
 * -Customer Name
 * -Pizzas they ordered (Comment out pizzas that aren't bought)
 * -Price of each pizza and total
 *
\***********************************************************************************/
public class GeometryJoe {

	public static void main(String[] args) { 
		// TODO Auto-generated method stub
		/*Costs of different pizza sizes*/
		final double LARGE_PIZZA_DIAMETER = 14; //Note: these are doubles so they won't be rounded when calculating radius, etc.
		final double MEDIUM_PIZZA_DIAMETER = 12;
		final double SMALL_PIZZA_DIAMETER = 10;
		
		/*Customer's order choices (Pizza #1)*/
		final double CUSTOMER_PIZZA_DIAMETER_1 = LARGE_PIZZA_DIAMETER; //Change these for different customer orders
		final int REGULAR_TOPPINGS_AMOUNT_1 = 2;
		final int PREMIUM_TOPPINGS_AMOUNT_1 = 0;
		final int NUM_PIZZA_1 = 8; //Number of this type of pizza
		
		/*Customer's order choices (Pizza #2)*/
		final double CUSTOMER_PIZZA_DIAMETER_2 = LARGE_PIZZA_DIAMETER; //Change these for different customer orders
		final int REGULAR_TOPPINGS_AMOUNT_2 = 6;
		final int PREMIUM_TOPPINGS_AMOUNT_2 = 4;
		final int NUM_PIZZA_2 = 16; //Number of this type of pizza
		
		/*Customer's order choices (Pizza #3)*/
		final double CUSTOMER_PIZZA_DIAMETER_3 = SMALL_PIZZA_DIAMETER; //Change these for different customer orders
		final int REGULAR_TOPPINGS_AMOUNT_3 = 0;
		final int PREMIUM_TOPPINGS_AMOUNT_3 = 0;
		final int NUM_PIZZA_3 = 32; //Number of this type of pizza
		
		/*Customer's order choices (Pizza #4)*/
		final double CUSTOMER_PIZZA_DIAMETER_4 = MEDIUM_PIZZA_DIAMETER; //Change these for different customer orders
		final int REGULAR_TOPPINGS_AMOUNT_4 = 2;
		final int PREMIUM_TOPPINGS_AMOUNT_4 = 1;
		final int NUM_PIZZA_4 = 64; //Number of this type of pizza
		
		/*Calculates needed values for receipt (Pizza #1)*/
		double pizzaCost1 = 0.05* Math.PI * Math.pow((CUSTOMER_PIZZA_DIAMETER_1/2), 2);
		double regularToppingCost1 = REGULAR_TOPPINGS_AMOUNT_1 * Math.sqrt(0.49 * CUSTOMER_PIZZA_DIAMETER_1);
		double premiumToppingCost1 = PREMIUM_TOPPINGS_AMOUNT_1 * Math.sqrt(0.79 * CUSTOMER_PIZZA_DIAMETER_1);
		double pizzaSubtotal1 = NUM_PIZZA_1*(pizzaCost1 + regularToppingCost1  + premiumToppingCost1);
		
		/*Calculates needed values for receipt (Pizza #2)*/
		double pizzaCost2 = 0.05* Math.PI * Math.pow((CUSTOMER_PIZZA_DIAMETER_2/2), 2);
		double regularToppingCost2 = REGULAR_TOPPINGS_AMOUNT_2 * Math.sqrt(0.49 * CUSTOMER_PIZZA_DIAMETER_2);
		double premiumToppingCost2 = PREMIUM_TOPPINGS_AMOUNT_2 * Math.sqrt(0.79 * CUSTOMER_PIZZA_DIAMETER_2);
		double pizzaSubtotal2 = NUM_PIZZA_2*(pizzaCost2 + regularToppingCost2  + premiumToppingCost2);
		
		/*Calculates needed values for receipt (Pizza #3)*/
		double pizzaCost3 = 0.05* Math.PI * Math.pow((CUSTOMER_PIZZA_DIAMETER_3/2), 2);
		double regularToppingCost3 = REGULAR_TOPPINGS_AMOUNT_3 * Math.sqrt(0.49 * CUSTOMER_PIZZA_DIAMETER_3);
		double premiumToppingCost3 = PREMIUM_TOPPINGS_AMOUNT_3 * Math.sqrt(0.79 * CUSTOMER_PIZZA_DIAMETER_3);
		double pizzaSubtotal3 = NUM_PIZZA_3*(pizzaCost3 + regularToppingCost3  + premiumToppingCost3);
		
		/*Calculates needed values for receipt (Pizza #4)*/
		double pizzaCost4 = 0.05* Math.PI * Math.pow((CUSTOMER_PIZZA_DIAMETER_4/2), 2);
		double regularToppingCost4 = REGULAR_TOPPINGS_AMOUNT_4 * Math.sqrt(0.49 * CUSTOMER_PIZZA_DIAMETER_4);
		double premiumToppingCost4 = PREMIUM_TOPPINGS_AMOUNT_4 * Math.sqrt(0.79 * CUSTOMER_PIZZA_DIAMETER_4);
		double pizzaSubtotal4 = NUM_PIZZA_4*(pizzaCost4 + regularToppingCost4  + premiumToppingCost4);
		
		double subtotal = pizzaSubtotal1 + pizzaSubtotal2 + pizzaSubtotal3+ pizzaSubtotal4;
		double tax = subtotal * 0.07;
		double shippingCost = Math.min(((tax + subtotal) * 0.1), 5);
		double finalTotal = subtotal + tax + shippingCost;
		
		/*Prints out formatted receipt; edit as needed for different customers*/
		System.out.printf("%-27s","Geometry Joe's Pizza Parlor");
		System.out.printf("\n%-25s","Customer K. Sawicki"); //Edit for cutomer's name
		//Edit for Orders (Comment out unused ones)
		System.out.printf("\n%-2s%2s %-40s$%6.2f", "  ", NUM_PIZZA_1,"Large Pepperoni Extra Cheese:", pizzaSubtotal1);
		System.out.printf("\n%-2s%2s %-40s$%6.2f", "  ", NUM_PIZZA_2,"Large With Everything:", pizzaSubtotal2);
		System.out.printf("\n%-2s%2s %-40s$%6.2f", "  ", NUM_PIZZA_3,"Small Cheese:", pizzaSubtotal3);
		System.out.printf("\n%-2s%2s %-40s$%6.2f", "  ", NUM_PIZZA_4,"Medium Meat Lover:", pizzaSubtotal4);
		
		//Tax, shipping, etc. (Don't change)
		System.out.printf("\n%-2s%-43s$%6.2f", "  ", "Tax:", tax);
		System.out.printf("\n%-2s%-43s$%6.2f", "  ", "Delivery Charge:", shippingCost);
		System.out.printf("\n%-2s%-43s$%6.2f", "  ", "Total:", finalTotal);
		System.out.printf("\n%-25s","Thank you for your order!");
	}

}
