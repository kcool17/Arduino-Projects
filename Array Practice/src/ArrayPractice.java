import java.lang.Math;
public class ArrayPractice {

	public static void r6_1(char problemLetter){
		System.out.print(Character.toUpperCase(problemLetter)+": ");
		if (problemLetter=='a') {
			int[] stuff = new int[10];
			for(int x=0;x<10;x++) {
				stuff[x] = x+1;
			}
			for(int x=0;x<stuff.length;x++) {
				System.out.print(stuff[x] + ", ");
			}
		}else if (problemLetter=='b') {
			int[] stuff = new int[11];
			for(int x=0;x<11;x++) {
				stuff[x] = x*2;
			}
			for(int x=0;x<stuff.length;x++) {
				System.out.print(stuff[x] + ", ");
			}
		}else if (problemLetter=='c') {
			int[] stuff = new int[11];
			for(int x=0;x<11;x++) {
				stuff[x] = (int)Math.pow(x, 2);
			}
			for(int x=0;x<stuff.length;x++) {
				System.out.print(stuff[x] + ", ");
			}
		}else if (problemLetter=='d') {
			int[] stuff = new int[10];
			for(int x=0;x<10;x++) {
				stuff[x] = 0;
			}
			for(int x=0;x<stuff.length;x++) {
				System.out.print(stuff[x] + ", ");
			}
		}else if (problemLetter=='e') {
			int[] stuff = {1, 4, 9, 16, 9, 7, 4, 9, 11};
			for(int x=0;x<stuff.length;x++) {
				System.out.print(stuff[x] + ", ");
			}
		}else if (problemLetter=='f') {
			int[] stuff = new int[10];
			for(int x=0;x<10;x++) {
				stuff[x] = x%2;
			}
			for(int x=0;x<stuff.length;x++) {
				System.out.print(stuff[x] + ", ");
			}
		}else if (problemLetter=='g') {
			int[] stuff = new int[10];
			for(int x=0;x<10;x++) {
				stuff[x] = x%5;
			}
			for(int x=0;x<stuff.length;x++) {
				System.out.print(stuff[x] + ", ");
			}
		}else {
			System.out.println("Idiot! You can't JAVA AT ALL! LEARN TO JAVA! (Next time, enter a *valid* problem letter)");
		}
		System.out.println();
	}
	
	public static void p6_1(){
		int[] stuff = new int[10];
		for (int x=0; x<10; x++) {
			stuff[x] = (int)(Math.random()*100);
		}
		System.out.print("1: ");
		for (int x =0; x<10; x+=2) {
			System.out.print(stuff[x]+", ");
		}
		System.out.println();
		
		System.out.print("2: ");
		for (int x =0; x<10; x++) {
			if(stuff[x]%2==0) {
				System.out.print(stuff[x]+", ");
			}
		}
		System.out.println();
		
		System.out.print("3: ");
		for (int x =9; x>=0; x--) {
			System.out.print(stuff[x]+", ");
		}
		System.out.println();
		
		System.out.print("4: ");
		System.out.print(stuff[0]+", ");
		System.out.print(stuff[9]+", ");
		System.out.println();
	}
	
	public static int p6_6(int lengthArray) {
		int[] stuff = new int[lengthArray];
		System.out.print("Original Array: ");
		for (int x =0; x<stuff.length; x++) {
			stuff[x] = ((int)(Math.random()*20))+1;
			System.out.print(stuff[x]+", ");
		}
		int lengthNew = 0;
		boolean testBool = false;
		for (int x =0; x<stuff.length; x++) {
			int test = stuff[x];
			testBool = false;
			for (int y =x-1; y>=0; y--) {
				if( test ==stuff[y]) {
					testBool = true;
				}
			}
			if (!testBool) {
				lengthNew++;
			}
		}
		int z = 0;
		int[] newStuff = new int[lengthNew];
		for (int x =0; x<stuff.length; x++) {
			int test = stuff[x];
			testBool = false;
			for (int y =x-1; y>=0; y--) {
				if( test ==stuff[y]) {
					testBool = true;
				}
			}
			if (!testBool) {
				newStuff[z] = test;
				z++;
			}
		}
		System.out.println();
		System.out.print("New Array: ");
		for (int x =0; x<newStuff.length; x++) {
			System.out.print(newStuff[x]+", ");
			
		}
		System.out.println();
		System.out.print("New Array Length: ");
		return newStuff.length;
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("Problem R6.1: ");
		r6_1('a');
		r6_1('b');
		r6_1('c');
		r6_1('d');
		r6_1('e');
		r6_1('f');
		r6_1('g');
		System.out.println();
		System.out.println("Problem P6.1: ");
		p6_1();
		System.out.println();
		System.out.println("Problem P6.6: ");
		System.out.print(p6_6(30));
	}

}
