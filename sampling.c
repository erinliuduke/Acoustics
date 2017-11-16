#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <ctype.h>
#include <math.h>
#include <unistd.h>

#include "pmd.h"
#include "usb_1608G.h"

#define MAX_COUNT		(0xffff)
#define FALSE 0
#define TRUE 1

int main (int argc, char **argv) {
	libusb_device_handle *udev = NULL;

	double voltage;
	double frequency, duty_cycle;
	float temperature;
	float table_AIN[NGAINS_1608G][2];
	float table_AO[NCHAN_AO_1608GX][2];
	ScanList list[NCHAN_1608G];

	int ch;
	int i, j, m, k, nchan, repeats;
	int nread;
	int nScans = 0;
	uint8_t input;
	int temp, ret;
	uint8_t options;
	char serial[9];
	uint32_t period;
	uint16_t version;
	uint16_t status;
	int usb1608GX_2AO = FALSE;
	int flag;
	int transferred;            // number of bytes transferred
	uint16_t value, data;
	uint16_t *sdataIn;          // holds 16 bit unsigned analog input data
	uint16_t sdataOut[512];     // holds 16 bit unsigned analog output data

	uint8_t mode, gain, channel;

	udev = NULL;

	ret = libusb_init(NULL);

	if (ret < 0) {
		perror("fail to initialize libsusb");
		exit(1);
	}

	if ((udev = usb_device_find_USB_MCC(USB1608G_V2_PID, NULL))) {
		printf("found USB 1608G\n");
		usbInit_1608G(udev, 2);
	}
	else if ((udev = usb_device_find_USB_MCC(USB1608G_PID, NULL))) {
		printf("found USB 1608G\n");
		usbInit_1608G(udev, 1);
	}
	else {
		printf("fail to find the device\n");
		return 0;
	}

	usbBuildGainTable_USB1608G(udev, table_AIN);

	printf("start sampling\n");
	usbAInScanStop_USB1608G(udev);
	usbAInScanClearFIFO_USB1608G(udev);
	mode = SINGLE_ENDED;
	gain = BP_10V;
	nchan = 3;
	nScans = 10000;
	frequency = 250000;


	for (channel = 0; channel < nchan; channel++) {
		list[channel].range = gain;
		list[channel].mode = mode;
		list[channel].channel = channel;
	}

	list[nchan-1].mode |= LAST_CHANNEL;

	usbAInConfig_USB1608G(udev, list);

	if ((sdataIn = malloc(2*nchan*nScans)) == NULL) {
		perror("cannot allocate memory for sdataIn");
		break;
	}

	usbAInScanStart_USB1608G(udev, nScans, 0, frequency, 0x0);
	ret = usbAInScanRead_USB1608G(udev, nScans, nchan, sdataIn, 20000, 0);
	for (i = 0; i < nScans; i++) {
		printf("%6d", i);
		for (j = 0; j < nchan; j++) {
			gain = list[j].range;
			k = i*nchan + j;
			data = rint(sdataIn[k]*table_AIN[gain][0] + table_AIN[gain][1]);
			printf(", %8.4lf", volts_USB1608G(gain, data));
		}
		printf("\n");
	}
	free(sdataIn);

}