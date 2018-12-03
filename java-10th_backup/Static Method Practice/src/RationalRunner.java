
public class RationalRunner {
	public static Rational modRational(Rational myRational) {
		myRational = Rational.add(myRational, new Rational(30, 1));
		return myRational;
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Rational myRational = new Rational(5, 1);
		System.out.println(myRational);
		myRational = modRational(myRational);
		System.out.println(myRational);
	}

}
