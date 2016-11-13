#include "header.h"
#include <stdio.h>

void printCvMat(CvMat *cvmat, int dp, int mode){
	int i, j;
	for(i= 0; i < cvmat->rows; i++){
		for(j = 0; j < cvmat->cols; j++){
			if(mode == 0){ //０は表示しない
				if(cvmGet(cvmat, i, j) == 0){
					printf(" ");
				}
				else{
					switch(dp){
						case 0: printf("%d", (int)cvmGet(cvmat, i, j)%10);break; //下一桁のみ表示
						case 1: printf("%.1f", cvmGet(cvmat, i, j));break;
						case 2: printf("%.2f", cvmGet(cvmat, i, j));break;
						case 3: printf("%.3f", cvmGet(cvmat, i, j));break;
						default: printf("%f", cvmGet(cvmat, i, j));break;
					}
				}
			}
			else if(mode == 1){
				switch(dp){
					case 0: printf("%.0f ", cvmGet(cvmat, i, j));break;
					case 1: printf("%.1f ", cvmGet(cvmat, i, j));break;
					case 2: printf("%.2f ", cvmGet(cvmat, i, j));break;
					case 3: printf("%.3f ", cvmGet(cvmat, i, j));break;
					default: printf("%f ", cvmGet(cvmat, i, j));break;
				}
			}
			else if(mode == 2){
				switch(dp){
					case 0: printf("%5d ", (int)cvmGet(cvmat, i, j));break;
					case 1: printf("%.1f ", cvmGet(cvmat, i, j));break;
					case 2: printf("%.2f ", cvmGet(cvmat, i, j));break;
					case 3: printf("%.3f ", cvmGet(cvmat, i, j));break;
					default: printf("%f ", cvmGet(cvmat, i, j));break;
				}
			}
		}
		printf("\n");
	}
}

void copyIplImage(const IplImage *original, IplImage *copied){
	int x, y;
	for(y = 0; y < original->height; y++){
		for(x = 0; x < original->width; x++){
			copied->imageData[copied->widthStep * y + x] = 
					original->imageData[original->widthStep * y + x];
		}
	}
}

void printTwoDCvPoint(int rows, int cols, CvPoint points[][cols]){
	int x, y;
	
	for(y = 0; y < rows; y++){
		for(x = 0; x < cols; x++){
			printf(" x:%d y:%d |", points[y][x].x, points[y][x].y);
		}
		printf("\n");
	}
}
/*
int makeNewDirectory(char *file_name){
	if (mkdir(file_name,
		S_IRUSR | S_IWUSR | S_IXUSR |
		S_IRGRP | S_IWGRP | S_IXGRP |
		S_IROTH | S_IXOTH | S_IXOTH) == 0) {
		printf("%s was created.\n", file_name);
	}
	else {
		printf("%s was not created.\n", file_name);
		perror("");
		return -1;
	}
	
	return 0;
}


void readCharData(){
	DIR *dir;
	struct dirent *dp;
	char buff[256];
	char *attached_dir_name = "_extracted";
	char *path_char_data = "./char_data/";
	char *path_extracted_chars = "./extracted_chars/";
	int i;
	
	if((dir=opendir(path_char_data))==NULL){
		perror("opendir");
		exit(-1);
	}
	
	for(dp=readdir(dir), i = 0; dp!=NULL, i < 1; dp=readdir(dir), i++){
	}
	
	for(dp=readdir(dir); dp!=NULL; dp=readdir(dir)){
		printf("%s\n",dp->d_name);
		strcpy(buff, path_extracted_chars);
		strcat(buff, dp->d_name);
		strcat(buff, attached_dir_name);
		makeNewDirectory(buff);
	}
	
	closedir(dir);
}
*/

void initializeIplImage(IplImage *image){
	int x, y;
	for(x = 0; x < image->widthStep; x++){
		for(y = 0; y < image->height; y++){
			image->imageData[image->widthStep * y + x] = 0;
		}
	}
}
