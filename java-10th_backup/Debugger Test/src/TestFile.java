public class TestFile {

    public static void main(String[] args)
    {
    	mystery(321);
    }    
    
    public static void mystery(int x) {
        if (x>=0) {
            System.out.print(x%10);
            if ((x/10) != 0) {
                mystery(x/10);
            }
            System.out.print(x%10);
        }
    }
}