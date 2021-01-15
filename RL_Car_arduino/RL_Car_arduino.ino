int RF = 8;
int RB = 9;
int LF = 10;
int LB = 11;
int R_motor = 5;
int L_motor = 6;
int trgF = 12;
int echoF = 13;

int echoL = 7;
int echoR = 3;
int trgR = 2;
int trgL = 4; 

long senF;
long senL;
long senR;

long dst_F;
long dst_L;
long dst_R;

int Cspeed = 160;

char data_F[20];
char data_L[20];
char data_R[20];

char Ard[5] = {0};
char check[1];
int action;
bool ingame = false;
String sig;

void setup() {
Serial.begin(115200);

pinMode(LB,OUTPUT);
pinMode(LF,OUTPUT);
pinMode(RB,OUTPUT);
pinMode(RF,OUTPUT);
pinMode(L_motor,OUTPUT);
pinMode(R_motor,OUTPUT);
pinMode(trgF,OUTPUT);
pinMode(echoF, INPUT);
pinMode(echoR, INPUT);
pinMode(echoL, INPUT);
pinMode(trgR, OUTPUT);
pinMode(trgL,OUTPUT);

//Initializing.
initialize();
}

void loop() {
Sensing();
delay(20);
send_data();
delay(20);
read_data();
delay(20);
//choose_action();
delay(20);
}



///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void initialize()
{
  analogWrite(R_motor,0);
  analogWrite(L_motor,0);
  digitalWrite(RF,LOW);
  digitalWrite(RB,LOW);
  digitalWrite(LF,LOW);
  digitalWrite(LB,LOW);
}

void Sensing(){
      digitalWrite(trgF,LOW);
      delayMicroseconds(2);
      digitalWrite(trgF,HIGH);
      delayMicroseconds(5);
      digitalWrite(trgF,LOW);
      senF = pulseIn(echoF, HIGH);
      dst_F = constrain(senF/58,0,999);
      
      
      digitalWrite(trgL,LOW);
      delayMicroseconds(2);
      digitalWrite(trgL,HIGH);
      delayMicroseconds(5);
      digitalWrite(trgL,LOW);  
      senL = pulseIn(echoL, HIGH);
      dst_L = constrain(senL/58,0,999);
      
      
      digitalWrite(trgR,LOW);
      delayMicroseconds(2);
      digitalWrite(trgR,HIGH);
      delayMicroseconds(5);
      digitalWrite(trgR,LOW); 
      senR = pulseIn(echoR, HIGH);
      dst_R = constrain(senR/58,0,999);
      
}

void send_data(){
  sprintf(data_F, "%03d", dst_F);
  sprintf(data_L, "%03d", dst_L);
  sprintf(data_R, "%03d", dst_R);
  Serial.print("S");
  Serial.print(data_F);
  Serial.print(data_L);
  Serial.print(data_R);
  Serial.println("E");
}



void forward(){
  digitalWrite(RF,HIGH);
  digitalWrite(RB,LOW);
  digitalWrite(LF,HIGH);
  digitalWrite(LB,LOW);
  analogWrite(L_motor,Cspeed);
  analogWrite(R_motor,Cspeed);  
}

void back(){
  digitalWrite(RF,LOW);
  digitalWrite(RB,HIGH);
  digitalWrite(LF,LOW);
  digitalWrite(LB,HIGH);

  analogWrite(L_motor,Cspeed);
  analogWrite(R_motor,Cspeed);
  
}
void turn()
{
  digitalWrite(RF,LOW);
  digitalWrite(RB,HIGH);
  digitalWrite(LF,HIGH);
  digitalWrite(LB,LOW);
  analogWrite(L_motor,Cspeed);
  analogWrite(R_motor,Cspeed);
}

void left(){
  digitalWrite(RF,HIGH);
  digitalWrite(RB,LOW);
  digitalWrite(LF,LOW);
  digitalWrite(LB,HIGH);
  
  analogWrite(L_motor,Cspeed);
  analogWrite(R_motor,Cspeed);
    

}

void right(){
  digitalWrite(RF,LOW);
  digitalWrite(RB,HIGH);
  digitalWrite(LF,HIGH);
  digitalWrite(LB,LOW);

  analogWrite(L_motor,Cspeed);
  analogWrite(R_motor,Cspeed);
 
}

void read_data(){
  while(Serial.available())
  {
    char wait = Serial.read();
    sig.concat(wait);
  }
  sig.substring(0,1).toCharArray(check,2);
  if(check[0] == 'S')
  {
    ingame = true;
    sig.substring(1,2).toCharArray(Ard,5);
    action = atoi(Ard);
    sig = "";
  }
  else if (check[0] == 'R')
  {
    ingame = false;
    restart();
    sig = "";
    
  }
  else if (check[0] == 'E')
  {
    ingame = false;
    initialize();
    sig = "";
  }
  else if (check[0] != 'S')
  {sig = "";}
}



void choose_action()
{
  if (ingame == true)
  {
    if (action == 0)
    {
      forward();
    }
    else if (action == 1)
    {
      left();
    }
    else if (action == 2)
    {
      right();
    }
  }
  else if (ingame == false)
  {
    analogWrite(R_motor,0);
    analogWrite(L_motor,0);
    digitalWrite(RF,LOW);
    digitalWrite(RB,LOW);
    digitalWrite(LF,LOW);
    digitalWrite(LB,LOW);
  }
}

void restart(){
  //back();
  //delay(500);
  //turn();
  //delay(1500);
  initialize();
}
