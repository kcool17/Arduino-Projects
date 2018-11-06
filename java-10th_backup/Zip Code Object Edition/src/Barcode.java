
public class Barcode {

	private int zipNum;
	
	private final String [] BARS =  {"||:::", ":::||", "::|:|", "::||:", ":|::|", ":|:|:", ":||::", "|:::|", "|::|:", "|:|::"};
	
	private String barCode = "";
	
	/**
	 * Constructor for when the class is given a barcode string.
	 * @param barCode
	 */
	public Barcode(String barCode){
		
		this.barCode = barCode;
	}
	
	/**
	 * Constructor for when the class is given a zipcode integer. It corrects the zipcode, and passes it to encode(), which creates a barcode.
	 * @param zipCode
	 */
	public Barcode(int zipCode){
		String myZip = Integer.toString(zipCode);
		
		if (myZip.length()<5) 
		{
			String tempZip = "";
			
			for (int i = 0; i< 5-myZip.length(); i++) 
			{
				
				tempZip = tempZip + "0";
				
			}
			myZip = tempZip + myZip;
		}
		encode(myZip);
	}
	
	/**
	 * Sets the barcode variable.
	 * @param barCode
	 */
	public void setBar(String barCode) {
		this.barCode = barCode;
	}
	
	/**
	 * Returns the barcode variable.
	 * @return
	 */
	public String getBar() {
		
		return barCode;
	
	}
	
	/**
	 * ToString method, which returns the barcode.
	 */
	public String toString() {
		
		return barCode;
	}
	
	/**
	 * Encodes a zipcode into a barcode.
	 * @param zipCode
	 */
	private void encode(String zipCode) {
		
		String barCode = "";
		
		int sixthDig;
		
		int checkDig = 0;
		
		for(int i = 0; i < zipCode.length(); i++)
		{
			zipNum = Integer.parseInt(zipCode.substring(i, i+1));
			
			barCode = barCode + BARS[zipNum];
			
			checkDig = checkDig + zipNum;
		}
		
		sixthDig = 10 - checkDig % 10;
		
		if (sixthDig == 10) sixthDig = 0;
		
		this.barCode = "|" + barCode + BARS[sixthDig] + "|";
	
	}
	
	/**
	 * Checks if a barcode is valid or not.
	 * @return
	 */
	public boolean isValid() {
		
		String barCode = this.barCode;
		
		int[] barDigits = new int[6];
			
			int sum = 0;
			
			String barString;
			
			int barIndex = 0;
			
			for(int i = 1; i < barCode.length() - 5; i+=5) 
			{
				
				barString = barCode.substring(i, i + 5);
			
				
				barDigits[barIndex] = convertBars(barString);
				
				sum = sum + barDigits[barIndex];	
				
				barIndex++;
			
			}
			
			if(sum % 10 == 0) 
			{
				return true;
			}
		return false;
	}
	
	/**
	 * Helper method that takes in a set of 5 bars and turns it into the number it represents.
	 * @param nBars
	 * @return
	 */
	private int convertBars(String nBars) {
		
		int [] barVal = new int[4];
		
		int zipEq;
		
		for(int i = 0; i < 4; i++) 
		{
			
			if(nBars.charAt(i) == '|') 
			{
				barVal[i] = 1;
			}
			
			else
			{
				barVal[i] = 0;
			}
				
			
		}
		
		zipEq = (barVal[0] * 7) + (barVal[1] * 4) + (barVal[2] * 2) + (barVal[3]);
		
		if(zipEq > 9) 
		{
			zipEq = 0;
		}
		
		return zipEq;
		
	}
	
	

}
