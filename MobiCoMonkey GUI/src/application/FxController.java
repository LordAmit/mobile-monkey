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

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
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
	private Button result;
	@FXML
	private Button browse;
	
	public static String python = "/usr/bin/python3.6";
	public static String directory;
	public static String filePath;
	public static String logaddress;
	public static String eventLog;
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
		            
		            
		            String command2 = python+" "+directory+"/test.py";
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
    	process2.destroy();
		process.destroy();
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
    private void handleResultButtonAction(ActionEvent event) throws IOException{
    	Parent root = FXMLLoader.load(getClass().getResource("resultDisplayView.fxml"));
        Scene scene = new Scene(root);
        Stage stage = new Stage();
        stage.setTitle("Mobile Monkey Result");
        stage.setScene(scene);
        stage.show();
        
        result.getScene().getWindow().hide();
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
    	
    	logaddress = root+"/"+package_name + "_.log";
    	eventLog = root+"/EventLog";
    	
    	System.out.println(logaddress);
    	
    	input.close();
		
	}

    @Override 
    public void initialize(URL url, ResourceBundle rb) {
        config.setDisable(true);
    }   
	
}
