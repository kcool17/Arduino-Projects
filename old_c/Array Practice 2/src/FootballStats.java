import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;

/**
 * Practice working with arrays using Quarterback Ratings (QBR)
 * Read input from a file into an array
 * Find the average, min, and max QBR from array data
 * Print the QBR array & calculated statistics
 * Use a separate method for printing the array, 
 * and calculating the minimum, maximum, and average QBR ratings.
 */
public class FootballStats
{
	
 /**
  * Prints an array of doubles on one line with a valid separator character (i.e. | )
  * @param arr
  */
	
public static int index = 0;

  public static void printArray(double[] arr)
  {
	  for(int x=0; x<arr.length; x++) {
		  System.out.print(x+1+": "+arr[x] + " | ");
	  }
  }
  public static void printArray(String[] arr)
  {
	  for(int x=0; x<arr.length; x++) {
		  System.out.print(x+1+": "+arr[x] + " | ");
	  }
  }
  
  /**
   * Calculates the average value in the array
   * @param arr
   * @return average
   */
  public static double calcAverage(double[] arr)
  {
	  double total = 0;
	  for(double element : arr) {
		  total = total + element;
	  }
	  return total/arr.length;
  }
  
  /**
   * Calculates the max value in the array
   * @param arr
   * @return maximum value
   */
  public static double calcMax(double[] arr)
  {
	  double current = arr[0];
	  index = 0;
	  int x =0; 
	  for (double element: arr) {
		  
		  if (element>current) {
			  current = element;
			  index = x;
		  }
		  x++;
	  }
	  return current;
  }
  
  /**
   * Calculates the min value in the array
   * @param arr
   * @return minimum value
   */
  public static double calcMin(double[] arr)
  {
	  double current = arr[0];
	  index = 0;
	  int x =0; 
	  for (double element: arr) {
		  
		  if (element<current) {
			  current = element;
			  index = x;
			  
		  }
		  x++;
	  }
	  return current;
  }
  
  public static int[] aboveAverage(double[] arr, double average) {
	  int arrNewLength = 0;
	  for(int x = 0; x<arr.length; x++) {
		  if (arr[x]>average) {
			  arrNewLength++;
		  }
	  }
	  int[] arrNew = new int[arrNewLength];
	  int y =0;
	  for(int x = 0; x<arr.length; x++) {
		  if (arr[x]>average) {
			  arrNew[y] = x;
			  y++;
		  }
	  }
	  return arrNew;
  }
  public static int quarterScore(String[] arr, String quarterBack) {
	  for(int x =0; x<arr.length; x++) {
		  if(arr[x].equals(quarterBack)) {
			  return x;
		  }
	  }
	  return -1;
  }
  
  
  public static void main(String[] args) throws IOException
  {
    //Set up Input using file QBRating2017.txt
	//Add the text file to your project folder in Eclipse
	File inFile = new File("QBRating2017.txt");
	Scanner in = new Scanner(inFile);

    //Determine size and initialize array of Quarterback ratings
    //The number of Quarterbacks is the first entry in the file, followed by the QB name and QBR, one per line
	//<Add code here to read the number of QBs and declare and initialize the QBR array>
	int length = in.nextInt();
	double[] quarterBacks = new double[length];
	String[] quarterBacksName = new String[length];
	
    //read QBRs into array, you will need to read the player name to skip over it
    //<Add for loop here that reads the QBRs from the file into the array. QBRs are floating point numbers>
	for(int x=0; x<length; x++) {
		quarterBacksName[x] = in.next();
		quarterBacks[x] = in.nextDouble();
	}
	
    //Print all the QBRs from array on one line using a space separator
	//<Add a method call to a printArray method here>
	System.out.println("The 2017 Quarterback Ratings:");
    printArray(quarterBacks);
    System.out.println();
    printArray(quarterBacksName);
    System.out.println();
    System.out.println();
    //Calculate the average QBR
	//Your method should take the array as a parameter and return the average
	//<Add a method call to a calcAverage method here>
    double average = calcAverage(quarterBacks);
    
    //Find the min and max QBR
	//Your methods should take the array as a parameter and return the maximum or the minimum
	//<Add two method calls to minAverage and maxAverage methods here>
    double min = calcMin(quarterBacks);
    int minDex = index;
    double max = calcMax(quarterBacks);
    int maxDex = index;
    //Print the returned average, min and max QBRs 
	//<Add code here to print the resulting statistics>
    System.out.println("The Average: " + average);
    
    int[] aboveAverage= aboveAverage(quarterBacks, average);
    String[] aboveAveragers = new String[aboveAverage.length];
    for (int x=0; x<aboveAverage.length; x++) {
    	aboveAveragers[x] = quarterBacksName[aboveAverage[x]];
    }
    double[] aboveAveragersScore = new double[aboveAverage.length];
    for (int x=0; x<aboveAverage.length; x++) {
    	aboveAveragersScore[x] = quarterBacks[aboveAverage[x]];
    }
    System.out.println("All players above the average: " );
    printArray(aboveAveragers);
    System.out.println();
    printArray(aboveAveragersScore);
    System.out.println();
    System.out.println();
    System.out.println("The Max: " + quarterBacksName[maxDex] + " with a score of "+ max);
    System.out.println("The Min: " + quarterBacksName[minDex] + " with a score of "+ min);
    System.out.println();
    String qB = "TomBrady,NE";
    System.out.println(qB+"'s rating is: " + quarterBacks[quarterScore(quarterBacksName, qB)]);
    in.close();
  }

}
