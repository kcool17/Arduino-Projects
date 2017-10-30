import java.util.Scanner;
public final class WhilePractice {
	
	public static int While1(int start, int end, boolean evenOdd, boolean square, boolean digitCount, int digit) {
		int step = start;
		int total = 0;
		boolean quit = false;
		if (evenOdd==true) {
			while(step<=end) {
				total = total + step;
				step= step+2;
			}
		}else if (square) {
			while(quit!=true) {
				if (Math.pow(step, 2)>end) {
					quit = true;
				}else {
					total = total + (int)Math.pow(step, 2);
				}
				step++;
			}
		}else if (digitCount) {
			
		}else {
			while(step<=end) {
				total = total + step;
				step++;
			}
		}
		return total;
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner input = new Scanner(System.in);
		System.out.println(While1(1, 100, true, false, false, 0));
		input.close();
	}

}
