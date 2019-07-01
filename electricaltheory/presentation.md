# Electrical Theory

This document will cover some of the basics of electricity and Electrical 
Engineering with the use of a traffic light. To wire up a traffic light, 
requires knowledge of AC and DC circuits, wiring standards, wiring gauge, 
and relays. 

This document is designed to function as a presentation. 

## Topics
* Alternating Current (AC) and Direct Current (DC)
* Series and Parallel Circuits 
* Relays
* Wire Gauge and Colors

----

## Alternating Current (AC) and Direct Current (DC)

### Alternating Current (AC)

* Eletrons move back and forth (alternate), like liquid shaking in a bottle.
* Has lower losses over longer distances.
* Varies by country and continents
* Typically 120, 240, or higher voltage
* Can be deadly, regardless of amperage
* Normally used in residential and commercial buildings
* Examples: stove, refrigerator

### Direct Current (DC)

* Electrons flow in one direction, like a one way street.
* Has high losses over long distances
* Mostly consistent in other countries and continents
* Typically 3.3, 5, 9, or 12 Volts
* Generally safe, but can be deadly at high amperage
* Examples: cars, Raspberry Pi, electronics

### Does it use AC or DC Voltage?

* Doorbell
* Cell phone
* Stove
* Computer 
* Ceiling fan
* Lamp
* Television
* Router

### Traffic Light Implementation

* Identify AC Components
* Identify DC Components

----

## Series and Parallel Circuits

### Series Circuit

* First light is connected to second, second connected to third, etc.
* If one light is defective, then other lights will be inoperable or malfunction.
* Example: Christmas Lights 

### Parallel Circuit

* All lights connected to common source
* If one light is defective, then other lights still operate.
* Example: Brake Lights

### Factors for Series vs Parallel

* Safety
* Cost
* Wiring

### Traffic Light Implementation

* Discussion

----

## Relays

* Fancy name for "electrical controlled switch"
* Used for controlling different current types
* Used for controlling different amperages
* Run current from one circuit, to energize another circuit

### NO (Naturally Open) and NC (Naturally Closed) 

* Naturally Open relays complete the circuit when a signal is received.
* Naturally Closed relays complete the circuit unless a signal is received.

### Common Relay Types: SPST, SPDT, DPST, DPDT

* Single Pole, Single Throw (headlight relay)
* Single Pole, Double Throw (turn signal)
* Double Pole, Single Throw (2 SPST controlled by one switch)
* Double Pole, Double Throw (motor)

### Traffic Light Implementation

* Used by the controller to switch the signals on and off
* Controller is 5VDC, lights are 120VAC
* Controller is 5VDC and can switch 5VDC
* Reach relay is SPDT

----

## Wire Gauge and Colors

* Wire colors are governed by the NEC (National Electrical Code)
* Color indicates purpose
* Color notes type of circuit (AC or DC)

### AC Wiring

* Black = Hot/Positive
* White = Neutral
* Green/Bare = Ground
* Red = Hot/Postive (Phase 2)
* White with Black Tape = Hot/Positive

### DC Wiring 

* Red = Positive
* Black = Negative

### Traffic Light Implementation

* Red = Red Signal
* Yellow = Yellow Signal
* Black/Brown = Green Signal
* White = Neutral
* Green not used for Green Signal
