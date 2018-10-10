/**
 * This class creates a Die object, which can be rolled to get a random face from 1-6,
 * and can then return it as either a string or an integer.
 * @author kcool
 *
 */
public class Die {
	//The Die's current face value is stored in this variable.
	public int face;
	/**
	 * This method rolls the die, by setting the face from a random number from 1-6.
	 */
	public void rollDie() {
		face = (int)(Math.random()*6) + 1;
	}
	/**
	 * This function returns the die's face as an integer.
	 * @return
	 */
	public int checkFace() {
		return face;
	}
	/**
	 * This function returns the die's face as a String.
	 * @return
	 */
	public String stringFace() {
		return Integer.toString(face);
	}
}
