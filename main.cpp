
//#include "IVideoSource.h"
#include "Source.h"
#include "VideoProcessThread.h"
#include "VideoEncodeThread.h"
#include "RtmpProcessThread.h"
#include "AudioEncodeThread.h"
#include "AudioProcessThread.h"
#include "ShmQueue.h"
#include <iostream>
#include <map>

const int w = 640;
const int h = 480;
const int fps = 15;
const int keyframe = 3;
const int vbitrate = 256;

const int sample = 44100;
const int chnl = 2;
const int bit = 16;
const int abitrate = 48;

char * rtmp = "rtmp://202.91.251.12/olived3/2129";

int main() {
	std::cout << "test" << std::endl;
	std::cout << "master first commit after branch commit" << std::endl;
	std::cout << "sqn_test"  <<std::endl;
	/*std::cout << IVideoSourceInterfaceFnNameLen << std::endl;
	for (int i=0; i<IVideoSourceInterfaceFnNameLen; ++i) {
		std::cout << IVideoSourceInterfaceFnName[i] << std::endl;
	}*/
	CSource capture_source;
	std::vector<CString> config;
#ifdef _DEBUG
	capture_source.LoadModule(L"CamCaptureSourceD.dll", config);
#else
	capture_source.LoadModule(L"CamCaptureSource.dll", config);
#endif

	std::map<CString, CString> devices;
	capture_source.ListVideoDevices(devices);
	//capture_source.SetVideoDevice(L"@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{8E14549A-DB61-4309-AFA1-3578E927E933}");
	//capture_source.SetVideoDevice(L"@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\6RoomsCamV9");
	//capture_source.SetVideoDevice(L"@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{7F879077-C93C-4EB6-8C91-C70029959C2D}");
	capture_source.SetVideoDevice(L"@device:pnp:\\\\?\\usb#vid_5986&pid_0364&mi_00#7&ff87627&0&0000#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\\global");
	//capture_source.SetDevice(L"@device:pnp:\\\\?\\usb#vid_0ac8&pid_3016&mi_00#7&2970f0e&0&0000#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\\global");
	std::vector<CString> ts;
	std::vector<int> ws;
	std::vector<int> hs;
	capture_source.GetVideoFormat(ts, ws, hs);
	capture_source.SetVideoFormat(w, h, fps);
	capture_source.SetVideoLayerType(VIDEO_LAYER_BACKGROUND, 0, 0.0f);

	std::map<CString, CString> audio_devices;
	CSource audio_source;
	audio_source.LoadModule(L"AudioCaptureSource.dll", config);
	audio_source.ListAudioDevices(audio_devices);
	audio_source.SetAudioDevice(L"@device:cm:{33D9A762-90C8-11D0-BD43-00A0C911CE86}\\Âó¿Ë·ç (Realtek High Definition Au");
	audio_source.SetAudioFormat(sample, bit, chnl);

	//capture_source.StartPtr();
	/*unsigned int timestamp = 0;
	CxImage image;
	while(!capture_source.GetOneImagePtr(timestamp, image, 0)) {
	}
	image.Save(L"test.jpg", CXIMAGE_FORMAT_JPG);
	capture_source.StopPtr();*/

	CVideoProcessThread video_process_thread(w, h, fps);
	video_process_thread.AddVideoSource(&capture_source);

	CAudioProcessThread audio_precess_thread(sample, bit, chnl);
	audio_precess_thread.AddAudioSource(&audio_source);

	CRtmpProcessThread rtmp_process_thread;
	rtmp_process_thread.SetRtmpUrl(rtmp);
	rtmp_process_thread.SetVideoInfo(w, h, fps);

	CAudioEncodeThread audio_encode_thread(&audio_precess_thread, &rtmp_process_thread,
		sample, bit, chnl, abitrate);

	rtmp_process_thread.SetAudioInfo(sample, bit, chnl, audio_encode_thread.IsSupportSBR(),
		audio_encode_thread.IsSupportPS(), audio_encode_thread.GetMaxOutBytes());

	CVideoEncodeThread video_encode_thread(&video_process_thread,
		&rtmp_process_thread,
		w, h, fps, keyframe, vbitrate);

	video_process_thread.Start();
	video_encode_thread.Start();

	audio_precess_thread.Start();
	audio_encode_thread.Start();

	rtmp_process_thread.Start();

	while (true) {
		Sleep(100);
	}

	capture_source.UnloadModule();

	//int in;
	//std::cin >> in;
	return 0;
}
