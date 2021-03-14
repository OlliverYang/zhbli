/*
	THIS FILE IS A PART OF GTA V SCRIPT HOOK SDK
				http://dev-c.com			
			(C) Alexander Blade 2015
*/

#include "scenario.h"
#include <string.h>
#include <direct.h>
#include <fstream>
#include "files.h"
#include <list>
#include <experimental/filesystem>
#include "keyboard.h"

DWORD	vehUpdateTime;
DWORD	pedUpdateTime;
using namespace std;
namespace fs = std::experimental::filesystem;


void record() {
	char path[] = "JTA\\";
	char scenarios_path[] = "JTA-Scenarios\\";

	_mkdir(path);

	int max_samples = 30 * 60 * 1 + 1;
	DatasetAnnotator* S;

	int seq_number = 0;

	// Day sequences
	for (auto &p : fs::recursive_directory_iterator(scenarios_path)) {
		if (fs::is_regular_file(p)) {
			int nsamples = 0;
			std::string output_path = std::string(path) + std::string("seq_") + std::to_string(seq_number);
			_mkdir(output_path.c_str());
			S = new DatasetAnnotator(output_path, p.path().string().c_str(), max_samples, 0);
			Sleep(10);
			while (nsamples < max_samples) {
				nsamples = (*S).update();
				WAIT(0);
			}
			delete static_cast <DatasetAnnotator *>(S);
			seq_number++;
		}
	}

	// Night sequences
	for (auto &p : fs::recursive_directory_iterator(scenarios_path)) {
		if (fs::is_regular_file(p)) {
			int nsamples = 0;
			std::string output_path = std::string(path) + std::string("\\seq_") + std::to_string(seq_number);
			_mkdir(output_path.c_str());
			S = new DatasetAnnotator(output_path, p.path().string().c_str(), max_samples, 1);
			Sleep(10);
			while (nsamples < max_samples) {
				nsamples = (*S).update();
				WAIT(0);
			}
			delete static_cast <DatasetAnnotator *>(S);
			seq_number++;
		}
	}

}


void main()
{	
	std::ofstream strm("logme.txt");
	while (true) {
		if (IsKeyJustUp(VK_F8)) {
			strm << "gg\n";
			record();
		}
		WAIT(0);

	}
}

void ScriptMain()
{	
	srand(GetTickCount());
	main();
}
