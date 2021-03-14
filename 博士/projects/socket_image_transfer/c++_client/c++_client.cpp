#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <WinSock2.h>
#include <cv.h>
#include <highgui.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <stdio.h>
#include <iostream>
#include <fstream>
using namespace cv;
using namespace std;
#pragma comment(lib, "ws2_32.lib")
#define FRAME_WIDTH         640
#define FRAME_HEIGHT        480


int main() {
	WSADATA wsaData;
	WSAStartup(MAKEWORD(2, 2), &wsaData);
	SOCKET sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
	sockaddr_in sockAddr;
	memset(&sockAddr, 0, sizeof(sockAddr));
	sockAddr.sin_family = PF_INET;
	sockAddr.sin_addr.s_addr = inet_addr("172.18.32.31");
	sockAddr.sin_port = htons(2019);

	if (connect(sock, (SOCKADDR*)&sockAddr, sizeof(SOCKADDR)) < 0)
		printf("ERROR connecting");
	else
		printf("SUCCESS connecting");
	
	int IM_HEIGHT, IM_WIDTH, n, counter = 0;

	while (true)
	{
		counter = counter + 1;
		Mat cameraFeed;
		if (counter % 2 == 1) {
			cameraFeed = Mat::ones(FRAME_HEIGHT, FRAME_WIDTH, CV_8UC3);
		}
		else
			cameraFeed = Mat::zeros(FRAME_HEIGHT, FRAME_WIDTH, CV_8UC1);
		int height = cameraFeed.rows;
		int width = cameraFeed.cols;

		Mat cropped = Mat(cameraFeed, Rect(width / 2 - width / 7,
			height / 2 - height / 9,
			2 * width / 7, 2 * height / 7));
		cameraFeed = cropped;

		IM_HEIGHT = FRAME_HEIGHT;
		IM_WIDTH = FRAME_WIDTH;

		resize(cameraFeed, cameraFeed, Size(IM_WIDTH, IM_HEIGHT));

		int imgSize = cameraFeed.total()*cameraFeed.elemSize();
		n = send(sock, (char*)cameraFeed.data, imgSize, 0);
		if (n < 0) printf("ERROR writing to socket");
	}
	return 0;
}