import cv2
import pickle

# Load the video
video_path = 'video.mp4'
cap = cv2.VideoCapture(video_path)

# Check if the video is available
if not cap.isOpened():
    print("Error opening the video")
    exit()

everything = []


framcounter = 0
# Read the video frame by frame
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("The video has ended or an error occurred while reading the frame.")
        break

    # Resize the video for the in-game canvas
    resized_frame = cv2.resize(frame, (156, 104), interpolation=cv2.INTER_AREA)
    frames = []
    #print out the current frame number
    print(framcounter)
    framcounter += 1
    # go through the frame by a 4x4 segment
    for i in range(0, 156, 4):
        for j in range(0, 104, 4):
            # kocka = cube
            kocka = []
            # go through the current segment
            for x in range(4):
                for y in range(4):
                    # check if the current pixel's red value is greater than 127 (white)
                    if resized_frame[j+y][i+x][0] > 127:
                        # append 9 (white - reality) to the cube
                        kocka.append(9)
                    else:
                        # append 8 (black - void) to the cube
                        kocka.append(8)
            # append the cube to the frame
            frames.append(kocka)
    # append the frame to everything (it's the whole video in one array, where array[0] is the 1st frame, array[0][0] is the 1st cube of the 1st frame)
    everything.append(frames)

# save the converted video to a file, since it's a one time conversion (it's a huge file, for bad apple it is ~200MB)
with open('my_array.pkl', 'wb') as f:
    pickle.dump(everything, f)
# Releases resources and closes windows
cap.release()
cv2.destroyAllWindows()
