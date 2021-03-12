#include <winsock2.h>//winsock的头文件
#include <ws2tcpip.h>//sockaddr_in6的头文件
#include <iostream>

using  namespace  std;

//指定动态库的lib文件
#pragma comment(lib,"ws2_32.lib")

//TCP服务端IPv6版
int main() {

	//初始化winsock2.2相关的动态库
	WSADATA  wd;//获取socket相关信息
	if (WSAStartup(MAKEWORD(2, 2), &wd) != 0)//0表示成功
	{
		cout << "WSAStartup  error:" << WSAGetLastError() << endl;
		return 0;
	}

	//1.创建TCP   socket , 流式套接字   ， AF_INET改为AF_INET6
	SOCKET   s = socket(AF_INET6, SOCK_STREAM, IPPROTO_TCP);
	if (s == INVALID_SOCKET) {
		cout << "socket  error:" << WSAGetLastError() << endl;
		return 0;
	}

	//2.绑定socket到一个IP地址和端口，  sockaddr_in改为sockaddr_in6
	sockaddr_in6   addr;//不建议使用sockaddr，建议用sockaddr_in
	memset(&addr, 0, sizeof(sockaddr_in6)); //重点，否则就10049错误
	addr.sin6_port = htons(8890);//网络字节序
	addr.sin6_family = AF_INET6; //地址族AF_INET改为AF_INET6

								 //addr.sin6_addr = in6addr_any;//  把INADDR_ANY替换为in6addr_any，表示绑定任意ip 
								 //addr.sin6_addr = inet_addr("127.0.0.1");//绑定指定地址， ipv4
	inet_pton(AF_INET6, "0:0:0:0:0:0:0:1", &addr.sin6_addr);//绑定指定地址， ipv6 格式 /*"fe80::ce6:3cc:f93a:4203%5",*/

	int len = sizeof(sockaddr_in6);//地址结构大小改变 sizeof(sockaddr_in6)
	if (bind(s, (sockaddr *)&addr, len) == SOCKET_ERROR) {
		cout << "bind  error:" << WSAGetLastError() << endl;
		return 0;
	}

	//3.监听, 5代表正在等待完成相应的TCP三路握手过程的队列长度
	if (listen(s, 5) == SOCKET_ERROR) {
		cout << "listen  error:" << WSAGetLastError() << endl;
		return 0;
	}

	//4.接受客户端请求，并且返回和客户端通讯的套接字，sockaddr_in改为sockaddr_in6
	sockaddr_in6   addrClient;// 保存客户端IP地址端口 
	memset(&addrClient, 0, sizeof(sockaddr_in6));
	len = sizeof(sockaddr_in6);//地址结构大小改变 sizeof(sockaddr_in6)
	SOCKET c = accept(s, (sockaddr*)&addrClient, &len);//成功返回套接字
	if (c == INVALID_SOCKET) {
		cout << "accept  error:" << WSAGetLastError() << endl;
		return 0;
	}

	//5.发送，接受消息
	int  ret = 0;
	do {
		char *str = "I am  Server!";
		//向客户端发送数据,不能用监听套接字s，而应该用accept返回的套接字c
		ret = send(c, str, strlen(str), 0);//把flag置0

										   //接受客户端的消息
		char buf[64] = { '\0' };
		ret = recv(c, buf, 64, 0);//把flag置0

		char ipbuf[100] = { 0 };
		inet_ntop(AF_INET6, (LPVOID)&addrClient.sin6_addr, ipbuf, 100);

		cout << "recv	" << ipbuf << ":    " << buf << endl;// inet_ntoa转换为IP字符串
	} while (ret != SOCKET_ERROR &&  ret != 0);//对方关闭，返回0 ，错误返回SOCKET_ERROR


											   //6.关闭套接字
	closesocket(s);


	//清理winsock环境
	WSACleanup();


	return   0;
}

