
public class Bash extends CommandLine{
	
	//Instance Variables
	private boolean isRoot;
	
	//Constructors
	public Bash(int programmerSkill, String userCode) {
		super(".sh", 6, 6, programmerSkill, userCode, "Linux/Unix", "Bash");
		this.isRoot = false;
		
	}
	public Bash(int programmerSkill, String userCode, boolean isRoot) {
		super(".sh", 6, 6 - (isRoot ? 3 : 0), programmerSkill, userCode, "Linux/Unix", "Bash");
		this.isRoot = isRoot;
		
	}
	
	//Getters
	public boolean isRoot() {
		return isRoot;
	}
	
	
	//Overridden Methods
	@Override
	public String run() {
		int result = this.interpret(this.getUserCode());
		if (result == 0) {
			return "Hey, you're pretty good at this! You actually managed to accomplish what you wanted to do, in an efficient manner!";
		}else if (result == 1) {
			return "Well, it's not very efficient, but it gets the job done. Mostly.";
		}else if (result == 2) {
			if (isRoot) return "Anddddd you accidentally deleted your entire hard drive. Nice. That's gonna be fun to fix.";
			else return "I hope you didn't have anything important saved on there, because it's gone now. Luckily, the computer still works.";
		}else {
			if (isRoot) return "Uhh... things may be a little messed up from what you did. Things still work, at least, but you both accomplished nothing and broke a couple programs that were on your PC. Stick to GUIs.";
			else return "At least no one trusted you with root privileges. Your code just didn't do what it was supposed to.";
		}
	}
	
	@Override
	public String toString() {
		return "Is Root?: " + this.isRoot + "\n" + super.toString();
	}
	
	@Override
	public boolean equals(Object object2) {
		if (!(object2 instanceof Bash)) return false;
		if (super.equals(object2) && this.isRoot == ((Bash)object2).isRoot()) return true;
		else return false;
	}
}
