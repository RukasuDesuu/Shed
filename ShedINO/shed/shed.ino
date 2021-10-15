String inputString = ""; 
bool stringComplete = false; 
#define led 2

String chaveObj[] = {"cortina", "led", "luz"};
int chavesSize = 3;
bool bCond = false;
bool bObj= false;

void setup() {
  Serial.begin(9600); 
  inputString.reserve(200);
  pinMode(led, OUTPUT);
}


void loop() {
  Serial.println(inputString);  
  if (stringComplete){ 
    Serial.print("Running..."); 
    Serial.print(inputString); 
  if ((inputString.startsWith("Abrindo/Ligando"))){
     bCond = true;
  }
  for (int t =0; t <= chavesSize; t++){
    if ((inputString.endsWith(chaveObj[t]))){
      bObj = true;
    }
  }
  if (bObj == true){
    if ((inputString.endsWith("led"))){
      digitalWrite(led, bCond);
      Serial.println("Ligou");
    } 
  }
  inputString = ""; 
  stringComplete = false; 
  }
}

//Evento que ocorre toda vez após o void loop
void serialEvent(){ 
  while (Serial.available()){ 
    char inChar = (char)Serial.read(); 
    inputString += inChar; 
    if (inChar == '\n'){ 
      stringComplete = true;
    }
  }
}
