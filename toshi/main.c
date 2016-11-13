#include "header.h"
#include <opencv2/highgui/highgui_c.h>

// argv[1] = filename inside chars
// argv[2] = segment size
int main(int argc, char ** argv)
{
    int g_dct_level = atoi(argv[2]);
    char filename[256];
    strcpy(filename, argv[1]);
    IplImage * image;
    IplImage * invImage;
    CvMat *dct,*idct;
    int x, y;
    
    
    //gray scaleで画像読み込み
    image = cvLoadImage( filename, CV_LOAD_IMAGE_GRAYSCALE );
    if( !image ){
        return -1;
    }
    
    if(image->width % 2) //transform can only handle even numbered rows
    {
        --image->width;
    }
    if(image->height % 2)
    {
        --image->height;
    }
    
    
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
    
    makeIdctImage(dct, idct, invImage, g_dct_level);
    //printCvMat(dct, 0, 2);
    
    locateTopAndBottom(invImage);
    
    
    
    return 0;
}
