/**
 * This is a class that plays the GUI version of the Tens game.
 * See accompanying documents for a description of how Tens is played.
 */
public class TensGUIRunner {

	/**
	 * Plays the GUI version of Tens.
	 * @param args is not used.
	 */
	public static void main(String[] args) {
		Board board = new TensBoard();
		CardGameGUI gui = new CardGameGUI(board);
		gui.displayGame();
	}
}
