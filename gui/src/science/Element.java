package science;

public class Element {
	
	// PROPERTIES OF AN ELEMENT
	int group_number = 0;
	int period = 0;
	String name = "";
	double atomic_mass = 0.0;
	double melting_point = 0.0;
	double boiling_point = 0.0;
	double density = 0.0;
	double electronegativity = 0.0;	// PAULING SCALE
	int[] ionization_potential = {0, 0, 0}; // 1ST, 2ND, 3RD IONIZATION POTENTIAL (eV)
	double electron_affinity = 0.0;
	int oxidation_state = 0;
	String electron_configuration = "";
	double atomic_radius = 0.0;
	double atomic_volume = 0.0;
	String crystal_structure = "";
	double electrical_conductivity = 0.0;
	boolean toxic = false;
	boolean carcinogenic = false;
	double atomic_weight = 0.0;
	
	// CONSTRUCTOR FOR AN ELEMENT
	public Element(String n, boolean tox) {
		
		name = n;
		toxic = tox;
		
	}
	
	public Element hydrogen = new Element("hydrogen", false);
	public Element helium = new Element("helium", false);
	
	// GENERATE A PERIODIC TABLE IN THE FORM OF AN ARRAY USING SELECTED DATA

}
