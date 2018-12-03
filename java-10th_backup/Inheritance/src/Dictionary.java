
public class Dictionary extends Book{
	private int definitions = 52500;
	
	public Dictionary(int pages, int definitions) {
		super(pages);
		this.definitions = definitions;
	}
	
	public int getDefinitions() {
		return definitions;
	}
	
	public int getPages() {
		return this.getPages();
	}
	@Override
	public void printMessage() {
		super.printMessage();
		System.out.print("Definitions per page: " + definitions/this.getPages());
	}
}
