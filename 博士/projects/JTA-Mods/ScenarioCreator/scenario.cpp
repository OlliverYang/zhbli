#define _CRT_SECURE_NO_WARNINGS
#define _SILENCE_TR2_SYS_NAMESPACE_DEPRECATION_WARNING

#include "scenario.h"
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include <direct.h>
#include <stdlib.h>
#include "export.h"
#include <cv.h>
#include <highgui.h>
#include <direct.h>
#include <io.h>
#include <cmath>
#include "math.h"
#include <opencv2/imgproc/imgproc.hpp>
#pragma comment(lib, "ws2_32.lib")
namespace fs = std::experimental::filesystem;

using namespace std::tr2::sys;
using namespace cv;


int logLenght = 100;
char *logString = (char*)malloc(logLenght * sizeof(char));

FILE *f;
const char *filesPath = "JTA-Scenarios\\";
char fileName[20] = "None";
int nFiles = 0, currentFile = 1;

std::string statusText;
DWORD statusTextDrawTicksMax;
bool statusTextGxtEntry;

bool firstTime = true;
bool menuActive = false;
bool fly = false;

//menu commands
bool	bUp = false,
bDown = false,
bLeft = false,
bRight = false,
bEnter = false,
bBack = false,
bQuit = false;
bool stopCoords = false;

Vector3 playerCoords;
Vector3 fixCoords;
Vector3 goFrom, goTo;
Vector3 A, B, C;
Vector3 TP1, TP2, TP1_rot, TP2_rot;

//cam variables
Cam activeCam;
Vector3 camCoords, camRot;
bool camLock = true;
bool camMoving = false;

//menu parameters
float mHeight = 9, mTopFlat = 60, mTop = 36, mLeft = 3, mTitle = 5;
int activeLineIndexMain = 0;
bool visible = false;

//menu peds parameters
int activeLineIndexPeds = 0;
int nPeds = 1;
int currentBehaviour = 0;
bool group = false;
const int nMaxPeds = 50;
const int numberTaks = 9;


LPCSTR tasks[numberTaks] = {
	"SCENARIO",
	"STAND",
	"PHONE",
	"COWER",
	"WANDER",
	"CHAT",
	"COMBAT",
	"COVER",
	"MOVE"
};

bool subMenuActive = false;

//behaviour params
int maxNumber = 1000000;
const int nScenario = 14;
float speed = 1;

struct {
	LPCSTR  text;
	int param;
} paramsLines[10] = {
	{ "Task Time", 1000000 },
	{ "Type", 0 },
	{ "Radius", 20 },
	{ "Minimal Lenght", 1 },
	{ "Time between Walks", 1 },
	{ "Spawning Radius", 1 }
};

static char scenarioTypes[nScenario][40]{
	"NEAREST",
	"RANDOM",
	"WORLD_HUMAN_MUSICIAN",
	"WORLD_HUMAN_SMOKING",
	"WORLD_HUMAN_BINOCULARS",
	"WORLD_HUMAN_CHEERING",
	"WORLD_HUMAN_DRINKING",
	"WORLD_HUMAN_PARTYING",
	"WORLD_HUMAN_PICNIC",
	"WORLD_HUMAN_STUPOR",
	"WORLD_HUMAN_PUSH_UPS",
	"WORLD_HUMAN_LEANING",
	"WORLD_HUMAN_MUSCLE_FLEX",
	"WORLD_HUMAN_YOGA"
};

//wped
typedef struct wPed {
	Ped ped;
	bool goingTo = true;
	Vector3 from, to;
	int stopTime;
	int timeFix = -1;
	float speed;
} wPed;

wPed wPeds[200];
int nwPeds = 0;

int activeLineIndexCamera = 0;
int activeLineIndexPlace = 0;
int activeLineIndexTime = 0;
int activeLineIndexWeather = 0;
int activeLineIndexSubmenu = 0;
int activeLineIndexFile = 0;
bool wind = false;
const double pi = std::acos(-1);

void update_status_text()
{
	if (GetTickCount() < statusTextDrawTicksMax)
	{
		UI::SET_TEXT_FONT(0);
		UI::SET_TEXT_SCALE(0.55f, 0.55f);
		UI::SET_TEXT_COLOUR(255, 255, 255, 255);
		UI::SET_TEXT_WRAP(0.0, 1.0);
		UI::SET_TEXT_CENTRE(1);
		UI::SET_TEXT_DROPSHADOW(0, 0, 0, 0, 0);
		UI::SET_TEXT_EDGE(1, 0, 0, 0, 205);
		if (statusTextGxtEntry)
		{
			UI::_SET_TEXT_ENTRY((char *)statusText.c_str());
		}
		else
		{
			UI::_SET_TEXT_ENTRY((char*)"STRING");
			UI::_ADD_TEXT_COMPONENT_STRING((char *)statusText.c_str());
		}
		UI::_DRAW_TEXT(0.5f, 0.1f);
	}
}

void set_status_text(std::string str, DWORD time = 2000, bool isGxtEntry = false)
{
	statusText = str;
	statusTextDrawTicksMax = GetTickCount() + time;
	statusTextGxtEntry = isGxtEntry;
}

void draw_rect(float A_0, float A_1, float A_2, float A_3, int A_4, int A_5, int A_6, int A_7)
{
	GRAPHICS::DRAW_RECT((A_0 + (A_2 * 0.5f)), (A_1 + (A_3 * 0.5f)), A_2, A_3, A_4, A_5, A_6, A_7);
}

void draw_menu_line(std::string caption, float lineWidth, float lineHeight, float lineTop, float lineLeft, float textLeft, bool active, bool title, bool rescaleText = true)
{
	// default values
	int text_col[4] = { 255, 255, 255, 255 },
		rect_col[4] = { 0, 0, 0, 190 };
	float text_scale = 0.35f;
	int font = 0;

	// correcting values for active line
	if (active)
	{
		text_col[0] = 0;
		text_col[1] = 0;
		text_col[2] = 0;

		rect_col[0] = 0;
		rect_col[1] = 180;
		rect_col[2] = 205;
		rect_col[3] = 220;

		if (rescaleText) text_scale = 0.35f;
	}

	if (title)
	{
		rect_col[0] = 0;
		rect_col[1] = 0;
		rect_col[2] = 0;

		if (rescaleText) text_scale = 0.70f;
		font = 1;
	}

	int screen_w, screen_h;
	GRAPHICS::GET_SCREEN_RESOLUTION(&screen_w, &screen_h);

	textLeft += lineLeft;

	float lineWidthScaled = lineWidth / (float)screen_w; // line width
	float lineTopScaled = lineTop / (float)screen_h; // line top offset
	float textLeftScaled = textLeft / (float)screen_w; // text left offset
	float lineHeightScaled = lineHeight / (float)screen_h; // line height

	float lineLeftScaled = lineLeft / (float)screen_w;

	// this is how it's done in original scripts

	// text upper part
	UI::SET_TEXT_FONT(font);
	UI::SET_TEXT_SCALE(0.0, text_scale);
	UI::SET_TEXT_COLOUR(text_col[0], text_col[1], text_col[2], text_col[3]);
	UI::SET_TEXT_CENTRE(0);
	UI::SET_TEXT_DROPSHADOW(0, 0, 0, 0, 0);
	UI::SET_TEXT_EDGE(0, 0, 0, 0, 0);
	UI::_SET_TEXT_ENTRY((char*)"STRING");
	UI::_ADD_TEXT_COMPONENT_STRING((LPSTR)caption.c_str());
	UI::_DRAW_TEXT(textLeftScaled, (((lineTopScaled + 0.00278f) + lineHeightScaled) - 0.005f));

	// text lower part
	UI::SET_TEXT_FONT(font);
	UI::SET_TEXT_SCALE(0.0, text_scale);
	UI::SET_TEXT_COLOUR(text_col[0], text_col[1], text_col[2], text_col[3]);
	UI::SET_TEXT_CENTRE(0);
	UI::SET_TEXT_DROPSHADOW(0, 0, 0, 0, 0);
	UI::SET_TEXT_EDGE(0, 0, 0, 0, 0);
	UI::_SET_TEXT_GXT_ENTRY((char*)"STRING");
	UI::_ADD_TEXT_COMPONENT_STRING((LPSTR)caption.c_str());
	int num25 = UI::_0x9040DFB09BE75706(textLeftScaled, (((lineTopScaled + 0.00278f) + lineHeightScaled) - 0.005f));

	// rect
	draw_rect(lineLeftScaled, lineTopScaled + (0.00278f),
		lineWidthScaled, ((((float)(num25)* UI::_0xDB88A37483346780(text_scale, 0)) + (lineHeightScaled * 2.0f)) + 0.005f),
		rect_col[0], rect_col[1], rect_col[2], rect_col[3]);
}

Cam lockCam(Vector3 pos, Vector3 rot) {
	CAM::DESTROY_ALL_CAMS(true);
	Cam lockedCam = CAM::CREATE_CAM_WITH_PARAMS((char*)"DEFAULT_SCRIPTED_CAMERA", pos.x, pos.y, pos.z, rot.x, rot.y, rot.z, 50, true, 2);
	CAM::SET_CAM_ACTIVE(lockedCam, true);
	CAM::RENDER_SCRIPT_CAMS(1, 0, 3000, 1, 0);
	return lockedCam;
}

void camLockChange()
{
	if (camLock) {
		CAM::RENDER_SCRIPT_CAMS(0, 0, 3000, 1, 0);
	}
	else {
		Vector3 oldCamCoords = CAM::GET_GAMEPLAY_CAM_COORD();
		Vector3 oldCamRots = CAM::GET_GAMEPLAY_CAM_ROT(2);
		float fov = CAM::GET_GAMEPLAY_CAM_FOV();
		CAM::DESTROY_ALL_CAMS(true);
		activeCam = CAM::CREATE_CAM_WITH_PARAMS((char*)"DEFAULT_SCRIPTED_CAMERA", oldCamCoords.x, oldCamCoords.y, oldCamCoords.z, oldCamRots.x, oldCamRots.y, oldCamRots.z, fov, true, 2);
		CAM::SET_CAM_ACTIVE(activeCam, true);
		CAM::RENDER_SCRIPT_CAMS(1, 0, 3000, 1, 0);
	}
}


