/**
 * This class creates a Die object, which can be rolled to get a random face from 1-6,
 * and can then return it as either a string or an integer.
 * @author kcool
 *
 */
public class Die {
	//The Die's current face value is stored in this variable.
	private int face;
	//The # of sides on the die.
	private int sides;
	/**
	 * Constructor method; rolls the die once.
	 */
	public Die() {
		rollDie();
		sides = 6;
	}
	/**
	 * Constructor method for number of sides.
	 */
	public Die(int sideNum) {
		if (sideNum>1)sides = sideNum;
		else sides=2;
	}
	/**
	 * This method rolls the die, by setting the face from a random number from 1-6.
	 */
	public void rollDie() {
		face = (int)(Math.random()*sides) + 1;
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
	public String toString() {
		return Integer.toString(face);
	}
	/**
	 * Changes the amount of sides on the die.
	 * @param sideNum
	 */
	public void changeSides(int sideNum) {
		if (sideNum>1)sides = sideNum;
		else sides=2;
	}
	/**
	 * Returns the amount of sides.
	 * @return
	 */
	public int getSides() {
		return sides;
	}
	/**
	 * Checks if this die has the same face as another die.
	 * @param otherDie
	 * @return
	 */
	public boolean isDoubles(Die otherDie) {
		if(face==otherDie.checkFace())return true;
		else return false;
	}
}
