
public class DieMain {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		//Creates 5 new die objects
		Die die1 = new Die(), die2 = new Die(), die3 = new Die(), die4 = new Die(), die5 = new Die();
		Die[] dieArr = {die1, die2, die3, die4, die5};
		int[] rollArr = new int[5];
		//Variables for determining how many moves until doubles are rolled.
		int counter = 0;
		boolean yahtzee = false;
		//Loop that rolls the dice until doubles are found.
		while(!yahtzee) {
			//Increases counter by 1, so we know how many rolls it took to get Yahtzee.
			counter++;
			int x=0;
			for (Die myDie : dieArr) {
				myDie.rollDie();
				rollArr[x] = myDie.checkFace();
				x++;
			}
			System.out.println(rollArr[0] + " | " + rollArr[1] + " | " + rollArr[2] + " | " + rollArr[3] + " | " + rollArr[4]);
			if (rollArr[0] == rollArr[1] && rollArr[1] == rollArr[2] && rollArr[2] == rollArr[3] && rollArr[3] == rollArr[4]) yahtzee = true;
		}
		//Prints how many rolls it took to get doubles.
		System.out.println("Yahtzee gotten in " + counter + " rolls!");
	}

}
