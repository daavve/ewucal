
void scaleCharSize(int *to_top, int *to_bottom, int *to_left, int *to_right
				,int val_x, int val_y
				,int map_height, int map_width, int top_bottom_map[][map_width]){
	int x, y;
	char first_time;
	(*to_top) = 0, (*to_bottom) = 0, (*to_left) = 0, (*to_right) = 0;
	
	first_time = 1;
	for(x = val_x, y = val_y; y >= 0 && top_bottom_map[y][x] >= 0; y--, (*to_top)++){
		if(first_time){
			first_time = 0;
			(*to_top)--;
		}
	}
	first_time = 1;
	for(x = val_x, y = val_y; y < map_height && top_bottom_map[y][x] >= 0; y++, (*to_bottom)++){
		if(first_time){
			first_time = 0;
			(*to_bottom)--;
		}
	}
	first_time = 1;
	for(x = val_x, y = val_y; x >= 0 && top_bottom_map[y][x] >= 0; x--, (*to_left)++){
		if(first_time){
			first_time = 0;
			(*to_left)--;
		}
	}
	first_time = 1;
	for(x = val_x, y = val_y; x < map_width && top_bottom_map[y][x] >= 0; x++, (*to_right)++){
		if(first_time){
			first_time = 0;
			(*to_right)--;
		}
	}
}

void extractCharFromTopBottomMap(int val_x, int val_y, int index, int map_height, int map_width, int top_bottom_map[][map_width]){
	printf("%d. Extract Char @ x:%d y%d\n", index, val_x, val_y);
	
	int x, y;
	char filename[256];
	IplImage *image, *image_out;
	char *fout_name = "char";
	char *fout_extention = ".bmp";
	char buff[256];
	char itoa_buff[16];
	int to_top, to_bottom, to_left, to_right;
	
	strcpy(filename, sub_dir);
	strcat(filename, g_fin_name);
	image = cvLoadImage( filename, CV_LOAD_IMAGE_GRAYSCALE );
	if( !image ){
		return;
	}
	
	scaleCharSize(&to_top, &to_bottom, &to_left, &to_right, val_x, val_y, map_height, map_width, top_bottom_map);
	printf("to_top:%d | to_bottom:%d | to_left:%d | to_right:%d\n", to_top, to_bottom, to_left, to_right);
	
	image_out = cvCreateImage( cvSize(to_left+to_right+1, to_top+to_bottom+1), IPL_DEPTH_8U, 1);
	initializeIplImage(image_out);
	
	for(y = val_y - to_top; y <= val_y + to_bottom; y++){
		for(x = val_x - to_left; x <= val_x + to_right; x++){
			if( (y>=0 && y < image->height) && (x>=0 && x < image->width) ){
				//printf("y:%d, x:%d\n", (y-val_y+to_top), (x-val_x+to_left));
				image_out->imageData[image_out->widthStep * (y-val_y+to_top) + (x-val_x+to_left)] = 
					image->imageData[image->widthStep * y + x];
			}
			else{
				//image_out->imageData[image_out->widthStep * y + x] = 0;
			}
		}
	}
	
	strcpy(buff, sub_dir);
	strcat(buff, "extracted_chars/");
	strcat(buff, fout_name);
	sprintf(itoa_buff, "%d", index);
	strcat(buff, itoa_buff);
	strcat(buff, fout_extention);
	cvSaveImage(buff, image_out, 0);
}

