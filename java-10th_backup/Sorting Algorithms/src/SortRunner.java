
public class SortRunner {

	public static int[] bubbleSort(int[] arr) {
		boolean done = false;
		while (!done) {
			done = true;
			for (int x = 0; x < arr.length - 1; x++) {
				if (arr[x] > arr[x+1]) {
					int temp = arr[x];
					arr[x] = arr[x+1];
					arr[x+1] = temp;
					done = false;
				}
			}
		}
		return arr;
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int[] bubbleArr = {10, 0, 5, 3, 7, 103, 3, 1};
		for(int x : bubbleArr) System.out.print(x + " ");
		System.out.println();
		for(int x : bubbleSort(bubbleArr)) System.out.print(x+ " ");
	}

}
