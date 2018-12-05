
public abstract class CommandLine extends ScriptLanguage{
	
	//Instance Variables
	private String osType;
	
	//Constructor
	public CommandLine(String fileExtension, int easeOfUse, int safetyOfUse, int programmerSkill, String userCode, String osType, String languageName) {
		super(fileExtension, easeOfUse, safetyOfUse, programmerSkill, userCode, "OS programming", languageName);
		this.osType = osType;
	}
	
	//Getters
	public String getOsType() {
		return osType;
	}
	
	
	//Overridden Methods
	@Override
	public int interpret(String userCode) {
		if (this.getProgrammerSkill() > 8) return 0;
		else if (this.getProgrammerSkill() > 6)  return 1;
		else if (this.getProgrammerSkill() < 3) return 2;
		else return 3;
	}
	@Override
	public String toString() {
		return "OS: " + this.osType + "\n" + super.toString();
	}
}
