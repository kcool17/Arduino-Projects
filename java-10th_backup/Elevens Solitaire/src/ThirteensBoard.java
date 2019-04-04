import java.util.List;
import java.util.ArrayList;

/**
 * The ThirteensBoard class represents the board in a game of Thirteens.
 */
public class ThirteensBoard extends Board {

	/**
	 * The size (number of cards) on the board.
	 */
	private static final int BOARD_SIZE = 10;

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
		{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0};

	/**
	 * Flag used to control debugging print statements.
	 */
	private static final boolean I_AM_DEBUGGING = false;


	/**
	 * Creates a new <code>ThirteensBoard</code> instance.
	 */
	 public ThirteensBoard() {
	 	super(BOARD_SIZE, RANKS, SUITS, POINT_VALUES);
	 }

	/**
	 * Determines if the selected cards form a valid group for removal.
	 * In Thirteens, the legal groups are (1) a pair of non-king cards
	 * whose values add to 13 (jack is 11 and queen is 12), and (2) a 
	 * singular king card.
	 * @param selectedCards the list of the indices of the selected cards.
	 * @return true if the selected cards form a valid group for removal;
	 *         false otherwise.
	 */
	@Override
	public boolean isLegal(List<Integer> selectedCards) {
		return (selectedCards.size() == 2 && containsPairSum13(selectedCards)) || (selectedCards.size() == 1 && containsK(selectedCards));
	}

	/**
	 * Determine if there are any legal plays left on the board.
	 * In Thirteens, the legal groups are (1) a pair of non-king cards
	 * whose values add to 13 (jack is 11 and queen is 12), and (2) a 
	 * singular king card.
	 * @return true if there is a legal play left on the board;
	 *         false otherwise.
	 */
	@Override
	public boolean anotherPlayIsPossible() {
		return containsPairSum13(cardIndexes()) || containsK(cardIndexes());
	}

	/**
	 * Check for a 13-pair in the selected cards.
	 * @param selectedCards selects a subset of this board.  It is list
	 *                      of indexes into this board that are searched
	 *                      to find a 13-pair.
	 * @return true if the board entries in selectedCards
	 *              contain a 13-pair; false otherwise.
	 */
	protected boolean containsPairSum13(List<Integer> selectedCards) {
		for (int x = 0; x < selectedCards.size() - 1; x++) {
			for (int y = x + 1; y < selectedCards.size(); y++) {
				if (cardAt(selectedCards.get(x)).pointValue() + cardAt(selectedCards.get(y)).pointValue() == 13) return true;
			}
		}
		return false;
	}

	/**
	 * Check for a King in the selected cards.
	 * @param selectedCards selects a subset of this board.  It is list
	 *                      of indexes into this board that are searched
	 *                      to find a King.
	 * @return true if the board entries in selectedCards
	 *              include a king; false otherwise.
	 */
	protected boolean containsK(List<Integer> selectedCards) {
		for(Integer index : selectedCards) {
			if (cardAt(index).rank() == "king") return true;
		}
		return false;
	}
}
