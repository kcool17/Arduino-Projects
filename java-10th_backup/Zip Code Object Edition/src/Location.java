
public class Location {
	private String zipCity;
	private String zipState;
	
	/**
	 * Empty Constructor.
	 * Sets zipCity/zipState to an empty string.
	 */
	public Location() {
		zipCity = "";
		zipState = "";
	}
	/**
	 * Normal constructor.
	 * Sets zipCity/zipState to the values you give it.
	 * @param city
	 * @param state
	 */
	public Location(String city, String state) {
		zipCity = city;
		zipState = state;
	}
	
	/**
	 * Returns the zipCity variable.
	 * @return String
	 */
	public String getCity() {
		return zipCity;
	}
	/**
	 * Returns the zipState variable.
	 * @return String
	 */
	public String getState() {
		return zipState;
	}
	/**
	 * toString method, that puts the city and state together into something good for printing.
	 */
	public String toString() {
		return zipCity + ", " + zipState;
	}
	
	/**
	 * Sets zipCity to a value you choose.
	 * @param city
	 */
	public void setCity(String city) {
		zipCity = city;
	}
	/**
	 * Sets zipState to a value you choose.
	 * @param state
	 */
	public void setState(String state) {
		zipState = state;
	}
	
	
	
	
	
}
