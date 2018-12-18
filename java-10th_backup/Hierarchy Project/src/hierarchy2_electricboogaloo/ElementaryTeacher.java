package hierarchy2_electricboogaloo;

public class ElementaryTeacher extends Teacher{
	
	//Constructor
	public ElementaryTeacher(String name, int gradeLevel, int teacherDifficultyFactor) {
		super(name, gradeLevel, 0, 0, teacherDifficultyFactor);
	}
	
	//Methods
	public String teachClass() {
		return "It's elementary school. I'm sure you have fond memories of doing simple worksheets and learning easy subjects. Oh, how times have changed.";
	}
	
	public String giveGrade(int studentIntelligence) {
		if (studentIntelligence > getDifficulty() * 2)
			return "That's a pretty smart student! They probably get a decent amount of 4s, and will be in higher level classes later.";
		else if (studentIntelligence > getDifficulty())
			return "Hey, they're doing pretty well. Mostly 3s, this is what to be expected of elementary schoolers.";
		else
			return "Eh, they're not doing that great; quite a few 2s. Ah well, it's only elementary school. It means nothing.";
	}
	
	
	//Overrides
	@Override
	public boolean equals(Object obj2) {
		if (!(obj2 instanceof ElementaryTeacher)) return false;
		if (getGradeLevel() == ((Teacher)obj2).getGradeLevel()) return true;
		else return false;
	}
}
