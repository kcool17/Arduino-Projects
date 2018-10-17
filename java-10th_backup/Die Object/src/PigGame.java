
public class PigGame {
	private int playerScore;
	private int computerScore;
	private int playerTurn;
	private int computerTurn;
	private boolean isPlayerTurn;
	private Die die1;
	private Die die2;
	
	public PigGame(){
		playerScore = 0;
		computerScore = 0;
		playerTurn = 0;
		computerTurn = 0;
		isPlayerTurn = true;
		die1 = new Die();
		die2 = new Die();
	}
	
	public void switchTurn() {
		playerTurn = 0;
		computerTurn = 0;
		if(isPlayerTurn) isPlayerTurn = false;
		else isPlayerTurn = true;
	}
	
	public String takeTurn() {
		die1.rollDie();
		die2.rollDie();
		int rollOne = die1.checkFace();
		int rollTwo = die2.checkFace();
		if (rollOne == 1 && rollTwo == 1) {
			if (isPlayerTurn) playerScore = 0;
			else computerScore = 0;
			return "a " + rollOne + " and a" + rollTwo + ". Switching turns!";
		}else if (rollOne == 1 || rollTwo == 1) {
			if (isPlayerTurn) playerTurn = 0;
			else computerTurn = 0;
			return "a " + rollOne + " and a" + rollTwo + ". Switching turns";
		}else {
			playerTurn = playerTurn + rollOne + rollTwo;
		}
		
		return "a " + rollOne + " and a" + rollTwo + ".";
	}
	
	public int didWin() {
		if (playerScore + playerTurn >= 100) return 1;
		else if (computerScore + computerTurn >= 100) return -1;
		else return 0;
	}
	
	//Getters
	public int getCompScore() {
		return computerScore;
	}
	
	public int getCompTurn() {
		return computerTurn;
	}
	
	public int getPlayerScore() {
		return playerScore;
	}
	
	public int getPlayerTurn() {
		return playerTurn;
	}
	
	public boolean isPlayerTurn() {
		return isPlayerTurn;
	}
}
