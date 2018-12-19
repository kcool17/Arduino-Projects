package hierarchy2_electricboogaloo;

public class APBioTeacher extends ScienceTeacher implements AP{
	
	//Constructor
	public APBioTeacher(String name, int gradeLevel, int period, int difficultyLevel, int teacherDifficultyFactor, int amountHW, String scienceType) {
		super(name, gradeLevel, period, difficultyLevel, teacherDifficultyFactor, amountHW, "AP Biology");
	}
	
	
	
	
	
	//Overrides
	@Override
	public boolean equals(Object obj2) {
		if (!(obj2 instanceof APBioTeacher)) return false;
		else return super.equals(obj2);
		
	}
	
	@Override
	public String toString() {
		
	}
}
