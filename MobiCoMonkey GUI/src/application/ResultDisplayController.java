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
import javafx.scene.layout.GridPane;
import javafx.scene.text.Text;

public class ResultDisplayController {

	@FXML
    private ListView<String> firstListView;

    @FXML
    private ListView<String> secondListView;

    @FXML
    private ListView<String> thirdListView;

    @FXML
    private ListView<String> fourthListView;
    
    @FXML
    private GridPane baseGrid;
    
    HashMap<String, String> hmap = new HashMap<String, String>();
    
    public void initialize() throws IOException{
    	
        ObservableList<String> firstItems = FXCollections.observableArrayList (
                "Fatal", "Error","Warning");
        firstListView.setItems(firstItems);
        ObservableList<String> secondItems = FXCollections.observableArrayList();
        secondListView.setItems(secondItems);
        ObservableList<String> thirdListViewItems = FXCollections.observableArrayList();
        thirdListView.setItems(thirdListViewItems);
        ObservableList<String> fourthListViewItems = FXCollections.observableArrayList();
        fourthListView.setItems(fourthListViewItems);
        
        
        firstListView.getSelectionModel().selectedItemProperty().addListener(
                
        		new ChangeListener<String>() {
                	
                    public void changed(ObservableValue<? extends String> observable, String oldValue, String newValue) {
                                	
                    	if(!secondItems.isEmpty())secondItems.clear();
						
                    	FileInputStream fis = null;
                        BufferedReader reader = null;
                        
                        try {
							
							fis = new FileInputStream(FxController.activityList);
				            reader = new BufferedReader(new InputStreamReader(fis));
						} catch (FileNotFoundException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
                        
                        try {
                        	String myLine;
                        	while ( (myLine = reader.readLine()) != null){
                        		String activity = myLine.split("\\.")[3];
                        		secondItems.add(activity);
                        	}
						} catch (Exception e) {
							// TODO: handle exception
							e.printStackTrace();
						}
                        
/*						try {
							
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
								if(newValue == "Error"){
									if(myLine.contains("E")){
										String time = myLine.split(" ")[1].split(".")[0];
										String[] array2 = array[1].split(":");
										rightItems.add(array2[0]);
										errorSets = errorSets+ "\n"+array2[1];
									}
		                    	}
								
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
								
								if(newValue == "Fatal"){
									if(myLine.contains("F")){
										String[] array = myLine.split("F ");
										String[] array2 = array[1].split(":");
										rightItems.add(array2[0]);
										errorSets = errorSets+ "\n"+array2[1];
									}
		                    	}
								
							}
							
						} catch (IOException | ParseException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}*/
                    	
						
                    }
                }
        		
        );
        
        secondListView.getSelectionModel().selectedItemProperty().addListener(
    			new ChangeListener<String>() {
            	
                    public void changed(ObservableValue<? extends String> observable, String oldValue, String newValue) {
                    	
                    	if(!thirdListViewItems.isEmpty()) {
                    		thirdListViewItems.clear();
                    		fourthListViewItems.clear();
                    	}
                    	
                    	FileInputStream fis = null, fis2 = null;
                        BufferedReader reader = null, reader2 = null;
                    	
                    	try {
							
							fis = new FileInputStream(FxController.eventLog);
				            reader = new BufferedReader(new InputStreamReader(fis));
				            
				            fis2 = new FileInputStream(FxController.log);
				            reader2 = new BufferedReader(new InputStreamReader(fis2));
				            
						} catch (FileNotFoundException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
                    	
                    	try {
                    		
                    		String activity = secondListView.getSelectionModel().getSelectedItem();
                    		String type = firstListView.getSelectionModel().getSelectedItem();
                    		
                    		String eventLogLine, logCatLine;
                    		SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss");
							
                    		while ( (eventLogLine = reader.readLine()) != null)
							
                    		{
								String eventTime = eventLogLine.split(" ")[1];
								
								while ((logCatLine = reader2.readLine())!= null) {
									
									String logTime = logCatLine.split(" ")[1].split("\\.")[0];
									
								    Date d1 = sdf.parse(logTime);
								    Date d2 = sdf.parse(eventTime);
								    
								    if(Math.abs(d1.getTime()-d2.getTime()) <= 100000){
								    	
								    	String[] arr = logCatLine.split(" ");
								    	String error = "";
								    	for (int i = 0; i < arr.length; i++) {
											if(i>5){
												error = error + arr[i]; 
											}
										}
								    	
								    	thirdListViewItems.add("");
								    	
								    }
								}
							}
							
						} catch (IOException | ParseException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
                    	
						
						thirdListViewItems.add("IInputConnectionWrapper: finishComposingText");
						
                    	
                    }
                }
        );
        
        thirdListView.getSelectionModel().selectedItemProperty().addListener(
    			new ChangeListener<String>() {
            	
                    public void changed(ObservableValue<? extends String> observable, String oldValue, String newValue) {
                    	
                    	if(!fourthListViewItems.isEmpty())fourthListViewItems.clear();
						
						fourthListViewItems.add("id/ride_name	KEYCODE_B");
						fourthListViewItems.add("Airpane Mode	On");
						fourthListViewItems.add("id/ride_name	KEYCODE_X");
						fourthListViewItems.add("id/ride_name	KEYCODE_F");
						fourthListViewItems.add("id/ride_name	KEYCODE_L");
						fourthListViewItems.add("id/ride_name	KEYCODE_M");
						
                    	
                    }
                }
        );
    }

}
