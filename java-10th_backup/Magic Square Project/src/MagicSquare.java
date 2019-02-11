
public class MagicSquare {
	
	//Instance Data
	private int[][] magicSquare; //The magic square array
	
	/**
	 * Default Constructor; makes a 3x3 magic square.
	 */
	public MagicSquare() {
		magicSquare = new int[3][3];
		int magicNum = 1;
		int x = 0;
		int y = 1;
		while (magicNum <= 9) {
			magicSquare[x][y] = magicNum;
			magicNum++;
			x--;
			y++;
			//Goes to the opposite side if needed.
			if (x < 0) x += 3;
			if (y > 2) y -= 3;
			//If the next square is already filled in, move down one square instead.
			if (magicSquare[x][y] != 0) {
				x+=2;
				y--;
				if (y < 0) y += 3;
				if (x > 2) x -= 3;
			}
			
		}
			
	}
	
	/**
	 * Constructor that takes a specific size for the magic square as input, and then constructs one based on that.
	 * @param size The size of the magic square
	 */
	public MagicSquare(int size) {
		if (size < 3) size = 3;
		if (size % 2 == 0) size++;
		magicSquare = new int[size][size];
		int magicNum = 1;
		int x = 0;
		int y = ((size + 1) / 2) - 1;
		while (magicNum <= size * size) {
			magicSquare[x][y] = magicNum;
			magicNum++;
			x--;
			y++;
			//Goes to the opposite side if needed.
			if (x < 0) x += size;
			if (y > size - 1) y -= size;
			//If the next square is already filled in, move down one square instead.
			if (magicSquare[x][y] != 0) {
				x+=2;
				y--;
				if (y < 0) y += size;
				if (x > size - 1) x -= size;
			}
			
		}
			
	}
	
	/**
	 * Gets the size of the magic square.
	 * @return The size of the magic square
	 */
	public int getSize() {
		return magicSquare.length;
	}
	
	/**
	 * Gets the magic sum of the square. (The sum of a row/column/diagonal.
	 * @return The magic sum of the square.
	 */
	public int getSum() {
		int sum = 0;
		for (int num : magicSquare[0]) {
			sum += num;
		}
		return sum;
	}
	
	/**
	 * Checks if the magic square is valid, by making sure all of the diagonals, rows, and columns add up to the same number.
	 * @return Whether the square is valid or not.
	 */
	public boolean validSquare() {
		int currentSum;
		
		for (int x = 0; x < getSize(); x++) {
			currentSum = 0;
			for (int y = 0; y < getSize(); y++) {
				currentSum += magicSquare[x][y];
			}
			if (currentSum != getSum()) return false;
		}
		
		for (int y = 0; y < getSize(); y++) {
			currentSum = 0;
			for (int x = 0; x < getSize(); x++) {
				currentSum += magicSquare[x][y];
			}
			if (currentSum != getSum()) return false;
		}
		
		currentSum = 0;
		for (int x = 0; x < getSize(); x++) {
			currentSum += magicSquare[x][x];
		}
		if (currentSum != getSum()) return false;
		
		currentSum = 0;
		for (int x = 0; x < getSize(); x++) {
			currentSum += magicSquare[x][getSize() - 1 - x];
		}
		if (currentSum != getSum()) return false;
		
		return true;
	}
	
	/**
	 * ToString method, returning a formatted magic square.
	 */
	@Override
	public String toString() {
		String myString = "";
		for (int[] x : magicSquare) {
			for (int y : x) {
				myString += y + "\t";
			}
			myString += "\n";
		}
		return myString;
	}	
	
	
}
