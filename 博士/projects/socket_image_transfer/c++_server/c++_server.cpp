#include <winsock2.h>//winsock��ͷ�ļ�
#include <ws2tcpip.h>//sockaddr_in6��ͷ�ļ�
#include <iostream>

using  namespace  std;

//ָ����̬���lib�ļ�
#pragma comment(lib,"ws2_32.lib")

//TCP�����IPv6��
int main() {

	//��ʼ��winsock2.2��صĶ�̬��
	WSADATA  wd;//��ȡsocket�����Ϣ
	if (WSAStartup(MAKEWORD(2, 2), &wd) != 0)//0��ʾ�ɹ�
	{
		cout << "WSAStartup  error:" << WSAGetLastError() << endl;
		return 0;
	}

	//1.����TCP   socket , ��ʽ�׽���   �� AF_INET��ΪAF_INET6
	SOCKET   s = socket(AF_INET6, SOCK_STREAM, IPPROTO_TCP);
	if (s == INVALID_SOCKET) {
		cout << "socket  error:" << WSAGetLastError() << endl;
		return 0;
	}

	//2.��socket��һ��IP��ַ�Ͷ˿ڣ�  sockaddr_in��Ϊsockaddr_in6
	sockaddr_in6   addr;//������ʹ��sockaddr��������sockaddr_in
	memset(&addr, 0, sizeof(sockaddr_in6)); //�ص㣬�����10049����
	addr.sin6_port = htons(8890);//�����ֽ���
	addr.sin6_family = AF_INET6; //��ַ��AF_INET��ΪAF_INET6

								 //addr.sin6_addr = in6addr_any;//  ��INADDR_ANY�滻Ϊin6addr_any����ʾ������ip 
								 //addr.sin6_addr = inet_addr("127.0.0.1");//��ָ����ַ�� ipv4
	inet_pton(AF_INET6, "0:0:0:0:0:0:0:1", &addr.sin6_addr);//��ָ����ַ�� ipv6 ��ʽ /*"fe80::ce6:3cc:f93a:4203%5",*/

	int len = sizeof(sockaddr_in6);//��ַ�ṹ��С�ı� sizeof(sockaddr_in6)
	if (bind(s, (sockaddr *)&addr, len) == SOCKET_ERROR) {
		cout << "bind  error:" << WSAGetLastError() << endl;
		return 0;
	}

	//3.����, 5�������ڵȴ������Ӧ��TCP��·���ֹ��̵Ķ��г���
	if (listen(s, 5) == SOCKET_ERROR) {
		cout << "listen  error:" << WSAGetLastError() << endl;
		return 0;
	}

	//4.���ܿͻ������󣬲��ҷ��غͿͻ���ͨѶ���׽��֣�sockaddr_in��Ϊsockaddr_in6
	sockaddr_in6   addrClient;// ����ͻ���IP��ַ�˿� 
	memset(&addrClient, 0, sizeof(sockaddr_in6));
	len = sizeof(sockaddr_in6);//��ַ�ṹ��С�ı� sizeof(sockaddr_in6)
	SOCKET c = accept(s, (sockaddr*)&addrClient, &len);//�ɹ������׽���
	if (c == INVALID_SOCKET) {
		cout << "accept  error:" << WSAGetLastError() << endl;
		return 0;
	}

	//5.���ͣ�������Ϣ
	int  ret = 0;
	do {
		char *str = "I am  Server!";
		//��ͻ��˷�������,�����ü����׽���s����Ӧ����accept���ص��׽���c
		ret = send(c, str, strlen(str), 0);//��flag��0

										   //���ܿͻ��˵���Ϣ
		char buf[64] = { '\0' };
		ret = recv(c, buf, 64, 0);//��flag��0

		char ipbuf[100] = { 0 };
		inet_ntop(AF_INET6, (LPVOID)&addrClient.sin6_addr, ipbuf, 100);

		cout << "recv	" << ipbuf << ":    " << buf << endl;// inet_ntoaת��ΪIP�ַ���
	} while (ret != SOCKET_ERROR &&  ret != 0);//�Է��رգ�����0 �����󷵻�SOCKET_ERROR


											   //6.�ر��׽���
	closesocket(s);


	//����winsock����
	WSACleanup();


	return   0;
}

