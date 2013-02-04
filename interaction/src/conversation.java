import com.google.code.chatterbotapi.*;
import com.sun.speech.freetts.VoiceManager;

/* FOR THE APIS USED REFER TO COPYRIGHT AND USAGE TEXT FILES */

public class conversation {
	
	public static String s = "default text";
	
	public static void main(String[] argv) throws Exception {
		
		// INITIALISE SPEECH SYNTHESIS AND RECOGNITION
		voce.SpeechInterface.init("lib", true, true, "./lib/grammar", "test");
		
		ChatterBotFactory factory = new ChatterBotFactory();
		
		ChatterBot bot1 = factory.create(ChatterBotType.CLEVERBOT);
		ChatterBotSession bot1session = bot1.createSession();
		
		Voice voiceKevin16 = new Voice("kevin16");
		
		String say = "hello world";

		System.out.println("Speak now, say 'quit' to quit.");

		boolean quit = false;
		while (!quit) {
			System.out.println("bot1> " + say);
			voiceKevin16.say(say);
			say = bot1session.think(s);

			while (voce.SpeechInterface.getRecognizerQueueSize() > 0) {
				s = voce.SpeechInterface.popRecognizedString();

				// QUIT SPEECH RECOGNITION IF INSTRUCTED
				if (-1 != s.indexOf("quit")) {
					quit = true;
				}
				
				// POSSIBLE RESPONSE
				if (-1 != s.indexOf("how are you")) {
					voce.SpeechInterface.synthesize("I am good");
				}
				
				// POSSIBLE RESPONSE
				if (-1 != s.indexOf("thank you")) {
					voce.SpeechInterface.synthesize("your welcome");
				}

				System.out.println("You said: " + s);
				//voce.SpeechInterface.synthesize(s);
			}
		}

		voce.SpeechInterface.destroy();
		System.exit(0);
	}
}

// VOICE CLASS DEFINES CHARACTERISTICS OF THE CHAT BOT'S VOICE
class Voice {
    private String name;
    private com.sun.speech.freetts.Voice systemVoice;

    public Voice(String name) {
        this.name = name;
        this.systemVoice = VoiceManager.getInstance().getVoice(this.name);
        this.systemVoice.allocate();
    }

    public void say(String[] thingsToSay) {
        for (int i = 0; i < thingsToSay.length; i++) {
            this.say(thingsToSay[i]);
        }
    }

    public void say(String thingToSay) {
        this.systemVoice.speak(thingToSay);
    }

    public void dispose() {
        this.systemVoice.deallocate();
    }
}
