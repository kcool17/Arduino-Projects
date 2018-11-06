import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class ZipCodeRunner {

	public static void main(String[] args) throws FileNotFoundException {
		// TODO Auto-generated method stub
		File zipCodes = new File("ZipCodes.txt");
		
		Scanner in = new Scanner(zipCodes);
		
		ZipCode[] zipList = new ZipCode[10];
		
		ZipCode currentZip;
		
		int x=0;
		while (in.hasNextLine()) 
		{
			currentZip = new ZipCode(in.nextLine());
			
			zipList[x] = currentZip;
			
			x++;
		}
		
		for(ZipCode zip : zipList) 
		{
			
			System.out.println(zip);
			
		}
		
		in.close();
	}

}