void set_camera()
{
	Vector3 oldCamCoords = CAM::GET_GAMEPLAY_CAM_COORD();
	Vector3 oldCamRots = CAM::GET_GAMEPLAY_CAM_ROT(2);
	float fov = CAM::GET_GAMEPLAY_CAM_FOV();
	CAM::DESTROY_ALL_CAMS(true);

	//定义视点（朝哪看）坐标。
	Vector3 v = ENTITY::GET_ENTITY_COORDS(PLAYER::PLAYER_PED_ID(), TRUE);
	
	float look_x = (goFrom.x + goTo.x) / 2;
	float look_y = (goFrom.y + goTo.y) / 2;
	float look_z = v.z;

	int flag = 0; // 0: 原来的版本，从端点看。1：新版本：从中间看。
	float x1, y1, z1;
	if (flag == 0)
	{
		//设计相机摆放位置
		//计算直线斜率
		float k = (goFrom.y - goTo.y) / (goFrom.x - goTo.x);
		//定义到端点的距离
		float d = 6;
		float x, y, z; //在直线上且在线段外的点
		float delta_x = sqrt(d*d / (k*k + 1));
		if (goTo.x > goFrom.x)
		{
			x = goTo.x + delta_x;
		}
		else
		{
			x = goTo.x - delta_x;
		}
		y = k*(x - goTo.x) + goTo.y;
		z = goTo.z + 4;// + rand() / (RAND_MAX / 2.0);

		//下面开始在垂线上移动
		//垂线斜率
		float k1 = -1 / k;
		//float d1 = rand() / (RAND_MAX / 5.0);
		float d1 = 0;
		float delta_x1 = sqrt(d1*d1 / (k1*k1 + 1));
		x1 = x + delta_x1;
		y1 = k1*(x1 - x) + y;
		z1 = z;
	}
	else if (flag == 1)
	{
		float k = (goFrom.y - goTo.y) / (goFrom.x - goTo.x + 0.01);
		float k1 = -1 / (k + 0.01);
		float cx = (goFrom.x + goTo.x) / 2;
		float cy = (goFrom.y + goTo.y) / 2;
		float d = 22;
		float x = sqrt(d*d / (1 + k1*k1)) + cx;
		float y = k1*(x - cx) + cy;
		float z = goTo.z + 2 + rand() / (RAND_MAX / 2.0);
		x1 = x;
		y1 = y;
		z1 = z;
	}

	//隐藏本人
	ENTITY::SET_ENTITY_VISIBLE(PLAYER::PLAYER_PED_ID(), FALSE, FALSE);
	
	//set cam pos
	//activeCam = CAM::CREATE_CAM_WITH_PARAMS((char*)"DEFAULT_SCRIPTED_CAMERA", goFrom.x, goFrom.y, goFrom.z+2, oldCamRots.x, oldCamRots.y, oldCamRots.z, fov, true, 2);
	activeCam = CAM::CREATE_CAM_WITH_PARAMS((char*)"DEFAULT_SCRIPTED_CAMERA", x1, y1, z1, oldCamRots.x, oldCamRots.y, oldCamRots.z, fov, true, 2);
	CAM::SET_CAM_ACTIVE(activeCam, true);
	CAM::RENDER_SCRIPT_CAMS(1, 0, 3000, 1, 0);

	//设定视点坐标,朝哪看
	CAM::POINT_CAM_AT_COORD(activeCam, look_x, look_y, look_z);
}


void search_road(Vector3 pos)
{
	int candidate_counter = 0;
	vector<Vector3> candidate_pos;
	vector<std::pair<float, int> > candidate_dist;  //用于保存附近是道路的点，以及该点与参考点的高度差的绝对值。因为我需要高度差最小的，防止跌落现象。因为是按第一个元素排序，所以距离差放在前面。

	Entity ptr = NULL;
	BOOL res = PATHFIND::IS_POINT_ON_ROAD(pos.x, pos.y, pos.z, ptr);
	set_status_text(std::to_string(res));
	int bound = 20;  //40 m
	/*
	for (int i = -bound; i < bound; i++)
	{
		for (int j = -bound; j < bound; j++)
		{
			if (!(i == bound-1 || j == bound-1 || i == -bound || j == -bound))
			{
				continue;
			}
			Vector3 pos1;
			pos1.x = pos.x + i;
			pos1.y = pos.y + j;
			GAMEPLAY::GET_GROUND_Z_FOR_3D_COORD(pos1.x, pos1.y, 9999, &pos1.z, 0);
			Entity ptr = NULL;
			BOOL res = PATHFIND::IS_POINT_ON_ROAD(pos1.x, pos1.y, pos1.z, ptr);
			if (res == TRUE)  //在那个位置生成人。
			{
				//计算高度差
				float z_dist = abs(pos1.z - pos.z);
				//得到一个候选点
				candidate_dist.push_back(std::make_pair(z_dist, candidate_counter));
				candidate_pos.push_back(pos1);
				candidate_counter += 1;
			}
		}
	}
	*/

	for (int i = 0; i < 360; i++)
	{
		Vector3 pos1;
		float angle = float(i) / 180.0;
		pos1.x = pos.x + int(std::cos(pi * angle) * bound);
		pos1.y = pos.y + std::sin(pi * angle) * bound;
		GAMEPLAY::GET_GROUND_Z_FOR_3D_COORD(pos1.x, pos1.y, 9999, &pos1.z, 0);
		Entity ptr = NULL;
		BOOL res = PATHFIND::IS_POINT_ON_ROAD(pos1.x, pos1.y, pos1.z, ptr);
		if (res == TRUE)  //在那个位置生成人。
		{
			//计算高度差
			float z_dist = abs(pos1.z - pos.z);
			//得到一个候选点
			candidate_dist.push_back(std::make_pair(z_dist, candidate_counter));
			candidate_pos.push_back(pos1);
			candidate_counter += 1;
		}
	}

	//从候选点中找到最好的，即高度差最小的。
	std::sort(candidate_dist.begin(), candidate_dist.end());
	int best_id = candidate_dist[0].second;  //升序排列，所以第一个元素就是高度差最小的。
	goTo = candidate_pos[best_id];
	
	return;
}


void delete_peds()
{
	for (int i = 0; i < nwPeds; i++)
	{
		ENTITY::DELETE_ENTITY(&wPeds[i].ped);
	}

	//重置变量
	nwPeds = 0;
}


int width = 1024, height = 768;
void run_per_frame(int j, string video_dir, SOCKET sock)
{	
	//得到帧的编号（字符串）,及保存文件名
	char frame_name[10];
	sprintf(frame_name, "%06d", j);
	string fram_name_s(frame_name);
	std::string save_color_path = video_dir +  "\\images\\" + fram_name_s + ".jpg";
	string save_label_path = video_dir + "\\labels\\" + fram_name_s + ".png";

	
}


void set_weather()
{
	static LPCSTR lines[13] = {
		"EXTRASUNNY",
		"CLEAR",
		"CLOUDS",
		"SMOG",
		"FOGGY",
		"OVERCAST",
		"RAIN",
		"THUNDER",
		"CLEARING",
		"NEUTRAL",
		"SNOW",
		"BLIZZARD",
		"SNOWLIGHT",
	};
	int rand_weather_id = rand() % 13;
	GAMEPLAY::CLEAR_OVERRIDE_WEATHER();
	GAMEPLAY::SET_WEATHER_TYPE_NOW_PERSIST((char *)lines[rand_weather_id]);
	GAMEPLAY::CLEAR_WEATHER_TYPE_PERSIST();

	//设定时间
	//int h = rand() % 24;
	TIME::SET_CLOCK_TIME(12, 0, 0);
}

float speeds[100];
void showSpeed(std::ofstream& outFile)
{
	float speed;
	for (int i = 0; i < nwPeds; i++) //for every ped
	{
		speed = ENTITY::GET_ENTITY_SPEED(wPeds[i].ped);
		//speeds[i] = speed;
		outFile << speed << " ";
	}
	outFile << std::endl;
}

ScenarioCreator::ScenarioCreator() {}

void saveFile()
{
	std::string fname = "";
	int stop = 0;

	if (stopCoords)
		stop = 1;

	fname = fname + std::string(filesPath) + std::string(fileName);
	f = fopen(fname.c_str(), "w");

	if (camMoving)
		fprintf_s(f, "%d %f %f %f %d %f %f %f %f %f %f\n", (int)camMoving, A.x, A.y, A.z, stop, B.x, B.y, B.z, C.x, C.y, C.z);
	else
		fprintf_s(f, "%d %f %f %f %d %f %f %f\n", (int)camMoving, camCoords.x, camCoords.y, camCoords.z, stop, camRot.x, camRot.y, camRot.z);

	fprintf_s(f, "%f %f %f %f %f %f\n", TP1.x, TP1.y, TP1.z, TP1_rot.x, TP1_rot.y, TP1_rot.z);
	fprintf_s(f, "%f %f %f %f %f %f\n", TP2.x, TP2.y, TP2.z, TP2_rot.x, TP2_rot.y, TP2_rot.z);

	fprintf_s(f, "%s", logString);
	fclose(f);

	fname = fname + "  SAVED!";
	set_status_text(fname);
}

int readLine(FILE *f, Vector3 *pos)
{
	int ngroup = 0;
	int result = fscanf_s(f, "%d %f %f %f %d %d %f %f %f %f %f %f %f %d %d %d %d %d %d \n", &nPeds, &(*pos).x, &(*pos).y, &(*pos).z, &ngroup, &currentBehaviour, &speed, &goFrom.x, &goFrom.y, &goFrom.z, &goTo.x, &goTo.y, &goTo.z, &paramsLines[0].param, &paramsLines[1].param, &paramsLines[2].param, &paramsLines[3].param, &paramsLines[4].param, &paramsLines[5].param);
	if (ngroup == 0)
		group = false;
	if (ngroup == 1)
		group = 1;
	char message[5];
	sprintf_s(message, "%d", result);
	set_status_text(message);
	return result;
}

