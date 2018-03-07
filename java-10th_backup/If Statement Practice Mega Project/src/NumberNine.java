import java.util.Scanner;
public class NumberNine {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner input = new Scanner(System.in);
		int randNum = (int)(Math.random() * 100);
		System.out.println("Guess a number from 1 to 100!");
		int myNum = input.nextInt();
		if (myNum == randNum) {
			System.out.println("You Win!");
		}else {
			System.out.println("You Lose!");
			System.out.println("The number was:" + randNum);
		}
		input.close();
	}

}
