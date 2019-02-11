
public class MagicSquare {
	
	private int[][] magicSquare;
	
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
			if (x < 0) x += 3;
			if (y > 2) y -= 3;
			if (magicSquare[x][y] != 0) {
				x+=2;
				y--;
				if (y < 0) y += 3;
				if (x > 2) x -= 3;
			}
			
		}
			
	}
	
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
			if (x < 0) x += size;
			if (y > size - 1) y -= size;
			if (magicSquare[x][y] != 0) {
				x+=2;
				y--;
				if (y < 0) y += size;
				if (x > size - 1) x -= size;
			}
			
		}
			
	}
	
	public int getSize() {
		return magicSquare.length;
	}
	
	public int getSum() {
		int sum = 0;
		for (int num : magicSquare[0]) {
			sum += num;
		}
		return sum;
	}
	
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
