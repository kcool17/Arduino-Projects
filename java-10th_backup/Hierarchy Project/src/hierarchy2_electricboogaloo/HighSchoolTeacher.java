package hierarchy2_electricboogaloo;

public abstract class HighSchoolTeacher extends Teacher{
	
	//Instance variables
	private String subjectCategory;
	private int amountHW; //Value from 1-10, with 10 being a huge amount of HW, and 1 being near none.
	
	//Constructor
	public HighSchoolTeacher(String name, int gradeLevel, int period, int difficultyLevel, int teacherDifficultyFactor, String subjectCategory, int amountHW) {
		super(name, gradeLevel, period, difficultyLevel, teacherDifficultyFactor);
		this.subjectCategory = subjectCategory;
		if (amountHW >= 10) this.amountHW = 10;
		else if (amountHW <= 1) this.amountHW = 1;
		else this.amountHW = amountHW;
	}
	
	//Getters
	public String getSubjectCategory() {
		return subjectCategory;
	}
	
	public int getAmountHW() {
		return amountHW;
	}
	
	//Anstract Methods
	public abstract String giveTest(int studentIntelligence, int studentStudyAmount);
	
	//Overrides
	@Override
	public String toString() {
		return super.toString() + "\nSubject Category: " + subjectCategory + "\nAmount of HW (1-10 scale): " + amountHW;
	}
	
	
}