bool file_exist(std::string fileName)
{
	std::ifstream infile(fileName);
	return infile.good();
}

void readDirr() {
	int i = 0;
	std::string s;
	do {
		i++;
		s = std::string(filesPath) + "log_" + std::to_string(i) + ".txt";
		
	} while (file_exist(s));
	nFiles = i - 1;
}

void addwPed(Ped p, Vector3 from, Vector3 to, int stop, float spd)
{
	if (nwPeds > 199)
		return;

	wPeds[nwPeds].ped = p;
	wPeds[nwPeds].from = from;
	wPeds[nwPeds].to = to;
	wPeds[nwPeds].stopTime = stop;
	wPeds[nwPeds].speed = spd;

	nwPeds++;
}

Vector3 coordsToVector(float x, float y, float z)
{
	Vector3 v;
	v.x = x;
	v.y = y;
	v.z = z;
	return v;
}

void writeLogLine(float x, float y, float z)
{
	char line[200];
	int size;
	//line format: "nPeds X Y Z group currentBehaviour speed goFrom[3] goTo[3] paramLines.param[5] \n"
	int ngroup = 0;
	if (group) ngroup = 1;
	sprintf_s(line, "%d %f %f %f %d %d %f %f %f %f %f %f %f %d %d %d %d %d %d \n", nPeds, x, y, z, ngroup, currentBehaviour, speed, goFrom.x, goFrom.y, goFrom.z, goTo.x, goTo.y, goTo.z, paramsLines[0].param, paramsLines[1].param, paramsLines[2].param, paramsLines[3].param, paramsLines[4].param, paramsLines[5].param);

	size = (int)(strlen(line) + strlen(logString));
	if (size >= logLenght)
		logString = (char*)realloc(logString, (100 + size) * sizeof(char));

	strcat(logString, line);
}


ScenarioCreator::~ScenarioCreator() {
	// todo: implement a destroyer
	ReleaseDC(hWnd, hWindowDC);
	DeleteDC(hCaptureDC);
	DeleteObject(hCaptureBitmap);
}

void ScenarioCreator::update() {

	PLAYER::SET_POLICE_IGNORE_PLAYER(PLAYER::PLAYER_PED_ID(), TRUE);
	PLAYER::SET_EVERYONE_IGNORE_PLAYER(PLAYER::PLAYER_PED_ID(), TRUE);

	listen_for_keystrokes();

	cameraCoords();

	stopControl();

	walking_peds();

	update_status_text();
}

void ScenarioCreator::stopControl()
{
	if (stopCoords) {
		ENTITY::SET_ENTITY_COORDS_NO_OFFSET(PLAYER::PLAYER_PED_ID(), fixCoords.x, fixCoords.y, fixCoords.z, 0, 0, 0);
	}
}

void ScenarioCreator::show_text(std::string caption) {//貌似不能更新文字
	const float lineWidth = 500.0;
	while (true) {
		draw_menu_line(caption, lineWidth, mHeight, mHeight * 2, mLeft, mTitle, false, true);
		update();
		WAIT(0);
	}
}

void ScenarioCreator::generate_car()
{
	VEHICLE::SET_ALL_VEHICLE_GENERATORS_ACTIVE();
	Ped playerPed = PLAYER::PLAYER_PED_ID();
	//Vector3 coords = ENTITY::GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(PLAYER::PLAYER_PED_ID(), 0.0, 5.0, 0.0);
	Vector3 coords = ENTITY::GET_ENTITY_COORDS(PLAYER::PLAYER_PED_ID(), 1);
	DWORD model = GAMEPLAY::GET_HASH_KEY((char *)"ROCKET");
	Vehicle veh = VEHICLE::CREATE_VEHICLE(model, coords.x, coords.y, coords.z, 1, 0, 0);
	VEHICLE::SET_VEHICLE_ON_GROUND_PROPERLY(veh);
	std::ostringstream ss;
	ss << model << ", " << veh;
	std::string caption(ss.str());
	ScenarioCreator::show_text(caption);
}


// 尝试记录：试图 spawn 一辆车，结果不成功。
// 尝试记录：试图让人非常快速的运动，结果不成功。
SOCKET sock;
int size, imgSize, n;
void ScenarioCreator::listen_for_keystrokes() {
	if (IsKeyJustUp(VK_F9)) {
		Ped playerPed = PLAYER::PLAYER_PED_ID();
		std::ostringstream ss;
		if (PED::IS_PED_IN_ANY_VEHICLE(playerPed, 0)) {
			PED::SET_DRIVER_ABILITY(playerPed, 1.0);  // range 0.0f - 1.0f  
			PED::SET_DRIVER_AGGRESSIVENESS(playerPed, 1.0); // range 0.0f - 1.0f  
			Vehicle veh = PED::GET_VEHICLE_PED_IS_USING(playerPed);
			AI::TASK_VEHICLE_DRIVE_WANDER(playerPed, veh, 80.0, 2);  // mode = 2 时横冲直撞。=1时不会。
			ss << veh;
			ENTITY::SET_ENTITY_VISIBLE(playerPed, FALSE, true);
			ENTITY::SET_ENTITY_VISIBLE(veh, FALSE, true);
		}
		else {
			ss << "player isn't in a vehicle";
		}

		/////////////创建 socket//////////////////
		WSADATA wsaData;
		WSAStartup(MAKEWORD(2, 2), &wsaData);
		sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
		sockaddr_in sockAddr;
		memset(&sockAddr, 0, sizeof(sockAddr));
		sockAddr.sin_family = PF_INET;
		sockAddr.sin_addr.s_addr = inet_addr("172.18.32.31");
		sockAddr.sin_port = htons(2019);

		if (connect(sock, (SOCKADDR*)&sockAddr, sizeof(SOCKADDR)) < 0)
			printf("ERROR connecting");
		else
			printf("SUCCESS connecting");
		/////////////创建 socket//////////////////
		
	}

	//clear log string
	if (IsKeyJustUp(VK_F11)) {
		ENTITY::SET_ENTITY_MAX_HEALTH(PLAYER::PLAYER_PED_ID(), 9999);
		ENTITY::SET_ENTITY_HEALTH(PLAYER::PLAYER_PED_ID(), 8888);
		ENTITY::SET_ENTITY_CAN_BE_DAMAGED(PLAYER::PLAYER_PED_ID(), 0);
		//generate_car();
		int i_zhbli = 0;
		while (true) {
			i_zhbli = i_zhbli - 2;
			int max_health = ENTITY::GET_ENTITY_MAX_HEALTH(PLAYER::PLAYER_PED_ID());
			int now_health = ENTITY::GET_ENTITY_HEALTH(PLAYER::PLAYER_PED_ID());
			std::ostringstream ss;
			ss << i_zhbli << ", " <<  max_health << ", " << now_health;
			std::string caption(ss.str());
			show_text(caption);
			UI::DISPLAY_HELP_TEXT_THIS_FRAME((char*)caption.c_str(), 0); // 无效 **The bool appears to always be false (if it even is a bool, as it's represented by a zero)**  
			
			//UI::_SET_TEXT_ENTRY((char*)caption.c_str());
			//UI::_DRAW_TEXT(500, 500);//无效

			UI::_SET_TEXT_ENTRY((char*)"STRING");
			UI::_ADD_TEXT_COMPONENT_STRING((LPSTR)caption.c_str());
			UI::_DRAW_TEXT(500, 500);

			WAIT(20);
		}

	}

	//Show MainMenu (with F5)
	if (IsKeyJustUp(VK_F5)) {
		while (true){  // 不能无时间间隔的一直循环。这样的话画面根本动不了。
			WAIT(200);

			//角色不被通缉
			PLAYER::SET_PLAYER_WANTED_LEVEL(PLAYER::PLAYER_ID(), 0, 0);
			//Call SET_PLAYER_WANTED_LEVEL_NOW for immediate effect
			//wantedLevel is an integer value representing 0 to 5 stars even though the game supports the 6th wanted level but no police will appear since no definitions are present for it in the game files
			//disableNoMission - Disables When Off Mission - appears to always be false
			PLAYER::SET_PLAYER_WANTED_LEVEL_NOW(PLAYER::PLAYER_ID(), 0);
			//Forces any pending wanted level to be applied to the specified player immediately.  
			//Call SET_PLAYER_WANTED_LEVEL with the desired wanted level, followed by SET_PLAYER_WANTED_LEVEL_NOW.
			//Second parameter is unknown(always false).

			//角色血量不下降
			ENTITY::SET_ENTITY_HEALTH(PLAYER::PLAYER_PED_ID(), 200);
			/*
			health >= 0
			male ped ~= 100 - 200
			female ped ~= 0 - 100
			because something.
			*/
			PED::SET_PED_DIES_WHEN_INJURED(PLAYER::PLAYER_PED_ID(), 0);
			//以上两句无用
			ENTITY::SET_ENTITY_MAX_HEALTH(PLAYER::PLAYER_PED_ID(), 9999);
			ENTITY::SET_ENTITY_HEALTH(PLAYER::PLAYER_PED_ID(), 8888);
			ENTITY::SET_ENTITY_CAN_BE_DAMAGED(PLAYER::PLAYER_PED_ID(), 0);

			//车辆血量不下降
			Vehicle veh = PED::GET_VEHICLE_PED_IS_USING(playerPed);
			VEHICLE::SET_VEHICLE_ENGINE_HEALTH(veh, 1000);
			/*
			Returns 1000.0 if the function is unable to get the address of the specified vehicle or if it's not a vehicle.  
			Minimum: -4000  
			Maximum: 1000  
			-4000: Engine is destroyed  
			0 and below: Engine catches fire and health rapidly declines  
			300: Engine is smoking and losing functionality  
			1000: Engine is perfect  
			*/
			VEHICLE::SET_VEHICLE_PETROL_TANK_HEALTH(veh, 1000);
			//1000 is max health. Begins leaking gas at around 650 health
			VEHICLE::SET_VEHICLE_BODY_HEALTH(veh, 1000);
			// p2 often set to 1000.0 in the decompiled scripts.  

			//是否在车内
			if (PED::IS_PED_IN_ANY_VEHICLE(PLAYER::PLAYER_PED_ID(), 1) == FALSE)
			/*
			Parameters:
				ped: The ped to check.
				atGetIn: true to also consider attempting to enter a vehicle.
			Returns:
				Whether or not the ped is currently involved in any vehicle.
				Returns whether the specified ped is in any vehicle. If atGetIn is set to true, also returns true if the ped is currently in the process of entering a vehicle (a specific stage check for CTaskEnterVehicle).
			*/
			{
			    std::ostringstream ss;
			    ss << "log.txt";
			    std::string caption(ss.str());
				f = fopen(caption.c_str(), "a");
				fprintf_s(f, "%s", (char*)"NOT IN CAR\n");
				fclose(f);
			}

			//保存画面
			void *buf_color;
			size = export_get_color_buffer(&buf_color);
			Mat image_color(Size(width, height), CV_8UC4, buf_color, Mat::AUTO_STEP); //注意，这里是四通道
			cvtColor(image_color, image_color, CV_RGBA2RGB); //把四通道转为三通道？ important
			imgSize = image_color.total()*image_color.elemSize();
			n = send(sock, (char*)image_color.data, imgSize, 0);
			if (n < 0) {
				f = fopen("log.txt", "a");
				fprintf_s(f, "%s", (char*)"ERROR writing to socket");
				fclose(f);
			}

			char szBuffer[MAXBYTE] = { 0 };
			recv(sock, szBuffer, MAXBYTE, NULL);
			while (true) {
				if (strcmp(szBuffer, "got_color") == 0) {
					printf("client received\n");
					break;
				}
			}

			//保存分割模板
			void* buf;
			size = export_get_stencil_buffer(&buf);
			Mat image(Size(width, height), CV_8UC1, buf, Mat::AUTO_STEP); // 写这句话会出错：cvtColor(image, image, CV_GRAY2RGB);
			imgSize = image.total()*image.elemSize();
			n = send(sock, (char*)image.data, imgSize, 0);
			if (n < 0) printf("ERROR writing to socket");

			char szBuffer1[MAXBYTE] = { 0 };
			recv(sock, szBuffer1, MAXBYTE, NULL);
			while (true) {
				if (strcmp(szBuffer1, "got_mask") == 0) {
					printf("client received\n");
					break;
				}
			}
		}
	}

	if (menuActive) {
		if (IsKeyJustUp(VK_RETURN))							bEnter = true;
		if (IsKeyJustUp(VK_NUMPAD0) || IsKeyJustUp(VK_BACK))	bBack = true;
		if (IsKeyJustUp(VK_UP))							bUp = true;
		if (IsKeyJustUp(VK_DOWN))							bDown = true;
		if (IsKeyJustUp(VK_RIGHT))							bRight = true;
		if (IsKeyJustUp(VK_LEFT))							bLeft = true; 
	}


	//fly keys
	if (fly)
	{
		if (IsKeyJustUp(0x45)) //button E to go up
			ENTITY::APPLY_FORCE_TO_ENTITY_CENTER_OF_MASS(PLAYER::PLAYER_PED_ID(), 1, 0, 0, 2, true, true, true, true);
		if (IsKeyJustUp(0x51)) //button Q to go down
			ENTITY::APPLY_FORCE_TO_ENTITY_CENTER_OF_MASS(PLAYER::PLAYER_PED_ID(), 1, 0, 0, -2, true, true, true, true);
	}

	if (IsKeyJustUp(VK_SPACE)) //button SPACE to stop 
	{
		if (fly) {
			stopCoords = !stopCoords;
			char message[] = "UNLOCK";
			if (stopCoords)
				strcpy(message, "LOCK");
			fixCoords = playerCoords;
			ENTITY::SET_ENTITY_VELOCITY(PLAYER::PLAYER_PED_ID(), 0, 0, 0);
			set_status_text(message);
		}
		else if (stopCoords) {		//unlock if not flying
			stopCoords = !stopCoords;
			char message[] = "UNLOCK";
			set_status_text(message);
		}
	}
}

