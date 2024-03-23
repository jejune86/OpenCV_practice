import cv2 as cv

def cartoonize(img) :
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Apply median blur to reduce noise
    gray = cv.medianBlur(gray, 5)
    # Detect edges using adaptive thresholding
    edges = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 9)
    # Convert the image to color
    color = cv.bilateralFilter(img, 9, 300, 300)
    # Combine the color image with the edges mask
    cartoon = cv.bitwise_and(color, color, mask=edges)
    return cartoon

option = input("Enter 'v' for video or 'i' for image: ")

if option == 'v':
    video = cv.VideoCapture('Cartoonizer/input/sample1.mp4')
    if video.isOpened():
        fps = video.get(cv.CAP_PROP_FPS)
        wait_msec = int(1/fps*1000)

        width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv.VideoWriter_fourcc(*'XVID')
        rec = cv.VideoWriter('Cartoonizer/output/record.avi', fourcc, fps, (width, height))

        while True:
            valid, img = video.read()
            if not valid:
                break

            cartoon = cartoonize(img)

            rec.write(cartoon)

            cartoon_screen = cv.resize(cartoon, (width//6, height//6)) # 화면에 표시되는 창의 크기를 절반으로 줄임
            cv.imshow('Cartoonized Video', cartoon_screen)

            key = cv.waitKey(wait_msec)
            if key == ord('q'):
                break

        video.release()
        rec.release()
        cv.destroyAllWindows()

elif option == 'i':
    img = cv.imread('Cartoonizer/input/sampleImg2.png')
    cartoon = cartoonize(img)
    cv.imshow('Cartoonized Image', cartoon)
    cv.imwrite('Cartoonizer/output/resultImg2.png', cartoon)
    cv.waitKey(0)
    cv.destroyAllWindows()

else:
    print("Invalid option. Please enter 'v' or 'i'.")
