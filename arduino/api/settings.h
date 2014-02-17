// CHANGE THIS TO THE UNIQUE VALUE OF YOUR ETHERNET SHIELD
static uint8_t mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0x00, 0x8F };

// CHANGE THIS TO MATCH YOUR HOST NETWORK
static uint8_t ip[] = { 192, 168, 1, 177 };

// USED FOR WEB SERVER
#define PREFIX ""

const int text_to_speech_i2c_address = 4;

// NOTES FOR LATER
//int relayPin1 = 4; // relay connected to digital pin 4 (D3 on relay shield - on switch)
//int relayPin2 = 7; // relay connected to digital pin 5 (D2 on relay shield) - Inferred LEDs
//int relayPin3 = 6; // relay connected to digital pin 6 (D1 on relay shield) - Ultraviolte LEDs
//int relayPin4 = 5; // relay connected to digital pin 7 (D0 on relay shield) (not used)
