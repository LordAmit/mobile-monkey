package application;

import java.io.IOException;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.stage.Stage;
import javafx.scene.Parent;
import javafx.scene.Scene;


public class Main extends Application {
	
	@Override
	public void start(Stage stage) throws IOException{
		Parent root = FXMLLoader.load(getClass().getResource("mobile_monkey.fxml"));
	    Scene scene = new Scene(root);
	    stage.setScene(scene);
	    stage.setTitle("Mobile Monkey");
	    stage.show();
	}
	
	public static void main(String[] args) {
		launch(args);
	}
}
