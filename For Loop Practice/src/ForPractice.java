import java.util.Scanner;
public final class ForPractice {
	
	public static int While1(int start, int end, boolean evenOdd, boolean square, boolean digitCount, int digit) {
		int total = 0;
		if (evenOdd==true) {
			for(int x = start; x<=end; x=x+2) {
				total = total + x;
			}
		}else if (square) {
			for(int x = start; x<=end; x++) {
				if(Math.pow(x, 2)<=end) {
					total = total+(int)Math.pow(x, 2);
				}else {
					break;
				}
			}
		}else if (digitCount) {
			int digitLength = String.valueOf(digit).length();
			for(int i=1; i<=digitLength; i+=2) {
				int digitNum = (int) Math.pow(10, (i-1));
				total= total+((digit%(digitNum*10))/digitNum);
			}
		}else {
			for(int x = start; x<=end;x++) {
				System.out.println(x*3);
			}
		}
		return total;
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner input = new Scanner(System.in);
		System.out.println(While1(1, 100, false, false, true, 365038812));
		input.close();
	}

}
