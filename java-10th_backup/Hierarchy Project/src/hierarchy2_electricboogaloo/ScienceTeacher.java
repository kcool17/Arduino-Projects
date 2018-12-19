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
	
	public String doLab(int studentSafetyLevel) { //studentSafetyLevel is a number from 1-10, with 1 being the least safe.
		if (studentSafetyLevel > 7) return "Hey, that's a prettu safe student. Nothing bad happened!";
		else if (studentSafetyLevel > 3) return "Well, they broke some stuff. At least it was only some glass beakers, rather than a beaker of dangerous chemicals.";
		else return "Annnnnddd they spilled the dangerous chemicals. Time to evacuate. And actually use the eyewash station that we learned about at the beginning of the year.";
	}
	
	
	//Overrides
	@Override
	public boolean equals(Object obj2) {
		if (!(obj2 instanceof ScienceTeacher)) return false;
		if (super.equals(obj2) && scienceType == ((ScienceTeacher)obj2).getScienceType()) return true;
		else return false;
		
	}
	
	@Override
	public String toString() {
		return super.toString() + "\nType of Science: " + scienceType;
	}
}
