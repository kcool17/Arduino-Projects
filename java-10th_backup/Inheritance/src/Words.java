
public class Words {
	
	
	public static void main(String args[]) {
		Dictionary myDict = new Dictionary(1000, 52500);
		
		int pages = myDict.getPages();
		int definitions = myDict.getDefinitions();
		System.out.println("Number of pages: " + pages);
		System.out.println("Number of definitions: " + definitions);
		System.out.println("Definitons per page: " + definitions/pages);
	}
}
