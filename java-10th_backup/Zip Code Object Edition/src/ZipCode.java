import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class ZipCode {
	private final String[] barNums = {"||:::", ":::||", "::|:|", "::||:", ":|::|", ":|:|:", ":||::", "|:::|", "|::|:", "|:|::"};
	private String zipCode;
	private Barcode barCode;
	private Location[] zipLocations;
	
	/**
	 * String constructor, for when you give the ZipCode class a zipcode to start with.
	 * @param myZip
	 * @throws FileNotFoundException
	 */
	public ZipCode(String myZip) throws FileNotFoundException {
		zipCode = myZip;
		findLocations();
		int intZip = Integer.parseInt(zipCode);
		barCode = new Barcode(intZip);
	}
	/**
	 * Barcode constructor, for when you give the ZipCode class a barcode to start with.
	 * @param myBar
	 * @throws FileNotFoundException
	 */
	public ZipCode(Barcode myBar) throws FileNotFoundException {
		barCode = myBar;
		if (readBarcode()) {
			findLocations();
		}
	}
	
	/**
	 * Returns the barcode.
	 * @return
	 */
	public Barcode getBar() {
		return barCode;
	}
	/**
	 * Returns the zipcode.
	 * @return
	 */
	public String getZip() {
		return zipCode;
	}
	/**
	 * ToString method (returns a string with the zipcode, barcode, and locations all in one string)
	 */
	public String toString() {
		if (!barCode.isValid()) return "INVALID BARCODE";
		
		String locString = "";
		for(Location loc : zipLocations) {
			if (loc != null) locString = locString + " | " + loc;
		}
		return "" + zipCode + " | " + barCode + locString;
	}
	/**
	 * Returns the list of locations.
	 * @return
	 */
	public Location[] getLocations() {
		return zipLocations;
	}
	
	/**
	 * Method that finds all of the locations corresponding to a zipcode, and puts them in an array of location objects.
	 * @throws FileNotFoundException
	 */
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
	/**
	 * Reads the barcode, and turns it into a zipcode. If it's invalid, it returns false.
	 * @return
	 */
	private boolean readBarcode() {
		if (!barCode.isValid()) return false;
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
		return true;
	}
	
}
