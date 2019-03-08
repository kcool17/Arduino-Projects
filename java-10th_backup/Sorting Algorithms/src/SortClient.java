
public class SortClient {

	/**
	 * Randomly fills an array -20 to 20
	 * @param arr integer array
	 */
	private static void fillRandomArr(int arr[]) {
		for(int x = 0; x < arr.length; x++) {
			arr[x] = (int)(Math.random() * 41) - 20;
		}
	}
	/**
	 * Randomly fills an array 1 to given value
	 * @param arr integer array
	 * @param value the integer value you want to go to
	 */
	private static void fillRandomArrLarge(int arr[], int value) {
		for(int x = 0; x < arr.length; x++) {
			arr[x] = (int)(Math.random() * value);
		}
	}
	
	/**
	 * Times a sort and formats a neat table entry for it. Copy/pasting is dumb.
	 * @param size size of the array
	 * @param sort type of sort, from 0-4 (Bubble, Selection, Insertion, Merge, Quick)
	 * @param range the range of the random numbers
	 */
	private static void timeSort(int size, int sort, int range) {
		StopWatch1 s = new StopWatch1();
		String sortName = "";
		int[] arr = new int[size];
		fillRandomArrLarge(arr, size);
		if (sort == 0) {
			sortName = "Bubble Sort";
			s.start();
			Sort.bubbleSort(arr);
			s.stop();
		} if (sort == 1) {
			sortName = "Selection Sort";
			s.start();
			Sort.selectionSort(arr);
			s.stop();
		} if (sort == 2) {
			sortName = "Insertion Sort";
			s.start();
			Sort.insertionSort(arr);
			s.stop();
		} if (sort == 3) {
			sortName = "Merge Sort";
			s.start();
			Sort.mergeSort(arr);
			s.stop();
		} if (sort == 4) {
			sortName = "Quick Sort";
			s.start();
			Sort.quickSort(arr);
			s.stop();
		}
		System.out.printf("%7d | %15s | %10d ms\n", size, sortName, s.getElapsedTime());
	}
	/**
	 * Same as timeSort, but it's for the special cases (sorted + reversed)
	 * @param size size of the array
	 * @param sort type of sort, from 0-4 (Bubble, Selection, Insertion, Merge, Quick)
	 * @param reversed whether or not it's reverse sorted
	 */
	private static void timeSort(int size, int sort, boolean reversed) {
		StopWatch1 s = new StopWatch1();
		String sortName = "";
		int[] arr = new int[size];
		if (!reversed) {
			for(int x = 0; x < arr.length; x++) {
				arr[x] = x + 1;
			}
		} else {
			int y = arr.length;
			for(int x = 0; x < arr.length; x++) {
				arr[x] = y;
				y--;
			}
		}
		if (sort == 0) {
			sortName = "Bubble Sort";
			s.start();
			Sort.bubbleSort(arr);
			s.stop();
		} if (sort == 1) {
			sortName = "Selection Sort";
			s.start();
			Sort.selectionSort(arr);
			s.stop();
		} if (sort == 2) {
			sortName = "Insertion Sort";
			s.start();
			Sort.insertionSort(arr);
			s.stop();
		} if (sort == 3) {
			sortName = "Merge Sort";
			s.start();
			Sort.mergeSort(arr);
			s.stop();
		} if (sort == 4) {
			sortName = "Quick Sort";
			s.start();
			Sort.quickSort(arr);
			s.stop();
		}
		System.out.printf("%7d | %15s | %10d ms\n", size, sortName, s.getElapsedTime());
	}
	
	private static void timeSearch(int num, boolean isLinear, boolean isSorted) {
		StopWatch1 s = new StopWatch1();
		String searchName = "";
		String sortString = "";
		int[] arr = new int[50000000];
		if (isSorted) {
			sortString = "Sorted";
			for (int i = 0; i < arr.length; i++) {
				arr[i] = i;
			}
		} else {
			sortString = "Unsorted";
			fillRandomArrLarge(arr, 50000000);
		}
		if (isLinear) {
			searchName = "Linear Search";
			s.start();
			Search.linearSearch(arr, num);
			s.stop();
		} else {
			searchName = "Binary Search";
			s.start();
			Search.binarySearch(arr, num);
			s.stop();
		}
		System.out.printf("%8s | %15s | %10d ms\n", sortString, searchName, s.getElapsedTime());
	}

