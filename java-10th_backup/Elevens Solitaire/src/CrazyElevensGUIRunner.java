/**
 * This is a class that plays the GUI version of the Crazy Elevens game.
 * See accompanying documents for a description of how Elevens is played.
 */
public class CrazyElevensGUIRunner {

	/**
	 * Plays the GUI version of Crazy Elevens.
	 * @param args is not used.
	 */
	public static void main(String[] args) {
		Board board = new CrazyElevensBoard();
		CardGameGUI gui = new CardGameGUI(board);
		gui.displayGame();
	}
}
