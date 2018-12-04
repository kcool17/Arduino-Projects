
public class Textbook extends Book{
	private int indexPages;
	public Textbook(int pages, int indexPages) {
		super(pages);
		this.indexPages = indexPages;
	}
	
	public int getPages() {
		return this.getPages() + indexPages;
	}
}
