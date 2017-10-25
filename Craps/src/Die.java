/**
 * Represents a single Die that generates a random integer in the range 1 to 6
 * 
 * @author rodriguezd (defined by Case Study in Java Methods by Maria Litwin & Gary Litwin
 *
 */
		
public class Die 
{
	private int dots;  //1 to 6
	
	/**
	 * Rolls the Die, generating and setting the Die dots to a random integer from 1 to 6
	 * Post: dots is updated with the new roll
	 */
	public void roll()
	{
		//<Add code here>
		dots = (int)(Math.random()*(6-1+1)+1); //Sets the number of dots to a random number from 1 to 6
	}
	
	/**
	 * Returns the number of dots from the last roll as held in the variable dots
	 * @return
	 */
	public int getNumDots()
	{
		return dots;
	}
}
