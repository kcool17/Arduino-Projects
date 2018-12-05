
public abstract class ScriptLanguage extends ProgrammingLanguage{
	
	//Instance Variables
	private String mainUsage;
	//Constructor
	public ScriptLanguage(String fileExtension, int easeOfUse, int safetyOfUse, int programmerSkill, String userCode, String mainUsage, String languageName) {
		super(fileExtension, easeOfUse, safetyOfUse, programmerSkill, userCode, languageName);
		this.mainUsage = mainUsage;
		
	}
	
	//Getters
	public String getMainUsage() {
		return mainUsage;
	}
	
	//Abstract Methods
	public abstract int interpret(String userCode); //Imagine that this method actually interprets the code in some meaningful way, before getting a result based off the programmer's skill.
		
	
	//Overridden Methods
	@Override
	public String toString() {
		return "Main Usage: " + mainUsage + "\n" + super.toString();
	}
	
}
