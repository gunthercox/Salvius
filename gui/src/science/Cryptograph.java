package science;

public class Cryptograph {

	// CAESAR CRYPTOGRAPHY WITH CYCLICAL ROTATOR
	public static String caesar(String input, int rotator) {

		// DECLARE VARIABLES
		char[] encrypted = new char[100];
		String sentence = "ERROR";
		
		String output = "";

		while (rotator != 0) {

			// STRING TO BE ENCRYPTED
			sentence = "HELLO WORLD";

			// CONVERT STRING TO AN ARRAY OF ITS SEPERATE CHARACTERS
			encrypted = sentence.toCharArray();

			for (int k = 0; k < encrypted.length; k++) {
				if (encrypted[k] >= 'Z') {

					// CYCLE THE ALPHABET
					encrypted[k] += (char) (rotator - 26);
					output += k;
				}

				// PRESERVE SPACES
				else if (encrypted[k] != 32) {
					encrypted[k] += rotator;
				}

				output += encrypted[k];
			}
		}
		
		return output;

	}
}
