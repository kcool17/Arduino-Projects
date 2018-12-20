package hierarchy2_electricboogaloo;

public class StudentClient {

	public static void main(String[] args) {
		System.out.println("Kyle Sawicki's Hierarchy Project #2");
		System.out.println("AP CS Period 1 | Mrs. Rodriguez");
		System.out.println("Client Class Examples");
		System.out.println("Hey, don't actually grade this project. It's meant to be a joke. You should still look at it, though. Just make sure to finish the other projects first!");
		System.out.println();
		System.out.println("----------------------------------------------Inherited methods-------------------------------------------------------");
		
		//Inherited methods
		APBioTeacher drRyan = new APBioTeacher("Dr. Ryan", 11, 4, 3, 2);
		System.out.println("Subject Category: " + drRyan.getSubjectCategory());
		System.out.println("Type of Science: " + drRyan.getScienceType());
		System.out.println("--------------------------------------------Constants---------------------------------------------------------");
		
		//Constants
		System.out.println("Language used in AP CS: " + APCSTeacher.AP_LANGUAGE);
		System.out.println("---------------------------------------------CompareTo--------------------------------------------------------");
		
		//CompareTo
		APCSTeacher mrsRodriguez = new APCSTeacher("Mrs. Rodriguez", 11, 1, 0, 4);
		int result = drRyan.compareTo(mrsRodriguez);	
		
		if (result == -1) System.out.println("AP CS is harder than AP Bio!");
		else if (result == 1) System.out.println("AP Bio is harder than AP CS!");
		else System.out.println("Both classes are about as difficult!");
		System.out.println();
		
		
		System.out.println("---------------------------------------------Equals--------------------------------------------------------");
		
		//Equals
		ElementaryTeacher elementary1 = new ElementaryTeacher("Mrs. Robertson", 5, -1);
		ElementaryTeacher elementary2 = new ElementaryTeacher("Mrs. Auen", 6, 1);
		ElementaryTeacher elementary3 = new ElementaryTeacher("Mrs. Yablonski", 4, 0);
		
		System.out.println("elementary1 and elementary2: " + elementary1.equals(elementary2));
		System.out.println("elementary1 and elementary3: " + elementary1.equals(elementary3));
		System.out.println("elementary1 and drRyan: " + elementary1.equals(drRyan));
		System.out.println("--------------------------------------------------toString---------------------------------------------------");
		
		//toString
		System.out.println(mrsRodriguez);
		System.out.println("----------------------------------------------Aliases-------------------------------------------------------");
		
		//Aliases
		mrsRodriguez.giveProject(14);
		mrsRodriguez.makeDayPass();
		APCSTeacher rodriguezClone = mrsRodriguez;
		System.out.println(mrsRodriguez.getProjectDueInDays());
		rodriguezClone.makeDayPass();
		System.out.println(mrsRodriguez.getProjectDueInDays());
		System.out.println("---------------------------------------------Static methods--------------------------------------------------------");
		
		//Static methods
		System.out.println("Number of teachers in existence: " + Teacher.getTeachersInExistence());
		System.out.println("-------------------------------------------------Polymorphism, Object array, for each loop, casting objects.----------------------------------------------------");
		
		//Polymorphism, Object array, for each loop, casting objects.
		Teacher teacher1 = new ElementaryTeacher("Mrs. Robertson", 5, -1);
		Teacher teacher2 = new ElementaryTeacher("Mrs. Auen", 6, 1);
		Teacher teacher3 = new ElementaryTeacher("Mrs. Yablonski", 4, 0);
		Teacher teacher4 = new ElementarySpecialTeacher("Mr. Mumby", 5, 0, 1);
		Teacher teacher5 = new APCSTeacher("Mrs. Rodriguez", 11, 1, 0, 4);
		Teacher teacher6 = new APBioTeacher("Dr. Ryan", 11, 4, 3, 2);
		//Yes, I know I already made identical objects to these, and I could just use them over again with an alias as a Teacher object. I just didn't want to here.
		
		Teacher[] schoolArray = {teacher1, teacher2, teacher3, teacher4, teacher5, teacher6};
		System.out.println("Creating project... " + ((APCSTeacher)teacher5).giveProject(10));
		System.out.println();
		for (Teacher teacher : schoolArray) {
			System.out.println(teacher.toString());
			System.out.println();
		}
		System.out.println("-----------------------------------------------------------------------------------------------------");
		System.out.println("Ok, the whole reason I made this project is for this part. This is really the only important part here.");
		System.out.println(mrsRodriguez.getProjectDueInDays());
		while (mrsRodriguez.getProjectDueInDays() > 0) {
			mrsRodriguez.makeDayPass();
		}
		System.out.println(mrsRodriguez.getProjectDueInDays());
		//vvvvvvvvvv
		mrsRodriguez.extendDueDate(3);
		//^^^^^^^^^^
		System.out.println(mrsRodriguez.getProjectDueInDays());
		
		while (mrsRodriguez.getProjectDueInDays() > 0) {
			mrsRodriguez.makeDayPass();
		}
		System.out.println(mrsRodriguez.getProjectDueInDays());
		//vvvvvvvvvv
		mrsRodriguez.extendDueDate(2);
		//^^^^^^^^^^
		System.out.println(mrsRodriguez.getProjectDueInDays());
		
		while (mrsRodriguez.getProjectDueInDays() > 0) {
			mrsRodriguez.makeDayPass();
		}
		System.out.println(mrsRodriguez.getProjectDueInDays());
		//vvvvvvvvvv
		mrsRodriguez.extendDueDate(4);
		//^^^^^^^^^^
		System.out.println(mrsRodriguez.getProjectDueInDays());
		
		while (mrsRodriguez.getProjectDueInDays() > 0) {
			mrsRodriguez.makeDayPass();
		}
		mrsRodriguez.makeDayPass();
		System.out.println(mrsRodriguez.getProjectDueInDays());
		
		System.out.println("Anyway, I hope you enjoyed this project. Hopefully the rest of the grading has been/is going smoothly!");
		System.out.println("-----------------------------------------------------------------------------------------------------");
	}

}