void ScenarioCreator::cameraCoords()
{
	char text[100];

	if (camLock) {
		camCoords = CAM::GET_GAMEPLAY_CAM_COORD();
		camRot = CAM::GET_GAMEPLAY_CAM_ROT(2);
	}
	else {
		camCoords = CAM::GET_CAM_COORD(activeCam);
		camRot = CAM::GET_CAM_ROT(activeCam, 2);
	}

	Vector3 v = ENTITY::GET_ENTITY_COORDS(PLAYER::PLAYER_PED_ID(), TRUE);
	sprintf_s(text, "player_coords: (%.3f, %.3f, %.3f)", v.x, v.y, v.z);
	//draw_text(text, 0.978, 0.205, 0.3);

	playerCoords = ENTITY::GET_ENTITY_COORDS(PLAYER::PLAYER_PED_ID(), TRUE);

	v = camCoords;
	sprintf_s(text, "cam_coords: (%.3f, %.3f, %.3f)", v.x, v.y, v.z);
	//draw_text(text, 0.978 - 1 * 0.03, 0.205, 0.3);

	v = camRot;
	sprintf_s(text, "cam_rot: (%.3f, %.3f, %.3f)", v.x, v.y, v.z);
	//draw_text(text, 0.978 - 2 * 0.03, 0.205, 0.3);

}

void ScenarioCreator::main_menu()
{
	const float lineWidth = 250.0;
	const int lineCount = 8;
	menuActive = true;

	std::string caption = "EF SIMULATOR";

	static LPCSTR lineCaption[lineCount] = {
		"PEDS",
		"CAMERA",
		"PLACE",
		"TIME",
		"WEATHER",
		"INVISIBLE",
		"FLY",
		"FILE"
	};

	DWORD waitTime = 150;
	while (true)
	{
		// timed menu draw, used for pause after active line switch
		DWORD maxTickCount = GetTickCount() + waitTime;

		if (visible)
			lineCaption[5] = "INVISIBLE		~g~ON";
		else
			lineCaption[5] = "INVISIBLE		~r~OFF";

		if (fly)
			lineCaption[6] = "FLY		~g~ON";
		else
			lineCaption[6] = "FLY		~r~OFF";

		do
		{
			// draw menu
			draw_menu_line(caption, lineWidth, mHeight, mHeight * 2, mLeft, mTitle, false, true);
			for (int i = 0; i < lineCount; i++)
			if (i != activeLineIndexMain)
				draw_menu_line(lineCaption[i], lineWidth, mHeight, mTopFlat + i * mTop, mLeft, mHeight, false, false);
			draw_menu_line(lineCaption[activeLineIndexMain], lineWidth, mHeight, mTopFlat + activeLineIndexMain * mTop, mLeft, mHeight, true, false);

			update();
			WAIT(0);
		} while (GetTickCount() < maxTickCount);
		waitTime = 0;

		update();
		// process buttons
		if (bEnter)
		{
			resetMenuCommands();

			switch (activeLineIndexMain)
			{
			case 0:
				//process peds menu;
				peds_menu();
				break;
			case 1:
				//process camera menu;
				camera_menu();
				break;
			case 2:
				//process place menu;
				place_menu();
				break;
			case 3:
				//process time menu;
				time_menu();
				break;
			case 4:
				//process wweather menu;
				weather_menu();
				break;
			case 5:
				//change visibility;
				visible = !visible;
				if (visible)
					ENTITY::SET_ENTITY_VISIBLE(PLAYER::PLAYER_PED_ID(), FALSE, true);
				else
					ENTITY::SET_ENTITY_VISIBLE(PLAYER::PLAYER_PED_ID(), TRUE, true);
				break;
			case 7:
				//process file menu;
				file_menu();
				break;
			case 6:
				//change visibility;
				fly = !fly;
				Entity me = PLAYER::PLAYER_PED_ID();
				if (fly) {
					ENTITY::SET_ENTITY_HAS_GRAVITY(me, false);
					ENTITY::SET_ENTITY_COLLISION(me, FALSE, FALSE);
				}
				else {
					ENTITY::SET_ENTITY_HAS_GRAVITY(me, true);
					ENTITY::SET_ENTITY_COLLISION(me, TRUE, TRUE);
				}
				break;
			}
			waitTime = 200;
		}

		if (bBack || bQuit)
		{
			menuActive = false;
			resetMenuCommands();
			break;
		}
		else if (bUp)
		{
			if (activeLineIndexMain == 0)
				activeLineIndexMain = lineCount;
			activeLineIndexMain--;
			waitTime = 150;
		}
		else if (bDown)
		{
			activeLineIndexMain++;
			if (activeLineIndexMain == lineCount)
				activeLineIndexMain = 0;
			waitTime = 150;
		}
		resetMenuCommands();
	}
}

