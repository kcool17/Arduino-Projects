package hierarchy2_electricboogaloo;

public class ElementarySpecialTeacher extends ElementaryTeacher{
	
	//Instance Variables
	private int dayOfTheWeek; //1-5, Mon-Fri
	
	//Constructor
	public ElementarySpecialTeacher(String name, int gradeLevel, int teacherDifficultyFactor, int dayOfTheWeek) {
		super(name, gradeLevel, teacherDifficultyFactor);
		this.dayOfTheWeek = dayOfTheWeek;
	}
	
	//Getters
	public int getDayOfTheWeek() {
		return dayOfTheWeek;
	}
	
	//Overrides
	@Override
	public String teachClass() {
		return "Remember when you used to have specials? Those were fun and easy. Those didn't last long; only gym really remained.";	
	}
	@Override
	public String giveGrade(int studentIntelligence) {
		return "This is a special. You get the same grade as everyone, as long as you try.";
	}
	
	@Override
	public boolean equals(Object obj2) {
		if (!(obj2 instanceof ElementarySpecialTeacher)) return false;
		if (super.equals(obj2) && dayOfTheWeek == ((ElementarySpecialTeacher)obj2).getDayOfTheWeek()) return true;
		else return false;
	}
	
	@Override
	public String toString() {
		String dayOfTheWeekStr;
		switch(dayOfTheWeek) {
			case 1: dayOfTheWeekStr = "Monday";
					break;
			case 2: dayOfTheWeekStr = "Tuesday";
					break;
			case 3: dayOfTheWeekStr = "Wednesday";
					break;
			case 4: dayOfTheWeekStr = "Thursday";
					break;
			default:dayOfTheWeekStr = "Friday";
		}
		return super.toString() + "\nDay of the Week: " + dayOfTheWeekStr;
	}
}
