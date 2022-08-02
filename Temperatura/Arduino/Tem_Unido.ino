//Definimos los paquetes para sensor Ds18B20
#include <OneWire.h>
#include <DallasTemperature.h>
const int pinDatosDQ = 9; // Pin donde se conecta el bus 1-Wire

//Definimos los paquetes para sensor digital  DHT
#include "DHT.h"
#define DHTPIN 2          // Pin donde está conectado el sensor
#define DHTTYPE DHT22     // Sensor DHT22
DHT dht(DHTPIN, DHTTYPE);
 
// Instancia a las clases OneWire y DallasTemperature
OneWire oneWireObjeto(pinDatosDQ);
DallasTemperature sensorDS18B20(&oneWireObjeto);

//Sensor de sonido
const int Trigger = 5;   //Pin digital 5 para el Trigger del sensor
const int Echo = 6;      //Pin digital 6 para el Echo del sensor





//Sensor de Analogico Tmp36
//Creamos una variable de tipo entero
int lec_A0 = 0;
int lec_A1 = 0;
int lec_A2 = 0;
int lec_A3 = 0;
int lec_A4 = 0;

//Creamos una variable de tipo flotante
float temp_A0 = 0.0;
float temp_A1 = 0.0;
float temp_A2 = 0.0;
float temp_A3 = 0.0;
float temp_A4 = 0.0;





void setup() {
    // Iniciamos la comunicación serie
    Serial.begin(9600);
    // Iniciamos el Ds18B20-Dht-Sonido
    sensorDS18B20.begin(); 
    dht.begin();
    
    pinMode(Trigger, OUTPUT);      //pin como salida
    pinMode(Echo, INPUT);          //pin como entrada
    digitalWrite(Trigger, LOW);    //Inicializamos el pin con 0
}
 
void loop() {
    //Mandamos comandos para toma de temperatura a los sensores
    sensorDS18B20.requestTemperatures();
 
    // Leemos y mostramos los datos de los sensores DS18B20
    Serial.print(sensorDS18B20.getTempCByIndex(0)); //en C
    Serial.print(",");

    float h = dht.readHumidity();          //Leemos la Humedad
    float t = dht.readTemperature();       //Leemos la temperatura en grados Celsius
    float f = dht.readTemperature(true);   //Leemos la temperatura en grados Fahrenheit

    Serial.print(t);
    Serial.print(",");

    long ts;         //timepo que demora en llegar el eco
    long ds;         //distancia en centimetros
  
    digitalWrite(Trigger, HIGH);
    delayMicroseconds(10);          //Enviamos un pulso de 10us
    digitalWrite(Trigger, LOW);
    
    ts = pulseIn(Echo, HIGH);    //obtenemos el ancho del pulso
    ds = ts/59;                   //escalamos el tiempo a una distancia en cm
    Serial.print(ds);
    Serial.print(",");
    
  //Tomamos la lectura analógica del pin al cual conectamos
  //la señal de nuestro sensor
  lec_A0 = analogRead(0);
  lec_A1 = analogRead(1);
  lec_A2 = analogRead(2);
  lec_A3 = analogRead(3);
  lec_A4 = analogRead(4);


  //Obtenemos la temperatura con la siguiente formula:
  temp_A0 = TempFunction(lec_A0);
  temp_A1 = TempFunction(lec_A1);
  temp_A2 = TempFunction(lec_A2);
  temp_A3 = TempFunction(lec_A3);
  temp_A4 = TempFunction(lec_A4);
  
  //Imprimimos por monitor serie la temperatura en celcius 
  Serial.print(temp_A0);
  Serial.print(",");
  Serial.print(temp_A1);
  Serial.print(",");
  Serial.print(temp_A2);
  Serial.print(",");
  Serial.print(temp_A3);
  Serial.print(",");
  Serial.println(temp_A4);
  delay(1000);
}
//Serial.println("proceso culminado imprime Ds18B20, Dht, Distancia,A0,A1,A2,A3,A4");

float TempFunction(int lect){
  return ( lect * (500.0 / 1023.0) ) - 50.0;
}
