#ifndef CRC_H
#define CRC_H

#include <stdint.h>

class CRC {
  private:
    uint16_t byteTable[256]; //table of pre-computed crc values
    uint16_t generator; // generator polynomial
    bool machineEndianness; // native machine endianness

    /**
     * precompute the table of crc values. generator polynomial must
     * be set prior to calling. uninitialized generator variable will 
     * lead to undefined behavior.
     */
    void setupTable();
  

  public:
  /**
   * default constructor
   * generator poly is 0x1021
   */
    CRC();

    /**
     * set the generator polynomial. recomputes the byteTable.
     * 
     * @param nGenerator the new generator polynomial
     */
    void setGenerator(uint16_t nGenerator);

    /**
     * get the generator polynomial
     * 
     * @return generator polynomial
     */
    uint16_t getGenerator();

    /**
     * get the endianess of the current system. 
     * @return: 
     *          - true if current system is little endian
     *          - false if current system is big endian
     */
    bool getEndianness();

    /**
     * compute the crc 16 checksum of an array of bytes with specified size.
     * 
     * @param bytes pointer to array of bytes
     * @param size size of byte array.
     * 
     * @return checksum value of the byte array
     */
    uint16_t compute_CRC16(uint8_t* bytes, int size);


};

#endif