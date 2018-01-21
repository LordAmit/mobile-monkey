package application;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.Properties;
import java.util.ResourceBundle;

import com.sun.corba.se.spi.orbutil.fsm.Guard.Result;

import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.stage.FileChooser;
import javafx.stage.Stage;

public class FxController implements Initializable{
	
	@FXML
	private TextField config;
	@FXML
	private TextField min_inteval;
	@FXML
	private TextField max_interval;
	@FXML
	private TextField duration;
	@FXML
	private TextField seed;
	
	@FXML
	private Button browse;
	
	@FXML
	private Button stop;
	
	@FXML
	private Button result;
	
	@FXML
	private Button run;
	
	@FXML
	private Button gsm;
	
	@FXML
	private Button network_status;
	
	@FXML
	private Button network_delay;
	
	public static String python = "/usr/bin/python3.6";
	public static String directory;
	public static String filePath;
	public static String log;
	public static String eventLog;
	public static String contextEventLog;
	public static String activityList;
	public static String networkstatus;
	public static String networkdelay;
	public static String gsmprofile;
	public static String package_name;
	public static String root;
	final FileChooser fileChooser = new FileChooser();
	private BufferedReader bufRead;
	private Process process, process2;
	
	
    @FXML
    private void handleRunButtonAction(ActionEvent event) {
    	
    	new Thread(new Runnable() {
			
			@Override
			public void run() {
				
				String s = null;
		        try {
		        	String command = python+" "+directory+"/install_app.py";
		            process = Runtime.getRuntime().exec(command); 
		     
		            BufferedReader stdInput = new BufferedReader(new 
		                InputStreamReader(process.getInputStream()));

		            while ((s = stdInput.readLine()) != null) {
		                System.out.println(s);
		            }
		            
		            process.waitFor();
		            
		            String command2 = python+" "+directory+"/MobiCoMonkey.py";
		            process2 = Runtime.getRuntime().exec(command2);
		            
		            stdInput = new BufferedReader(new 
			                InputStreamReader(process2.getInputStream()));
		            
		            while ((s = stdInput.readLine()) != null) {
		                System.out.println(s);
		            }
		            
		            
		        }
		        catch (IOException e) {
		        	System.out.println("exception happened: ");
		            e.printStackTrace();
		            System.exit(-1);
		        } catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
			}
		}).start();
    }
    
