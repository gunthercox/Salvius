package web_interface;

// CONVERT VARIOUS UNITS OF MEASUREMENT
public class Convert {
	
	// RANKINE TO KELVIN
	public static double rankine_to_kelvin(double rankine) {
		return rankine * 5 / 9;
	}
	
	// RANKINE TO CELSIUS
	public static double rankine_to_celsius(double rankine) {
		return Convert.kelvin_to_celsius(Convert.rankine_to_kelvin(rankine));
	}
	
	// RANKINE TO FAHRENHEIT
	public static double rankine_to_fahrenheit(double rankine) {
		return Convert.kelvin_to_fahrenheit(Convert.rankine_to_kelvin(rankine));
	}
	
	// KELVIN TO RANKINE
	public static double kelvin_to_rankine(double kelvin) {
		return kelvin * 9 / 5;
	}
	
	// KELVIN TO CELSIUS
	public static double kelvin_to_celsius(double kelvin) {
		return kelvin - 273.15;
	}
	
	// KELVIN TO FAHRENHEIT
	public static double kelvin_to_fahrenheit(double kelvin) {
		return ((kelvin - 273.15) * 1.8000) + 32.00;
	}
	
	// CELSIUS TO RANKINE
	public static double celsius_to_rankine(double celsius) {
		return celsius * 1.8000 + 491.67;
	}
	
	// CELSIUS TO KELVIN
	public static double celsius_to_kelvin(double celsius) {
		return celsius + 273.15;
	}
	
	// CELSIUS TO FAHRENHEIT
	public static double celsius_to_fahrenheit(double celsius) {
		return ((9 / 5) * celsius) + 32;
	}
	
	// FAHRENHEIT TO RANKINE
	public static double fahrenheit_to_rankine(double fahrenheit) {
		return (fahrenheit - 32) + 491.67;
	}
	
	// FAHRENHEIT TO KELVIN
	public static double fahrenheit_to_kelvin(double fahrenheit) {
		return ((fahrenheit - 32) * 5 / 9) + 273.15;
	}
	
	// FAHRENHEIT TO CELSIUS
	public static double fahrenheit_to_celsius(double fahrenheit) {
		return (fahrenheit - 32) * 5 / 9;
	}
	
	// CANDLEPOWER AND LUMENS
	public static double candlepower_to_lumens (double candlepower, boolean isInCandlepower) {
		
		// CALCULATE LUMENS
		double lumens = 4 * Math.PI;
		
		// RETURN VALUE IN CANDEL POWER OR LUMENS
		if (isInCandlepower == true) {
			return candlepower * lumens;
		} else {
			return candlepower / lumens;
		}
	}
	
