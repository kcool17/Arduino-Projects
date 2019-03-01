import java.util.Arrays;

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
	
	public static int[] selectionSort(int[] arr) {
		for(int x = 0; x < arr.length; x++) {
			int temp = x;
			for(int y = x; y < arr.length; y++) {
				if (arr[y] < arr[temp]) temp = y;
			}
			int temp2 = arr[temp];
			arr[temp] = arr[x];
			arr[x] = temp2;
		}
		return arr;
	}
	
	public static int[] insertionSort(int[] arr) {
		for (int x = 1; x < arr.length; x++) {
			for (int y = 0; y < x; y++) {
				if (arr[x] < arr[y]) {
					int temp = arr[y];
					arr[y] = arr[x];
					for (int z = y + 1; z <= x; z++) {
						int temp2 = arr[z];
						arr[z] = temp;
						temp = temp2;
					}
				}
			}
		}
		return arr;
	}
	
	public static int[] mergeSort(int[] arr) {
		if(arr.length == 0) return arr;
		mergeSort(Arrays.copyOfRange(arr, 0, (arr.length)/2));
		mergeSort(Arrays.copyOfRange(arr, (arr.length)/2, arr.length));
		
	}
	
	public static int[] quickSort(int[] arr, int pivotIndex) {
		if (arr.length <= 1) return arr;
		int tempCount = 0;
		for(int x = 1; x < arr.length; x++) {
			if (arr[x] < arr[pivotIndex]) tempCount++;
		}
		int[] beforeArr = new int[tempCount];
		int[] afterArr = new int[arr.length-1-tempCount];
		int beforeCount = 0;
		int afterCount = 0;
		
		for(int x = 1; x< arr.length; x++) {
			if (arr[x] < arr[pivotIndex]) {
				beforeArr[beforeCount] = arr[x];
				beforeCount++;
			} else {
				afterArr[afterCount] = arr[x];
				afterCount++;
			}
		}
		
		return combine(quickSort(beforeArr), arr[pivotIndex], quickSort(afterArr));
	}
	public static int[] combine(int[] beforeArr, int pivotIndex, int[] afterArr) {
		int[] newArr = new int[beforeArr.length + 1 + afterArr.length];
		for(int x = 0; x < newArr.length; x++) {
			if (x < beforeArr.length) newArr[x] = beforeArr[x];
			else if (x == beforeArr.length) newArr[x] = pivotIndex;
			else newArr[x] = afterArr[x - (beforeArr.length + 1)];
		}
		return newArr;
	}
	public static int[] quickSort(int[] arr) {
		return quickSort(arr, 0);
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("Bubble Sort");
		int[] bubbleArr = {10, 0, 5, 3, 7, 103, 3, 1};
		for(int x : bubbleArr) System.out.print(x + " ");
		System.out.println();
		for(int x : bubbleSort(bubbleArr)) System.out.print(x+ " ");
		System.out.println();
		
		System.out.println("Selection Sort");
		int[] selectArr = {10, 0, 5, 3, 7, 103, 3, 1};
		for(int x : selectArr) System.out.print(x + " ");
		System.out.println();
		for(int x : selectionSort(selectArr)) System.out.print(x+ " ");
		System.out.println();
		
		System.out.println("Insertion Sort");
		int[] insertArr = {10, 0, 5, 3, 7, 103, 3, 1};
		for(int x : insertArr) System.out.print(x + " ");
		System.out.println();
		for(int x : insertionSort(insertArr)) System.out.print(x+ " ");
		System.out.println();
		
		/*
		System.out.println("Merge Sort");
		int[] mergeArr = {10, 0, 5, 3, 7, 103, 3, 1};
		for(int x : mergeArr) System.out.print(x + " ");
		System.out.println();
		for(int x : mergeSort(mergeArr)) System.out.print(x+ " ");
		*/
		
		System.out.println("Quick Sort");
		int[] quickArr = {10, 0, 5, 3, 7, 103, 3, 1};
		for(int x : quickArr) System.out.print(x + " ");
		System.out.println();
		for(int x : quickSort(quickArr)) System.out.print(x+ " ");
		System.out.println();
		
		
	}

}

