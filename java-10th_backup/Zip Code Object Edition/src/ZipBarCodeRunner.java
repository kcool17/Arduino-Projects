import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class ZipBarCodeRunner {

	public static void main(String[] args) throws FileNotFoundException{
		// TODO Auto-generated method stub
		File zipBarCodes = new File("ZipBarCodes.txt");
		Scanner barInput = new Scanner(zipBarCodes);
		ZipCode[] myZips = new ZipCode[11];
		Barcode currentBar;
		ZipCode currentZip;
		int x=0;
		while (barInput.hasNextLine()) {
			currentBar = new Barcode(barInput.nextLine());
			currentZip = new ZipCode(currentBar);
			myZips[x] = currentZip;
			x++;
		}
		for(ZipCode zip : myZips) {
			System.out.println(zip);
		}
		barInput.close();
		
	}

}
