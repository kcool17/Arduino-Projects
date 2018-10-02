import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;

public class ZipCode {
	
	public static String getCities(String zipCode) throws FileNotFoundException {
		File zipCodesCity = new File("ZipCodesCity.txt");
		Scanner cityInput = new Scanner(zipCodesCity);
		
		
		cityInput.close();
		
	}
	
	public static String makeBarCode(String zipCode) {
		
	}
	
	public static String readBarCode(String barCode) {
		
	}
	
	public static void main(String[] args) throws FileNotFoundException{
		// TODO Auto-generated method stub
		File zipCodes = new File("ZipCodes.txt");
		File zipBarCodes = new File("ZipBarCodes.txt");
		
		Scanner zipInput = new Scanner(zipCodes);
		Scanner barInput = new Scanner(zipBarCodes);
		
		while (zipInput.hasNextLine()){
			String zipCode = zipInput.nextLine(); 
			String zipCities = getCities(zipCode);
			System.out.println(zipCities);
			String zipBar = makeBarCode(zipCode);
			System.out.println(zipBar);
			System.out.println();
		}
		
		while (barInput.
		
		zipInput.close();
		
		barInput.close();
	}

}
