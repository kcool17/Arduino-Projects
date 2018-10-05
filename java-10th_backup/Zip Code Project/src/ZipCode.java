import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;

public class ZipCode {
	
	//Bar Code translation array
	public static final String[] barNums = {"||:::", ":::||", "::|:|", "::||:", ":|::|", ":|:|:", ":||::", "|:::|", "|::|:", "|:|::"};
	
	/**
	 * This method takes a zipcode input and uses it to find all of the cities in ZipCodesCity.txt, and
	 * return a string of all of the cities (returns "ERROR, INVALID ZIPCODE CITY", if the zipcode isn't found.
	 * @param zipCode
	 * @return
	 * @throws FileNotFoundException
	 */
	public static String getCities(String zipCode) throws FileNotFoundException {
		File zipCodesCity = new File("ZipCodesCity.txt");
		Scanner cityInput = new Scanner(zipCodesCity);
		String currentCity;
		String cityReturn = "";
		while(cityInput.hasNext()) {
			currentCity = cityInput.nextLine();
			if(zipCode.equals(currentCity.substring(0, 5))) {
				cityReturn = cityReturn + currentCity.substring(6) + ", ";
			}
		}
		cityInput.close();
		if (cityReturn.equals("")) {
			return "ERROR, INVALID ZIPCODE CITY!";
		}
		else {
			return cityReturn;
		}
		
		
		
	}
	/**
	 * Takes a zipcode input, and converts into a postal barcode, which it then returns.
	 * @param zipCode
	 * @return
	 */
	public static String makeBarCode(String zipCode) {
		int total = 0;
		int[] zipArray = new int[5];
		for(int x=0; x<5; x++) {
			int intZip = Integer.parseInt(String.valueOf(zipCode.charAt(x)));
			zipArray[x] = intZip;
			total = total + intZip;
		}
		int checkSum = 10 - total % 10;
		if (checkSum== 10) checkSum =0;
		String postalBar = "|" + barNums[zipArray[0]] + barNums[zipArray[1]] + barNums[zipArray[2]] + barNums[zipArray[3]] + barNums[zipArray[4]] + barNums[checkSum] + "|";
		return postalBar;
	}
	/**
	 * Takes a barcode input, and converts it into a proper zipcode, and then returns that. If the barcode is
	 * invalid, it returns "Invalid Barcode".
	 * @param barCode
	 * @return
	 */
	public static String readBarCode(String barCode) {
		String[] barArray = new String[6];
		int z = 0;
		for(int x = 1; x<27; x+=5) {
			barArray[z] = barCode.substring(x, x+5);
			z++;
		}
		int[] zipArray = new int[6];
		for(int x=0;x<6;x++) {
			for(int y=0; y<10; y++) {
				if (barArray[x].equals(barNums[y])){
					zipArray[x] = y;
					break;
				}
				if(y==9) return "Invalid Barcode";
			}
		}
		int total = 0;
		for(int x=0; x<6; x++) {
			total = total + zipArray[x];
		}
		if(!(total%10 == 0)) {
			return "Invalid Barcode";
		}else {
			String toReturn = "";
			for(int x=0;x<5;x++) {
				toReturn = toReturn + zipArray[x];
			}
			return toReturn;
		}
	}
	
	public static void main(String[] args) throws FileNotFoundException{
		// TODO Auto-generated method stub
		//File init
		File zipCodes = new File("ZipCodes.txt");
		File zipBarCodes = new File("ZipBarCodes.txt");
		//Scanner init
		Scanner zipInput = new Scanner(zipCodes);
		Scanner barInput = new Scanner(zipBarCodes);
		//Parts 1 and 2
		while (zipInput.hasNextLine()){
			String zipCode = zipInput.nextLine(); 
			String zipCities = getCities(zipCode);
			System.out.println(zipCode + ": " + zipCities);
			String zipBar = makeBarCode(zipCode);
			System.out.println("Postal Barcode:   " + zipBar);
			String readableBar = zipBar.substring(0, 1) + " " + zipBar.substring(1, 6) + " " + zipBar.substring(6, 11) + " " + zipBar.substring(11, 16) + " " + zipBar.substring(16, 21) + " " + zipBar.substring(21, 26) + " " + zipBar.substring(26, 31) + " " + zipBar.substring(31, 32);
			System.out.println("Readable Barcode: " + readableBar);
			System.out.println();
		}
		System.out.println("-----------------------------------------");
		System.out.println();
		//Part 3
		while (barInput.hasNextLine()) {
			String barCode = barInput.nextLine();
			System.out.println("Barcode: " + barCode);
			String readBarCode = readBarCode(barCode);
			System.out.println("Zipcode: " + readBarCode);
			String barCities;
			if(!readBarCode.equals("Invalid Barcode")) {
				barCities = getCities(readBarCode);
			}else {
				barCities = "No Cities Found";
			}
			System.out.println("Cities: " + barCities);
			System.out.println();
		}
		//Close scanners
		zipInput.close();
		barInput.close();
	}

}
