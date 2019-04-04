/**
 * This is a class that plays the GUI version of the Crazy Tens game.
 */
public class CrazyTensGUIRunner {

	/**
	 * Plays the GUI version of Crazy Tens.
	 * @param args is not used.
	 */
	public static void main(String[] args) {
		Board board = new CrazyTensBoard();
		CardGameGUI gui = new CardGameGUI(board);
		gui.displayGame();
	}
}
