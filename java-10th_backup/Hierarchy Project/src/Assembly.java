
public class Assembly extends ProgrammingLanguage{

	//Instance variables
	private String processorType;
	
	//Constructor
	public Assembly(int programmerSkill, String userCode, String processorType) {
		super(".s", 1, 1, programmerSkill, userCode, "Assembly");
		this.processorType = processorType;
		
	}
	
	//Getters
	public String getProcessorType() {
		return processorType;
	}
	
	//Overridden Methods
	@Override
	public String run() {
		if (this.getProgrammerSkill() > 9) {
			return "Wow, you actually were able to run it without screwing everything up! You created an entire OS, good job!";
		}else if (this.getProgrammerSkill() > 7){
			return "Assembly language is quite hard, isn't it? At least you didn't screw up everything! Your code is worthless, though.";
		}else if (this.getProgrammerSkill() == 1) {
			return "You somehow managed to blow up your entire computer. Next time, don't accidentally make your PSU unstable. I don't even know how you managed that.";
		}else {
			return "Don't try and program in assembly. Please. You have now corrupted every hard disk you had in the machine, and fried the processor. Nice job.";
		}
	}

	@Override
	public String toString() {
		return "Processor Type: " + processorType + "\n" + super.toString();
	}
	
	@Override
	public boolean equals(Object object2) {
		if (!(object2 instanceof Assembly)) return false;
		if (super.equals(object2) && this.processorType == ((Assembly)object2).getProcessorType()) return true;
		else return false;
	}
	
	
}
