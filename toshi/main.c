#include <cxcore.h>
#include <cv.h>
#include <highgui.h>
#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/stat.h>


#include "header.h"

#include "dct.c"
#include "locate_char.c"

int main(int argc, char ** argv)
{
	strcpy(g_fin_name, argv[1]);
    g_dct_level = atoi(argv[2]);
    
	
	char filename[256];
	IplImage * image;
	IplImage * invImage;
	CvMat *dct,*idct, *dct_temp, *idct_temp, *cm;
	int x, y, i, j, k, l;
	char buff[256];
	
	strcpy(filename, sub_dir);
	strcat(filename, g_fin_name);
	
	//gray scaleで画像読み込み
	image = cvLoadImage( filename, CV_LOAD_IMAGE_GRAYSCALE );
	if( !image ){
		return -1;
	}
	printf("%s\n", filename);
	printf("width: %d   height: %d\n", image->width, image->height);
	
	//逆変換した画像の領域確保
	invImage = cvCreateImage( cvGetSize(image), IPL_DEPTH_8U, 1);
	
	//DCT,IDCT用の行列作成(double)
	dct = cvCreateMat(image->height, image->width, CV_64FC1);
	idct = cvCreateMat(image->height, image->width, CV_64FC1);
	
	//行列dctに画像データをコピー
	for(y=0; y<image->height; y++){
		for(x=0; x<image->width; x++){
			cvmSet(dct,
			y,
			x,
			(double)(unsigned char)(image->imageData[image->widthStep * y + x]));
		}
	}

	//printCvMat(dct, 0, 2);
	//DCT
	cvDCT( dct, dct, CV_DXT_FORWARD);
	//printCvMat(dct, 0, 2);
	
	makeIdctImage(dct, idct, invImage);
	//printCvMat(dct, 0, 2);
	cvSaveImage("idct_out.bmp", invImage, 0);
	
	locateTopAndBottom(invImage);
	
	
	
	return 0;
}