import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;

public class Dictionary_2_0 {
	static File fWebsters;
	static Scanner in;
	
	public static String[] reduceDictionary() throws IOException{
		in = new Scanner(fWebsters); //Initialize the Scanner
		String[] stuff = new String[200];
		in.next(); //Skips the first element
		int currentWord = 0;
		int elementNum = 0;
		while(in.hasNext() && elementNum<200)
	    {
	    	currentWord++;
	    	if ((currentWord+1)%1000==0) {
	    		stuff[elementNum] = in.next();
	    		elementNum++;
	    	}else {
	    		in.next();
	    	}
	    }
		return stuff;
	}
	
	public static void printArray(String[] arr) {
		for(int x=0; x<arr.length; x++) {
			  System.out.print(x+1+": "+arr[x] + " | ");
		  }
	}
	
	public static String findSmall(String[] arr) {
		String currentSmall = arr[0];
		int smallLength = currentSmall.length();
		for(int x=0; x<arr.length; x++) {
			if(arr[x].length()<smallLength) {
				currentSmall=arr[x];
				smallLength=arr[x].length();
			}
		  }
		return currentSmall;
	}
	
	public static int numVowels(String word) {
		int vowels = 0;
		for (int x =0; x< word.length(); x++) {
			if (word.charAt(x)=='a'||word.charAt(x)=='e'||word.charAt(x)=='i'||word.charAt(x)=='o'||word.charAt(x)=='u'||word.charAt(x)=='A'||word.charAt(x)=='E'||word.charAt(x)=='I'||word.charAt(x)=='O'||word.charAt(x)=='U') {
				vowels++;
			}
		}
		return vowels;
	}
	
	
	public static String findLarge(String[] arr) {
		String currentLarge = arr[0];
		int largeLength = currentLarge.length();
		for(int x=0; x<arr.length; x++) {
			if(arr[x].length()>largeLength) {
				currentLarge=arr[x];
				largeLength=arr[x].length();
			}
		  }
		return currentLarge;
	}
	public static String secondLarge(String[] arr, String largest) {
		String currentLarge="";
		int largeLength=0;
		int oldMax = largest.length();
		for(int x=0; x<arr.length; x++) {
			if(arr[x].length()>=largeLength && arr[x].length()<oldMax) {
				currentLarge = arr[x];
				largeLength = arr[x].length();
			}
		  }
		return currentLarge;
	}
	
	public static String[] sixOrMore(String[] arr) {
		int arrLength = 0;
		for(int x =0; x<arr.length; x++) {
			if (numVowels(arr[x])>=6) {
				arrLength++;
			}
		}
		String[] thing = new String[arrLength];
		int thingPlace = 0;
		for(int x =0; x<arr.length; x++) {
			if (numVowels(arr[x])>=6) {
				thing[thingPlace] = arr[x];
				thingPlace++;
			
			}
		}
		return thing;
	}
	
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
	    fWebsters = new File ("websters_dictionary.txt");//Creates the dictionary file
	    System.out.println("Words in the new array: ");
	    String[] newDictionary = reduceDictionary(); //Creates the reduced dictionary
	    printArray(newDictionary);//Prints the dictionary
	    System.out.println();
	    System.out.println();
	    String shortest =findSmall(newDictionary);
	    String large = findLarge(newDictionary); //Finds the largest word in the dictionary, for later use.
	    System.out.println("Smallest Word: " +shortest); //Finds the smallest word in the array, and prints it
	    System.out.println("Smallest Word's Number of Vowels: " +numVowels(shortest)); //Finds the number of vowels in the smallest word in the array, and prints it
	    System.out.println("Second Largest Word: "+ secondLarge(newDictionary, large)); //Finds the second largest wor din the dictionary.
	    String[] sixVowel = sixOrMore(newDictionary);//Finds all the word with 6 or more vowels, and adds them to an array
	    System.out.println();
	    System.out.println("Words With 6 or More Vowels: ");
	    printArray(sixVowel);//Prints the array of words with 6 or more vowels
	}

}
