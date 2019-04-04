/**
 * This is a class that plays the GUI version of the Crazy Thirteens game.
 */
public class CrazyThirteensGUIRunner {

	/**
	 * Plays the GUI version of Crazy Thirteens.
	 * @param args is not used.
	 */
	public static void main(String[] args) {
		Board board = new CrazyThirteensBoard();
		CardGameGUI gui = new CardGameGUI(board);
		gui.displayGame();
	}
}
