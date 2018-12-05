
public class Java extends CLanguage{
	
	//Constants
	public static final double LATEST_JAVA_VERSION = 8.191; 
	//Instance Variables
	private double javaVersion;
	
	//Constructor
	public Java(int programmerSkill, String userCode, double javaVersion) {
		super(".java", 6, 7, programmerSkill, userCode, false, "Java");
		this.javaVersion = javaVersion;
		
	}
	
	//Getters
	public double getJavaVersion() {
		return javaVersion;
	}
	
	//Methods
	
	private int runInJVM(String userCode) {
		if (javaVersion != LATEST_JAVA_VERSION) {
			System.out.println("HEY, LISTEN! YOU SHOULD UPDATE JAVA TO THE NEWEST VERSION!");
		}
		if (this.getProgrammerSkill() > 7) return 0;
		else if (this.getProgrammerSkill() > 5)  return 1;
		else if (this.getProgrammerSkill() < 3) return 2;
		else return 3;
	}
	
	
	//Overridden Methods
	@Override
	public String run() {
		String compiledCode = compile(getUserCode());
		int result = runInJVM(compiledCode);
		if (result == 0) {
			return "You have now created Minecraft. Good job. I think.";
		}else if (result == 1) {
			return "You made a somewhat useful program, but it's written in Java, so it's gonna be annoying for other people to try and run, since they probbaly have the wrong version.";
		}else if (result == 3) {
			return "You are currently taking AP CS.";
		}else {
			return "You are currently taking the standard Java Programming class, and you actually didn't already know how to program when you started the class.";
		}
	}
	
	@Override
	public String toString() {
		return "Java Version: " + javaVersion + "\n" + super.toString();
	}
	
	@Override
	public boolean equals(Object object2) {
		if (!(object2 instanceof Java)) return false;
		if (super.equals(object2) && this.javaVersion == ((Java)object2).getJavaVersion()) return true;
		else return false;
	}
	
}
