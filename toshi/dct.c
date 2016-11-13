#include "header.h"
#include <stdio.h>

void reduceHigherFreq(CvMat *cm, int div){
	int x, y;
	
	for(y = 0; y < cm->rows; y++){
		for(x = 0; x < cm->cols; x++){
			if(y >= ( (-1 * (cm->rows / cm->cols) * x) + (2*cm->rows/div) ) ){
				cvmSet(cm, y, x, 0);
			}
		}
	}
	
	//for print out purpose only
	if(0){
		printf("print array\n");
		for(y=0; y < cm->rows; y++){
			for(x=0; x < cm->cols; x++){
				//printf("%d", a[i][j]%10);
				int temp = ((int)cvmGet(cm, y, x))%10;
				if(temp < 0){
					temp *= -1;
				}
				printf("%d", temp);
			}
			putchar('\n');
		}
	}
}


void reduceHigherFreqInSquare(CvMat *cm, int div){
	int x=0, y=0;
	
	for(y = 0; y < cm->rows; y++){
		for(x = 0; x < cm->cols; x++){
			if(x >= cm->cols/div || y >= cm->cols/div){
				cvmSet(cm, y, x, 0);
			}
			//printf("%d ", (int)(cvmGet(cm, y, x))%10);
		}
		//printf("\n");
	}
	
}

void makeIdctImage(CvMat *dct, CvMat *idct, IplImage *invImage, int g_dct_level){
	int x, y;
	
	reduceHigherFreq(dct, g_dct_level);
	//reduceHigherFreqInSquare(dct, g_dct_level);
	
	//IDCT
	cvDCT( dct, idct, CV_DXT_INVERSE);
	//逆変換用画像にデータをコピー
	for(y=0; y<invImage->height; y++){
		for(x=0; x<invImage->width; x++){
			invImage->imageData[invImage->widthStep * y + x] = (unsigned char)cvmGet(idct,y,x);
		}
	}
}

