// ----------------------------
// AGDAC_Automatic Gas Data Aquisition for Gas Counter
// ----------------------------

// Author: Carla Isabel Flores Rodriguez


// Input variables
// ----------------------

int PinSensors[]    = {3,6,10};          // Read pins
float VolChamber[]  = {3.37,3.25,3.4};//{3.37,3.25,3.22};  // Ritter cell volume
const unsigned long period = 300000L;    // Port reading period (1000 --> 1s)

int Pulse[3];                           // Current pulse level
int PulseLess1[]   = {1,1,1};           // Previous pulse level
int Counter[3];                         // Current counter
int CounterLess1[] = {0,0,0};           // Previous counter
float Volume[3];                        // Actual measured gas volume
int PulseAux[3];                        // Pulse level change indicator


unsigned long timenow = 0;              // Initial reference time


// Set digital pin mode
// -----------------------------

void setup() {

for (int i=0; i<3; i++){

    // Start serial for measurement display
    Serial.begin(9600);

    // Pull-up input mode
    pinMode(PinSensors[i], INPUT_PULLUP);

}
    
}

// Volume calculation per sensor
// -----------------------------

void loop() {

for (int i=0; i<3; i++){

  Pulse[i] = digitalRead(PinSensors[i]);  // Read digital pin (pulse level)

  // Update counter if pulse level changes
  if (Pulse[i] == 0){ 
    if (PulseLess1[i] == 0){
      Counter[i] = CounterLess1[i];
      PulseAux[i] = 0;
    }
    else{
      Counter[i] = CounterLess1[i] + 1;
      PulseAux[i] = 1;
    }
  }
  else {
    Counter[i] = CounterLess1[i]; 
    PulseAux[i] = 0;    
  }

  // Estimate real volume
  Volume[i] = VolChamber[i] * Counter[i];
  PulseLess1[i] = Pulse[i];
  CounterLess1[i] = Counter[i];
  
}

// Display sensor volumes if pulse changes
if (PulseAux[0] || PulseAux[1] || PulseAux[2]){

    Serial.print(Volume[0]);
    Serial.print("\t");
    Serial.print(Volume[1]);
    Serial.print("\t");
    Serial.println(Volume[2]);
    delay(4);
    
}

// Display sensor volumes at regular intervals
if (millis() - timenow > period) {
    timenow = millis();
    Serial.print(Volume[0]);
    Serial.print("\t");
    Serial.print(Volume[1]);
    Serial.print("\t");
    Serial.println(Volume[2]);
    delay(4);
}

}
