package hierarchy2_electricboogaloo;

public class APCSTeacher extends HighSchoolTeacher implements AP{
	
	//Instance Variables
	private int projectDueInDays;
	
	//Constant
	public static final String AP_LANGUAGE = "Java"; //The language the AP CS class uses.
	
	//Constructor
	public APCSTeacher(String name, int gradeLevel, int period, int teacherDifficultyFactor, int amountHW) {
		super(name, gradeLevel, period, 5, teacherDifficultyFactor, "Computer Science", amountHW);
		projectDueInDays = 0;
		
	}
	//Getters
	
	public int getProjectDueInDays() {
		return projectDueInDays;
	}
	
	
	
	//Methods
	public String giveAPTestGrade(int studentIntelligence) {
		if (studentIntelligence > 7) return "You got a 5 on the AP exam. Wow, that's pretty good! You must have either worked really hard in the class, or known what you were doing before taking it.";
		else if (studentIntelligence > 5) return "You got a 4 on the AP exam. Not bad. You clearly understand what you are doing.";
		else if (studentIntelligence > 4) return "You got a 3. Eh. Could've been worse, I guess. Still pretty disappointing for this class, though.";
		else if (studentIntelligence > 3) return "Well, you clearly had no idea what you were doing. It's almost like you needed constant help studying throughout the year from someone who actually knew what they were doing. You got a 2 on the test.";
		else return "You got a 1 on the exam. Did you even show up to class, ever?";
	}

	public String giveTest(int studentIntelligence, int studentStudyAmount) {
		if (studentIntelligence + studentStudyAmount > 14) return "Hey, you got an A. Good job. It's almost like you know what you're doing in this class.";
		else if (studentIntelligence + studentStudyAmount > 10) return "You got a B/C on the test. Not bad, not bad. You're learning, at least, and somewhat know what you're doing. Or made a really stupid mistake somewhere, like forget an equals sign or something because the quiz said it had to be inclusive but you didn't see that part.";
		else if (studentIntelligence + studentStudyAmount > 5) return "And... you got a D. You really should've studied for this test. Hopefully you do better next time. Remember to actually pay attention in class.";
		else return "...you failed. You clearly have no idea what you're doing in this class. Start paying attention to what's happening in this class, cause you of all people really need it.";
	}

	public String teachClass() {
		return "You're going to be doing a lot of practice things throughout this class. Make sure you understand them before the project, and especially before the test.";
	}

	public String giveGrade(int studentIntelligence) {
		if (studentIntelligence > 7) return "Good job! You actually know what you're doing in this class!";
		else if (studentIntelligence > 4) return "You're getting a B/C in this class. Not bad, but you could do better.";
		else return "Anddd.... you're failing the class. You should actually understand what you're doing, so you're not failing a fairly easy class.";
	}
	
	public String giveProject(int dueInDays) {
		projectDueInDays = dueInDays;
		return "The teacher gave a project due in " + dueInDays + " days! Don't forget about it!";
	}
	
	private void projectIsDue() {
		System.out.println("Hey! Turn in the project! It's due/late.");
	}
	
	public void extendDueDate(int days) {
		projectDueInDays += days;
	}
	
	public void makeDayPass() {
		if(projectDueInDays <=0) {
			projectDueInDays = 0;
			projectIsDue();
		}
		else projectDueInDays--;
	}
	
	//Overrides
	@Override
	public String toString() {
		return super.toString() + "\nDays until project is due: " + projectDueInDays;
	}
	
	@Override
	public boolean equals(Object obj2) {
		if (!(obj2 instanceof APCSTeacher)) return false;
		else return super.equals(obj2);
	}
}