void locateTopAndBottom(IplImage *image){
	int x, y;
	int val;
	int prev_val;
	int next_val;
	int equal_count;
	//printf("height:%d  width:%d\n", image->height, image->width);
	IplImage *copied = cvCreateImage( cvGetSize(image), IPL_DEPTH_8U, 1);
	//printf("locateTopAndBottom starts here.\n");
	int top_bottom_map[image->height][image->width];
	//printf("locateTopAndBottom starts here.\n");
	copyIplImage(image, copied);
	
	initializeIntTwoDArray(image->height, image->width, top_bottom_map);
	
	//printf("locateTopAndBottom starts here.\n");
	
	//X-axis scan (draw vertical lines)
	for(y = 0; y < image->height; y++){
		equal_count = 0;
		prev_val = (int)(unsigned char)(image->imageData[image->widthStep * y + 0]);
		for(x = 1; x < image->width-1; x++){
			//printf("y: %d | x: %d\n", y, x);
			val = (int)(unsigned char)(image->imageData[image->widthStep * y + x]);
			next_val = (int)(unsigned char)(image->imageData[image->widthStep * y + (x+1)]);
			if(prev_val < val && val > next_val){ //case top
				//printf("Vertex prev:%d val:%d next:%d | x: %d | y: %d\n", prev_val, val, next_val, x, y);
				copied->imageData[copied->widthStep * y + (x - equal_count/2)] = 0;
				top_bottom_map[y][x - equal_count/2] = 1;
			}
			else if(prev_val > val && val < next_val){ //case bottom
				copied->imageData[copied->widthStep * y + (x - equal_count/2)] = 255;
				top_bottom_map[y][x - equal_count/2] = -1;
			}
			if(val == next_val){
				equal_count++;
			}
			else{
				equal_count = 0;
				prev_val = val;
			}
		}
	}
	printf("locateTopAndBottom - X-axis scan done. (vertical lines drawn)\n");
	
	//Y-axis scan (draw Horizontal lines)
	for(x = 0; x < image->width; x++){
		equal_count = 0;
		prev_val = (int)(unsigned char)(image->imageData[image->widthStep * 0 + x]);
		for(y = 1; y < image->height-1; y++){
			val = (int)(unsigned char)(image->imageData[image->widthStep * y + x]);
			next_val = (int)(unsigned char)(image->imageData[image->widthStep * (y+1) + x]);
			if(prev_val < val && val > next_val){ //case top
				//printf("Vertex prev:%d val:%d next:%d | x: %d | y: %d\n", prev_val, val, next_val, x, y);
				if(top_bottom_map[y - equal_count/2][x] == 1){ //if crossed
					top_bottom_map[y - equal_count/2][x] = 3;
					copied->imageData[copied->widthStep * (y - equal_count/2) + x] = 255;
				}
				else if(top_bottom_map[y - equal_count/2][x] == -1){ // if top and bottom crossed
					top_bottom_map[y - equal_count/2][x] = -4;
					copied->imageData[copied->widthStep * (y - equal_count/2) + x] = 123;
				}
				else{
					top_bottom_map[y - equal_count/2][x] = 2;
					copied->imageData[copied->widthStep * (y - equal_count/2) + x] = 0;
				}
			}
			if(prev_val > val && val < next_val){ //case bottom
				//printf("Vertex prev:%d val:%d next:%d | x: %d | y: %d\n", prev_val, val, next_val, x, y);
				if(top_bottom_map[y - equal_count/2][x] == -1){ //if bottom crossed
					top_bottom_map[y - equal_count/2][x] = -3;
					copied->imageData[copied->widthStep * (y - equal_count/2) + x] = 255;
				}
				else if(top_bottom_map[y - equal_count/2][x] == 1){ //if bottom and top crossed
					top_bottom_map[y - equal_count/2][x] = -4;
					copied->imageData[copied->widthStep * (y - equal_count/2) + x] = 123;
				}
				else{
					top_bottom_map[y - equal_count/2][x] = -2;
					copied->imageData[copied->widthStep * (y - equal_count/2) + x] = 255;
				}
			}
			if(val == next_val){
				equal_count++;
			}
			else{
				equal_count = 0;
				prev_val = val;
			}
		}
	}
	printf("locateTopAndBottom - Y-axis scan done. (horizontal lines drawn)\n");
	
	cvSaveImage("locate_top_bottom.bmp", copied, 0);
	printf("a image \"locate_top_bottom.bmp\" saved.\n");
	
	int index = 0;
	for(y = 0; y < image->height; y++){
		for(x = 0; x < image->width; x++){
			if(top_bottom_map[y][x] == 3){
				index++;
				extractCharFromTopBottomMap(x, y, index, image->height, image->width, top_bottom_map);
				//return;
			}
		}
	}
	printf("%d characters were extracted.\n", index);
}
