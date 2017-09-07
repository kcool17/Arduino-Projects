
public class MultiplicationTable {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int x=1;
		int y=1;
		int printVar;
		int printSpace;
		while (y<=12) {
			while (x<=12) {
				printVar=x*y;
				if (printVar<10) {
					printSpace = 2;
				} else if (printVar<100) {
					printSpace = 1;
				}else {
					printSpace = 0;
				}
				System.out.printf(" ");
				while (printSpace>0) {
					System.out.printf(" ");
					printSpace= printSpace-1;
				}
				System.out.printf("" + printVar);
				x=x+1;
			}
			y=y+1;
			x=1;
			System.out.printf("\n");
		}
	}

}
