/**
 * This class implements a vendor that sells one kind
 * of items. A vendor carries out sales transactions.
 */
public class Vendor
{
	//Static variables:
	private static double totalSales = 0;
	
  // Fields:
  private int itemPrice;
  private int totalStock;
  private int centsIn;

  /**
   * Constructs a Vendor
   * @param price the price of a single item in cents (int)
   * @param stock number of items to place in stock (int)
   */
  Vendor(int itemPriceUser, int totalStockUser){
    itemPrice = itemPriceUser;
    totalStock = totalStockUser;
    centsIn = 0;
  }

  /**
   * Sets the quantity of items in stock.
   * @param qty number of items to place in stock (int)
   */
  public void setStock(int putInStock)  {
    totalStock = totalStock + putInStock;
  }

  /**
   * Returns the number of items currently in stock.
   * @return number of items currently in stock (int)
   */
  public int getStock()  {
    return totalStock;
  }

  /**
   * Adds a specified amount (in cents) to the
   * deposited amount.
   * @param number of cents to add to the deposit (int)
   */
  public void addMoney(int numCents)  {
    centsIn = centsIn + numCents;
  }

  /**
   * Returns the currently deposited amount (in cents).
   * @return number of cents in the current deposit (int)
   */
  public int getDeposit(){
    return centsIn;
  }

  /**
   * Implements a sale.  If there are items in stock and
   * the deposited amount is greater than or equal to
   * the single item price, then adjusts the stock
   * and calculates and sets change and returns true;
   * otherwise refunds the whole deposit (moves it into
   * change) and returns false.
   * @return true for a successful sale, false otherwise (boolean)
   */
  public boolean makeSale() {
    if (centsIn < itemPrice || totalStock <=0) return false;
    else {
    	totalSales = totalSales + ((double)itemPrice / 100.0);
    	centsIn = centsIn - itemPrice;
    	totalStock--;
    	return true;
    }
  }

  /**
   * Returns and zeroes out the amount of change (from
   * the last sale or refund).
   * @return number of cents in the current change (int)
   */
  public int getChange()  {
    int oldCents=centsIn;
    centsIn=0;
    return oldCents;
  }
  
  /**
   * 
   */
  public static double getTotalSales() {
	 double temp = totalSales;
	 totalSales = 0;
	 return temp;
  }
}
