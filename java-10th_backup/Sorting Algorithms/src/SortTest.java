import java.util.Arrays;

public class SortTest {

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
		mergeSortHelper(arr, 0, arr.length - 1);
		return arr;
	}
	private static void mergeSortHelper(int[] arr, int start, int end) {
		if (start < end) {
			int middle = (start + end) / 2;
			mergeSortHelper(arr, start, middle);
			mergeSortHelper(arr, middle + 1, end);
			merge(arr, start, middle, end);
		}
		
	}
	private static void merge(int[] arr, int start, int middle, int end) {
		int[] temp = new int[end - start + 1];
		int x = start;
		int y = middle + 1;
		
		for (int z = 0; z < temp.length; z++) {
			if (x <= middle && (y > end || arr[x] <= arr[y])) {
				temp[z] = arr[x];
				x++;
			} else if (y <= end && (x > middle || arr[y] < arr[x])) {
				temp[z] = arr[y];
				y++;
			}
		}
		
		int a = start;
		for (int z = 0; z < temp.length; z++) {
			arr[a] = temp[z];
			a++;
		}
	}
	
	public static int[] quickSort(int[] arr) {
		quickSortHelper(arr, 0, arr.length - 1);
		return arr;
	}
	private static void quickSortHelper(int[] arr, int start, int end) {
		if (start < end) {
			int middle = partition(arr, start, end);
			quickSortHelper(arr, start, middle);
			quickSortHelper(arr, middle + 1, end);
		}
	}
	private static int partition(int[] arr, int start, int end) {
		int pivot = arr[start];
		int x = start - 1;
		int y = end + 1;
		int temp;
		while(x < y) {
			x++;
			while (arr[x] < pivot) x++;
			y--;
			while (arr[y] > pivot) y--;
			if (x < y) {
				temp = arr[x];
				arr[x] = arr[y];
				arr[y] = temp;
			}
		}
		return y;
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
		
		System.out.println("Merge Sort");
		int[] mergeArr = {10, 0, 5, 3, 7, 103, 3, 1};
		for(int x : mergeArr) System.out.print(x + " ");
		System.out.println();
		for(int x : mergeSort(mergeArr)) System.out.print(x+ " ");
		System.out.println();
		
		System.out.println("Quick Sort");
		int[] quickArr = {10, 0, 5, 3, 7, 103, 3, 1, 10};
		for(int x : quickArr) System.out.print(x + " ");
		System.out.println();
		for(int x : quickSort(quickArr)) System.out.print(x+ " ");
		System.out.println();
		
		
	}

}

