import java.util.List;

/**
 * The CrazyElevensBoard class represents the board in a game of Crazy Elevens.
 */
public class CrazyElevensBoard extends ElevensBoard{
	
	public CrazyElevensBoard() {
		super();
	}
	
	
	/**
	 * Determines if the selected cards form a valid group for removal.
	 * The legal groups are the same as a normal game of Elevens, but with
	 * 1 small tweak. You have to choose one extra card to remove with
	 * each standard grouping.
	 * @param selectedCards the list of the indices of the selected cards.
	 * @return true if the selected cards form a valid group for removal;
	 *         false otherwise.
	 */
	@Override
	public boolean isLegal(List<Integer> selectedCards) {
		return (selectedCards.size() == 3 && super.containsPairSum11(selectedCards)) || (selectedCards.size() == 4 && containsJQK(selectedCards));
	}
	
	/**
	 * Override to make sure the anotherPlayIsPossible method fits in with
	 * the new rule stated in isLegal.
	 * @return true if there is a legal play left on the board;
	 *         false otherwise.
	 */
	@Override
	public boolean anotherPlayIsPossible() {
		return (containsPairSum11(cardIndexes()) && size() > 2) || (containsJQK(cardIndexes()) && size() > 2);
	}
}
