// Chapter 7 Question 21

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class Rps extends JFrame
    implements ActionListener
{
  private final char moves[] = {'R', 'P', 'S'};
  private JRadioButton rock, paper, scissors, lizard, spock;
  private JTextField display;

  public Rps()
  {
    super("Rock, paper, Scissors");

    rock = new JRadioButton("   Rock   ", true);
    paper = new JRadioButton("   Paper  ");
    scissors = new JRadioButton(" Scissors ");
    lizard = new JRadioButton(" Lizard ");
    spock = new JRadioButton("  Spock  ");

    ButtonGroup rpsButtons = new ButtonGroup();
    rpsButtons.add(rock);
    rpsButtons.add(paper);
    rpsButtons.add(scissors);
    rpsButtons.add(lizard);
    rpsButtons.add(spock);

    JButton go = new JButton("         Go         ");
    go.addActionListener(this);

    display = new JTextField(25);
    display.setEditable(false);
    display.setBackground(Color.yellow);

    Container c = getContentPane();
    c.setLayout(new FlowLayout());
    c.add(rock);
    c.add(paper);
    c.add(scissors);
    c.add(lizard);
    c.add(spock);
    c.add(go);
    c.add(display);
  }

  /**
   *  returns -1 if the player wins,
   *  0 if it's a tie, and 1 if the computer wins
   */
  private int nextPlay(char computerMove, char playerMove)
  {
    int result = 0; 
    final char PAPER = 'P';
    final char ROCK = 'R';
    final char SCISSORS = 'S';
    final char LIZARD = 'L';
    final char SPOCK = 'T';
    
    //Add your code here to determine the outcome of the throw
    if (playerMove== PAPER) {
    	if (computerMove== PAPER) {
        	result= 0;
        } else if (computerMove== ROCK) {
        	result= -1;
        } else if (computerMove== SCISSORS) {
        	result= 1;
        }else if (computerMove == LIZARD) {
        	result= 1;
        }else if (computerMove == SPOCK) {
        	result= -1;
        } else {
        	System.out.print("You can't even Java.");
        }
    } else if (playerMove== ROCK) {
    	if (computerMove== PAPER) {
        	result= 1;
        } else if (computerMove== ROCK) {
        	result= 0;
        } else if (computerMove== SCISSORS) {
        	result= -1;
        }else if (computerMove == LIZARD) {
        	result= -1;
        }else if (computerMove == SPOCK) {
        	result= 1;
        } else {
        	System.out.print("You can't even Java.");
        }
    } else if (playerMove== SCISSORS) {
    	if (computerMove== PAPER) {
        	result= -1;
        } else if (computerMove== ROCK) {
        	result= 1;
        } else if (computerMove== SCISSORS) {
        	result= 0;
        }else if (computerMove == LIZARD) {
        	result= -1;
        }else if (computerMove == SPOCK) {
        	result= 1;
        } else {
        	System.out.print("You can't even Java.");
        }
    }else if (playerMove == LIZARD) {
    	if (computerMove== PAPER) {
        	result= -1;
        } else if (computerMove== ROCK) {
        	result= 1;
        } else if (computerMove== SCISSORS) {
        	result= 1;
        }else if (computerMove == LIZARD) {
        	result= 0;
        }else if (computerMove == SPOCK) {
        	result= -1;
        } else {
        	System.out.print("You can't even Java.");
        }
    }else if (playerMove == SPOCK) {
    	if (computerMove== PAPER) {
        	result= 1;
        } else if (computerMove== ROCK) {
        	result= -1;
        } else if (computerMove== SCISSORS) {
        	result= -1;
        }else if (computerMove == LIZARD) {
        	result= 1;
        }else if (computerMove == SPOCK) {
        	result= 0;
        } else {
        	System.out.print("You can't even Java.");
        }
    } else {
    	System.out.print("You can't even Java.");
    }
    /*
    if (playerMove == computerMove) {
    	result = 0;
    }else {
    	if (playerMove == PAPER && computerMove == SCISSORS) {
    		result = 1;
    	}else if (playerMove == PAPER && computerMove == ROCK) {
    		result = -1;
    	}else if (playerMove == SCISSORS && computerMove == PAPER) {
    		result = -1;
    	}else if (playerMove == SCISSORS && computerMove == ROCK) {
    		result = 1;
    	}
    }*/
  
    return result;
  }

  public void actionPerformed(ActionEvent e)
  {
    char playerMove, computerMove;
    if (rock.isSelected())
      playerMove = 'R';
    else if (paper.isSelected())
      playerMove = 'P';
    else if (scissors.isSelected())
      playerMove = 'S';
    else if (spock.isSelected())
    	playerMove = 'T';
    else
    	playerMove = 'L';

    int k = (int)(Math.random() * 3);
    computerMove = moves[k];
    int result = nextPlay(computerMove, playerMove);

    String msg = "  You said " + makeWord(playerMove) + ", I said " +
                 makeWord(computerMove);
    if (result < 0)
      msg += " -- you win.";
    else if (result == 0)
      msg += " -- tie.";
    else // if (result > 0)
      msg += " -- I win.";
    display.setText(msg);
  }

  private String makeWord(char move)
  {
    String word = "";

    switch (move)
    {
      case 'R': word = "ROCK"; break;
      case 'P': word = "PAPER"; break;
      case 'S': word = "SCISSORS"; break;
      case 'L': word = "LIZARD"; break;
      case 'T': word = "SPOCK"; break;
    }
    return word;
  }

  public static void main(String[] args)
  {
    Rps window = new Rps();
    window.setBounds(300, 300, 300, 140);
    window.setDefaultCloseOperation(EXIT_ON_CLOSE);
    window.setVisible(true);
  }
}

