
public class BigORunner {

	public static int maxSequence(int[] arr) {
		int max = arr[0];
		int sum = 0;
		for(int x = 0; x < arr.length; x++) {
			sum = arr[x];
			for (int y = x + 1; y < arr.length; y++) {
				sum += arr[y];
				if (sum > max) max = sum;
			}
		}
		return max;
		
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int[] testArr = new int[10];
		for (int x = 0; x < testArr.length; x++) {
			testArr[x] = ((int)(Math.random() * 20))- 10;
			System.out.print(testArr[x] + "   ");
		}
		System.out.println();
		System.out.println(maxSequence(testArr));
	}

}
