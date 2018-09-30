// Java program to read JSON from a file 
  
import java.io.FileReader; 
import java.util.Iterator; 
import java.util.Map; 
  
import org.json.simple.JSONArray; 
import org.json.simple.JSONObject; 
import org.json.simple.parser.*; 
  
public class Runner
{ 
    public static void main(String[] args) throws Exception  
    { 
        System.out.println("hello there");

        // parsing file  
        Object obj = new JSONParser().parse(new FileReader("../data/message.json")); 

        // typecasting obj to JSONObject 
        JSONObject jo = (JSONObject) obj; 

        // getting messages
        JSONArray messages = (JSONArray) jo.get("messages");
        System.out.println(messages.get(100).toString());

        // typecasting a random message to to JSONObject
        JSONObject hundred = (JSONObject) messages.get(100);
        String sender = (String) hundred.get("sender_name"); 
        String content = (String) hundred.get("content"); 
        System.out.println(sender+ ": " + content);
    } 
} 
