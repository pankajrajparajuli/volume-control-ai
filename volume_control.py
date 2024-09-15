import cv2  # Import OpenCV for video capture and image processing
import mediapipe as mp  # Import MediaPipe for hand tracking
import pyautogui
import time  # Import time for adding delays

# Initialize variables for hand landmarks
x1 = x2 = y1 = y2 = 0

# Initialize video capture from the webcam with reduced resolution
webcam = cv2.VideoCapture(0)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set frame width
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set frame height

# Create an instance of MediaPipe Hands for hand tracking with optimized settings
my_hands = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Create an instance of MediaPipe DrawingUtils for drawing landmarks on the image
drawing_utils = mp.solutions.drawing_utils

# Initialize variables for volume adjustment
last_action_time = time.time()
action_delay = 1.0  # Delay between volume changes in seconds

# Start an infinite loop to continuously capture frames from the webcam
while True:
    # Read a frame from the webcam
    _, image = webcam.read()

    # Get the dimensions of the image
    frame_height, frame_width, _ = image.shape

    # Convert the image from BGR to RGB (MediaPipe requires RGB images)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the RGB image to detect hands and landmarks
    output = my_hands.process(rgb_image)

    # Get the list of detected hand landmarks
    hands = output.multi_hand_landmarks

    # Check if any hands were detected
    if hands:
        # Loop through each detected hand
        for hand in hands:
            # Draw landmarks on the original image
            drawing_utils.draw_landmarks(image, hand)

            # Get the list of landmarks for the current hand
            landmarks = hand.landmark

            # Loop through each landmark
            for id, landmark in enumerate(landmarks):
                # Convert the normalized coordinates of the landmark to pixel coordinates
                x = int(landmark.x * frame_width)  # Use frame_width for x-coordinate
                y = int(landmark.y * frame_height)  # Use frame_height for y-coordinate

                # Draw a circle at the tip of the index finger (landmark ID 8)
                if id == 8:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x1 = x
                    y1 = y

                # Draw a circle at the tip of the thumb (landmark ID 4)
                if id == 4:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 0, 255), thickness=3)
                    x2 = x
                    y2 = y

                # Draw a line between the thumb and index finger
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)

                # Calculate the distance between the thumb and index finger
                dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

                # Adjust volume based on the distance with a delay
                current_time = time.time()
                if dist > 50 and current_time - last_action_time > action_delay:
                    pyautogui.press("volumeup")
                    last_action_time = current_time
                elif dist <= 50 and current_time - last_action_time > action_delay:
                    pyautogui.press("volumedown")
                    last_action_time = current_time

    # Display the processed image in a window titled "Hand volume control"
    cv2.imshow("Hand volume control", image)

    # Wait for 10 milliseconds and check if the 'Esc' key was pressed (ASCII 27)
    key = cv2.waitKey(10)
    if key == 27:  # 'Esc' key to exit the loop
        break

# Release the webcam and close all OpenCV windows
webcam.release()
cv2.destroyAllWindows()
