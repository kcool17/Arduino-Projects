package hierarchy2_electricboogaloo;

public class APBioTeacher extends ScienceTeacher implements AP{
	
	//Constructor
	public APBioTeacher(String name, int gradeLevel, int period, int teacherDifficultyFactor, int amountHW) {
		super(name, gradeLevel, period, 5, teacherDifficultyFactor, amountHW, "AP Biology");
	}
	
	
	
	//Methods
	public String teachClass() {
		return "Have fun with the humongous amount of notes you're gonna have to take. Enjoy!";
	}
	
	public String giveGrade(int studentIntelligence) {
		if (studentIntelligence > 9) return "Wow, you actually have an A in this class. That's... very impressive, actually.";
		else if (studentIntelligence > 6) return "You're getting a B/C in this class, which is actually still good.";
		else return "You're failing the class. You may want to dedicate more time to studying. This class is not going to be easy, ya know.";
	}
	
	public String giveTest(int studentIntelligence, int studentStudyAmount) {
		if (this.getPeriod() < 3) studentIntelligence--; //If you have this class earlier in the morning, you're gonna do worse.
		
		if (studentIntelligence + studentStudyAmount > 17) return "Wow. You did well on the test. That's... almost unheard of. Nice.";
		else if (studentIntelligence + studentStudyAmount > 14) return "Eh, you didn't do terribly. Especially for this class. This is mostly how you're expected to do. You got a B/C";
		else if (studentIntelligence + studentStudyAmount > 9) return "Well, you got a D. In any other class, you'd probably get a C with this amount of effort/skill, but not here.";
		else return "You failed. Hopefully you'll do better next time. Remember, studying is very important in this class. You won't succeed otherwise.";
	}
	
	public String giveAPTestGrade(int studentIntelligence) {
		if (studentIntelligence > 9) return "...you got a 5 on the AP exam. How...? You probably already took this class before.";
		else if (studentIntelligence > 8) return "You got a 4 on the AP exam. That's pretty good; you must have studied a lot before this.";
		else if (studentIntelligence > 7) return "Honestly, this is to be expected for this class. It's pretty difficult, isn't it? Oh yeah, you got a 3 on the exam.";
		else if (studentIntelligence > 4) return "You got a 2 on the exam. Eh. Not very good, but it's a hard class.";
		else return "You got a 1 on the exam. That's bad, even for AP bio. Did you do nothing in class? Like, come on.";
	}
	
	//Overrides
	@Override
	public boolean equals(Object obj2) {
		if (!(obj2 instanceof APBioTeacher)) return false;
		else return super.equals(obj2);
		
	}
	

}