void ScenarioCreator::peds_menu()
{
	const float lineWidth = 250.0;
	const int lineCount = 4;
	menuActive = true;

	std::string caption = "PEDS";

	char lines[lineCount][30] = {
		"NUMBER",
		"BEHAVIOUR",
		"GROUP",
		"SPAWN PEDS"
	};

	DWORD waitTime = 150;
	while (true)
	{
		// timed menu draw, used for pause after active line switch
		DWORD maxTickCount = GetTickCount() + waitTime;

		sprintf_s(lines[0], "NUMBER			 ~y~[ %d ]", nPeds);
		sprintf_s(lines[1], "BEHAVIOUR		~y~[ %s ]", tasks[currentBehaviour]);
		if (group)
			sprintf_s(lines[2], "GROUP			~y~[ ON ]");
		else
			sprintf_s(lines[2], "GROUP			~y~[ OFF ]");

		do
		{
			// draw menu
			draw_menu_line(caption, lineWidth, mHeight, mHeight * 2, mLeft, mTitle, false, true);
			for (int i = 0; i < lineCount; i++)
			if (i != activeLineIndexPeds)
				draw_menu_line(lines[i], lineWidth, mHeight, mTopFlat + i * mTop, mLeft, mHeight, false, false);
			draw_menu_line(lines[activeLineIndexPeds], lineWidth, mHeight, mTopFlat + activeLineIndexPeds * mTop, mLeft, mHeight, true, false);

			if (!subMenuActive)
				update();
			else
				return;
			WAIT(0);
		} while (GetTickCount() < maxTickCount);
		waitTime = 0;

		update();
		// process buttons
		if (bEnter)
		{
			switch (activeLineIndexPeds)
			{
			case 0:
				if (nPeds == nMaxPeds)
					nPeds = 0;
				else
					nPeds++;
				break;
			case 1:
				resetMenuCommands();
				tasks_sub_menu();
				break;
			case 2:
				group = !group;
				break;
			case 3:
				break;
			}
			waitTime = 200;
		}
		if (bBack)
		{
			resetMenuCommands();
			break;
		}
		else if (bQuit)
		{
			resetMenuCommands();
			bQuit = true;
			break;
		}
		else if (bUp)
		{
			if (activeLineIndexPeds == 0)
				activeLineIndexPeds = lineCount;
			activeLineIndexPeds--;
			waitTime = 150;
		}
		else if (bDown)
		{
			activeLineIndexPeds++;
			if (activeLineIndexPeds == lineCount)
				activeLineIndexPeds = 0;
			waitTime = 150;
		}

		if (activeLineIndexPeds == 0)
		{
			if (bLeft) {
				if (nPeds == 0)
					nPeds = nMaxPeds;
				else
					nPeds--;
			}
			else if (bRight) {
				if (nPeds == nMaxPeds)
					nPeds = 0;
				else
					nPeds++;
			}
		}
		if (activeLineIndexPeds == 1)
		{
			if (bLeft) {
				if (currentBehaviour == 0)
					currentBehaviour = numberTaks - 1;
				else
					currentBehaviour--;
			}
			else if (bRight) {
				if (currentBehaviour == numberTaks - 1)
					currentBehaviour = 0;
				else
					currentBehaviour++;
			}
		}
		resetMenuCommands();
	}
}

void ScenarioCreator::camera_menu()
{
	const float lineWidth = 250.0;
	const int lineCount = 10;
	menuActive = true;

	std::string caption = "CAMERA COORDS";

	char lines[lineCount][50] = { "", "", "", "", "", "", "", "", "", "" };
	DWORD waitTime = 150;
	while (true)
	{
		// timed menu draw, used for pause after active line switch
		DWORD maxTickCount = GetTickCount() + waitTime;

		if (camLock)
			sprintf_s(lines[0], "LOCK		~g~ON");
		else
			sprintf_s(lines[0], "LOCK		~r~OFF");

		sprintf_s(lines[1], "X			~y~[ %0.1f ]", camCoords.x);
		sprintf_s(lines[2], "Y			~y~[ %0.1f ]", camCoords.y);
		sprintf_s(lines[3], "Z			~y~[ %0.1f ]", camCoords.z);
		if (camMoving)
			sprintf_s(lines[4], "MOVING		~g~ON");
		else
			sprintf_s(lines[4], "MOVING		~r~OFF");

		sprintf_s(lines[5], "A	~y~[ x=%0.1f y=%0.1f ]", A.x, A.y);
		sprintf_s(lines[6], "B	~y~[ x=%0.1f y=%0.1f ]", B.x, B.y);
		sprintf_s(lines[7], "C	~y~[ x=%0.1f y=%0.1f ]", C.x, C.y);

		sprintf_s(lines[8], "Teleport 1	~y~[ x=%0.1f y=%0.1f ]", TP1.x, TP1.y);
		sprintf_s(lines[9], "Teleport 2	~y~[ x=%0.1f y=%0.1f ]", TP2.x, TP2.y);

		do
		{
			// draw menu
			draw_menu_line(caption, lineWidth, mHeight, mHeight * 2, mLeft, mTitle, false, true);
			for (int i = 0; i < lineCount; i++)
			if (i != activeLineIndexCamera)
				draw_menu_line(lines[i], lineWidth, mHeight, mTopFlat + i * mTop, mLeft, mHeight, false, false);
			draw_menu_line(lines[activeLineIndexCamera], lineWidth, mHeight, mTopFlat + activeLineIndexCamera * mTop, mLeft, mHeight, true, false);

			update();
			WAIT(0);
		} while (GetTickCount() < maxTickCount);
		waitTime = 0;

		update();
		// process buttons
		if (bBack)
		{
			resetMenuCommands();
			break;
		}
		else if (bQuit)
		{
			resetMenuCommands();
			bQuit = true;
			break;
		}
		else if (bUp)
		{
			if (activeLineIndexCamera == 0)
				activeLineIndexCamera = lineCount;
			activeLineIndexCamera--;
			waitTime = 150;
		}
		else if (bDown)
		{
			activeLineIndexCamera++;
			if (activeLineIndexCamera == lineCount)
				activeLineIndexCamera = 0;
			waitTime = 150;
		}
		else if (bEnter)
		{
			if (activeLineIndexCamera == 0)
			{
				camLock = !camLock;
				camLockChange();
			}
			else if (activeLineIndexCamera == 4)
			{
				camMoving = !camMoving;
			}
			else if (activeLineIndexCamera == 5)
			{
				A = playerCoords;
			}
			else if (activeLineIndexCamera == 6)
			{
				B = playerCoords;
			}
			else if (activeLineIndexCamera == 7)
			{
				C = playerCoords;
			}
			else if (activeLineIndexCamera == 8)
			{
				TP1 = playerCoords;
				TP1_rot = CAM::GET_GAMEPLAY_CAM_ROT(2);
			}
			else if (activeLineIndexCamera == 9)
			{
				TP2 = playerCoords;
				TP2_rot = CAM::GET_GAMEPLAY_CAM_ROT(2);
			}
			waitTime = 150;
		}
		else if (bLeft)
		{
			switch (activeLineIndexCamera)
			{
			case 1:
				camCoords.x -= 1;
				CAM::SET_CAM_COORD(activeCam, camCoords.x, camCoords.y, camCoords.z);
				break;
			case 2:
				camCoords.y -= 1;
				CAM::SET_CAM_COORD(activeCam, camCoords.x, camCoords.y, camCoords.z);
				break;
			case 3:
				camCoords.z -= 1;
				CAM::SET_CAM_COORD(activeCam, camCoords.x, camCoords.y, camCoords.z);
				break;
			}
		}
		else if (bRight)
		{
			switch (activeLineIndexCamera)
			{
			case 1:
				camCoords.x++;
				CAM::SET_CAM_COORD(activeCam, camCoords.x, camCoords.y, camCoords.z);
				break;
			case 2:
				camCoords.y++;
				CAM::SET_CAM_COORD(activeCam, camCoords.x, camCoords.y, camCoords.z);
				break;
			case 3:
				camCoords.z++;
				CAM::SET_CAM_COORD(activeCam, camCoords.x, camCoords.y, camCoords.z);
				break;
			}

		}

		resetMenuCommands();
	}
}

void ScenarioCreator::place_menu(){
}

void ScenarioCreator::time_menu(){}

void ScenarioCreator::weather_menu()
{
	const float lineWidth = 250.0;
	const int lineCount = 14;
	menuActive = true;

	std::string caption = "WEATHER  OPTIONS";

	static LPCSTR lines[lineCount] = {
		"WIND",
		"EXTRASUNNY",
		"CLEAR",
		"CLOUDS",
		"SMOG",
		"FOGGY",
		"OVERCAST",
		"RAIN",
		"THUNDER",
		"CLEARING",
		"NEUTRAL",
		"SNOW",
		"BLIZZARD",
		"SNOWLIGHT",
	};

	DWORD waitTime = 150;
	while (true)
	{
		// timed menu draw, used for pause after active line switch
		DWORD maxTickCount = GetTickCount() + waitTime;

		if (wind)
			lines[0] = "WIND		~g~ON";
		else
			lines[0] = "WIND		~r~OFF";

		do
		{
			// draw menu
			draw_menu_line(caption, lineWidth, mHeight, mHeight * 2, mLeft, mTitle, false, true);
			for (int i = 0; i < lineCount; i++)
			if (i != activeLineIndexWeather)
				draw_menu_line(lines[i], lineWidth, mHeight, mTopFlat + i * mTop, mLeft, mHeight, false, false);
			draw_menu_line(lines[activeLineIndexWeather], lineWidth, mHeight, mTopFlat + activeLineIndexWeather * mTop, mLeft, mHeight, true, false);

			update();
			WAIT(0);
		} while (GetTickCount() < maxTickCount);
		waitTime = 0;

		update();
		// process buttons
		if (bEnter)
		{
			switch (activeLineIndexWeather)
			{
				// wind
			case 0:
				wind = !wind;
				if (wind)
				{
					GAMEPLAY::SET_WIND(1.0);
					GAMEPLAY::SET_WIND_SPEED(11.99f);
					GAMEPLAY::SET_WIND_DIRECTION(ENTITY::GET_ENTITY_HEADING(PLAYER::PLAYER_PED_ID()));
				}
				else
				{
					GAMEPLAY::SET_WIND(0.0);
					GAMEPLAY::SET_WIND_SPEED(0.0);
				}
				break;
				// set weather
			default:
				GAMEPLAY::CLEAR_OVERRIDE_WEATHER();
				GAMEPLAY::SET_WEATHER_TYPE_NOW_PERSIST((char *)lines[activeLineIndexWeather]);
				GAMEPLAY::CLEAR_WEATHER_TYPE_PERSIST();
			}
			waitTime = 200;
		}
		else if (bBack)
		{
			resetMenuCommands();
			break;
		}
		else if (bQuit)
		{
			resetMenuCommands();
			bQuit = true;
			break;
		}
		else if (bUp)
		{
			if (activeLineIndexWeather == 0)
				activeLineIndexWeather = lineCount;
			activeLineIndexWeather--;
			waitTime = 150;
		}
		else if (bDown)
		{
			activeLineIndexWeather++;
			if (activeLineIndexWeather == lineCount)
				activeLineIndexWeather = 0;
			waitTime = 150;
		}
		resetMenuCommands();
	}
}

