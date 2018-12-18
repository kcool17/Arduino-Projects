package hierarchy2_electricboogaloo;

public abstract class Teacher implements Comparable<Teacher>{
	
	//Static variables
	private static int teachersInExistence = 0;
	
	//Instance variables
	private String name;
	private int gradeLevel;
	private int period; //Period 0 means the teacher doesn't have a period. (E.g. teach throughout the whole day)
	private int difficultyLevel;
	private int teacherDifficultyFactor; //How much harder the specific teacher makes the class. Can be negative or positive. 0 is a standard teacher.
	
	//Constructor
	public Teacher(String name, int gradeLevel, int period, int difficultyLevel, int teacherDifficultyFactor) {
		this.name = name;
		this.gradeLevel = gradeLevel;
		this.period = period;
		this.difficultyLevel = difficultyLevel;
		this.teacherDifficultyFactor = teacherDifficultyFactor;
		teachersInExistence++;
	}
	
	//Getters
	public String getName() {
		return name;
	}
	
	public int getGradeLevel() {
		return gradeLevel;
	}
	
	public int getPeriod() {
		return period;
	}
	
	public int getDifficultyLevel() {
		return difficultyLevel;
	}
	
	public int getTeacherDifficultyFactor() {
		return teacherDifficultyFactor;
	}
	
	//Static methods
	public static int getTeachersInExistence() {
		return teachersInExistence;
	}
	
	
	
	//Abstract Methods
	public abstract String teachClass();
	public abstract String giveGrade(int studentIntelligence); //StudentIntelligence is an integer from 1-20, determining how good they are at the subject at hand.
	
	
	
	//Methods
	public int getDifficulty() {
		return gradeLevel + difficultyLevel + teacherDifficultyFactor;
	}
	
	
	//compareTo (Compares the difficulty of the teachers).
	public int compareTo(Teacher obj2) {
		if (this.getDifficulty() < obj2.getDifficulty()) return -1;
		else if (this.getDifficulty() < obj2.getDifficulty()) return 1;
		else return 0;
	}
	
	//Overrides
	//Equals method, which checks to see if they teach the same type of class (grade/difficulty)
	@Override
	public boolean equals(Object obj2) {
		if (!(obj2 instanceof Teacher)) return false;
		if (gradeLevel == ((Teacher)obj2).getGradeLevel() && difficultyLevel == ((Teacher)obj2).getDifficultyLevel()) return true;
		else return false;
		
	}
	
	@Override
	public String toString() {
		String periodStr = "";
		if (period == 0) periodStr = "None/All";
		else periodStr = "" + period;
		
		return "Name: " + name + "\nGrade: " + gradeLevel + "\nPeriod: " + periodStr + "\nClass Difficulty Level: " + difficultyLevel + "\nTeacher's Difficulty Factor: " + teacherDifficultyFactor + "\nOverall Difficulty: " + getDifficulty() ;
	}
}
