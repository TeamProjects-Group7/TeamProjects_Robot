from picamera.array import PiRGBArray
from picamera import PiCamera
import datetime
import imutils
import time
import cv2

class MotionDetector:
	def __init__(self, cameraWarmupTime : float, framerate: int):
		self.framerate = framerate
		self.camera = PiCamera()
		self.camera.resolution = (640, 480)
		self.camera.framerate = self.framerate
		self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
		time.sleep(cameraWarmupTime)

		self.camera.capture(self.rawCapture, format="bgr")
		frame = self.rawCapture.array
		cv2.imshow("Security Feed", frame)
		
		cv2.waitKey(1)

	def __del__(self):
		self.camera.stop()
		cv2.destroyAllWindows()


	def scan(self, time: int):
		frameCount = 0
		referenceFrame = None
		scanning = True
		# loop over the frames of the video
		for capture in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
			if not scanning:
				break
			frame = capture.array
			text = "No Motion"

			if frame is None:
				break

			gray = processFrame(frame)

			if referenceFrame is None:
				referenceFrame = gray
				continue

			contours = getContoursAbsolute(referenceFrame, gray, False)
			#contours = getContoursWeighted(referenceFrame, gray, 5, True)

			text = checkMotion(contours, 5000, frame)

			updateStatus(frame, text)

			cv2.imshow("Security Feed", frame)

			if (frameCount > (self.framerate * time)):
				scanning = False
			else:
				frameCount += 1
			cv2.waitKey(1)
			
			# clear the stream in preparation for the next frame
			self.rawCapture.truncate(0)

		frame = self.read_camera()
		cv2.imshow("Security Feed", frame)
		cv2.waitKey(1)


def processFrame(frame):
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	return gray

# threshold the delta image, dilate the thresholded image to fill
# in holes, then find contours on thresholded image
def getContoursAbsolute(referenceFrame, currentFrame, displayResults: bool):
	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(referenceFrame, currentFrame)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	if displayResults:
		cv2.imshow("Thresh", thresh)
		cv2.imshow("Frame Delta", frameDelta)

	return imutils.grab_contours(contours)

def getContoursWeighted(referenceFrame, currentFrame, deltaThresh, displayResults: bool):
	avg = referenceFrame.copy().astype("float")
	cv2.accumulateWeighted(currentFrame, avg, 0.5)
	frameDelta = cv2.absdiff(currentFrame, cv2.convertScaleAbs(avg))

	thresh = cv2.threshold(frameDelta, deltaThresh, 255,
	cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	if displayResults:
		cv2.imshow("Thresh", thresh)
		cv2.imshow("Frame Delta", frameDelta)

	return imutils.grab_contours(contours)

def checkMotion(contours, minArea, frame):
	text = "Not Detected"
	for c in contours:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < minArea:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Motion Detected"
	return text

def updateStatus(frame, statusText: str):
	cv2.putText(frame, "Scanning...: {}".format(statusText), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)