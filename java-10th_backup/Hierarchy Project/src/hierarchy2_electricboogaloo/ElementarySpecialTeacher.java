package hierarchy2_electricboogaloo;

public class ElementarySpecialTeacher extends ElementaryTeacher{
	
	//Instance Variables
	private int dayOfTheWeek; //1-7, Sun-Sat
	
	//Constructor
	public ElementarySpecialTeacher(String name, int gradeLevel, int teacherDifficultyFactor, int dayOfTheWeek) {
		super(name, gradeLevel, teacherDifficultyFactor);
		this.dayOfTheWeek = dayOfTheWeek;
	}
	
}
