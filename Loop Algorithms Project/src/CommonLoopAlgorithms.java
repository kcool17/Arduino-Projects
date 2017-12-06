/**
 * Template to practice Common Loop Algorithms
 * Add your code after the comments to solve each problem.
 * Run the code to check the correctness of your implementation of the algorithms
 * @author rodriguezd
 *
 */
public class CommonLoopAlgorithms 
{
	final static int MAX_GRADE = 100;
	final static int MIN_GRADE = 50;
	
	/**
	 * Generates a random grade in the range of MIN_GRADE to MAX_GRADE
	 * @return random grade
	 */
	public static int randomGrade()
	{
		int rndGrade = (int)(Math.random()*(MAX_GRADE-MIN_GRADE+1) + MIN_GRADE);
		return rndGrade;
	}
	
	/**
	 * Add your code below the //--> comments as needed to calculate the average grade.
	 * Post Condition: prints the random list of grades
	 * @return the average
	 */
	public static double averageGrade()
	{
		double average = 0;
		int runningTotal = 0;
		//--> Add additional variables as needed
		
		for (int i=0; i<20; i++)
		{
			int grade = randomGrade();
			System.out.print(grade+" "); //Prints the grades
			
			//--> Add additional code to determine the average
			runningTotal+=grade;
		}
		
		//--> Add additional code to determine the average
		average = runningTotal/20;
		System.out.println();
		return average;
	}
	
	/**
	 * Add your code below the //--> comments to calculate the maximum grade.
	 * Post Condition: prints the random list of grades
	 * @return the maximum
	 */
	public static int maxGrade()
	{
		int max = 0;
		
		//--> Initialize max and add additional variables as needed
		
		for (int i=0; i<20; i++)
		{
			int grade = randomGrade();
			System.out.print(grade+" "); //Prints the grades
			
			//--> Add additional code to determine the max grade
			if (grade>max) {
				max = grade;
			}
		}
		
		//--> Add additional code to determine the max grade if needed
		System.out.println();
		return max;
	}
	
	/**
	 * Add your code below the //--> comments to calculate the minimum grade.
	 * Post Condition: prints the random list of grades
	 * @return the minimum grade
	 */
	public static int minGrade()
	{
		int min = 100;
		
		//--> Initialize min and add additional variables as needed
		
		for (int i=0; i<20; i++)
		{
			int grade = randomGrade();
			System.out.print(grade+" "); //Prints the grades
			
			//--> Add additional code to determine the minimum grade
			if (grade<min) {
				min = grade;
			}
		
		}
		
		//--> Add additional code to determine the minimum grade if needed
		System.out.println();
		return min;
	}
	
	/**
	 * Add your code below the //--> comments to calculate the number of passing grades (60+).
	 * Post Condition: prints the random list of grades
	 * @return the number of passing grades
	 */
	public static int countPassing()
	{
		int numPassing = 0;
		
		//--> Initialize numPassing and add additional variables as needed
		
		for (int i=0; i<20; i++)
		{
			int grade = randomGrade();
			System.out.print(grade+" "); //Prints the grades
		
			//--> Add additional code to determine the number of passing grades
			if (grade >=60) {
				numPassing++;
			}
		}
		
		//--> Add additional code to determine the number of passing grades if needed
		
		System.out.println();
		return numPassing;
	}
	
	/**
	 * Add your code below the //--> comments to find the first A.
	 * Post Condition: prints the random list of grades up to the found A
	 * @return the numeric value of the first A, return 0 if no A is found.
	 */
	public static int findA()
	{
		int firstA = 0;
		int i = 0;
		//--> Initialize firstA and add additional variables as needed
		
		while(i<20) //--> Add the condition needed to terminate the loop
		{
			int grade = randomGrade();
			System.out.print(grade+" "); //Prints the grades
			
			//--> Add additional code to find the first A
			if (grade>=90 && firstA == 0) {
				firstA = grade;
			}
			i++;
		}
		
		//--> Add additional code to find the first A if needed
		
		System.out.println();
		return firstA;
	}
	
	public static void main(String[] args) 
	{
		//Calls the method for each loop algorithm
		//The list and the result are printed
		System.out.println("The average of the above grades is "+ averageGrade());
		System.out.println();
		System.out.println("The maximum of the above grades is "+ maxGrade());
		System.out.println();
		System.out.println("The minimum of the above grades is "+ minGrade());
		System.out.println();
		System.out.println("The number of students passing with the above grades is "+ countPassing());
		System.out.println();
		System.out.println("The first A student earned a "+ findA());
		System.out.println();
	}

}