void ScenarioCreator::resetMenuCommands()
{
	bEnter = false;
	bBack = false;
	bUp = false;
	bLeft = false;
	bRight = false;
	bDown = false;
	bQuit = false;
}

void ScenarioCreator::tasks_sub_menu()
{
	const float lineWidth = 320.0;
	int lineCount = 0;
	activeLineIndexSubmenu = 0;
	subMenuActive = true;

	switch (currentBehaviour)
	{
	case 0:
		lineCount = 2;
		break;
	case 1:
	case 2:
	case 3:
		lineCount = 1;
		break;
	case 4:
		lineCount = 3;
		break;
	case 8:
		lineCount = 5;
		break;
	default:
		subMenuActive = false;
		return;
		break;
	}


	char lines[5][40] = { "", "", "", "", "" };
	DWORD waitTime = 150;
	while (true)
	{
		// timed menu draw, used for pause after active line switch
		DWORD maxTickCount = GetTickCount() + waitTime;

		switch (currentBehaviour)
		{
		case 0:
			sprintf_s(lines[0], "%s			 ~y~[ %d ]", paramsLines[0].text, paramsLines[0].param);
			sprintf_s(lines[1], "%s		~y~[ %s ]", paramsLines[1].text, scenarioTypes[paramsLines[1].param]);
			break;
		case 1:
		case 2:
		case 3:
			sprintf_s(lines[0], "%s			 ~y~[ %d ]", paramsLines[0].text, paramsLines[0].param);
			break;
		case 4:
			sprintf_s(lines[0], "%s			 ~y~[ %d ]", paramsLines[2].text, paramsLines[2].param);
			sprintf_s(lines[1], "%s			 ~y~[ %d ]", paramsLines[3].text, paramsLines[3].param);
			sprintf_s(lines[2], "%s			 ~y~[ %d ]", paramsLines[4].text, paramsLines[4].param);
			break;
		case 8:
			sprintf_s(lines[0], "From	~y~[ x=%0.1f y=%0.1f ]", goFrom.x, goFrom.y);
			sprintf_s(lines[1], "To		~y~[ x=%0.1f y=%0.1f ]", goTo.x, goTo.y);
			sprintf_s(lines[2], "Speed			 ~y~[ %0.1f ]", speed);
			sprintf_s(lines[3], "%s			 ~y~[ %d ]", paramsLines[4].text, paramsLines[4].param);
			sprintf_s(lines[4], "%s			 ~y~[ %d ]", paramsLines[5].text, paramsLines[5].param);
			break;
		}

		do
		{
			// draw menu
			for (int i = 0; i < lineCount; i++)
			if (i != activeLineIndexSubmenu)
				draw_menu_line(lines[i], lineWidth, mHeight, mTopFlat + i * mTop, mLeft + 260, mHeight, false, false);
			draw_menu_line(lines[activeLineIndexSubmenu], lineWidth, mHeight, mTopFlat + activeLineIndexSubmenu * mTop, mLeft + 260, mHeight, true, false);

			update();
			peds_menu();
			WAIT(0);
		} while (GetTickCount() < maxTickCount);
		waitTime = 0;

		update();
		peds_menu();
		// process buttons
		if (bEnter)
		{
			if (currentBehaviour == 8)
			{
				if (activeLineIndexSubmenu == 0)
					goFrom = playerCoords;
				if (activeLineIndexSubmenu == 1)
					goTo = playerCoords;
			}
			waitTime = 200;
		}
		else if (bBack)
		{
			resetMenuCommands();
			subMenuActive = false;
			break;
		}
		else if (bQuit)
		{
			resetMenuCommands();
			subMenuActive = false;
			bQuit = true;
			break;
		}
		else if (bUp)
		{
			if (activeLineIndexSubmenu == 0)
				activeLineIndexSubmenu = lineCount;
			activeLineIndexSubmenu--;
			waitTime = 150;
		}
		else if (bDown)
		{
			activeLineIndexSubmenu++;
			if (activeLineIndexSubmenu == lineCount)
				activeLineIndexSubmenu = 0;
			waitTime = 150;
		}
		else if (bLeft)
		{
			switch (currentBehaviour)
			{
			case 0:
				switch (activeLineIndexSubmenu)
				{
				case 0:
					if (paramsLines[0].param == 0)
						paramsLines[0].param = maxNumber;
					else
						paramsLines[0].param--;
					break;
				case 1:
					if (paramsLines[1].param == 0)
						paramsLines[1].param = nScenario - 1;
					else
						paramsLines[1].param--;
					break;
				}
				break;
			case 1:
			case 2:
			case 3:
				if (paramsLines[0].param == 0)
					paramsLines[0].param = maxNumber;
				else
					paramsLines[0].param--;
				break;
			case 4:
				if (paramsLines[activeLineIndexSubmenu + 2].param == 0)
					paramsLines[activeLineIndexSubmenu + 2].param = maxNumber;
				else
					paramsLines[activeLineIndexSubmenu + 2].param--;
				break;
			case 8:
				if (activeLineIndexSubmenu == 2)
				if (speed < 1.01)
					speed = 2;
				else
					speed -= 0.1f;
				if (activeLineIndexSubmenu == 3)
				if (paramsLines[4].param == 0)
					paramsLines[4].param = maxNumber;
				else
					paramsLines[4].param--;
				if (activeLineIndexSubmenu == 4)
				if (paramsLines[5].param == 0)
					paramsLines[5].param = maxNumber;
				else
					paramsLines[5].param--;
				break;
			}
		}
		else if (bRight)
		{
			switch (currentBehaviour)
			{
			case 0:
				switch (activeLineIndexSubmenu)
				{
				case 0:
					if (paramsLines[0].param == maxNumber)
						paramsLines[0].param = 0;
					else
						paramsLines[0].param++;
					break;
				case 1:
					if (paramsLines[1].param == nScenario - 1)
						paramsLines[1].param = 0;
					else
						paramsLines[1].param++;
					break;
				}
				break;
			case 1:
			case 2:
			case 3:
				if (paramsLines[0].param == maxNumber)
					paramsLines[0].param = 0;
				else
					paramsLines[0].param++;
				break;
			case 4:
				if (paramsLines[activeLineIndexSubmenu + 2].param == maxNumber)
					paramsLines[activeLineIndexSubmenu + 2].param = 0;
				else
					paramsLines[activeLineIndexSubmenu + 2].param++;
				break;
			case 8:
				if (activeLineIndexSubmenu == 2)
				if (speed > 1.99)
					speed = 1;
				else
					speed += 0.1f;
				if (activeLineIndexSubmenu == 3)
				if (paramsLines[4].param == maxNumber)
					paramsLines[4].param = 0;
				else
					paramsLines[4].param++;
				if (activeLineIndexSubmenu == 4)
				if (paramsLines[5].param == maxNumber)
					paramsLines[5].param = 0;
				else
					paramsLines[5].param++;
				break;
			}
		}
		resetMenuCommands();
	}
}

void ScenarioCreator::cancelLastLog() {
	int nchar = (int)strlen(logString);
	int n = 0;
	for (int i = nchar; i >= 0; i--) {
		if (logString[i] == '\n') {
			n++;
		}
		if (n == 2) {
			break;
		}
		logString[i] = '\0';
	}
}


void ScenarioCreator::spawn_peds_detect(Vector3 pos, int num_ped) {
	Ped ped[100];
	Vector3 current;
	int i = 0;

	float rnX, rnY;
	int rn;

	writeLogLine(pos.x, pos.y, pos.z);


	// spawning 'num_ped' pedestrians
	for (int i = 0; i<num_ped; i++) {
		float offer_set = float(i - num_ped / 2) * 5;
		ped[i] = PED::CREATE_RANDOM_PED(pos.x+ offer_set, pos.y, pos.z);
		WAIT(50);
	}


	// killing all pedestrians in order to prevent a bug
	for (int i = 0; i<num_ped; i++) {
		ENTITY::SET_ENTITY_HEALTH(ped[i], 0);
		WAIT(50);
	}

	WAIT(500);

	int groupId = 0;
	if (group)
		groupId = PED::CREATE_GROUP(1);

	// resurrecting all pedestrians and assigning them a task
	for (int i = 0; i<num_ped; i++) {
		float offer_set = float(i - num_ped / 2) * 5;
		float offer_set2 = float(i - num_ped / 2) * 2;
		WAIT(50);

		AI::CLEAR_PED_TASKS_IMMEDIATELY(ped[i]);
		PED::RESURRECT_PED(ped[i]);
		PED::REVIVE_INJURED_PED(ped[i]);

		// in order to prevent them from falling in hell
		ENTITY::SET_ENTITY_COLLISION(ped[i], TRUE, TRUE);
		PED::SET_PED_CAN_RAGDOLL(ped[i], TRUE);

		current = ENTITY::GET_ENTITY_COORDS(ped[i], TRUE);

		Ped targetPed = ped[0];
		//if (num_ped > 1)
		//	targetPed = ped[1];

		if (group) {
			PED::SET_PED_AS_GROUP_MEMBER(ped[i], groupId);
			PED::SET_PED_NEVER_LEAVES_GROUP(ped[i], true);
		}
		//srand((unsigned int)time(NULL));

		PED::SET_BLOCKING_OF_NON_TEMPORARY_EVENTS(ped[i], TRUE);
		PED::SET_PED_COMBAT_ATTRIBUTES(ped[i], 1, FALSE);
		Vector3 pp = ENTITY::GET_ENTITY_COORDS(PLAYER::PLAYER_ID(), TRUE);
		float base_speed = 30;
		int speed_range = 10;
		switch (currentBehaviour)
		{
		case 0: {
			if (paramsLines[5].param == -1) {
				rnX = (float)(((rand() % 81) - 40) / 10.0);
				rnY = (float)(((rand() % 81) - 40) / 10.0);
			}
			else {
				rnX = (float)((rand() % (paramsLines[5].param * 2)) - paramsLines[5].param);
				rnY = (float)((rand() % (paramsLines[5].param * 2)) - paramsLines[5].param);
			}

			float speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			//goFrom.x -= 5;
			addwPed(ped[i], coordsToVector(goFrom.x + rnX + offer_set, goFrom.y + rnY, goFrom.z), coordsToVector(goTo.x + rnX + offer_set2, goTo.y + rnY, goTo.z), paramsLines[4].param, speed_rnd);
			//goFrom.x += 5;
			Object seq;
			// waiting time proportional to distance
			float atob = GAMEPLAY::GET_DISTANCE_BETWEEN_COORDS(goFrom.x, goFrom.y, goFrom.z, goTo.x, goTo.y, goTo.z, 1);
			int max_time = (int)((atob / 2.5) * 1000);
			max_time = 15000;

			AI::OPEN_SEQUENCE_TASK(&seq);
			//goFrom.x += 10;
			//goTo.x -= 5;
			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goFrom.x + rnX + offer_set, goFrom.y + rnY, goFrom.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goTo.x + rnX + offer_set2, goTo.y + rnY, goTo.z, speed_rnd, 0, 0, 786603, 0xbf800000);

			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goFrom.x + rnX + offer_set, goFrom.y + rnY, goFrom.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goTo.x + rnX + offer_set2, goTo.y + rnY, goTo.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goFrom.x + rnX + offer_set, goFrom.y + rnY, goFrom.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goTo.x + rnX + offer_set2, goTo.y + rnY, goTo.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			AI::CLOSE_SEQUENCE_TASK(seq);
			AI::TASK_PERFORM_SEQUENCE(ped[i], seq);
			AI::CLEAR_SEQUENCE_TASK(&seq);
		}
				break;
		default:
			break;
		}

	}
}

