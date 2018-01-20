package application;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;

import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.ListView;
import javafx.scene.text.Text;

public class ResultDisplayController {

    @FXML
    private ListView<String> leftListView;

    @FXML
    private ListView<String> rightListView;

    @FXML
    private Text leftListOptionSelectedText;

    @FXML
    private Text rightListOptionSelectedText;
    
    HashMap<String, String> hmap = new HashMap<String, String>();
    
    public void initialize() throws IOException{
    	
        ObservableList<String> leftItems = FXCollections.observableArrayList (
                "Fatal", "Error","Warning");
        leftListView.setItems(leftItems);
        ObservableList<String> rightItems = FXCollections.observableArrayList();
        rightListView.setItems(rightItems);
        
        leftListView.getSelectionModel().selectedItemProperty().addListener(
                
        		new ChangeListener<String>() {
                	
                    public void changed(ObservableValue<? extends String> observable, String oldValue, String newValue) {
                    	
                    	//leftListOptionSelectedText.setText(newValue);
                    	
                    	if(!rightItems.isEmpty())rightItems.clear();
						
                    	FileInputStream fis = null, fis2 = null;
                        BufferedReader reader = null, reader2 = null;
 
						try {
							
							fis = new FileInputStream(FxController.logaddress);
				            reader = new BufferedReader(new InputStreamReader(fis));
				            
				            fis2 = new FileInputStream(FxController.eventLog);
				            reader2 = new BufferedReader(new InputStreamReader(fis2));

						} catch (FileNotFoundException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
                    	
                    	try {
                    		String myLine, eventLogLine;
                    		SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss");
							while ( (myLine = reader.readLine()) != null)
							{
								/*if(newValue == "Error"){
									if(myLine.contains("E")){
										String time = myLine.split(" ")[1].split(".")[0];
										String[] array2 = array[1].split(":");
										rightItems.add(array2[0]);
										errorSets = errorSets+ "\n"+array2[1];
									}
		                    	}*/
								
								if(newValue == "Warning"){
									if(myLine.contains("W")){
										
										String events = null;
										String logTime = myLine.split(" ")[1].split("\\.")[0];
										
										while ((eventLogLine = reader2.readLine())!= null) {
											String eventTime = eventLogLine.split(" ")[1];
											
										    Date d1 = sdf.parse(logTime);
										    Date d2 = sdf.parse(eventTime);
										    
										    if(Math.abs(d1.getTime()-d2.getTime()) <= 100000){
										    	
										    	String activity = eventLogLine.split("\t")[1].split("\\.")[3];
										    	String id = eventLogLine.split("\t")[2].split(":")[1];
										    	String keycode = eventLogLine.split("\t")[3];
										    	
										    	if(rightItems.contains(activity)){
										    		events = events + "\n\n" + id + " " + keycode;
										    	}
										    	
										    	else{
										    		
										    		if(rightItems.size()>0){
										    			hmap.put(rightItems.get(rightItems.size()-1), events);	
										    		}
										    		rightItems.add(activity);
										    		events = null + "\n\n" + id + " " + keycode;
										    	}
										    	
										    }
										}
										//String[] array2 = array[1].split(":");
										//rightItems.add(array2[0]);
										//errorSets = errorSets+ "\n"+array2[1];
									}
		                    	}
								
								/*if(newValue == "Fatal"){
									if(myLine.contains("F")){
										String[] array = myLine.split("F ");
										String[] array2 = array[1].split(":");
										rightItems.add(array2[0]);
										errorSets = errorSets+ "\n"+array2[1];
									}
		                    	}*/
								
							}
							
						} catch (IOException | ParseException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
                    	
						
                    }
                }
        		
        );
        
        rightListView.getSelectionModel().selectedItemProperty().addListener(
        			new ChangeListener<String>() {
                	
	                    public void changed(ObservableValue<? extends String> observable, String oldValue, String newValue) {
	                    	rightListOptionSelectedText.setText(hmap.get(newValue));
	                    	System.out.println(hmap.size());
	                    }
        			}
        );
    }

}
