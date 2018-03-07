import java.util.Scanner;
public class IfPractice {
	
	public static void numToLetter() {
		Scanner input = new Scanner(System.in);
		System.out.println("What was your quiz grade (Number)?");
		double userGrade = input.nextDouble();
		if (userGrade >=100) {
			System.out.print("You got an A+");
		} else if (userGrade >=90) {
			System.out.print("You got an A");
			if (userGrade-(((int)userGrade/10)*10)>=7) {
				System.out.print("+\n");
			}else if (userGrade-(((int)userGrade/10)*10)>=3) {
				System.out.print("\n");
			}else {
				System.out.print("-\n");
			}
		} else if (userGrade >=80) {
			System.out.print("You got a B");
			if (userGrade-(((int)userGrade/10)*10)>=7) {
				System.out.print("+\n");
			}else if (userGrade-(((int)userGrade/10)*10)>=3) {
				System.out.print("\n");
			}else {
				System.out.print("-\n");
			}
		} else if (userGrade >=70) {
			System.out.print("You got a C");
			if (userGrade-(((int)userGrade/10)*10)>=7) {
				System.out.print("+\n");
			}else if (userGrade-(((int)userGrade/10)*10)>=3) {
				System.out.print("\n");
			}else {
				System.out.print("-\n");
			}
		} else if (userGrade >=60) {
			System.out.print("You got a D");
			if (userGrade-(((int)userGrade/10)*10)>=7) {
				System.out.print("+\n");
			}else if (userGrade-(((int)userGrade/10)*10)>=3) {
				System.out.print("\n");
			}else {
				System.out.print("-\n");
			}
		} else {
			System.out.print("You got an F!");
		}
		input.close();
	}
	public static void letterToNum() {
		Scanner input = new Scanner(System.in);
		System.out.println("What was your quiz grade (Letter)?");
		String userGrade = input.next();
		userGrade = userGrade.toLowerCase();
		char userLetter = userGrade.charAt(0);
		char userSymbol;
		try {
			userSymbol = userGrade.charAt(1);
		}catch (IndexOutOfBoundsException error) {
			userSymbol = 0;
		}
		double newUserGrade = 0;
		if (userLetter == 'a') {
			newUserGrade = newUserGrade + 90;
			System.out.print("Your grade is greater than or equal to ");
			if (userSymbol == '+') {
				System.out.print("97 and less than or equal to 100\n");
			}else if (userSymbol == '-') {
				System.out.print("90 and less than or equal to 92\n");
			}else {
				System.out.print("93 and less than or equal to 96\n");
			}
			
		}else if (userLetter == 'b') {
			newUserGrade = newUserGrade + 80;
			System.out.print("Your grade is greater than or equal to ");
			if (userSymbol == '+') {
				System.out.print("87 and less than or equal to 89\n");
			}else if (userSymbol == '-') {
				System.out.print("80 and less than or equal to 82\n");
			}else {
				System.out.print("83 and less than or equal to 86\n");
			}
		}else if (userLetter == 'c') {
			newUserGrade = newUserGrade + 70;
			System.out.print("Your grade is greater than or equal to ");
			if (userSymbol == '+') {
				System.out.print("77 and less than or equal to 79\n");
			}else if (userSymbol == '-') {
				System.out.print("70 and less than or equal to 72\n");
			}else {
				System.out.print("73 and less than or equal to 76\n");
			}
		}else if (userLetter == 'd') {
			newUserGrade = newUserGrade + 60;
			System.out.print("Your grade is greater than or equal to ");
			if (userSymbol == '+') {
				System.out.print("67 and less than or equal to 69\n");
			}else if (userSymbol == '-') {
				System.out.print("60 and less than or equal to 62\n");
			}else {
				System.out.print("63 and less than or equal to 66\n");
			}
		}else {
			System.out.print("Your grade is less than 60!");
		}
		input.close();
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		letterToNum();
		
		
		
	}

}
