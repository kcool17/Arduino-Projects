
public class Python extends ScriptLanguage implements Compiler{
		
	//Constructor
	public Python(int programmerSkill, String userCode) {
		super(".py", 7, 7, programmerSkill, userCode, "All-Purpose", "Python");
		
	}

	//Methods
	public String compile(String userCode) {
		//Imagine that this method actually compiles the code.
		return userCode;
	}
	
	//Overridden Methods
	@Override
	public int interpret(String userCode) {
		if (this.getProgrammerSkill() > 7) return 0;
		else if (this.getProgrammerSkill() > 5)  return 1;
		else if (this.getProgrammerSkill() < 3) return 2;
		else return 3;
	}
	
	
	@Override
	public String run() {
		String compiledCode = compile(this.getUserCode());
		int result = interpret(compiledCode);
		if (result == 0) {
			return "Wow, you're pretty good at Python. In fact, you're so good that you're one of the people who actually posts the answers on StackOverflow.";
		}else if (result == 1) {
			return "Not bad. The code is pretty inefficient, but it gets the job done without any serious issues.";
		}else if (result == 3) {
			return "Eh. Your code works, but it's pretty inefficient, and relatively simple as well. You also copied a bit too much code from StackOverflow, and now things are acting weird.";
		}else {
			return "You'll learn. Hopefully.";
		}
	}

	@Override
	public boolean equals(Object object2) {
		if (!(object2 instanceof Python)) return false;
		return super.equals(object2);
	}
	

}
