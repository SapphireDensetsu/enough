#include <opencv/cv.h>
#include <opencv/highgui.h>


#include <stdio.h>

#define VERIFY_NOT_NULL_GOTO(_var) do { \
        if (NULL == _var) {                       \
            printf("Error: " #_var " is NULL\n"); \
            goto NULL_ERROR;                      \
        }                                         \
    } while (0)

int main(const int argc, const char const *argv[])
{

    CvVideoWriter *writer = NULL;
    IplImage *img = NULL;
    IplImage *converted = NULL;
    int i = 0;

    CvSize target_size;
    float resize_factor;
    
    if (argc < 3) {
        printf("Usage: %s <out file> <inimage1> [inimage2] ...\n", argv[0]);
        return 1;
    }

    cvInitSystem(0, NULL);

    img = cvLoadImage(argv[2], CV_LOAD_IMAGE_COLOR);
    VERIFY_NOT_NULL_GOTO(img);

    target_size = cvGetSize(img);
    resize_factor = 720.0 / target_size.width;
    target_size.width = 720;
    target_size.height = target_size.height * resize_factor;

    converted = cvCreateImage(target_size, IPL_DEPTH_8U, 3);
    
    writer = cvCreateVideoWriter(argv[1], CV_FOURCC('D','I','V','X'), 20, target_size, 1);
    VERIFY_NOT_NULL_GOTO(writer);

    for (i = 2; i < argc; i++) {
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
