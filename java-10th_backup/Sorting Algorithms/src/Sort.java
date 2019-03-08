/******************************************************************
 * A Project of Sorts
 * 
 * Implements Sort Algorithms on integer arrays Includes Bubble, Insertion,
 * Selection, Merge, and Quick Sorts Merge and Quick Sorts are recursive All
 * Sort methods are static All Sort helper methods are private
 * 
 * @author Kyle Sawicki
 *
 *******************************************************************/
public class Sort {

	/************************
	 * Implements Bubble Sort 1.Scan list and compare adjacent elements 2.Swap if
	 * out of order and set a flag 3.Repeat 1-2 until no swaps are made (flag is
	 * false) scanning one less at the end each pass Pre: unsorted array parameter
	 * Post: sorted array parameter
	 * 
	 * @param arr integer array
	 **/
	public static void bubbleSort(int[] arr) {
		boolean done = false;
		while (!done) {
			done = true;
			for (int x = 0; x < arr.length - 1; x++) {
				if (arr[x] > arr[x + 1]) {
					int temp = arr[x];
					arr[x] = arr[x + 1];
					arr[x + 1] = temp;
					done = false;
				}
			}
		}
	}

	/************************
	 * Implements Insertion Sort 1.Start with a sorted list of one value 2.Add
	 * another value and sort the values, placing in correct location 3.Repeat 2-3
	 * shifting sorted values to the right until it is placed in the correct
	 * position Pre: unsorted array parameter Post: sorted array parameter
	 * 
	 * @param arr integer array
	 **/
	public static void insertionSort(int[] arr) {
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
	}

	/************************
	 * Implements Selection Sort 1.Scan the list to find the smallest value 2.Swap
	 * with first position 3.Repeat 1-2 Scanning and swapping with the next position
	 * in the list Until you are at the end of the list Pre: unsorted array
	 * parameter Post: sorted array parameter
	 * 
	 * @param arr integer array
	 **/
	public static void selectionSort(int[] arr) {
		for (int x = 0; x < arr.length; x++) {
			int temp = x;
			for (int y = x; y < arr.length; y++) {
				if (arr[y] < arr[temp])
					temp = y;
			}
			int temp2 = arr[temp];
			arr[temp] = arr[x];
			arr[x] = temp2;
		}
	}

	/************************
	 * Implements Merge Sort recursively 1.Divide the list in half 2.Sort each half
	 * (recursively) 3.Merge the two sorted lists Note: Use indexes into the array
	 * to mark two sublists and a temporary array when merging Pre: unsorted array
	 * parameter Post: sorted array parameter
	 * 
	 * @param arr integer array
	 **/
	public static void mergeSort(int[] arr) {
		mergeSortHelper(arr, 0, arr.length - 1);
	}

	/**
	 * Merge Sort helper method. It splits the array into smaller pieces, and then calls merge() on them toi put them together sorted.
	 * @param arr integer array
	 * @param start beginning index of what you want to sort
	 * @param end end Index of what you want to sort
	 */
	private static void mergeSortHelper(int[] arr, int start, int end) {
		if (start < end) {
			int middle = (start + end) / 2;
			mergeSortHelper(arr, start, middle);
			mergeSortHelper(arr, middle + 1, end);
			merge(arr, start, middle, end);
		}

	}
	
	/**
	 * Merge Sort helper method. It merges two subarrays into one, sorted array.
	 * @param arr integer array
	 * @param start beginning index of what you want to sort
	 * @param middle point that splits the two subarrays
	 * @param end end index of what you want to sort
	 */
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

	/************************
	 * Implements Quick Sort recursively 1.Divide into two sublists, < and > a pivot
	 * value 2.Recursively sort each sublist Use the first element in the list as
	 * the pivot Note: Use indexes into the array to mark two sublists Pre: unsorted
	 * array parameter Post: sorted array parameter
	 * 
	 * @param arr integer array
	 **/
	public static void quickSort(int[] arr) {
		quickSortHelper(arr, 0, arr.length - 1);
	}
	
	/**
	 * Helper method for quick sort. It divides the array into two sublists, on either side of a pivot value. It calls partition() to get the pivot and sort the array on either side of the pivot.
	 * @param arr integer array
	 * @param start beginning index of what you want to sort
	 * @param end end index of what you want to sort
	 */
	private static void quickSortHelper(int[] arr, int start, int end) {
		int middle = partition(arr, start, end);
		if (start < middle - 1) 
			quickSortHelper(arr, start, middle - 1);
		if (middle < end)
			quickSortHelper(arr, middle, end);
		
	}
	/**
	 * Helper method for quick sort. It partitions the given array on either side of a pivot, and then returns the index of the pivot.
	 * @param arr integer array
	 * @param start beginning index of what you want to sort
	 * @param end end index of what you want to sort
	 * @return index of the pivot
	 */
	private static int partition(int[] arr, int start, int end) {
		int pivot = arr[(start + end) / 2];
		int x = start - 1;
		int y = end + 1;
		int temp;
		while(x <= y) {
			x++;
			while (arr[x] < pivot) x++;
			y--;
			while (arr[y] > pivot) y--;
			if (x <= y) {
				temp = arr[x];
				arr[x] = arr[y];
				arr[y] = temp;
				x++;
				y--;
			}
		} 
		return x;
	}

}
