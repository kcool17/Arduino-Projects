
public abstract class ProgrammingLanguage implements Comparable<ProgrammingLanguage>{
	
	//Static Variables
	private static int programsWritten;
	public static final String PROGRAMMING_LANGUAGE_DEFINITION = "A programming language is a formal language, which comprises a set of instructions used to produce various kinds of output. Programming languages are used in computer programming to create programs that implement specific algorithms. - Source: Wikipedia";
	
	//Instance Variables
	private String languageName;
	private String fileExtension;
	private int easeOfUse; //Value from 1-10, with 1 being the farthest from English/hardest to understand, and 10 being the closest/easiest to understand.
	private int safetyOfUse; //Value from 1-10, with 1 being it has low-level access and is easy to mess up everything if done wrong, with 10 being the opposite of that.
	private int programmerSkill; //Value from 1-10, with 1 being the programmer is a complete beginner at programming, and 10 being they basically invented the language.
	private String userCode; //The code the user wants to run, or the file that they want to run.
	
	//Constructor
	public ProgrammingLanguage(String fileExtension, int easeOfUse, int safetyOfUse, int programmerSkill, String userCode, String languageName) {
		this.fileExtension = fileExtension;
		this.easeOfUse = easeOfUse;
		this.safetyOfUse = safetyOfUse;
		if (programmerSkill > 10) programmerSkill = 10;
		else if (programmerSkill < 1) programmerSkill = 1;
		this.programmerSkill = programmerSkill;
		this.userCode = userCode;
		this.languageName = languageName;
		programsWritten += 1;
	}
	
	//Getters
	public String getFileExtension() {
		return fileExtension;
	}
	
	public int getEaseOfUse() {
		return easeOfUse;
	}
	
	public int getSafetyOfUse() {
		return safetyOfUse;
	}
	
	public int getProgrammerSkill() {
		return programmerSkill;
	}
	
	public String getUserCode() {
		return userCode;
	}
	
	public String getLanguage() {
		return languageName;
	}
	
	//Abstract methods
	public abstract String run(); //Returns what happens as a result of the program being run by the user with the current skill level.
	
	//Other methods
	public void setUserCode(String code) {
		userCode = code;
	}
	
	public static String whatIsProgramming() {
		return "Defintion: " + PROGRAMMING_LANGUAGE_DEFINITION;
	}
	
	public static int programsWritten() {
		return programsWritten;
	}
	
	//compareTo method (Compares the ease of use)
	public int compareTo(ProgrammingLanguage object2) {
		if (this.easeOfUse < object2.getEaseOfUse()) return -1;
		else if (this.easeOfUse > object2.getEaseOfUse()) return 1;
		else return 0;
	}
	
	
	
	//toString method
	@Override
	public String toString() {
		return "Language Name: " + languageName + "\nFile Extension: " + fileExtension + "\nEase of Use: " + easeOfUse + "\nSafety of Use: "  + safetyOfUse + "\nProgrammer's Skill Level: " + programmerSkill + "\nUser's code: \n" + userCode + "\nResults when run: \n" + run();
		
	}
	//equals method
	@Override
	public boolean equals(Object object2) {
		if (!(object2 instanceof ProgrammingLanguage)) return false;
		if (this.programmerSkill == ((ProgrammingLanguage)object2).getProgrammerSkill() && this.userCode == ((ProgrammingLanguage)object2).getUserCode()) return true;
		else return false;
	}
}
