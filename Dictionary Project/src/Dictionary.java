import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;
/**
 * Words 'R Fun Dictionary Project Template
 * Complete the methods to analyze the dictionary.
 * Add additional methods as needed. All variables except the File and Scanner
 * should be local.
 * @author rodriguezd
 *
 */
public class Dictionary
{
  static File fWebsters;
  static Scanner in;
  
  /*
   * Counts how many total words and five-letter words
   * are in this dictionary
   * Pre: File is opened, Scanner declared
   * Post: Number of words is printed
   */
  public static void countWords() throws IOException
  {
    in = new Scanner(fWebsters); //Initialize the Scanner
    //Local Variables
    int fiveLetters = 0;
    int numWords = 0;
    //While there is still another word in the dictionary, do this:
    while(in.hasNext())
    {
    	if (in.next().length() == 5) {//Checks if the length of the word is 5, and increments the running total for five-letter words if so
    		fiveLetters++;
    	}
    	numWords++; //Increments the running total by one for each word tested
    }
    //Prints out results
    System.out.println("Number of Words in Dictionary: "+ numWords);
    System.out.println("Number of Five-Letter Words in Dictionary: "+ fiveLetters);

  }
   
  /*
   * Counts how many five-letter words have 5,4,3,2,1,and 0 vowels
   * Only a e i o u upper and lower case are vowels
   * Pre: File is opened, Scanner declared
   * Post: Number of different vowel words are printed
   * Post: 0-Vowel words are printed
   */
  public static void countVowels() throws IOException
  {   
	  //reset Scanner to start of file
	  in = new Scanner(fWebsters);
	  System.out.print("Words with no vowels: ");
	  //Local Variables
	  int noVowels=0;
	  int oneVowel=0;
	  int twoVowels=0;
	  int threeVowels=0;
	  int fourVowels=0;
	  int fiveVowels=0;
	  int currentVowels=0;
	  String testString = "";
	  //While there is still another word in the dictionary, do this
	  while(in.hasNext()) {
		  testString = in.next(); 
		  
		  if (testString.length() == 5) {//Determines if the word is five letters or not
			  currentVowels=0;
			  for(int x=0; x<=4; x++) {//Checks if one of the letters is a vowel, and increments the current number of vowels in the word accordingly
				  if(testString.charAt(x)=='a'||testString.charAt(x)=='e'||testString.charAt(x)=='i'||testString.charAt(x)=='o'||testString.charAt(x)=='u'||testString.charAt(x)=='A'||testString.charAt(x)=='E'||testString.charAt(x)=='I'||testString.charAt(x)=='O'||testString.charAt(x)=='U') {
					  currentVowels++;
				  }
			  }
			  //Depending on the number of vowel, increases the total for each type of word
			  if (currentVowels==5) {
				  fiveVowels++;
			  }else if (currentVowels==4) {
				  fourVowels++;
			  }else if (currentVowels==3) {
				  threeVowels++;
			  }else if (currentVowels==2) {
				  twoVowels++;
			  }else if (currentVowels==1) {
				  oneVowel++;
			  }else {
				  noVowels++;
				  System.out.print(testString+", "); //Prints the number of 5-letter words with no vowels
			  }
		  }
		  
	  }
	  //Prints info
	  System.out.println("Number of Five Letter Words with Five Vowels in Dictionary: "+ fiveVowels);
	  System.out.println("Number of Five Letter Words with Four Vowels in Dictionary: "+ fourVowels);
	  System.out.println("Number of Five Letter Words with Three Vowels in Dictionary: "+ threeVowels);
	  System.out.println("Number of Five Letter Words with Two Vowels in Dictionary: "+ twoVowels);
	  System.out.println("Number of Five Letter Words with One Vowel in Dictionary: "+ oneVowel);
	  System.out.println("Number of Five Letter Words with No Vowels in Dictionary: "+ noVowels);
  }
  
  /*
   * Counts the number of characters in the longest and shortest word
   * Pre: File is opened, Scanner declared
   * Post: Number of characters in the longest word is printed
   * Post: Number of characters in the shortest word is printed
   */
  public static void longestAndShortestCount() throws IOException{
	  in = new Scanner(fWebsters);
	  //Local variables
	  int currentShort=10;
	  int currentLong=0;
	  int wordLength=0;
	  //While there is still another word in the dictionary, do this
	  while(in.hasNext()) {
		  wordLength = in.next().length();//Checks the length of the current word to be tested
		  if(wordLength>currentLong) {
			  currentLong = wordLength; //Replaces the current longest if the new one is larger
		  }
		  if (wordLength<currentShort) {
			  currentShort = wordLength;//Replaces the current shortest if the new one is smaller
		  }
	  }
	  //Prints output
	  System.out.println("The Longest Word's Length is: "+currentLong);
	  System.out.println("The Shortest Word's Length is: "+currentShort);
  }
  
  
  /*
   * Counts and displays all the words containing "java" in any case.
   * Pre: File is opened, Scanner declared
   * Post: Number of java words is printed
   * Post: All the java words are printed with java converted to all upper case
   */
  public static void javaWords()throws IOException{
	  in = new Scanner(fWebsters); //Scanner
	  //Local Variables
	  int totalJava = 0;
	  boolean isJava = false;
	  String newWord = "";
	  String testWord = "";
	  String testSubstring = "";
	  System.out.println("Words containing 'Java'");
	  //Replaces the current longest if the new one is larger
	  while(in.hasNext()) {
		  newWord = "";
		  testWord = in.next();
		  for(int x=0; x<testWord.length(); x++) {
			  if(x+3<testWord.length()) {
				  testSubstring = (testWord.substring(x, x+4)).toUpperCase(); //Creates a substring uses the test word to check for "Java"
				  if(testSubstring.equals("JAVA")) {
					  newWord=newWord+testSubstring; //Used to create the new word
					  isJava = true;
					  x=x+3;
				  }else {
					  newWord = newWord +testWord.charAt(x); //Used to create the new word
				  }
			  }else {
				  newWord = newWord +testWord.charAt(x); //Used to create the new word
			  }
			  
		  }
		  if (isJava == true) { //If java was contained in the word, print the word
			  System.out.println(newWord);
			  isJava = false;
			  totalJava++;
		  }
		  
	  }
	  //Print output
	  System.out.println("The number of words containing 'java' is: "+ totalJava);
	  
  }
  
  public static void main(String[] args) throws IOException
  {
    //Open file
	//Add file to project folder
    fWebsters = new File ("websters_dictionary.txt");
    
    //Analyze words
    countWords();
    countVowels();
    longestAndShortestCount();
    javaWords();
  }
}
