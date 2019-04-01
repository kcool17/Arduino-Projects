/**
 * This is a class that tests the Deck class.
 */
public class DeckTester {

	/**
	 * The main method in this class checks the Deck operations for consistency.
	 *	@param args is not used.
	 */
	public static void main(String[] args) {
		String[] cardNames = {"King", "Queen", "Jack"};
		String[] suits = {"Diamond", "Spade"};
		int[] cardValues = {1, 3, 6};
		Deck deck1 = new Deck(cardNames , suits, cardValues);
		System.out.println(deck1);
		deck1.deal();
		System.out.println(deck1);
		deck1.shuffle();
		System.out.println(deck1);
		deck1.deal();
	}
}
