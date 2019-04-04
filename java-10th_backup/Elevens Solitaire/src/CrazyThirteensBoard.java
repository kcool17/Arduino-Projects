import java.util.List;

/**
 * The CrazyThirteensBoard class represents the board in a game of Crazy Thirteens.
 */
public class CrazyThirteensBoard extends ThirteensBoard{
	
	public CrazyThirteensBoard() {
		super();
	}
	
	/**
	 * Determines if the selected cards form a valid group for removal.
	 * The main rule change in this game is that you must get a quartet of kings
	 * in order to remove them, rather than just one king. The rest of the rules
	 * from Thirteens are the same.
	 * @param selectedCards the list of the indices of the selected cards.
	 * @return true if the selected cards form a valid group for removal;
	 *         false otherwise.
	 */
	@Override
	public boolean isLegal(List<Integer> selectedCards) {
		return (selectedCards.size() == 2 && containsPairSum13(selectedCards)) || (selectedCards.size() == 4 && containsK(selectedCards));
	}
	
	/**
	 * This method checks for a quartet of kings in the selected cards,
	 * in order to make sure to comply with the new rule. 
	 * @param selectedCards selects a subset of this board.  It is list
	 *                      of indexes into this board that are searched
	 *                      to find a quartet of Kings.
	 * @return true if the board entries in selectedCards
	 *              includes a quartet of kings; false otherwise.
	 */
	@Override
	protected boolean containsK(List<Integer> selectedCards) {
		int kingNum = 0;
		for(Integer index : selectedCards) {
			if (cardAt(index).rank() == "king") kingNum++;
		}
		return kingNum == 4;
	}
}
