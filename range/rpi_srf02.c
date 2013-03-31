// SRF02 example coder for the Raspberry pi
//
// This code will work for the SRF02/ 10/ 235 and 08.
// It will take a ranging from the module and print results
// to the screen.
//
// By James Henderson, 2012. 
// Hacked about slightly by Dav

#include <stdio.h>
#include <stdlib.h>
#include <linux/i2c-dev.h>
#include <fcntl.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <unistd.h>

int main(int argc, char **argv)
{
  
  int fd;                            // File description
  char *fileName = "/dev/i2c-1";                // Name of the port we will be using
  int i; 
  FILE *fdOut; // handle to output file
  char *outFileName = "rangeOutput";
  struct timeval t;
  int address = 0x70;                    // Address of the SRF02 shifted right one bit
  unsigned char buf[10];                    // Buffer for data being read/ written on the i2c bus
  unsigned int range;
  unsigned int minRange;
  
  if ((fd = open(fileName, O_RDWR)) < 0) {          // Open port for reading and writing
    printf("Failed to open i2c port\n");
    exit(1);
  }
  
  if (ioctl(fd, I2C_SLAVE, address) < 0) {          // Set the port options and set the address of the device we wish to speak to
    printf("Unable to get bus access to talk to slave\n");
    exit(1);
  }
  // open our log file and print a header line
  fdOut = fopen(outFileName, "w");
  fprintf(fdOut, "time,range,min_range\n");

  for (i=0;i<300;i++) {
    buf[0] = 0;                          // Commands for performing a ranging
    buf[1] = 81;
  
    if ((write(fd, buf, 2)) != 2) {                // Write ping command to the i2c port
      printf("Error writing to i2c slave\n");
      exit(1);
    }
    usleep(80000);                        // This sleep waits for the ping to come back
    buf[0] = 0;                          // This is the register we wish to read from
    if ((write(fd, buf, 1)) != 1) {                // Send the register to read from
      printf("Error writing to i2c slave\n");
      exit(1);
    }
    if (read(fd, buf, 6) != 6) {                // Read back data into buf[]
      printf("Unable to read from slave\n");
      exit(1);
    }
    else {
      // buf[0] software version. If this is 255, then the ping has not yet returned
      // buf[1] unused
      // buf[2] high byte range
      // buf[3] low byte range
      // buf[4] high byte minimum auto tuned range
      // buf[5] low byte minimum auto tuned range

      range = (buf[2] <<8) + buf[3];      // Calculate range as a word value
      minRange = (buf[4] <<8) + buf[5];   // Calculate range as a word value
    }

    printf("Range was: %u. Minimum: %u\n", range, minRange);
    gettimeofday(&t, NULL);
    fprintf(fdOut, "%u.%06d,%u,%u\n", t.tv_sec, t.tv_usec, range, minRange);

    usleep(100000); // wait another 100ms and perform another ranging
  }   // end for 300
  close(fd);
  fclose(fdOut);
  return 0;
}

