#!/usr/bin/python3
# -*- coding: Utf-8 -*-
# Fichier : parser.py

import binascii, struct

SERVER_QUEUE = []
CLIENT_QUEUE = []

def h_NOP(data):
    pass
    #return data

def h_Timer1(data):
    #print("deplacement -> %s" %(data.encode("hex")))
    return data[1:]

def h_Timer2(data):
    #print("deplacement -> %s" %(data.encode("hex")))
    return data[1:]

def h_Movement(data):  # Server
    #print("deplacement -> %s" %(data.encode("hex")))
    return data[4:]

def h_Attack(data):  # Client
    entityNumber = struct.unpack("H", data[1:3])[0]
    print("Attaque l'entite identifie %i" %(entityNumber))
    return data[5:]

def h_Spawn(data):  # Server
    entityNumber = struct.unpack("H", data[1:3])[0]
    print("spawn -> %i" %(entityNumber))
    return data[3:]

def h_GoToLoot(data):  # Client
    print("va loot -> %s" %(data.encode("hex")))
    return data[2:]

def h_InfoLoot(data):  # Server
    bytesToProcess = data
    print("Ouvre le loot -> %s" %(data.encode("hex")))
    return data[23:]

def h_TakeItem(data):  # Client
    itemNumber   = struct.unpack("B", data[1])[0]
    itemQuantity = struct.unpack("I", data[2:6])[0]
    print("Ramasse l'item -> item #%i*%s" %(itemNumber, itemQuantity))
    return data[6:]

def h_DropItem(data):  # Client
    itemNumber   = struct.unpack("B", data[1])[0]
    itemQuantity = struct.unpack("I", data[2:6])[0]
    print("Jete l'item item #%i*%s" %(itemNumber, itemQuantity))
    return data[6:]

def h_UseItem(data):  # Client
    itemNumber = struct.unpack("B", data[1])[0]
    print("Utilise l'item -> %s" %(data[1].encode("hex")))
    return data[6:]

def h_UseEnvironment(data):  # Client
    entityNumber = struct.unpack("H", data[1:3])[0]
    print("Utilise l'environnement identifie %i" %(entityNumber))
    return data[9:]

def h_UseLiving(data):  # Client
    entityNumber = struct.unpack("H", data[1:3])[0]
    print("Utilise l'entite vivante identifie %i" %(entityNumber))
    return data[9:]

def h_LookEnvironment(data):  # Client
    entityNumber = struct.unpack("H", data[1:3])[0]
    print("Regarde l'environnement identifie %i -> %s" %(entityNumber, data.encode("hex")))
    return data[9:]

def h_LookLiving(data):  # Client
    entityNumber = struct.unpack("H", data[1:3])[0]
    print("Regarde l'entite vivante identifie %i" %(entityNumber))
    return data[9:]

def h_HpDecrease(data):  # Server
    entityNumber = struct.unpack("H", data[1:3])[0]
    damage = struct.unpack("H", data[3:5])[0]
    print("Entity %i took %i damages -> %s" %(entityNumber, damage, data[5:7].encode("hex")))
    return data[7:]

def h_HpIncrease(data):  # Server
    entityNumber = struct.unpack("H", data[1:3])[0]
    damage = struct.unpack("H", data[3:5])[0]
    print("Entity %i gain %i hp -> %s" %(entityNumber, damage, data[5:7].encode("hex")))
    return data[6:]

def h_StatChange(data):  # Server
    #print("StatChange -> %s" %(data[:7].encode("hex")))
    return data[6:]

def h_dialogChoice(data):  # Client
    entityNumber = struct.unpack("H", data[1:3])[0]
    choice = struct.unpack("I", data[3:7])[0]
    print("Choix #%i lors du dialog avec l'entite %i -> %s" %(choice, entityNumber, data.encode('hex')))
    return data[7:]

def h_Farming(data):  # Client
    entityNumber = struct.unpack("H", data[1:3])[0]
    print("Va recolter l'entite identifie %i" %(entityNumber))
    return data[3:]

handlers = {
    0x0105: h_Timer1,
    0x0e01: h_Timer2,
    0x1a01: h_Timer2,
    0x3c01: h_Timer2,
    0x0204: h_Movement,
    0x2805: h_Attack,
    0x6103: h_Spawn,
    0x1902: h_GoToLoot,
    0x1717: h_InfoLoot,
    0x1706: h_TakeItem,
    0x1606: h_DropItem,
    0x3007: h_HpIncrease,
    0x2f07: h_HpDecrease,
    0x3106: h_StatChange,
    0x1f02: h_UseItem,
    0x1009: h_UseEnvironment,
    0x1c05: h_UseLiving,
    0x1b05: h_LookEnvironment,
    0x0505: h_LookLiving,
    0x1d07: h_dialogChoice,
    0x1503: h_Farming,
}

def parse(data, origin):
    if origin:
        while data:
            #data = binascii.hexlify(data).decode('ascii')
            packet_id = struct.unpack(">H", data[0:2])[0]

            if packet_id not in handlers and origin == 'client' and True:
                print("[%s] %s" %(origin, data.encode('hex')))
            #print(hex(packet_id), data)
            data = handlers.get(packet_id, h_NOP)(data[2:])


if __name__ == "__main__":
    print("Hello world!")
