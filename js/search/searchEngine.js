// These are the available "error strings" you can change them to affect the output
// of the search engine.
ERR_NoOptions		= "You didn't specify where to search for your keywords, please try again.";
ERR_NoSearchTerms	= "You didn't enter any words to search for, please enter some words to search for and try again.";
ERR_NoResults		= "Your search found no results, try less specific terms.";

// Performs an actual search and then returns the index number(s) in the db array
// where it found this element.
// keywords = the string they searched for (each space-separated word
//     is searched for separately)
// options can be
//     1 = search keywords, not description, not heading
//     2 = search keywords, search description, not heading
//     3 = search all
function performSearch(keywords, options) {
	// Check to make sure they entered some search terms
	if (!keywords || keywords.length == 0) {
		return ERR_NoSearchTerms;
	}

	// Determine where to check for the keywords entered
	if (options == 0) {
		return ERR_NoOptions;
	}
	else if (options == 1) {
		searchKeywords = true;
		searchDescription = false;
		searchHeading = false;
	}
	else if (options == 2) {
		searchKeywords = true;
		searchDescription = true;
		searchHeading = false;
	}
	else if (options == 3) {
		searchKeywords = true;
		searchDescription = true;
		searchHeading = true;
	}

	// Setting up the keywords array for searching
	// Remove common punctuation
	keywords = keywords.replace("\.,'", "");
	
	// get them all into an array so we can loop thru them
	// we assume a space was used to separate the terms
	searchFor = keywords.split(" ");

	// This is where we will be putting the results.
	results = new Array();
	
	// Loop through the db for potential results
	// For every entry in the "database"
	for (sDB = 0; sDB < searchDB.length; sDB++) {
		// For every search term we are working with
		for (t = 0; t < searchFor.length; t++) {
			// Check in the heading for the term if required
			if (searchHeading) {
				if (searchDB[sDB].heading.toLowerCase().indexOf(searchFor[t].toLowerCase()) != -1) {
					if (!in_array(String(sDB), results)) {
						results[results.length] = String(sDB);
					}
				}
			}

			// Check in the keywords for the term if required
			if (searchKeywords) {
				if (searchDB[sDB].terms.toLowerCase().indexOf(searchFor[t].toLowerCase()) != -1) {
					if (!in_array(String(sDB), results)) {
						results[results.length] = String(sDB);
					}
				}				
			}
			
			// Check in the description for the term if required
			if (searchDescription) {
				if (searchDB[sDB].description.toLowerCase().indexOf(searchFor[t].toLowerCase()) != -1) {
					if (!in_array(String(sDB), results)) {
						results[results.length] = String(sDB);
					}
				}				
			}
		}
	}
	
	if (results.length > 0) {
		return results;
	}
	else {
		return ERR_NoResults;
	}
}

// Constructor for each search engine item.
// Used to create a record in the searchable "database"
function searchOption(heading, terms, description, url) {
	this.heading     = heading;
	this.terms       = terms;
	this.description = description;
	this.url         = url;
	return this;
}

// Returns true or false based on whether the specified string is found
// in the array.
// This is based on the PHP function of the same name.
// stringToSearch = the string to look for
// arrayToSearch  = the array to look for the string in.
function in_array(stringToSearch, arrayToSearch) {
	for (s = 0; s < arrayToSearch.length; s++) {
		if (arrayToSearch[s].indexOf(stringToSearch) != -1) {
			return true;
			exit;
		}
	}
	return false;
}

// Code from http://www.optimalworks.net/blog/2007/web-development/javascript/array-detection
function is_array(array) { return !( !array || (!array.length || array.length == 0) || typeof array !== 'object' || !array.constructor || array.nodeType || array.item ); }

// This function grabs a specified value from a GET-style URL
// you call it with the name of the variable and it returns
// the value, or false if not found.
function getURLvalue(getName) {
	var i, pos, argname, argvalue, queryString, pairs;

	// get the string following the question mark
	queryString = location.href.substring(location.href.indexOf("?")+1);

	// split parameters into pairs, assuming pairs are separated by ampersands
	pairs = queryString.split("&");

	// for each pair, we get the name and the value
	for (i = 0; i < pairs.length; i++) { 
		pos = pairs[i].indexOf('='); 
		if (pos == -1) {
			continue; 
		}
		argname = pairs[i].substring(0,pos);
		argvalue = pairs[i].substring(pos+1); 
		
		// Replaces "Google-style" + signs with the spaces
		// they represent
		if (argname == getName) {
			return unescape(argvalue.replace(/\+/g, " "));
		}
	}
	return false;
}

// Function to execute when the focus is passed to the search filed.
// It just selects everything in the field, which will mean that if 
// the user clicks the search field then types, the placeholder text
// will be removed automagically :)
// call using onFocus="javascript:searchFocus(this);
function searchFocus(searchField) {
	searchField.focus();
	searchField.select();
}