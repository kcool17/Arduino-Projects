import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class ZipCode {
	private final String[] barNums = {"||:::", ":::||", "::|:|", "::||:", ":|::|", ":|:|:", ":||::", "|:::|", "|::|:", "|:|::"};
	private String zipCode;
	private Barcode barCode;
	private Location[] zipLocations;
	
	public ZipCode(String myZip) {
		zipCode = myZip;
		findLocations();
		barCode = new Barcode(zipCode);
	}
	public ZipCode(Barcode myBar) throws FileNotFoundException {
		barCode = myBar;
		readBarcode();
		findLocations();
	}
	
	public Barcode getBar() {
		return barCode;
	}
	public String getZip() {
		return zipCode;
	}
	public String toString() {
		return "" + barCode;
	}
	public Location[] getLocations() {
		return zipLocations;
	}
	
	private void findLocations() throws FileNotFoundException{
		File zipCodesCity = new File("ZipCodesCity.txt");
		Scanner cityInput = new Scanner(zipCodesCity);
		String currentLocation;
		String currentLocArr[];
		int x = 0;
		zipLocations = new Location[10];
		while(cityInput.hasNext() && x<10) {
			currentLocation = cityInput.nextLine();
			currentLocArr = currentLocation.split(",");
			if(zipCode.equals(currentLocArr[0])) {
				zipLocations[x] = new Location(currentLocArr[1], currentLocArr[2]);
				x++;
			}
		}
		cityInput.close();
		
	}
	private void readBarcode() {
		if (!barCode.isValid()) return;
		String myBar = barCode.toString();
		String[] barArray = new String[6];
		int z = 0;
		for(int x = 1; x<27; x+=5) {
			barArray[z] = myBar.substring(x, x+5);
			z++;
		}
		int[] zipArray = new int[6];
		for(int x=0;x<6;x++) {
			for(int y=0; y<10; y++) {
				if (barArray[x].equals(barNums[y])){
					zipArray[x] = y;
					break;
				}
				if(y==9) zipCode = "Invalid Barcode";
			}
		}
		
		String toReturn = "";
		for(int x=0;x<5;x++) {
			toReturn = toReturn + zipArray[x];
		}
		zipCode = toReturn;
		
	}
	
}
