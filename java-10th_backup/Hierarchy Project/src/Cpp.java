
public class Cpp extends CLanguage {


	//Constructor
	public Cpp(int programmerSkill, String userCode) {
		super(".cpp", 4, 5, programmerSkill, userCode, true, "C++");
		
	}
	
	
	//Overridden Methods
	@Override
	public String run() {
		compile(getUserCode());
		//Pretend that code is actually being run here before getting results.
		if (this.getProgrammerSkill() > 8) {
			return "Cool, you made a useful commercial program. BRING IN THE MONEY!";
		}else if (this.getProgrammerSkill() > 6){
			return "You were able to create a pretty complex game. Nice! Now, as for whether it's any good, we'll leave that up to the reviewers.";
		}else if (this.getProgrammerSkill() < 2) {
			return "Your code does nothing useful, and you somehow managed to make an infinite loop. I hope you saved this time.";
		}else {
			return "You created a decent program. It's not very advanced, but it gets the job done.";
		}
	}
	
	@Override
	public boolean equals(Object object2) {
		if (!(object2 instanceof Cpp)) return false;
		if (super.equals(object2)) return true;
		else return false;
	}

}