void ScenarioCreator::spawn_peds1(Vector3 pos, int num_ped) {
	Ped ped[100];
	Vector3 current;
	int i = 0;

	float rnX, rnY;
	int rn;

	writeLogLine(pos.x, pos.y, pos.z);


	// spawning 'num_ped' pedestrians
	for (int i = 0; i<num_ped; i++) {
		ped[i] = PED::CREATE_RANDOM_PED(pos.x, pos.y, pos.z);
		WAIT(50);
	}


	// killing all pedestrians in order to prevent a bug
	for (int i = 0; i<num_ped; i++) {
		ENTITY::SET_ENTITY_HEALTH(ped[i], 0);
		WAIT(50);
	}

	WAIT(500);

	int groupId = 0;
	if (group)
		groupId = PED::CREATE_GROUP(1);

	// resurrecting all pedestrians and assigning them a task
	for (int i = 0; i<num_ped; i++) {

		WAIT(50);

		AI::CLEAR_PED_TASKS_IMMEDIATELY(ped[i]);
		PED::RESURRECT_PED(ped[i]);
		PED::REVIVE_INJURED_PED(ped[i]);

		// in order to prevent them from falling in hell
		ENTITY::SET_ENTITY_COLLISION(ped[i], TRUE, TRUE);
		PED::SET_PED_CAN_RAGDOLL(ped[i], TRUE);

		current = ENTITY::GET_ENTITY_COORDS(ped[i], TRUE);

		Ped targetPed = ped[0];
		if (num_ped > 1)
			targetPed = ped[1];

		if (group) {
			PED::SET_PED_AS_GROUP_MEMBER(ped[i], groupId);
			PED::SET_PED_NEVER_LEAVES_GROUP(ped[i], true);
		}
		//srand((unsigned int)time(NULL));

		PED::SET_BLOCKING_OF_NON_TEMPORARY_EVENTS(ped[i], TRUE);
		PED::SET_PED_COMBAT_ATTRIBUTES(ped[i], 1, FALSE);
		Vector3 pp = ENTITY::GET_ENTITY_COORDS(PLAYER::PLAYER_ID(), TRUE);
		float base_speed = 30;
		int speed_range = 10;
		switch (currentBehaviour)
		{
		case 0: {
			if (paramsLines[5].param == -1) {
				rnX = (float)(((rand() % 81) - 40) / 10.0);
				rnY = (float)(((rand() % 81) - 40) / 10.0);
			}
			else {
				rnX = (float)((rand() % (paramsLines[5].param * 2)) - paramsLines[5].param);
				rnY = (float)((rand() % (paramsLines[5].param * 2)) - paramsLines[5].param);
			}

			float speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			goFrom.x -= 5;
			addwPed(ped[i], coordsToVector(goFrom.x + rnX, goFrom.y + rnY, goFrom.z), coordsToVector(goTo.x + rnX, goTo.y + rnY, goTo.z), paramsLines[4].param, speed_rnd);
			goFrom.x += 5;
			Object seq;
			// waiting time proportional to distance
			float atob = GAMEPLAY::GET_DISTANCE_BETWEEN_COORDS(goFrom.x, goFrom.y, goFrom.z, goTo.x, goTo.y, goTo.z, 1);
			int max_time = (int)((atob / 2.5) * 1000);
			max_time = 15000;

			AI::OPEN_SEQUENCE_TASK(&seq);
			goFrom.x += 10;
			goTo.x -= 5;
			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goFrom.x + rnX, goFrom.y + rnY, goFrom.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goTo.x + rnX, goTo.y + rnY, goTo.z, speed_rnd, 0, 0, 786603, 0xbf800000);

			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goFrom.x + rnX, goFrom.y + rnY, goFrom.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goTo.x + rnX, goTo.y + rnY, goTo.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goFrom.x + rnX, goFrom.y + rnY, goFrom.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goTo.x + rnX, goTo.y + rnY, goTo.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			AI::CLOSE_SEQUENCE_TASK(seq);
			AI::TASK_PERFORM_SEQUENCE(ped[i], seq);
			AI::CLEAR_SEQUENCE_TASK(&seq);
		}
				break;
		default:
			break;
		}

	}
}

void ScenarioCreator::spawn_peds(Vector3 pos, int num_ped) {	
	Ped ped[100];
	Vector3 current;
	int i = 0;

	float rnX, rnY;
	int rn;

	writeLogLine(pos.x, pos.y, pos.z);


	// spawning 'num_ped' pedestrians
	for (int i = 0; i<num_ped; i++) {
		ped[i] = PED::CREATE_RANDOM_PED(pos.x, pos.y, pos.z);
		WAIT(50);
	}


	// killing all pedestrians in order to prevent a bug
	for (int i = 0; i<num_ped; i++) {
		ENTITY::SET_ENTITY_HEALTH(ped[i], 0);
		WAIT(50);
	}

	WAIT(500);

	int groupId = 0;
	if (group)
		groupId = PED::CREATE_GROUP(1);

	// resurrecting all pedestrians and assigning them a task
	for (int i = 0; i<num_ped; i++) {

		WAIT(50);

		AI::CLEAR_PED_TASKS_IMMEDIATELY(ped[i]);
		PED::RESURRECT_PED(ped[i]);
		PED::REVIVE_INJURED_PED(ped[i]);

		// in order to prevent them from falling in hell
		ENTITY::SET_ENTITY_COLLISION(ped[i], TRUE, TRUE);
		PED::SET_PED_CAN_RAGDOLL(ped[i], TRUE);

		current = ENTITY::GET_ENTITY_COORDS(ped[i], TRUE);

		Ped targetPed = ped[0];
		if (num_ped > 1)
			targetPed = ped[1];

		if (group) {
			PED::SET_PED_AS_GROUP_MEMBER(ped[i], groupId);
			PED::SET_PED_NEVER_LEAVES_GROUP(ped[i], true);
		}
		//srand((unsigned int)time(NULL));

		PED::SET_BLOCKING_OF_NON_TEMPORARY_EVENTS(ped[i], TRUE);
		PED::SET_PED_COMBAT_ATTRIBUTES(ped[i], 1, FALSE);
		Vector3 pp = ENTITY::GET_ENTITY_COORDS(PLAYER::PLAYER_ID(), TRUE);
		float base_speed = 10;
		int speed_range = 10;
		switch (currentBehaviour)
		{
		case 0: { 
			if (paramsLines[5].param == -1) {
				rnX = (float)(((rand() % 81) - 40) / 10.0);
				rnY = (float)(((rand() % 81) - 40) / 10.0);
			}
			else {
				rnX = (float)((rand() % (paramsLines[5].param * 2)) - paramsLines[5].param);
				rnY = (float)((rand() % (paramsLines[5].param * 2)) - paramsLines[5].param);
			}
			
			float speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			addwPed(ped[i], coordsToVector(goFrom.x + rnX, goFrom.y + rnY, goFrom.z), coordsToVector(goTo.x + rnX, goTo.y + rnY, goTo.z), paramsLines[4].param, speed_rnd);
			Object seq;
			// waiting time proportional to distance
			float atob = GAMEPLAY::GET_DISTANCE_BETWEEN_COORDS(goFrom.x, goFrom.y, goFrom.z, goTo.x, goTo.y, goTo.z, 1);
			int max_time = (int)((atob / 2.5) * 1000);
			max_time = 15000;

			AI::OPEN_SEQUENCE_TASK(&seq);
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goFrom.x + rnX, goFrom.y + rnY, goFrom.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goTo.x + rnX, goTo.y + rnY, goTo.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goFrom.x + rnX, goFrom.y + rnY, goFrom.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goTo.x + rnX, goTo.y + rnY, goTo.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goFrom.x + rnX, goFrom.y + rnY, goFrom.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
			AI::TASK_GO_TO_COORD_ANY_MEANS(0, goTo.x + rnX, goTo.y + rnY, goTo.z, speed_rnd, 0, 0, 786603, 0xbf800000);
			AI::CLOSE_SEQUENCE_TASK(seq);
			AI::TASK_PERFORM_SEQUENCE(ped[i], seq);
			AI::CLEAR_SEQUENCE_TASK(&seq);

			if (paramsLines[5].param != -1) {
				rnX = (float)((rand() % (paramsLines[5].param * 2)) - paramsLines[5].param);
				rnY = (float)((rand() % (paramsLines[5].param * 2)) - paramsLines[5].param);
				speed_rnd = (float)(base_speed + rand() % speed_range) / 10;

				int ped_specular = PED::CREATE_RANDOM_PED(goTo.x, goTo.y, goTo.z);
				WAIT(100);
				
				ENTITY::SET_ENTITY_HEALTH(ped_specular, 0);
				WAIT(100);
				AI::CLEAR_PED_TASKS_IMMEDIATELY(ped_specular);
				PED::RESURRECT_PED(ped_specular);
				PED::REVIVE_INJURED_PED(ped_specular);

				// in order to prevent them from falling in hell
				ENTITY::SET_ENTITY_COLLISION(ped_specular, TRUE, TRUE);
				PED::SET_PED_CAN_RAGDOLL(ped_specular, TRUE);

				PED::SET_BLOCKING_OF_NON_TEMPORARY_EVENTS(ped_specular, TRUE);
				PED::SET_PED_COMBAT_ATTRIBUTES(ped_specular, 1, FALSE);
				addwPed(ped_specular, coordsToVector(goTo.x + rnX, goTo.y + rnY, goTo.z), coordsToVector(goFrom.x + rnX, goFrom.y + rnY, goFrom.z), paramsLines[4].param, speed_rnd);

				Object seq2;
				AI::OPEN_SEQUENCE_TASK(&seq2);
				speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
				AI::TASK_GO_TO_COORD_ANY_MEANS(0, goTo.x + rnX, goTo.y + rnY, goTo.z, speed_rnd, 0, 0, 786603, 0xbf800000);
				speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
				AI::TASK_GO_TO_COORD_ANY_MEANS(0, goFrom.x + rnX, goFrom.y + rnY, goFrom.z, speed_rnd, 0, 0, 786603, 0xbf800000);
				speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
				AI::TASK_GO_TO_COORD_ANY_MEANS(0, goTo.x + rnX, goTo.y + rnY, goTo.z, speed_rnd, 0, 0, 786603, 0xbf800000);
				speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
				AI::TASK_GO_TO_COORD_ANY_MEANS(0, goFrom.x + rnX, goFrom.y + rnY, goFrom.z, speed_rnd, 0, 0, 786603, 0xbf800000);
				speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
				AI::TASK_GO_TO_COORD_ANY_MEANS(0, goTo.x + rnX, goTo.y + rnY, goTo.z, speed_rnd, 0, 0, 786603, 0xbf800000);
				speed_rnd = (float)(base_speed + rand() % speed_range) / 10;
				AI::TASK_GO_TO_COORD_ANY_MEANS(0, goFrom.x + rnX, goFrom.y + rnY, goFrom.z, speed_rnd, 0, 0, 786603, 0xbf800000);
				AI::CLOSE_SEQUENCE_TASK(seq2);
				AI::TASK_PERFORM_SEQUENCE(ped_specular, seq2);
				AI::CLEAR_SEQUENCE_TASK(&seq2);
			}
		}
			break;
		default:
			break;
		}

	}
}

