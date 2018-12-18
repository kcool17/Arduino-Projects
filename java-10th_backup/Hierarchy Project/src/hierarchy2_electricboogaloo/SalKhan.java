package hierarchy2_electricboogaloo;

public class SalKhan extends Teacher{
	//Instance Variables
	private String subject;
	
	
	//Constructor
	//Sal Khan is a special teacher. He can be anything you wish him to be.
	public SalKhan(int gradeLevel, int difficultyLevel, String subject) {
		super("Sal Khan", gradeLevel, 0, difficultyLevel, -4);
		this.subject = subject;
	}
	
	//Getters
	public String getSubject() {
		return subject;
	}
	
	//Methods
	public String teachClass() {
		return "Sal Khan bestows his infinite wisdom upon you. If you do poorly, you can not be saved.";
	}
	public String giveGrade(int studentIntelligence) {
		if (studentIntelligence >= getDifficulty()) 
			return "You have done well, young one. You have benefitted greatly from the Khan, and are now one step closer to enlightenment.";
		else if (studentIntelligence<getDifficulty() && studentIntelligence > 1) 
			return "Very good, young one. You are learning, and will one day understand that which you seek to understand.";
		else 
			return "There is no saving you, child. Run, run away, to a place that will accept you. You will forever be in the shadows, and never reach True Enlightenment.";
	}
	
	//Overrides
	@Override
	public boolean equals(Object obj2) {
		if (obj2 instanceof SalKhan) return true; //All Sal Khans are created equal. What he teaches does not matter; he is One.
		else return false;
	}
	
	@Override
	public String toString() {
		return super.toString() + "\nSubject: " + subject;
	}
	
}