	// STANDARD UNIT CONVERSION
	public static double standard (double value, String type, String current, String desired) {
		double output = 0.0;	
		boolean lower = false;
		
		// NOTE THE DIFFERENCE BETWEEN THE BRITISH LONG TON AND THE AMERICAN SHORT TON
		// THE DIFFERENCE IN TONS IS DUE TO THE VALUE OF THE HUNDREDWEIGHT IN EACH COUNRY
		// US HUNDREDWEIGHT = 100 POUNDS, BRITISH HUNDREDWEIGHT = 112 POUNDS
		// THERE IS ALSO THE METRIC TON (1000 KILOGRAMS)
		
		// LENGTH
		
		// DRY MEASURE
		String[] dryMeasure = {"pint", "quart", "peck", "bushel"};
		double[] dryMeasureValues = {};
		double[] dryMeasureToLiters = {};
				
		// AVOIRDUPOIS WEIGHT
		String[] avoidupoisWeight = {"ounce", "pound", "hundredweight", "ton"};
		double[] avoidupoisWeightValues = {1, 16, 100, 20};
		double[] avoidupoisWeightToGrams = {28.3495, 453.59, 45360, 907180};
		
		
		// TROY WEIGHT
		String[] troyWeight = {"grain", "carat", "pennyweight", "ounce", "pound"};
		double[] troyWeightConversion = {1, 3.086, 24, 20, 12};
		double[] troyWeightToGrams = {0.0648, 0.2, 1.5552, 31.1035, 373.24};
		
		if (type.equals("troyweight")) {
			
			output = value;
			
			for (int i = troyWeight.length; i >= 0; i--) {
				
				// CONVERT INPUT TO SMALLEST UNIT OF MEASURE
				if (! (troyWeight[i].equals(current)) || lower == true) {
					output = output / troyWeightConversion[i];
					lower = true;
				}
				
				if (troyWeight[i].equals(desired)) {
					output = output * troyWeightConversion[i];
				}
				
			}
			
		}
		
		if (type.equals("troyToMetric")) {
			
			output = value;
			
			for (int i = troyWeight.length; i >= 0; i--) {
				
				// CONVERT INPUT TO SMALLEST UNIT OF MEASURE
				if (! (troyWeight[i].equals(current)) || lower == true) {
					output = output / troyWeightToGrams[i];
					lower = true;
				}
				
				if (troyWeight[i].equals(desired)) {
					output = output * troyWeightToGrams[i];
				}
				
			}
			
		}
		
		return output;
	}
	
	
	// METRIC UNITS
	public static double metric(double value, String current, String desired) {
		
		String[] prefix = {"yocto", "zepto", "atto", "femto", "pico", "nano", 
				"micro", "milli", "centi", "deci", "none", "deka", "hecto", 
				"kilo", "mega", "giga", "tera", "peta", "exa", "zetta", "yotta"};
		
		String[] symbol = {"y", "z", "a", "f", "p", "n", "u", "m", "c", "d", 
				"none", "D", "h", "K", "M", "G", "T", "P", "E", "Z", "Y"};
		
		double[] power = {-24, -21, -18, -15, -12, -9, -6, -3, -2, -1, 
							0, 1, 2, 3, 6, 9, 12, 15, 18, 21, 24};
		
		double converted = 0;
		double temp;
		
		for (int i = 0; i < prefix.length; i++) {
			
			// CONVERT TO BASE
			if (prefix[i].equals(current) || symbol[i].equals(current)) {
				temp = value * (-1 * power[i]);
				
				for (int j = 0; j < prefix.length; j++) {
					
					// CONVERT TO DESIRED UNIT
					if (prefix[j].equals(desired) || symbol[j].equals(current)) {
						converted = temp * Math.pow(10, power[j]);
					}
				}
			}
			
		}
		
		return converted;
	}
	
	// ENGLISH TO PIG-LATIN
	public static String english_to_piglatin(String str) {
	    String[] temp;
	    String last = null;
	    String piglatin = "";
	    temp = str.split(" ");
	    for (int i = 0; i < temp.length; i++) {
	        char first = '\u0000';
	        String s = "";
	        char[] third = temp[i].toCharArray();
	        for (int counter = 0; counter < third.length; counter++) {
	            // IF VOWELS
	            if (third[0] == 'a' || third[0] == 'e' || third[0] == 'i'
	                    || third[0] == 'o' || third[0] == 'u') {
	                last = "yo";
	            } else {
	                // LETTER IS CONSONENT
	                last = "oy";
	            }
	            if (counter == 0) {
	                first = third[0];
	            } else
	                s = s + third[counter];
	        }
	        piglatin += s + first + last + " ";
	    }
	    return piglatin;
	}
	
	// ARABIC TO ROMAN NUMERATION
	public static String arabic_to_roman(int arabic) {
	    if (arabic < 1 || arabic > 3999) {
	        return "-1";
	    }
	
	    int[] arabicVals = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
	    String[] romanVals = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};
	    String roman = "";
	
	    for(int i = 0; i<arabicVals.length; i++ ) {
	        while(arabic >= arabicVals[i]) {
	            roman += romanVals[i];
	            arabic -= arabicVals[i];
	        }
	    }

