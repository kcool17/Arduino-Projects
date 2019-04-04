import java.util.List;

/**
 * The CrazyTensBoard class represents the board in a game of Crazy Tens.
 */
public class CrazyTensBoard extends TensBoard{
	
	public CrazyTensBoard() {
		super();
	}
	
	
	/**
	 * Determines if the selected cards form a valid group for removal.
	 * The legal groups are the same as a normal game of Tens, but with
	 * 1 small tweak. You have to choose one extra card to remove with
	 * each normal grouping.
	 * @param selectedCards the list of the indices of the selected cards.
	 * @return true if the selected cards form a valid group for removal;
	 *         false otherwise.
	 */
	@Override
	public boolean isLegal(List<Integer> selectedCards) {
		return (selectedCards.size() == 3 && super.containsPairSum10(selectedCards)) || (selectedCards.size() == 5 && containsQuartet(selectedCards));
	}
	
	/**
	 * Override to make sure the anotherPlayIsPossible method fits in with
	 * the new rule stated in isLegal.
	 * @return true if there is a legal play left on the board;
	 *         false otherwise.
	 */
	@Override
	public boolean anotherPlayIsPossible() {
		return (containsPairSum10(cardIndexes()) && size() > 2) || (containsQuartet(cardIndexes()) && size() > 4);
	}
}
