
public abstract class Book {
	private int pages;
	
	
	public Book(int pages) {
		this.pages = pages;
	}
	
	
	public abstract int getPages();
	
	public void printMessage() {
		System.out.print("Number of pages: " + pages);
	}
}
