import java.util.Scanner;
public class NumberSix {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner input = new Scanner(System.in);
		System.out.println("Enter your name:");
		String name = input.nextLine();
		System.out.println("Enter your salary (money per hour):");
		double salary = input.nextDouble();
		System.out.println("Enter the hours you worked this week:");
		double hours = input.nextDouble();
		double money;
		if (hours<=40) {
			money = salary*hours;
		}else {
			money = (salary*40)+(salary*hours*1.5);
		}
		
		System.out.print("\nName: "+ name);
		if (hours>168) {
			System.out.print(", the Doc Brown of our time.\n");
		}else {
			System.out.print("\n");
		}
		System.out.printf("%-23s%5.2f","Money made this week: $", money);
		
		input.close();
	}

}
