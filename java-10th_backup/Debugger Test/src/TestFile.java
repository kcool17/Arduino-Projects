public class TestFile {

    public static void main(String[] args)
    {
    	TestClass1 test = new TestClass1(4);
    	System.out.println(test.getConst());
    	
    	
    	
    	
    	/*
        int row = 3;
        int col = 5;
        int x = 0; int y = 0;
        
        int [][] matrix = new int[row][col];
        System.out.println("ORIGINAL MATRIX");
        printMatrix(matrix);
        
        while(x < row)
        {
            while(y < col)
            {
                matrix[x][y] = matrix[x][y] + 2;
                y++;
            }
            
            x++;
    
        }
        
        System.out.println("TWO MORE MATRIX");
        printMatrix(matrix);
        */
    }    
    
    static public void printMatrix(int[][] matrix)
    {
        for (int r = 0; r < matrix.length; r++)  {
            for (int c = 0; c < matrix[0].length; c++)  {
                System.out.print(matrix[r][c] + " ");
            }
            System.out.print("\n");
        }
    }
}