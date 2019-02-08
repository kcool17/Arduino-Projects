import java.util.ArrayList;
import java.util.List;
import java.util.ListIterator;

public class ZooClient {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		ArrayList<Animal> zoo = new ArrayList<Animal>();
		zoo.add(new Dog("Snoopy"));
		zoo.add(new Cat("Garfield"));
		//System.out.println(zoo.get(1).getSpecies());
		//for(Animal myAnimal : zoo) {
		//	System.out.println(myAnimal.getSpecies());
		//}
		ListIterator<Animal> myIter= zoo.listIterator();
		while (myIter.hasNext()) {
			System.out.println(myIter.next().getSpecies());
		}
	}

}
