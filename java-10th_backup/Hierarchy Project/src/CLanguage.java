
public class CLanguage extends ProgrammingLanguage implements Compiler{
	
	//Instance Variables
	private boolean usesHeaders; //Whether or not the language uses header files as an important part of the language.
	//Constructors
	public CLanguage(int programmerSkill, String userCode) { //Constructor for the actual C language
		super(".c", 3, 3, programmerSkill, userCode, "C");
		this.usesHeaders = true;
	}
	public CLanguage(String fileExtension, int easeOfUse, int safetyOfUse, int programmerSkill, String userCode, boolean usesHeaders, String languageName) { //Constructor for derivatives of C
		super(fileExtension, easeOfUse, safetyOfUse, programmerSkill, userCode, languageName);
		this.usesHeaders = usesHeaders;
		
	}
	
	//Getters
	public boolean getUsesHeaders() {
		return usesHeaders;
	}
	
	//Methods
	public String compile(String userCode) {
		//Imagine that this method actually compiles the code.
		return userCode;
	}
	
	//Overridden Methods
	@Override
	public String run() {
		compile(getUserCode());
		//Imagine it actually runs code here.
		if (this.getProgrammerSkill() > 9) {
			return "Hey, nice job! You created a vital OS program! That's pretty useful.";
		}else if (this.getProgrammerSkill() > 7){
			return "Hey, you're pretty good at programming. You made a very useful computer program that you got to sell to people. You'd be rich, but you didn't have much education in business, and your \"partner\" ran off with all the profits.";
		}else if (this.getProgrammerSkill() < 3) {
			return "Welp, you screwed up badly. You manipulated the computer's memory in weird ways, and crashed it. And you forgot to save your work. Good job.";
		}else {
			return "C is quite difficult, isn't it? Ah well, you're learning, at least.";
		}
	}

	@Override
	public String toString() {
		return "Does it use Headers far too much?: " + usesHeaders + "\n" + super.toString();
	}
	
	@Override
	public boolean equals(Object object2) {
		if (!(object2 instanceof CLanguage)) return false;
		if (super.equals(object2) && this.usesHeaders == ((CLanguage)object2).getUsesHeaders()) return true;
		else return false;
	}
}
