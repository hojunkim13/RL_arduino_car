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

char a_left[6] = {0};
char a_right[6] = {0};
char check[1];
int action_left=0;
int action_right=0;
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
// Sense Distance
Sensing();
delay(100);
// Send to PC  
send_data();

read_data();
choose_action();
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
    sig.substring(1,5).toCharArray(a_left,6);
    sig.substring(5,9).toCharArray(a_right,6);
    action_left = atoi(a_left);
    action_right = atoi(a_right);
    sig = "";
  }
  else if (check[0] == 'R')
  {
    back();
    delay(500);
    turn();
    delay(1500);
    initialize();
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
    if (action_left < 0)
    {
      digitalWrite(LF,LOW);
      digitalWrite(LB,HIGH); 
    }
    else if (action_left > 0)
    {
      digitalWrite(LF,HIGH);
      digitalWrite(LB,LOW);
    }
    if (action_right < 0)
    {
      digitalWrite(RF,LOW);
      digitalWrite(RB,HIGH); 
    }
    else if (action_right > 0)
    {
      digitalWrite(RF,HIGH);
      digitalWrite(RB,LOW);
    }
    analogWrite(R_motor, action_right);
    analogWrite(L_motor, action_left);
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
