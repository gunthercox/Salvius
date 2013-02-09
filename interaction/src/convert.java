
// CONVERT VARIOUS UNITS OF MEASUREMENT
public class convert {
	
	// RANKINE TO KELVIN
	public static double rankine_to_kelvin(double rankine) {
		return rankine * 5 / 9;
	}
	
	// RANKINE TO CELSIUS
	public static double rankine_to_celsius(double rankine) {
		return convert.kelvin_to_celsius(convert.rankine_to_kelvin(rankine));
	}
	
	// RANKINE TO FAHRENHEIT
	public static double rankine_to_fahrenheit(double rankine) {
		return convert.kelvin_to_fahrenheit(convert.rankine_to_kelvin(rankine));
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