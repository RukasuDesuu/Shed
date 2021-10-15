String inputString = ""; 
bool stringComplete = false; 
#define pa 2 
#define pv 3 
#define pc 4
#define pg 5 


void setup() {
  Serial.begin(9600); 
  inputString.reserve(200);
  
  pinMode(pa, OUTPUT);
  pinMode(pv, OUTPUT);
  pinMode(pc, OUTPUT);
  pinMode(pg, OUTPUT);
}


void loop() {
  if (stringComplete){ 
    Serial.print("Running..."); 
    Serial.print(inputString); 

  inputString = ""; //Esvazia a variavel de texto
  stringComplete = false; //texto volta a ser incompleto
  }
}

//Evento que ocorre toda vez após o void loop
void serialEvent(){ 
  while (Serial.available()){ //Enquanto houver entrada pendente no monitor serial
    char inChar = (char)Serial.read(); //Pega cada caractere recebido no monitor serial
    inputString += inChar; //Adiciona cada caractere até completar o texto
    if (inChar == '\n'){ //Quando houver quebra de linha:
      stringComplete = true; //O texto esta completo
    }
  }
}