    @FXML
    private void handleStopButtonAction(ActionEvent event) {
  
		try {
			String command = python+" "+directory+"/kill_emulator.py";
			process = Runtime.getRuntime().exec(command);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
    
    @FXML
    private void handleBrowseButtonAction() {
    	File file = fileChooser.showOpenDialog(browse.getScene().getWindow());
        if (file != null) {
            openFile(file);
        }
		
	}
    
    @FXML
    private void handleGsmButtonAction(ActionEvent event) throws IOException{
    	Parent root = FXMLLoader.load(getClass().getResource("gsmprofile.fxml"));
        Scene scene = new Scene(root);
        GridPane baseGrid = (GridPane) root;
        Stage stage = new Stage();
        stage.setTitle("Gsm Profile Events Generation");
        stage.setScene(scene);
        stage.show();
        
        scene.widthProperty().addListener(new ChangeListener<Number>() {
            @Override public void changed(ObservableValue<? extends Number> observableValue, Number oldSceneWidth, Number newSceneWidth) {
            	System.out.println("Width: " +newSceneWidth);
            	baseGrid.setPrefWidth((double) newSceneWidth);
            }
        });
        
        scene.heightProperty().addListener(new ChangeListener<Number>() {
            @Override public void changed(ObservableValue<? extends Number> observableValue, Number oldSceneHeight, Number newSceneHeight) {
            	System.out.println("Height: " + newSceneHeight);
            	baseGrid.setPrefHeight((double) newSceneHeight);
            }
        });
        
    }
    
    @FXML
    private void handleNsButtonAction(ActionEvent event) throws IOException{
    	Parent root = FXMLLoader.load(getClass().getResource("networkstatus.fxml"));
        Scene scene = new Scene(root);
        GridPane baseGrid = (GridPane) root;
        Stage stage = new Stage();
        stage.setTitle("Network Status Events Generation");
        stage.setScene(scene);
        stage.show();
        
        scene.widthProperty().addListener(new ChangeListener<Number>() {
            @Override public void changed(ObservableValue<? extends Number> observableValue, Number oldSceneWidth, Number newSceneWidth) {
            	System.out.println("Width: " +newSceneWidth);
            	baseGrid.setPrefWidth((double) newSceneWidth);
            }
        });
        
        scene.heightProperty().addListener(new ChangeListener<Number>() {
            @Override public void changed(ObservableValue<? extends Number> observableValue, Number oldSceneHeight, Number newSceneHeight) {
            	System.out.println("Height: " + newSceneHeight);
            	baseGrid.setPrefHeight((double) newSceneHeight);
            }
        });
        
    }
    
    @FXML
    private void handleNdButtonAction(ActionEvent event) throws IOException{
    	Parent root = FXMLLoader.load(getClass().getResource("networkdelay.fxml"));
        Scene scene = new Scene(root);
        GridPane baseGrid = (GridPane) root;
        Stage stage = new Stage();
        stage.setTitle("Network Delay Events Generation");
        stage.setScene(scene);
        stage.show();
        
        scene.widthProperty().addListener(new ChangeListener<Number>() {
            @Override public void changed(ObservableValue<? extends Number> observableValue, Number oldSceneWidth, Number newSceneWidth) {
            	System.out.println("Width: " +newSceneWidth);
            	baseGrid.setPrefWidth((double) newSceneWidth);
            }
        });
        
        scene.heightProperty().addListener(new ChangeListener<Number>() {
            @Override public void changed(ObservableValue<? extends Number> observableValue, Number oldSceneHeight, Number newSceneHeight) {
            	System.out.println("Height: " + newSceneHeight);
            	baseGrid.setPrefHeight((double) newSceneHeight);
            }
        });
        
    }
    
    @FXML
    private void handleResultButtonAction(ActionEvent event) throws IOException{
    	Parent root = FXMLLoader.load(getClass().getResource("resultDisplayView.fxml"));
        Scene scene = new Scene(root);
        GridPane baseGrid = (GridPane) root;
        Stage stage = new Stage();
        stage.setTitle("MobiCoMonkey Result");
        stage.setScene(scene);
        stage.show();
        
        scene.widthProperty().addListener(new ChangeListener<Number>() {
            @Override public void changed(ObservableValue<? extends Number> observableValue, Number oldSceneWidth, Number newSceneWidth) {
            	System.out.println("Width: " +newSceneWidth);
            	baseGrid.setPrefWidth((double) newSceneWidth);
            }
        });
        
        scene.heightProperty().addListener(new ChangeListener<Number>() {
            @Override public void changed(ObservableValue<? extends Number> observableValue, Number oldSceneHeight, Number newSceneHeight) {
            	System.out.println("Height: " + newSceneHeight);
            	baseGrid.setPrefHeight((double) newSceneHeight);
            }
        });
        
    }
    
    private void openFile(File file) {
        try {
        	directory = file.getParentFile().toString();
        	filePath = file.getAbsolutePath().toString();
            config.setText(filePath);
            loadProperties();
        } catch (Exception ex) {
            ex.setStackTrace(null);
        }
    }
    
    private void loadProperties() throws IOException {	
    	
        run.setDisable(false);
        stop.setDisable(false);
        result.setDisable(false);
        gsm.setDisable(false);
        network_status.setDisable(false);
        network_delay.setDisable(false);
    	
    	FileReader input = new FileReader(filePath);
    	bufRead = new BufferedReader(input);
    	String myLine = null;

    	while ( (myLine = bufRead.readLine()) != null)
    	{    
    	    try {
    	    	String[] array = myLine.split(": ");
        	    
        	    if(array[0].equals("seed")) {
        	    	seed.setText(array[1]);
        	    }
        	    if(array[0].equals("minimum_interval")) {
        	    	min_inteval.setText(array[1]);
        	    }
        	    if(array[0].equals("maximum_interval")) {
        	    	max_interval.setText(array[1]);
        	    }
        	    if(array[0].equals("duration")) {
        	    	duration.setText(array[1]);
        	    }
        	    if(array[0].equals("apk_name")) {
        	    	package_name = array[1];
        	    }
        	    if(array[0].equals("root")) {
        	    	root = array[1];
        	    }
        	    
			} catch (Exception e) {
				e.printStackTrace();
			}
    	}
    	
    	log = directory + "/test/logcat.log";
    	eventLog = directory + "/test/EventLog";
    	contextEventLog = directory + "/test/ContextEventLog";
    	activityList = directory + "/test/activity_list";
    	networkstatus = directory + "/test/networkstatus.txt";
    	networkdelay = directory + "/test/networkdelay.txt";
    	gsmprofile = directory + "/test/gsmprofile.txt";
    	
    	System.out.println(log);
    	
    	input.close();
		
	}

    @Override 
    public void initialize(URL url, ResourceBundle rb) {
        config.setDisable(true);
        
        run.setDisable(true);
        stop.setDisable(true);
        result.setDisable(true);
        gsm.setDisable(true);
        network_status.setDisable(true);
        network_delay.setDisable(true);
    }   
	
}
