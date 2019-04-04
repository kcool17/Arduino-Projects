import java.util.Scanner;

/**
 * I didn't want to clog up the dropbox with a bunch of runner files, so I just put them all in here.
 */
public class MainRunner {

	/**
	 * Main runner class for all games.
	 * @param args is not used
	 */
	public static void main(String[] args) {
		int gameNum = -1;
		Scanner in = new Scanner(System.in);
		System.out.println("What game do you wish to play? Input the correct number for what game you want to play. \nElevens = 0\nTens = 1\nThirteens = 2\nCrazy Elevens = 3\nCrazy Tens = 4\nCrazy Thirteens = 5");
		String input = in.nextLine();
		boolean valid = false;
		while (!valid) {
			try {
				gameNum = Integer.parseInt(input);
			}
			catch (NumberFormatException e) {
				
			}
			finally {
				if (gameNum < 0 || gameNum > 5) {
					System.out.println("Invalid Input! Please try again, making sure to input a valid game number!");
					input = in.nextLine();
				}
				else valid = true;
			}
		}
		
		Board board = 			  new ElevensBoard();
		if (gameNum == 1) board = new TensBoard(); 
		if (gameNum == 2) board = new ThirteensBoard(); 
		if (gameNum == 3) board = new CrazyElevensBoard(); 
		if (gameNum == 4) board = new CrazyTensBoard(); 
		if (gameNum == 5) board = new CrazyThirteensBoard(); 
		CardGameGUI gui = new CardGameGUI(board);
		gui.displayGame();
		in.close();

	}

}
