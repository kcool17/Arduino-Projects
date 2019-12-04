import javax.swing.DefaultListModel;
import javax.swing.DropMode;
import javax.swing.GroupLayout;
import javax.swing.JButton;
import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.JList;
import javax.swing.JScrollPane;
import javax.swing.ListSelectionModel;
import javax.swing.TransferHandler;

import java.awt.Container;
import java.awt.Dimension;
import java.awt.EventQueue;
import java.awt.datatransfer.DataFlavor;
import java.awt.datatransfer.Transferable;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

    
public class main extends JFrame {

	private final String[] COMMAND_LIST = {"Move Forward", "Move Backward", "Turn Right"};
	
	
	
    private DefaultListModel model;
    private DefaultListModel model2;
    //private static JList programList;

    public main() {

        initUI();
    }

    private void initUI() {
    	//Init
        JScrollPane scrollPane = new JScrollPane();
        scrollPane.setPreferredSize(new Dimension(180, 150));
        
        //Button
        JButton createButton = new JButton("Generate File");
        
        
        //Commands
        String[] commandArr = COMMAND_LIST;
        JList commandList = new JList(commandArr);
        commandList.setDragEnabled(true);

        //Full program
        model = new DefaultListModel();
        JList programList = new JList(model);
        programList.setDropMode(DropMode.INSERT);
        programList.setDragEnabled(true);
        programList.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        programList.setTransferHandler(new ListHandler());
		programList.addKeyListener(new KeyAdapter() {
			public void keyPressed(KeyEvent e) {
				if (e.getKeyCode() == KeyEvent.VK_BACK_SPACE) {
					DefaultListModel myModel = (DefaultListModel) programList.getModel();
		        	int selectedIndex = programList.getSelectedIndex();
		        	if (selectedIndex != -1) {
		        	    myModel.remove(selectedIndex);
		        	}
				}
			}
		});
       
        
        //Layout
        scrollPane.getViewport().add(programList);
        createLayout(commandList, scrollPane, createButton);
        
        
        //Create window
        setTitle("Fleetbot Builder");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
    }

    private class ListHandler extends TransferHandler {

        public boolean canImport(TransferSupport support) {

            if (!support.isDrop()) {
                return false;
            }

            return support.isDataFlavorSupported(DataFlavor.stringFlavor);
        }

        public boolean importData(TransferSupport support) {

            if (!canImport(support)) {
                return false;
            }

            Transferable transferable = support.getTransferable();
            String line;

            try {
                line = (String) transferable.getTransferData(DataFlavor.stringFlavor);
            } catch (Exception e) {
                return false;
            }

            DropLocation dl = (JList.DropLocation) support.getDropLocation();
            int index = ((javax.swing.JList.DropLocation) dl).getIndex();

            
            model.add(index++, line);
            /*
            String[] data = line.split("[,\\s]");

            for (String item : data) {

                if (!item.isEmpty())
                    model.add(index++, item.trim());
            }
			*/
            
            return true;
        }
    }
  
    private void createLayout(JComponent... arg) {

        Container pane = getContentPane();
        GroupLayout gl = new GroupLayout(pane);
        pane.setLayout(gl);

        gl.setAutoCreateContainerGaps(true);
        gl.setAutoCreateGaps(true);

        gl.setHorizontalGroup(gl.createSequentialGroup()
                .addComponent(arg[0])
                .addComponent(arg[1])
                .addComponent(arg[2])
        );

        gl.setVerticalGroup(gl.createParallelGroup(GroupLayout.Alignment.BASELINE)
                .addComponent(arg[0])
                .addComponent(arg[1])
                .addComponent(arg[2])
        );

        pack();
    }

    public static void main(String[] args) {
        EventQueue.invokeLater(() -> {

            main ex = new main();
            ex.setVisible(true);
        });
        
    }
}