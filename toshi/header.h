#ifndef HEADER_FILE
#define HEADER_FILE
#define INPUT_MODE 1
#include <opencv2/core/core_c.h> //Provides CvMat

// dct.c //
void reduceHigherFreq(CvMat *cm, int div);
void makeIdctImage(CvMat *dct, CvMat *idct, IplImage *invImage, int g_dct_level);

// ex-header.c // <- These functions used to live inside header.h
void copyIplImage(const IplImage *original, IplImage *copied);

// locate_char.c //
void locateTopAndBottom(IplImage *image);
/*
#include <opencv/cv.h>

char g_fin_name[128];



*
void initializeIntTwoDArray(int height, int width, int [height][width]);
void printCvMat(CvMat *cvmat, int dp, int mode);
void printTwoDCvPoint(int rows, int cols, CvPoint points[][cols]);
int makeNewDirectory(char *file_name);
void readCharData();
void initializeIplImage(IplImage *image);
*/
#endif