void ScenarioCreator::walking_peds()
{
	for (int i = 0; i < nwPeds; i++)
	{
		if (PED::IS_PED_STOPPED(wPeds[i].ped))
		{
			int currentTime = (TIME::GET_CLOCK_HOURS()) * 60 + TIME::GET_CLOCK_MINUTES();
			if (wPeds[i].timeFix == -1)
				wPeds[i].timeFix = currentTime;
			if (true)
			{
				wPeds[i].goingTo = !wPeds[i].goingTo;
				wPeds[i].timeFix = -1;
				if (wPeds[i].goingTo)
					AI::TASK_GO_TO_COORD_ANY_MEANS(wPeds[i].ped, wPeds[i].to.x, wPeds[i].to.y, wPeds[i].to.z, wPeds[i].speed, 0, 0, 786603, 0xbf800000);
				else
					AI::TASK_GO_TO_COORD_ANY_MEANS(wPeds[i].ped, wPeds[i].from.x, wPeds[i].from.y, wPeds[i].from.z, wPeds[i].speed, 0, 0, 786603, 0xbf800000);
			}
		}
	}
}

void ScenarioCreator::loadFile()
{
	char fname[50] = "";
	strcat(fname, filesPath);
	strcat(fname, fileName);
	f = fopen(fname, "r");
	Vector3 cCoords, cRot;
	Vector3 vTP1, vTP2, vTP1_rot, vTP2_rot;
	int camMov;

	int stop;
	fscanf_s(f, "%d ", &camMov);
	if (camMov == 0)
		fscanf_s(f, "%f %f %f %d %f %f %f\n", &cCoords.x, &cCoords.y, &cCoords.z, &stop, &cRot.x, &cRot.y, &cRot.z);

	for (int i = 0; i < 10; i++) {
		Ped p = PED::CREATE_RANDOM_PED(cCoords.x, cCoords.y, cCoords.z);
		ENTITY::SET_PED_AS_NO_LONGER_NEEDED(&p);
	}

	fscanf_s(f, "%f %f %f %f %f %f\n", &vTP1.x, &vTP1.y, &vTP1.z, &vTP1_rot.x, &vTP1_rot.y, &vTP1_rot.z);
	fscanf_s(f, "%f %f %f %f %f %f\n", &vTP2.x, &vTP2.y, &vTP2.z, &vTP2_rot.x, &vTP2_rot.y, &vTP2_rot.z);

	Entity e = PLAYER::PLAYER_PED_ID();

	ENTITY::SET_ENTITY_COORDS_NO_OFFSET(e, vTP1.x, vTP1.y, vTP1.z, 0, 0, 1);
	lockCam(vTP1, vTP1_rot);
	WAIT(10000);

	ENTITY::SET_ENTITY_COORDS_NO_OFFSET(e, vTP2.x, vTP2.y, vTP2.z, 0, 0, 1);
	lockCam(vTP2, vTP2_rot);
	WAIT(10000);

	//ENTITY::SET_ENTITY_COORDS_NO_OFFSET(e, -1031.126831, -2726.527344, 14.794693, 0, 0, 1);
	ENTITY::SET_ENTITY_COORDS_NO_OFFSET(e, cCoords.x, cCoords.y, cCoords.z, 0, 0, 1);

	fixCoords = cCoords;
	WAIT(100);

	camLock = false;
	camLockChange();
	visible = true;
	ENTITY::SET_ENTITY_VISIBLE(PLAYER::PLAYER_PED_ID(), FALSE, true);
	CAM::SET_CAM_ROT(activeCam, cRot.x, cRot.y, cRot.z, 2);
	CAM::SET_CAM_COORD(activeCam, cCoords.x, cCoords.y, cCoords.z);

	Vector3 pos;
	while (readLine(f, &pos) >= 0) {
		spawn_peds(pos, nPeds);
		update();
	}

	if (stop == 1)
		stopCoords = true;

	fclose(f);

	sprintf_s(fname, "\"%s\" LOADED", fileName);
	set_status_text(fname);
}




void ScenarioCreator::file_menu()
{
	const float lineWidth = 250.0;
	const int lineCount = 4;
	menuActive = true;
	std::string caption = "FILE MANAGER";

	char lines[lineCount][50] = {
		"LOAD",
		"OVERWRITE",
		"SAVE NEW",
		"CLEAR LOG DATA"
	};
	char loadedFile[40];
	DWORD waitTime = 150;
	while (true)
	{
		// timed menu draw, used for pause after active line switch
		DWORD maxTickCount = GetTickCount() + waitTime;

		sprintf_s(loadedFile, "file:~y~ %s", fileName);

		readDirr();

		if (nFiles == 0){
			strcpy(fileName, "None");
			sprintf_s(lines[0], "LOAD	~y~[ no files ]");
		}
		else
			sprintf_s(lines[0], "LOAD	~y~[ log_%d.txt ]", currentFile);
		
		do
		{
			// draw menu
			draw_menu_line(caption, lineWidth, mHeight, mHeight * 2, mLeft, mTitle, false, true);
			for (int i = 0; i < lineCount; i++)
			if (i != activeLineIndexFile)
				draw_menu_line(lines[i], lineWidth, mHeight, mTopFlat + i * mTop, mLeft, mHeight, false, false);
			draw_menu_line(lines[activeLineIndexFile], lineWidth, mHeight, mTopFlat + activeLineIndexFile * mTop, mLeft, mHeight, true, false);

			// show time
			draw_menu_line(loadedFile, lineWidth, mHeight, mTopFlat + lineCount * mTop, mLeft, mHeight, false, false);

			update();
			WAIT(0);
		} while (GetTickCount() < maxTickCount);
		waitTime = 0;

		update();
		// process buttons
		
		if (bEnter)
		{
			switch (activeLineIndexFile)
			{
			case 0:
				if (nFiles > 0) {
					set_status_text("Not implemented!");
					//loadFile();
				}
				break;
			case 1:
				if (strcmp(fileName, "None") != 0)
					saveFile();
				break;
			case 2:
				sprintf_s(fileName, "log_%d.txt", nFiles + 1);
				saveFile();
				break;
			case 3:
				strcpy(logString, "");
				set_status_text("DATA CLEARED");
				break;
			default:
				break;
			}
			waitTime = 200;
		}
		if (bBack)
		{
			resetMenuCommands();
			break;
		}
		else if (bQuit)
		{
			resetMenuCommands();
			bQuit = true;
			break;
		}
		else if (bUp)
		{
			if (activeLineIndexFile == 0)
				activeLineIndexFile = lineCount;
			activeLineIndexFile--;
			waitTime = 150;
		}
		else if (bDown)
		{
			activeLineIndexFile++;
			if (activeLineIndexFile == lineCount)
				activeLineIndexFile = 0;
			waitTime = 150;
		}
		else if (bLeft)
		{
			if (activeLineIndexFile == 0) {
				if (currentFile == 1)
					currentFile = nFiles;
				else
					currentFile--;
			}
			waitTime = 150;
		}
		else if (bRight)
		{
			if (activeLineIndexFile == 0) {
				if (currentFile == nFiles)
					currentFile = 1;
				else
					currentFile++;
			}
			waitTime = 150;
		}
		resetMenuCommands();
	}

}
