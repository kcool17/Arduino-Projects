
public class DieMain {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		//Creates 2 new die objects, and sets the dice to die1 and die2. 
		Die die1 = new Die();
		Die die2 = new Die();
		//Variables for determining how many moves until doubles are rolled.
		int counter = 0;
		boolean doubles = false;
		//Loop that rolls the dice until doubles are found.
		while(!doubles) {
			//Increases counter by 1, so we know how many rolls it took to get doubles.
			counter++;
			//Rolls the two dice.
			die1.rollDie();
			die2.rollDie();
			//Prints the values of each side of the die.
			System.out.println("Die 1: " + die1.stringFace() + " | Die 2: " + die2.stringFace());
			//Checks if the dies' faces are equal, to know if doubles were found. It will then
			//set the variable doubles accordingly, so the loop will exit if they're gotten.
			if (die1.checkFace() == die2.checkFace()) doubles = true;
		}
		//Prints how many rolls it took to get doubles.
		System.out.println("Doubles gotten in " + counter + " rolls!");
	}

}
