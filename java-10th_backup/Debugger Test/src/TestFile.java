public class TestFile {

    public static void main(String[] args)
    {
    	String data = "142";
    	String[] process = data.split(",");
    	String nullTest = null;
    	
    	double test = Double.parseDouble(process[0]);
    	System.out.print(test);
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