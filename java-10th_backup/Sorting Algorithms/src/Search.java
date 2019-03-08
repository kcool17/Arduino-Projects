/******************************************************************
 * A Project of Sorts
 * 
 * Implements Search Algorithms on integer arrays
 * Includes Linear and Binary searches
 * Binary Search requires a sorted list
 * All Search methods are static
 * All Search helper methods are private
 * 
 * @author Kyle Sawicki
 *
 *******************************************************************/
public class Search 
{
	/**
	 * Implements a Linear Search
	 *    Iterates through the list until it finds the given value, and then returns the value.
	 *    If it's not in the list, it returns -1.
	 * @param arr - integer array to search in
	 * @param num - integer to search for
	 * @return index of found item, -1 if not found
	 */
	public static int linearSearch(int[] arr, int num) {
		for (int x = 0; x < arr.length; x++) {
			if (arr[x] == num) return x;
		}
		return -1;
	}
	
	/**
	 * Implements a Binary Search
	 *    If the array is size 1 and the element in it is not the correct value, it returns -1.
	 *    Starts at the halfway point of the list, and checks to see if the wanted number is larger, smaller, or the same as the element there.
	 *    If it's the same, it returns the value. 
	 *    If it's larger, it finds the midpoint of the part of the array after the halfway point, and repeats the process. 
	 *    If it's smaller, it does the same, just on the part of the array before the halfway point.
	 *    
	 * Pre: list must be sorted
	 * 
	 * @param arr - integer array to search in
	 * @param num - integer to search for
	 * @return index of found item, -1 if not found
	 */
	public static int binarySearch(int[] arr, int num) {
		return binarySearchHelper(arr, num, 0, arr.length - 1);
	}
	
	/**
	 * Helper method for binary search. It just implements the algorithm in the actual binary search method.
	 * @param arr integer array
	 * @param num integer to search for
	 * @param start beginning index to search at
	 * @param end end index to search at
	 * @return index of found item, -1 if not found.
	 */
	private static int binarySearchHelper(int[] arr, int num, int start, int end) {
		if (start <= end) {
			int middle = (start + end)/2;
			if (arr[middle] > num) {
	            return binarySearchHelper(arr, num, start, middle - 1);
	        } else if (arr[middle] < num) {
	            return binarySearchHelper(arr, num, middle+1, end);
	        }
	        return middle;   
		}
		return -1;
	}
}
