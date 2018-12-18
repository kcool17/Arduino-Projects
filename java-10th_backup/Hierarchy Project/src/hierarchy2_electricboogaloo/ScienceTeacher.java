package hierarchy2_electricboogaloo;

public abstract class ScienceTeacher extends HighSchoolTeacher{
	
	//Instance variables
	private String scienceType;
	
	//Constructor
	public ScienceTeacher(String name, int gradeLevel, int period, int difficultyLevel, int teacherDifficultyFactor, int amountHW, String scienceType) {
		super(name, gradeLevel, period, difficultyLevel, teacherDifficultyFactor, "Science", amountHW);
		this.scienceType = scienceType;
	}
	
	//Getters
	public String getScienceType() {
		return scienceType;
	}
	
	public String doLab(int studentSafetyLevel)
}
