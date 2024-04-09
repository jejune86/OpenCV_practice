import numpy as np
import cv2 as cv


def select_img_from_video(video_file, board_pattern, select_all=False, wait_msec=10, wnd_name='Camera Calibration'):
    # Open a video
    video = cv.VideoCapture(video_file)
    assert video.isOpened()

    # Select images
    img_select = []
    while True:
        # Grab an images from the video
        valid, img = video.read()
        if not valid:
            break

        if select_all:
            img_select.append(img)
        else:
            # Show the image
            display = img.copy()
            cv.putText(display, f'NSelect: {len(img_select)}', (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
            cv.imshow(wnd_name, display)

            # Process the key event
            key = cv.waitKey(wait_msec)
            if key == ord(' '):             # Space: Pause and show corners
                complete, pts = cv.findChessboardCorners(img, board_pattern)
                cv.drawChessboardCorners(display, board_pattern, pts, complete)
                cv.imshow(wnd_name, display)
                key = cv.waitKey()
                if key == ord('\r'):
                    img_select.append(img) # Enter: Select the image
            if key == 27:                  # ESC: Exit (Complete image selection)
                break

    cv.destroyAllWindows()
    return img_select

def calib_camera_from_chessboard(images, board_pattern, board_cellsize, K=None, dist_coeff=None, calib_flags=None):
    # Find 2D corner points from given images
    img_points = []
    for img in images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        complete, pts = cv.findChessboardCorners(gray, board_pattern)
        if complete:
            img_points.append(pts)
    assert len(img_points) > 0

    # Prepare 3D points of the chess board
    obj_pts = [[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])]
    obj_points = [np.array(obj_pts, dtype=np.float32) * board_cellsize] * len(img_points) # Must be `np.float32`

    # Calibrate the camera
    return cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], K, dist_coeff, flags=calib_flags)


# The given video and calibration data
video_file = 'Pose_Estimation_with AR\calibration.mp4'
board_pattern = (10, 7)
board_cellsize = 0.025  

img_select = select_img_from_video(video_file, board_pattern)
assert len(img_select) > 0, 'There is no selected images!'
rms, K, dist_coeff, rvecs, tvecs = calib_camera_from_chessboard(img_select, board_pattern, board_cellsize)

board_criteria = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FAST_CHECK

# Open a video
video = cv.VideoCapture(video_file)
assert video.isOpened(), 'Cannot read the given input, ' + video_file

# Prepare a 3D box for simple AR
pyramid_base = board_cellsize * np.array([[4, 2,  0], [5, 2,  0], [5, 4,  0], [4, 4,  0]])
pyramid_apex = board_cellsize * np.array([[4.5, 3, -1]])
# Prepare 3D points on a chessboard
obj_points = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])])

# Run pose estimation
while True:
    # Read an image from the video
    valid, img = video.read()
    if not valid:
        break

    # Estimate the camera pose
    success, img_points = cv.findChessboardCorners(img, board_pattern, board_criteria)
    if success:
        ret, rvec, tvec = cv.solvePnP(obj_points, img_points, K, dist_coeff)

        # Draw pyramid
        pyramid_base_proj, _ = cv.projectPoints(pyramid_base, rvec, tvec, K, dist_coeff)
        pyramid_apex_proj, _ = cv.projectPoints(pyramid_apex, rvec, tvec, K, dist_coeff)

        # Draw lines between the apex and base
        for i in range(4):
            cv.line(img, tuple(np.int32(pyramid_base_proj[i].flatten())), tuple(np.int32(pyramid_apex_proj[0].flatten())), (0, 0, 255), 2)

        # Draw the base of the pyramid
        for i in range(4):
            cv.line(img, tuple(np.int32(pyramid_base_proj[i-1].flatten())), tuple(np.int32(pyramid_base_proj[i].flatten())), (0, 0, 255), 2)

        # Print the camera position
        R, _ = cv.Rodrigues(rvec) # Alternative) `scipy.spatial.transform.Rotation`
        p = (-R.T @ tvec).flatten()
        info = f'XYZ: [{p[0]:.3f} {p[1]:.3f} {p[2]:.3f}]'
        cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

    # Show the image and process the key event
    cv.imshow('Pose Estimation (Chessboard)', img)
    key = cv.waitKey(10)
    if key == ord(' '):
        key = cv.waitKey()
    if key == 27: # ESC
        break

video.release()
cv.destroyAllWindows()