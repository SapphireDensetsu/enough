/* build like this: gcc video_writer.c -I /usr/include/opencv -lcv -lhighgui */
/* Video Writer - tiny program for creating videos out of a list of images, using OpenCV */
/* Copyright 2007, Noam Lewis, enoughmail@googlegroups.com */
/*
    This file is part of Enough.

    Enough is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    Enough is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <opencv/cv.h>
#include <opencv/highgui.h>


#include <stdio.h>

#define VERIFY_NOT_NULL_GOTO(_var) do { \
        if (NULL == _var) {                       \
            printf("Error: " #_var " is NULL at %d\n", __LINE__);        \
            goto NULL_ERROR;                      \
        }                                         \
    } while (0)

int main(const int argc, const char const *argv[])
{

    CvVideoWriter *writer = NULL;
    IplImage *img = NULL;
    IplImage *converted = NULL;
    int i = 0;
    double fps = 0;

    CvSize target_size;
    float resize_factor;
    
    if (argc < 4) {
        printf("Usage: %s <out file> <fps> <inimage1> [inimage2] ...\n", argv[0]);
        return 1;
    }

    cvInitSystem(0, NULL);

    fps = strtod(argv[2], NULL);
    if (0 == fps) {
        printf("Please specify an fps > 0. Not '%s'\n", argv[3]);
        return 1;
    }

    img = cvLoadImage(argv[3], CV_LOAD_IMAGE_COLOR);
    VERIFY_NOT_NULL_GOTO(img);

    target_size = cvGetSize(img);
    resize_factor = 720.0 / target_size.width;
    target_size.width = 720;
    target_size.height = target_size.height * resize_factor;

    converted = cvCreateImage(target_size, IPL_DEPTH_8U, 3);

    /* The fourcc seems to have no effect, at least on linux. */
    writer = cvCreateVideoWriter(argv[1], CV_FOURCC('D','I','V','X'), fps, target_size, 1);
    VERIFY_NOT_NULL_GOTO(writer);

    for (i = 3; i < argc; i++) {
        printf("Loading %s...", argv[i]);
        
        img = cvLoadImage(argv[i], CV_LOAD_IMAGE_COLOR);
        VERIFY_NOT_NULL_GOTO(img);

        cvResize(img, converted, CV_INTER_LINEAR);
        cvWriteFrame(writer, converted);
        printf("Written.\n");
        cvReleaseImage(&img);
        
    }
    cvReleaseVideoWriter(&writer);
    printf("Done\n");

    goto _EXIT;
    
NULL_ERROR:
    return 2;
    
_EXIT:
    return 0;
}
