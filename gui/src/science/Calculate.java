package science;

// GEOMETRIC FORMULAS
public class Calculate {

	// CALCULATE THE SPEED OF AN OBJECT
	public static double speed(double distance, double time) {
		return distance / time;
	}

	// CALCULATE THE VELOCITY OF AN OBJECT
	public static double[] velocity(double distance, double time, double direction) {
		double[] i = new double[2];
		i[0] = distance / time;
		
		// DIRECTION AS AN ANGLE
		i[1] = direction;
		return i;
	}

	// CALCULATE THE DENSITY OF AN OBJECT
	public static double density(double mass, double volume) {
		return mass / volume;
	}

	// CALCULATE THE AREA OF A PARALLELOGRAM
	public static double parallelogram_area(double base, double height) {
		return base * height;
	}

	// CALCULATE THE AREA OF A TRIANGLE
	public static double triangle_area(double base, double height) {
		return (base / 2) * height;
	}

	// CALCULATE THE AREA OF A TRAPAZOID
	public static double trapazoid_area(double height, double base_one, double base_two) {
		return (height / 2) * (base_one + base_two);
	}

	// CALCULATE THE CIRCUMFERANCE OF A CIRCLE
	public static double circumference(double radius) {
<<<<<<< HEAD
	// could also use: pi * diamiter;
	return 2 * Math.PI * radius;
=======
		// could also use: pi * diamiter;
		return 2 * Calculate.calc_pi() * radius;
>>>>>>> a0808fac6333bb3cfae80e32586d4870d99a9206
	}

	// CALCULATE THE AREA OF A CIRCLE
	public static double circle_area(double radius) {
<<<<<<< HEAD
	return Math.PI * Math.pow(radius, 2);
=======
		return Calculate.calc_pi() * Math.pow(radius, 2);
>>>>>>> a0808fac6333bb3cfae80e32586d4870d99a9206
	}

	// CALCULATE THE TOTAL SURFACE AREA OF A RECTANGULAR PRISM
	public static double rectangular_prism_surface_area(double length, double width, double height) {
		return (2 * (length * width)) + (2 * (length * height)) + (2 * (height * width));
	}

	// CALCULATE THE TOTAL SURFACE AREA OF A CYLANDER
	public static double surface_area_cylander(double radius, double height) {
<<<<<<< HEAD
	return 2 * Math.PI * radius * 2 + 2 * Math.PI * radius * height;
=======
		return 2 * Calculate.calc_pi() * radius * 2 + 2 * Calculate.calc_pi() * radius * height;
>>>>>>> a0808fac6333bb3cfae80e32586d4870d99a9206
	}

	// CALCULATE THE VOLUME OF A RECTANGULAR PRISM
	public static double volume_rectangular_prism(double length, double width, double height) {
		return length * width * height;
	}

	// CALCULATE THE VOLUME OF A RRIANGULAR PRISM
	public static double volume_rectangle(double base_area, double height) {
		return base_area * height;
	}

	// CALCULATE THE VOLUME OF A CYLANDER
	public static double volume_cylander(double base_area, double height) {
		return base_area * height;
	}

	// CALCULATE THE VOLUME OF A CUBE
	public static double cube_volume(double side_length) {
		return Math.pow(side_length, 3);
	}

	// CALCULATE THE PERIMETER OF A SQUARE
	public static double square_perimeter(double length) {
		return 4 * length;
	}

	// CALCULATE THE PERIMETER OF A RECTANGLE
	public static double rectangle_perimeter(double base, double height) {
		return 2 * base + 2 * height;
	}

	// CALCULATE THE PERIMETER OF A TRIANGLE
	public static double triangle_perimeter(double side_a, double side_b, double side_c) {
		return side_a + side_b + side_c;
	}

	// CALCULATE THE AREA OF A SQUARE
	public static double square_area(double side) {
		return side * side;
	}

	// CALCULATE THE AREA OF A RECTANGLE
	public static double rectangle_area(double length_of_base, double width_of_side) {
		return length_of_base * width_of_side;
	}

	// TIME CONVERSIONS
<<<<<<< HEAD
	public static final int SECONDS_PER_MONTH = 60*60*24*30;
	public static final int SECONDS_PER_YEAR = 60*60*24*365;
=======
	public static final int SECONDS_PER_MONTH = 60 * 60 * 24 * 30;
	public static final int SECONDS_PER_YEAR = 60 * 60 * 24 * 365;
	
	// UNIX EPOCH (STARTS MIDNIGHT, JAN 1, 1970)
	long totalMilliseconds = (System.currentTimeMillis());
	long totalSeconds = (totalMilliseconds / 1000);
	long currentSecond = (totalSeconds % 60);
	long totalMinutes = (totalSeconds / 60);
	long currentMinute = (totalMinutes % 60);
	long totalHours = (totalMinutes / 60);
	long currentHour = (totalHours % 24);

	// CALCULATE PI
	public static double digits_pi() {

		int input = 10; // ETERATIONS
		double output = 0.0;
		boolean positive = true;
		for (int i = 0; i < input; i++) { 
			double contribution = 1.0/(2.0 * ((double)i) + 1.0);
			if (positive) 
				output += contribution;
			else 
				output -= contribution;
			positive = !positive;
		}

		return output * 4.0;
	}
>>>>>>> a0808fac6333bb3cfae80e32586d4870d99a9206

}
