// Implements the game of Craps logic

public class CrapsGame
{
  private int point = 0;
  private int turn = 1;
  /**
   *  Calculates the result of the next dice total in the Craps game.
   *  The parameter total is the sum of dots on two dice.
   *  point is set to the saved total, if the game continues,
   *  or 0, if the game has ended.
   *  Returns 1 if player won, -1 if player lost,
   *  0 if player continues totaling.
   */
  public int processRoll(int total)
  {
	int result=0;

	//<Add code here>
	if (turn ==1){
		if (total == 7 || total == 11){
			result = 1;
		}else if (total == 2 || total == 3 || total == 12){
			result = -1;
		}else{
			point = total;
			turn++;
		}
	}else if (turn != 1){
		if (total == point){
			result = 1;	
		}else if (total == 7){
			result = -1;
		}
	}
	System.out.println(total);
    return result;
	
  }	

  /**
   *  Returns the saved point
   */
  public int getPoint()
  {
    return point;
  }
}

