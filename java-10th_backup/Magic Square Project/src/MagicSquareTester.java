/**
 * Client class to test the MagicSquare class
 * Creates and prints magic squares of various sizes
 * Prints their size, magic sum, and if they are 
 *    valid (all rows, columns, and major diagonals have the same magic sum)
 * @author rodriguezd
 *
 */
public class MagicSquareTester {
	/**
	 * Print the magic square, it's size, magic sum, and validity
	 * Display the message as a title
	 * @param square
	 * @param msg
	 */
	public static void printSquare(MagicSquare square, String msg)
	{
		System.out.println("***"+msg+"***");
		System.out.println("A Magic square of size "+ square.getSize() + " has a magic sum of " + square.getSum());
		System.out.println(square);
		
		//Check if valid magic square
		String val="";
		if(!square.validSquare())
			val="NOT";
		System.out.println("The magic square is "+val+" valid");
		System.out.println(); 
	}

	/**
	 * Test various sizes of magic squares
	 * @param args
	 */
	public static void main(String[] args) {
		MagicSquare square3 = new MagicSquare();
		printSquare(square3,"3x3 (default constructor) ");
		
		MagicSquare square5 = new MagicSquare(5);
		printSquare(square5,"5x5");
		
		MagicSquare square6 = new MagicSquare(6);
		printSquare(square6,"6x6");
		
		MagicSquare square1 = new MagicSquare(1);
		printSquare(square1,"1x1");

		MagicSquare square13 = new MagicSquare(13);
		printSquare(square13,"13x13");
		


	}

}