	public static void main(String[] args) {
		
		//Make arrays, and fill them randomly
		int[] bubbleArr = new int[20];
		fillRandomArr(bubbleArr);
		int[] selectArr = new int[20];
		fillRandomArr(selectArr);
		int[] insertArr = new int[20];
		fillRandomArr(insertArr);
		int[] mergeArr = new int[20];
		fillRandomArr(mergeArr);
		int[] quickArr = new int[20];
		fillRandomArr(quickArr);
		
		//Sort Testing
		System.out.println("----------------------------------------------------Sort Testing---------------------------------------------------------");
		System.out.println("\nBubble Sort");
		for(int x : bubbleArr) System.out.print(x + " ");
		Sort.bubbleSort(bubbleArr);
		System.out.println();
		for(int x : bubbleArr) System.out.print(x+ " ");
		
		System.out.println("\nSelection Sort");
		for(int x : selectArr) System.out.print(x + " ");
		Sort.selectionSort(selectArr);
		System.out.println();
		for(int x : selectArr) System.out.print(x+ " ");
		
		System.out.println("\nInsertion Sort");
		for(int x : insertArr) System.out.print(x + " ");
		Sort.insertionSort(insertArr);
		System.out.println();
		for(int x : insertArr) System.out.print(x+ " ");
		
		System.out.println("\nMerge Sort");
		for(int x : mergeArr) System.out.print(x + " ");
		Sort.mergeSort(mergeArr);
		System.out.println();
		for(int x : mergeArr) System.out.print(x+ " ");
		
		System.out.println("\nQuick Sort");
		for(int x : quickArr) System.out.print(x + " ");
		Sort.quickSort(quickArr);
		System.out.println();
		for(int x : quickArr) System.out.print(x+ " ");
		System.out.println();
		
		//Search Testing
		System.out.println("---------------------------------------------------Search Testing----------------------------------------------------------");
		System.out.println("Linear Search for 3   (QuickSort array) result: " + Search.linearSearch(quickArr, 3));
		System.out.println("Linear Search for -12 (QuickSort array) result: " + Search.linearSearch(quickArr, -12));
		System.out.println("Linear Search for 21  (QuickSort array) result: " + Search.linearSearch(quickArr, 21));
		System.out.println("Binary Search for 3   (QuickSort array) result: " + Search.binarySearch(quickArr, 3));
		System.out.println("Binary Search for -12 (QuickSort array) result: " + Search.binarySearch(quickArr, -12));
		System.out.println("Binary Search for 21  (QuickSort array) result: " + Search.binarySearch(quickArr, 21));
		
		//Sort timing
		System.out.println("---------------------------------------------------Sort Timing----------------------------------------------------------");
		System.out.printf("%7s | %15s | %10s ms\n", "Size", "Sort", "Time");
		int x = 1000;
		boolean foo = false;
		while(x < 10000000){
			for(int y = 0; y < 5; y++) {
				if (x < 100000 || y == 3 || y == 4 || (x < 1000000 && y != 0)) timeSort(x, y, x);
			}
			if (foo) {
				x = x*2;
				foo = false;
			} else {
				x = x*5;
				foo = true;
			}
		}
		//Sort timing (Special Cases)
		System.out.println("---------------------------------------------------Sort Timing (Special Cases)----------------------------------------------------------");
		System.out.printf("Type   |%7s | %15s | %10s ms\n", "Size", "Sort", "Time");
		System.out.print("1-200K |");
		for(int i = 1; i < 5; i++) timeSort(200000, i, 200000);
		System.out.print("Sorted |");
		for(int i = 1; i < 5; i++) timeSort(200000, i, false);
		System.out.print("Reverse|");
		for(int i = 1; i < 5; i++) timeSort(200000, i, true);
		System.out.print("1-20   |");
		for(int i = 1; i < 5; i++) timeSort(200000, i, 20);

		//Search Timing
		System.out.println("---------------------------------------------------Search Timing----------------------------------------------------------");
		
		//Linear unsorted
		for (int z = 0; z < 5; z++) {
			int num = (int)(Math.random() * 5000000);
			timeSearch(num, true, false);
		}
		//Linear sorted
		for (int z = 0; z < 5; z++) {
			int num = (int)(Math.random() * 5000000);
			timeSearch(num, true, true);
		}
		//Binary
		for (int z = 0; z < 5; z++) {
			int num = (int)(Math.random() * 5000000);
			timeSearch(num, false, true);
		}
		
	}

}