    return roman;
	}
	
	// ROMAN TO ARABIC NUMERATION
	public static String roman_to_arabic(String roman) {
		
		// DETERMINE IF ROMAN NUMERAL IS VALID
		boolean validRoman = true;
		
		// CHECK IF ROMAN NUMERAL CONTAINS ROMAN CHARACTERS
		for (int k = 0; k < roman.length(); k++) {
			if (roman.charAt(k) != 'I' &&
				roman.charAt(k) != 'V' &&
				roman.charAt(k) != 'X' &&
				roman.charAt(k) != 'L' &&
				roman.charAt(k) != 'C' &&
				roman.charAt(k) != 'D' &&
				roman.charAt(k) != 'M') {
				validRoman = false;
			}
		}

		// ONLY IF IT IS A VALID ROMAN NUMERAL
		if (validRoman) {

			int arabic = 0;
			int last_digit = 0;
			int current_digit = 0;

			for (int i = 0; i < roman.length(); i++) {

				if (roman.charAt(i) == 'I') {
					current_digit = 1;
				}
				if (roman.charAt(i) == 'V') {
					current_digit = 5;
				}
				if (roman.charAt(i) == 'X') {
					current_digit = 10;
				}
				if (roman.charAt(i) == 'L') {
					current_digit = 50;
				}
				if (roman.charAt(i) == 'C') {
					current_digit = 100;
				}
				if (roman.charAt(i) == 'D') {
					current_digit = 500;
				}
				if (roman.charAt(i) == 'M') {
					current_digit = 1000;
				}

				if (last_digit < current_digit && last_digit != 0) {
					current_digit -= last_digit;
					arabic -= last_digit;
					arabic += current_digit;
					last_digit = current_digit;
					current_digit = 0;
				} else {
					last_digit = current_digit;
					arabic += current_digit;
					current_digit = 0;
				}
			}

			return String.valueOf(arabic);

		} else {
			
		// THE INPUT WAS NOT A VALID ROMAN NUMBER
		return null;
		}
	}
	
	// BINARY TO HEX
	public static String binary_to_hex(String binary) {
		
		// BREAK THE BINARY VALUE INTO QUARTETS
		String[] quartet = new String[3];
		quartet[0] = binary.substring(0, 4);
		quartet[1] = binary.substring(4, 8);
		quartet[2] = binary.substring(8, 12);
		
		String hexidecimal = "";
		String hex;
		
		// SELECT A HEX VALUE FOR EACH BINARY VALUE
		for (int i = 0; i < quartet.length; i++) {
			switch (quartet[i]) {
            case "0000": hex = "0";
            break;
            case "0001": hex = "1";
            break;
            case "0010": hex = "2";
            break;
            case "0011": hex = "3";
            break;
            case "0100": hex = "4";
            break;
            case "0101": hex = "5";
            break;
            case "0110": hex = "6";
            break;
            case "0111": hex = "7";
            break;
            case "1000": hex = "8";
            break;
            case "1001": hex = "9";
            break;
            case "1010": hex = "A";
            break;
            case "1011": hex = "B";
            break;
            case "1100": hex = "C";
            break;
            case "1101": hex = "D";
            break;
            case "1110": hex = "E";
            break;
            case "1111": hex = "F";
            break;
            default: hex = "";
            break;
	        }
			
			// CONCATINATE THE QUARTETS
			hexidecimal += hex;
			
		}
		
		return hexidecimal;
	}
	
	// HEX TO BINARY
	public static String hex_to_binary(String hexidecimal) {
		
		String binary = "";
		String bin;
		
		// SELECT A BINARY VALUE FOR EACH HEX VALUE
		for (int i = 0; i < 4; i++) {
			
			switch (hexidecimal.substring(i)) {
            case "0": bin = "0000";
            break;
            case "1": bin = "0001";
            break;
            case "2": bin = "0010";
            break;
            case "3": bin = "0011";
            break;
            case "4": bin = "0100";
            break;
            case "5": bin = "0101";
            break;
            case "6": bin = "0110";
            break;
            case "7": bin = "0111";
            break;
            case "8": bin = "1000";
            break;
            case "9": bin = "1001";
            break;
            case "A": bin = "1010";
            break;
            case "B": bin = "1011";
            break;
            case "C": bin = "1100";
            break;
            case "D": bin = "1101";
            break;
            case "E": bin = "1110";
            break;
            case "F": bin = "1111";
            break;
            default: bin = "";
            break;
	        }
			
			// CONCATINATE THE QUARTETS
			binary += bin;
			
		}
		
		return binary;
	}
	
}