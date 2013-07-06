package cox.speech;
/*
import com.sun.speech.freetts.FreeTTS;
import com.sun.speech.freetts.VoiceManager;

//VOICE CLASS DEFINES CHARACTERISTICS OF THE ROBOT'S VOICE
public class Voice {
	
	 static com.sun.speech.freetts.Voice voice;
	 static FreeTTS freetts = new FreeTTS(voice);
	 static {
	 voice = VoiceManager.getInstance().getVoice("kevin16");
	 if(voice!=null) {
		 voice.allocate();
	 }
	 voice.speak("hello,world");
	 //freetts.startup();
	 //freetts.shutdown();
	 }
	
	 public Voice(String name) {
		 
		 VoiceManager voiceManager = VoiceManager.getInstance(); //getVoice(name);
		 com.sun.speech.freetts.Voice voice = voiceManager.getVoice("kevin16");
		 //System.setProperty("com.sun.speech.freetts.Voice", "com.sun.speech.freetts.audio.SingleFileAudioPlayer");
		 
		 if(voice != null) {
			 voice.allocate();
		 }
   
	 }

	public void say(String[] item) {
	    for (int i = 0; i < item.length; i++) {
	        say(item[i]);
	    }
	}
	
	public void say(String word) {
		voice.speak(word);
	}
	
	public void dispose() {
		voice.deallocate();
		//freetts.shutdown();
	}
}
*/
