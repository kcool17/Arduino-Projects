import java.util.Scanner;
import java.lang.Math;

public class rpsProgram {

	//1 = Rock, 2 = Paper, 3 = Scissors
	public static int whoWon(int humanGuess, int compGuess) {
		//Returns who won (1 = Player, -1 = Computer, 0 = Tie), and comes up with the computer's guess
		if ((compGuess == 3 && humanGuess == 2) || (compGuess == 2 && humanGuess == 1) || (compGuess == 1 && humanGuess == 3)) {
			return -1;
		}else if ((humanGuess == 3 && compGuess == 2) || (humanGuess == 2 && compGuess == 1) || (humanGuess == 1 && compGuess == 3)) {
			return 1;
		}else {
			return 0;
		}
	}
	
	public static void printTable(int[] humanArray, int[] compArray, int[] winArray) {
		//Prints out all the data in a nice table
		
		//Makes new arrays with Strings rather than integers
		String prettyHumanArray[] = new String[10];
		String prettyCompArray[] = new String[10];
		String prettyWinArray[] = new String[10];
		//Adds data from previous arrays to new ones
		for(int x=0; x<10; x++) {
			if (humanArray[x] == 1) {
				prettyHumanArray[x] = "Rock    ";
			}else if (humanArray[x] == 2) {
				prettyHumanArray[x] = "Paper   ";
			}else{ 
				prettyHumanArray[x] = "Scissors";
			}
			
			if (compArray[x] == 1) {
				prettyCompArray[x] = "Rock    ";
			}else if (compArray[x] == 2) {
				prettyCompArray[x] = "Paper   ";
			}else{
				prettyCompArray[x] = "Scissors";
			}
			
			if (winArray[x] == 1) {
				prettyWinArray[x] = "Human   ";
			}else if (winArray[x] == -1) {
				prettyWinArray[x] = "Computer";
			}else{
				prettyWinArray[x] = "Tie     ";
			}
		}
		//Prints table
		System.out.println("----------------------------------------------------------------------------------------------------------------------------------");
		System.out.print("| Game Turn        | ");
		for(int x=0; x<10; x++) {
			System.out.printf("%8d", (x+1));
			System.out.print(" | ");
		}
		System.out.println();
		System.out.println("----------------------------------------------------------------------------------------------------------------------------------");
		System.out.print("| Human's Guess    | ");
		for(int x=0; x<10; x++) {
			System.out.print(prettyHumanArray[x]);
			System.out.print(" | ");
		}
		System.out.println();
		System.out.println("----------------------------------------------------------------------------------------------------------------------------------");
		System.out.print("| Computer's Guess | ");
		for(int x=0; x<10; x++) {
			System.out.print(prettyCompArray[x]);
			System.out.print(" | ");
		}
		System.out.println();
		System.out.println("----------------------------------------------------------------------------------------------------------------------------------");
		System.out.print("| Game Result      | ");
		for(int x=0; x<10; x++) {
			System.out.print(prettyWinArray[x]);
			System.out.print(" | ");
		}
		System.out.println();
		System.out.println("----------------------------------------------------------------------------------------------------------------------------------");

		//Get game stats
		int winNum = 0;
		int loseNum = 0;
		int tieNum = 0;
		String didWin = "";
		for(int x=0; x<10; x++) {
			if (winArray[x] == 1) {
				winNum = winNum + 1;
			}else if (winArray[x] == -1) {
				loseNum = loseNum + 1;
			}else {
				tieNum = tieNum + 1;
			}
			if (winNum > loseNum) {
				didWin = "Human";
			}else if (winNum < loseNum) {
				didWin = "Computer";
			}else {
				didWin = "Nobody";
			}
		}
		//Print game stats
		System.out.println();
		System.out.print("# of wins: " + winNum + " | # of losses: " + loseNum + "| # of ties: " + tieNum + " | Winner: " + didWin);
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		//Creates variables/scanners
		Scanner myInput = new Scanner(System.in);
		int humanInputArray[] = new int[10];
		int compInputArray[] = new int[10];
		int winArray[] = new int[10];
		
		//Prints intro
		System.out.println("Welcome to Rock, Paper, Scissors!");
		System.out.println("I expect you know how to play, so lets start!");
		
		
		int myTurn = 0;
		while (myTurn<10) {
			//Asks for input
			System.out.println();
			System.out.println("Turn: " + (myTurn+1));
			System.out.println("Choose Rock, Paper, or Scissors!");
			
			//Gets input
			String humanInput = myInput.next();
			int altHumanInput = -666;
			boolean didSucceed = false;
			while (!didSucceed){
				humanInput = humanInput.toLowerCase();
				if (humanInput.equals("rock") || humanInput.equals("r")) {
					altHumanInput = 1;
					didSucceed = true;
				}else if (humanInput.equals("paper") || humanInput.equals("p")) {
					altHumanInput = 2;
					didSucceed = true;
				}else if (humanInput.equals("scissors") || humanInput.equals("s")) {
					altHumanInput = 3;
					didSucceed = true;
				}else {
					System.out.println("Invalid input! Please try again, this time entering Rock, Paper, or Scissors.");
					humanInput = myInput.next();
				}
			}
			int compInput = ((int) (Math.round((Math.random() *2.0)))) + 1; //Computer's guess
			//Checks who won
			int gameResult = whoWon(altHumanInput, compInput);
			//Adds data to arrays
			humanInputArray[myTurn] = altHumanInput;
			compInputArray[myTurn] = compInput;
			winArray[myTurn] = gameResult;
			//Formats the winner to a string
			String formatGameResult = "";
			if (gameResult == 1) {
				formatGameResult = "You! Congrats!";
			}else if (gameResult == -1) {
				formatGameResult = "The Computer! How unfortunate...";
			}else if (gameResult == 0){
				formatGameResult = "Nobody! It was a Tie!";
			}else {
				formatGameResult = "The Programmer! Ok, not really, there's an error.";
			}
			//Tells who won that round 
			System.out.println();
			System.out.println("The winner of that round was... " + formatGameResult);
			myTurn = myTurn + 1;
			if(myTurn <10){
				System.out.println("Let's go again!");
			}else {
				System.out.println("Game over! Let's see the results!");
			}
		}
		printTable(humanInputArray, compInputArray, winArray);
		myInput.close();
	}

}
