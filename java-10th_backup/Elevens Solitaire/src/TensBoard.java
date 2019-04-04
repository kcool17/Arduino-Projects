import java.util.List;
import java.util.ArrayList;

/**
 * The TensBoard class represents the board in a game of Tens.
 */
public class TensBoard extends Board {

	/**
	 * The size (number of cards) on the board.
	 */
	private static final int BOARD_SIZE = 13;
	/**
	 * The ranks of the cards for this game to be sent to the deck.
	 */
	private static final String[] RANKS =
		{"ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"};

	/**
	 * The suits of the cards for this game to be sent to the deck.
	 */
	private static final String[] SUITS =
		{"spades", "hearts", "diamonds", "clubs"};

	/**
	 * The values of the cards for this game to be sent to the deck.
	 */
	private static final int[] POINT_VALUES =
		{1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0};

	/**
	 * Flag used to control debugging print statements.
	 */
	private static final boolean I_AM_DEBUGGING = false;


	/**
	 * Creates a new <code>TensBoard</code> instance.
	 */
	 public TensBoard() {
	 	super(BOARD_SIZE, RANKS, SUITS, POINT_VALUES);
	 }

	/**
	 * Determines if the selected cards form a valid group for removal.
	 * In Tens, there is a legal play if the board contains
	 * (1) a pair of non-face cards whose values add to 10, or (2) a group
	 * of four cards consisting of only 10s, jacks, queens, or kings.
	 * @param selectedCards the list of the indices of the selected cards.
	 * @return true if the selected cards form a valid group for removal;
	 *         false otherwise.
	 */
	@Override
	public boolean isLegal(List<Integer> selectedCards) {
		return (selectedCards.size() == 2 && containsPairSum10(selectedCards)) || (selectedCards.size() == 4 && containsQuartet(selectedCards));
	}

	/**
	 * Determine if there are any legal plays left on the board.
	 * In Tens, there is a legal play if the board contains
	 * (1) a pair of non-face cards whose values add to 10, or (2) a group
	 * of four cards consisting of only 10s, jacks, queens, or kings.
	 * @return true if there is a legal play left on the board;
	 *         false otherwise.
	 */
	@Override
	public boolean anotherPlayIsPossible() {
		return containsPairSum10(cardIndexes()) || containsQuartet(cardIndexes());
	}

	/**
	 * Check for a 10-pair in the selected cards.
	 * @param selectedCards selects a subset of this board.  It is list
	 *                      of indexes into this board that are searched
	 *                      to find a 10-pair.
	 * @return true if the board entries in selectedCards
	 *              contain a 10-pair; false otherwise.
	 */
	protected boolean containsPairSum10(List<Integer> selectedCards) {
		for (int x = 0; x < selectedCards.size() - 1; x++) {
			for (int y = x + 1; y < selectedCards.size(); y++) {
				if (cardAt(selectedCards.get(x)).pointValue() + cardAt(selectedCards.get(y)).pointValue() == 10) return true;
			}
		}
		return false;
	}

	/**
	 * Check for a Quartet in the selected cards.
	 * @param selectedCards selects a subset of this board.  It is list
	 *                      of indexes into this board that are searched
	 *                      to find a Quartet.
	 * @return true if the board entries in selectedCards
	 *              include a quartet of 10s, jacks, queens, or kings; false otherwise.
	 */
	protected boolean containsQuartet(List<Integer> selectedCards) {
		int tenNum = 0;
		int jackNum = 0;
		int queenNum = 0;
		int kingNum = 0;
		for(Integer index : selectedCards) {
			if (cardAt(index).rank() == "10") tenNum++;
			if (cardAt(index).rank() == "jack") jackNum++;
			if (cardAt(index).rank() == "queen") queenNum++;
			if (cardAt(index).rank() == "king") kingNum++;
			if (tenNum == 4 || kingNum == 4 || queenNum == 4 || jackNum == 4) return true;
		}
		return (tenNum == 4 || kingNum == 4 || queenNum == 4 || jackNum == 4);
	}
}
