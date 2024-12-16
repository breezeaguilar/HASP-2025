#include "CRC.h"
#include <stdint.h>

CRC::CRC() {
  machineEndianness = getEndianness();
  generator = 0x1021;
  setupTable();
}

void CRC::setGenerator(uint16_t nGenerator) {
  generator = nGenerator;
  setupTable();
}

uint16_t CRC::getGenerator() {
  return generator;
}

//implementation of CRC-16 checksum
//Endianess of encode and decode system matters for ordering of data*
uint16_t CRC::compute_CRC16(uint8_t* bytes, int size) {
    uint16_t crc = 0;
    uint8_t pos;

    for (auto i = 0; i < size; i++) {
      // XOR-in next input byte into MSB of crc, that's our new intermediate dividend
      pos = (uint8_t)((crc >> 8) ^ bytes[i]);
      // Shift out the MSB used for division per lookuptable and XOR with the remainder
      crc = ((crc << 8) ^ byteTable[pos]);
    }

    return crc;
}

void CRC::setupTable() {
  uint16_t currByte = 0;

  for (int i = 0; i < 256; i++) {
    currByte = (uint16_t) i << 8; // shift value of i into MSB
    for (int i = 0; i < 8; i++) // iterate over all 256 values
    {
      if ((currByte & 0x8000) != 0) // test for MSB = bit 15 
      {
        currByte = (currByte << 1) ^ generator; // crc remainder
      }
      else
      {
        currByte <<= 1;
      }
    }
    byteTable[i] = currByte; // put precomputed value into table
  }
}

bool CRC::getEndianness() {
  uint16_t num[] = {0x0102}; // two byte value
  //if little endian, LSB will be stored in Least memory Byte cell.(reversed)
  //if big endian, LSB will be stored in Largest memory Byte cell.
  return ((uint8_t*)num)[0] == 0x02 ? true : false;
}