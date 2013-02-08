
// CONVERT VARIOUS UNITS OF MEASUREMENT
public class convert {
	
	// RANKINE TO KELVIN
	public static double rankine_to_kelvin (double rankine) {
		return rankine * 5 / 9;
	}
	
	// RANKINE TO CELSIUS
	public static double rankine_to_celsius (double rankine) {
		return convert.kelvin_to_celsius(convert.rankine_to_kelvin(rankine));
	}
	
	// RANKINE TO FAHRENHEIT
	public static double rankine_to_fahrenheit (double rankine) {
		return convert.kelvin_to_fahrenheit(convert.rankine_to_kelvin(rankine));
	}
	
	// KELVIN TO RANKINE
	public static double kelvin_to_rankine (double kelvin) {
		return kelvin * 9 / 5;
	}
	
	// KELVIN TO CELSIUS
	public static double kelvin_to_celsius (double kelvin) {
		return kelvin - 273.15;
	}
	
	// KELVIN TO FAHRENHEIT
	public static double kelvin_to_fahrenheit (double kelvin) {
		return ((kelvin - 273.15) * 1.8000) + 32.00;
	}
	
	// CELSIUS TO RANKINE
	public static double celsius_to_rankine (double celsius) {
		return celsius * 1.8000 + 491.67;
	}
	
	// CELSIUS TO KELVIN
	public static double celsius_to_kelvin (double celsius) {
		return celsius + 273.15;
	}
	
	// CELSIUS TO FAHRENHEIT
	public static double celsius_to_fahrenheit (double celsius) {
		return ((9 / 5) * celsius) + 32;
	}
	
	// FAHRENHEIT TO RANKINE
	public static double fahrenheit_to_rankine (double fahrenheit) {
		return (fahrenheit - 32) + 491.67;
	}
	
	// FAHRENHEIT TO KELVIN
	public static double fahrenheit_to_kelvin (double fahrenheit) {
		return ((fahrenheit - 32) * 5 / 9) + 273.15;
	}
	
	// FAHRENHEIT TO CELSIUS
	public static double fahrenheit_to_celsius (double fahrenheit) {
		return (fahrenheit - 32) * 5 / 9;
	}
	
}