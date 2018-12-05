
public class IDEClient {

	public static void main(String[] args) {
		System.out.println("Kyle Sawicki's Hierarchy Project");
		System.out.println("AP CS Period 1 | Mrs. Rodriguez");
		System.out.println("Client Class Examples");
		System.out.println();
		System.out.println("----------------------------------------------Inherited methods-------------------------------------------------------");
		
		//Inherited methods
		Bash inheritTestBash = new Bash(6, "some code here", false);
		System.out.println("OS Type: " + inheritTestBash.getOsType());
		System.out.println("Main Usage: " + inheritTestBash.getMainUsage());
		System.out.println("--------------------------------------------Constants---------------------------------------------------------");
		
		//Constants
		System.out.println("Newest Java Version: " + Java.LATEST_JAVA_VERSION);
		System.out.println("---------------------------------------------CompareTo--------------------------------------------------------");
		
		//CompareTo
		Java compareJava = new Java(5, "blah code", 8.181);
		Assembly compareAssembly = new Assembly(5, "blah code", "Intel Celeron [insert model number]");		
		Bash compareBash = new Bash(5, "cooooddddddeeeeeee");
		int result = compareJava.compareTo(compareAssembly);	
		
		if (result == -1) System.out.println("Java is harder than assembly!");
		else if (result == 1) System.out.println("Assembly is harder than Java!");
		else System.out.println("Assembly and Java have the same difficulty!");
		System.out.println();
		
		result = compareJava.compareTo(compareBash);
		if (result == -1) System.out.println("Java is harder than bash!");
		else if (result == 1) System.out.println("Bash is harder than Java!");
		else System.out.println("Bash and Java have the same difficulty!");
		
		System.out.println("---------------------------------------------Equals--------------------------------------------------------");
		
		//Equals
		Bash bash1 = new Bash(6, "blah blah programming", true);
		Bash bash2 = new Bash(6, "blah blah programming", true);
		Bash bash3 = new Bash(6, "blah blah programming", false);
		Assembly definitelyBash4 = new Assembly(6, "blah blah programming", "Intel Core i5-7200U");
		System.out.println("bash1 and bash2: " + bash1.equals(bash2));
		System.out.println("bash1 and bash3: " + bash1.equals(bash3));
		System.out.println("bash1 and bash4: " + bash1.equals(definitelyBash4));
		System.out.println("--------------------------------------------------toString---------------------------------------------------");
		
		//toString
		Java apCSProject = new Java(1, "ZipCode.java", 8.181);
		System.out.println(apCSProject);
		System.out.println("----------------------------------------------Aliases-------------------------------------------------------");
		
		//Aliases
		Python aliasTest = new Python(5, "some code here");
		Python aliasTestAlt = aliasTest;
		System.out.println(aliasTest.getUserCode());
		aliasTestAlt.setUserCode("some NEW code here");
		System.out.println(aliasTest.getUserCode());
		System.out.println("---------------------------------------------Static methods--------------------------------------------------------");
		
		//Static methods
		System.out.println("Number of ProgammingLanguage objects created: " + ProgrammingLanguage.programsWritten());
		System.out.println(ProgrammingLanguage.whatIsProgramming());
		System.out.println("-------------------------------------------------Polymorphism, Object array, for each loop, casting objects.----------------------------------------------------");
		
		//Polymorphism, Object array, for each loop, casting objects.
		ProgrammingLanguage language1 = new Assembly(1, "insert some code here that will definitely run", "Intel i7-8700k");
		ProgrammingLanguage language2 = new Bash(1, "insert some code here that will definitely run", true);
		ProgrammingLanguage language3 = new Python(1, "insert some code here that will definitely run");
		ProgrammingLanguage language4 = new CLanguage(1, "insert some code here that will definitely run");
		ProgrammingLanguage language5 = new Cpp(1, "insert some code here that will definitely run");
		ProgrammingLanguage language6 = new Java(1, "insert some code here that will definitely run", 8.191);
		ProgrammingLanguage[] manyProgramArray = {language1, language2, language3, language4, language5, language6};
		System.out.println("Java version: " + ((Java)language6).getJavaVersion());
		System.out.println();
		for (ProgrammingLanguage program : manyProgramArray) {
			System.out.println(program.toString());
			System.out.println();
		}
		System.out.println("-----------------------------------------------------------------------------------------------------");
				
		
	}

}
