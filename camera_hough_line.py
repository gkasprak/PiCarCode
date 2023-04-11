import cv2
import numpy as np

def draw_the_lines(img, lines):
	imge = np.copy(img)
	blank_image = np.zeros((imge.shape[0], imge.shape[1], 3), dtype=np.uint8)
	for line in lines:
		for x1, y1, x2, y2 in line:
			cv2.line(blank_image, (x1,y1), (x2,y2), (0,255,0), thickness = 3)
			imge  = cv2.addWeighted(imge, .8, blank_image, 1, 0.0)
	return imge

if __name__ == '__main__':
	cap = cv2.VideoCapture(0)
	
	if not cap.isOpened():
		print("Cannot open camera")
		exit()

	while True:

		# Capture frame-by-frame
		ret, frame = cap.read()

		# if frame is read correctly ret is True
		if not ret:
			print("Can't receive frame (stream end?). Exiting ...")
			break
		
		gray_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		blur_image = cv2.medianBlur(gray_image, 81)
		canny_image = cv2.Canny(blur, 100, 200, apertureSize = 5)
		lines = cv2.HoughLinesP(canny_image, rho=2, theta=np.pi / 120, threshold = 120, lines = np.array([]), minLineLength = 300, maxLineGap = 35)
		# Display the resulting frame
		cv.imshow('frame', canny_image)

		if cv.waitKey(1) == ord('q'):
			break

	# When everything done, release the capture
	cap.release()
	cv.destroyAllWindows()
	
						 