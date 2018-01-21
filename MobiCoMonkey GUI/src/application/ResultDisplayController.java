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
    
    HashMap<String, String> hmapTime = new HashMap<String, String>();
    
    public void initialize() throws IOException{
    	
    	hmap.put("Error", "E");
    	hmap.put("Fatal", "F");
    	hmap.put("Warning", "W");
    	    	
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
                                	
                    	if(!secondItems.isEmpty()){
                    		secondItems.clear();
                    		thirdListViewItems.clear();
                    		fourthListViewItems.clear();
                    	}
						
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
                        		String[] arr = myLine.split("\\.");
                        		String activity = "";  
                        		for(int i = 3; i<arr.length; i++){
                        			activity = activity +"."+ arr[i];
                        		}
                        		secondItems.add(activity);
                        	}
						} catch (Exception e) {
							// TODO: handle exception
							e.printStackTrace();
						}
						
                    }
                }
        		
        );
        
        secondListView.getSelectionModel().selectedItemProperty().addListener(
    			new ChangeListener<String>() {
            	
                    public void changed(ObservableValue<? extends String> observable, String oldValue, String newValue) {
                    	
                    	if(!thirdListViewItems.isEmpty()) {
                    		thirdListViewItems.clear();
                    		fourthListViewItems.clear();
                    		hmapTime.clear();
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
                    		
                    		//System.out.println(hmap.get(type));
                    		
                    		String eventLogLine, logCatLine;
                    		SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss");
							
                    		while ( (eventLogLine = reader.readLine()) != null)
							
                    		{	
                    			if (eventLogLine.contains(activity)) {
                    				
                    				String eventTime = eventLogLine.split(" ")[1].split("\t")[0];
    								
    								while ((logCatLine = reader2.readLine())!= null) {
    									   									
    									if (logCatLine.contains(hmap.get(type))) {
												
    										String logTime = logCatLine.split(" ")[1].split("\\.")[0];
        									
        									//System.out.println(eventTime + " " +logTime);
        									
        								    Date d1 = sdf.parse(logTime);
        								    Date d2 = sdf.parse(eventTime);
        								    
        								    if(Math.abs(d1.getTime()-d2.getTime()) <= 5000){
        								    	
        								    	String[] arr = logCatLine.split(" ");
        								    	String error = "";
        								    	
        								    	for (int i = 7; i < arr.length; i++) {
        											
        											error = error + " " + arr[i];
        											
        										}
        								    	
        								    	thirdListViewItems.add(error);
        								    	
        								    	hmapTime.put(error, logTime);
        								    }
    										
										}
    									
    								}
								}
                    			
							}
                    		
                    		thirdListView.setItems(thirdListViewItems);
							
						} catch (IOException | ParseException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
                    }
                }
        );
        
        thirdListView.getSelectionModel().selectedItemProperty().addListener(
    			new ChangeListener<String>() {
            	
                    public void changed(ObservableValue<? extends String> observable, String oldValue, String newValue) {
                    	
                    	if(!fourthListViewItems.isEmpty())fourthListViewItems.clear();
						
                    	FileInputStream fis = null, fis2 = null;
                        BufferedReader reader = null, reader2 = null;
                    	
                    	try {
							
							fis = new FileInputStream(FxController.eventLog);
				            reader = new BufferedReader(new InputStreamReader(fis));
				            
				            fis2 = new FileInputStream(FxController.contextEventLog);
				            reader2 = new BufferedReader(new InputStreamReader(fis2));
				            
						} catch (FileNotFoundException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
                    	
                    	try {
                    		
                    		SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss");
                    		String error = thirdListView.getSelectionModel().getSelectedItem();
                    		
                    		String eventLogLine;
                    		
                    		while ((eventLogLine = reader2.readLine())!= null) {
                    			
                    			System.out.println(eventLogLine);
                    			
                    			if (eventLogLine.isEmpty()) {
									break;
								}
								
                        		String eventTime = eventLogLine.split(" ")[1];
    							
    							//System.out.println(eventTime + " " +logTime);
    							
    						    Date d1 = sdf.parse(hmapTime.get(error));
    						    Date d2 = sdf.parse(eventTime);
    						    
    						    
    						    if(Math.abs(d1.getTime()-d2.getTime()) <= 10000){
    						    	
    						    	String[] arr = eventLogLine.split(" ");
							    	
    						    	String msg = "";
							    	
							    	for (int i = 2; i < arr.length; i++) {
										
										msg = msg + " " + arr[i];
										
									}
    						    	
    						    	fourthListViewItems.add(msg);
    						    	
    						    }
                        		
    						}
                    		
                        	
                        	while ((eventLogLine = reader.readLine())!= null) {
    								
                        		String eventTime = eventLogLine.split(" ")[1].split("\t")[0];
    							
    							//System.out.println(eventTime + " " +logTime);
    							
    						    Date d1 = sdf.parse(hmapTime.get(error));
    						    Date d2 = sdf.parse(eventTime);
    						    
    						    if(Math.abs(d1.getTime()-d2.getTime()) <= 5000){
    						    	
    						    	String id = eventLogLine.split("\t")[2].split(":")[1];
							    	String keycode = eventLogLine.split("\t")[3];
    						    	
    						    	fourthListViewItems.add(id + " " + keycode);
    						    	
    						    }
                        		
    						}
                        	
                        	fourthListView.setItems(fourthListViewItems);
                        	
						} catch (Exception e) {
							// TODO: handle exception
							e.printStackTrace();
						}
                    	
                    }
                }
        );
    }

}
