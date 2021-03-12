
#include <winsock2.h>//winsock的头文件
#include <ws2tcpip.h>//sockaddr_in6的头文件
#include <iostream>
using  namespace  std;

//指定动态库的lib文件
#pragma comment(lib,"ws2_32.lib")


//TCP客户端
int main() {

	//初始化winsock2.2相关的动态库
	WSADATA  wd;//获取socket相关信息
	if (WSAStartup(MAKEWORD(2, 2), &wd) != 0)//0表示成功
	{
		cout << "WSAStartup  error:" << WSAGetLastError() << endl;
		return 0;
	}

	//1.创建TCP   socket , 流式套接字, AF_INET改为AF_INET6
	SOCKET   s = socket(AF_INET6, SOCK_STREAM, IPPROTO_TCP);
	if (s == INVALID_SOCKET) {
		cout << "socket  error:" << WSAGetLastError() << endl;
		return 0;
	}

	//2.链接服务端
	sockaddr_in6   addr;//不建议使用sockaddr，建议用sockaddr_in
	memset(&addr, 0, sizeof(sockaddr_in6)); //重点，否则就10049错误
	addr.sin6_port = htons(8890);//网络字节序 

								 //addr.sin6_addr = inet_addr("127.0.0.1");//绑定指定地址， ipv4
	inet_pton(AF_INET6, "0:0:0:0:0:0:0:1", &addr.sin6_addr);//绑定指定地址， ipv6  格式 /*"fe80::ce6:3cc:f93a:4203%5",*/

	addr.sin6_family = AF_INET6; //地址族
	int len = sizeof(sockaddr_in6);//结构大小改变sizeof(sockaddr_in6)

	if (connect(s, (sockaddr*)&addr, len) == SOCKET_ERROR) {
		cout << "connect  error:" << WSAGetLastError() << endl;
		return 0;
	}

	//3.接受发送消息
	int  ret = 0;
	do {
		//接受客户端的消息
		char buf[64] = { '\0' };
		ret = recv(s, buf, 64, 0);//把flag置0

		char ipbuf[100] = { 0 };
		inet_ntop(AF_INET6, (LPVOID)&addr.sin6_addr, ipbuf, 100);

		cout << "recv	" << ipbuf << ":    " << buf << endl;// inet_ntoa转换为IP字符串
		char *str = "I am Client!";
		//发送
		ret = send(s, str, strlen(str), 0);

		Sleep(1000);
	} while (ret != SOCKET_ERROR &&  ret != 0);


	//4.关闭套接字
	closesocket(s);

	//清理winsock环境
	WSACleanup();


	return   0;
}

