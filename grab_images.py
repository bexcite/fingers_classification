import cv2
import os
import time

# Run this script from the same directory as your Data folder

# Grab your webcam on local machine
cap = cv2.VideoCapture(0)

# Give image a name type
name_type = 'Small_cat'

# Initialize photo count
number = 0

# Specify the name of the directory that has been premade and be sure that it's the name of your class
# Remember this directory name serves as your datas label for that particular class
data_dir = 'Data'
data_dir_stamp = time.strftime("%G%m%d_%H%M%S")
# print("data_dir = {}".format(data_dir))
set_dir = 'Cat'

print ("Photo capture enabled! Press any key to take photos! Pressed key - is a class.")

nums = dict()

curr_key = None

def crop_resize_rect(frame, size):
  fr = frame
  wy, wx = frame.shape[0], frame.shape[1]

  # Crop if not rect
  if wy > wx:
    b = int((wy / 2 - wx / 2))
    e = int((wy / 2 + wx / 2))
    fr = fr[b:e,:]
  elif wx > wy:
    b = int((wx / 2 - wy / 2))
    e = int((wx / 2 + wy / 2))
    fr = fr[:,b:e]

  # Resize
  fr = cv2.resize(fr,(size, size), interpolation = cv2.INTER_NEAREST)
  return fr

while True:
    # Read in single frame from webcam
    ret, frame = cap.read()

    # print('size = {}'.format(frame.shape))

    newWidth = 256
    # newHeight = int(640 * frame.shape[0]/frame.shape[1])

    # frame = cv2.resize(frame,(newWidth, newHeight), interpolation = cv2.INTER_NEAREST)
    frame = crop_resize_rect(frame, newWidth)

    # Use this line locally to display the current frame
    cv2.imshow('Color Picture', frame)

    key = cv2.waitKey(200)

    # Use esc to take photos when you're ready
    if (key & 0xFF >= ord('a') and key & 0xFF <= ord('z')) or (key & 0xFF >= ord('0') and key & 0xFF <= ord('9')):
        curr_key = chr(key)

        # If you want them gray
        #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        # If you want to resize the image
        # gray_resize = cv2.resize(gray,(360,360), interpolation = cv2.INTER_NEAREST)



    # Print key for debug
    if key > 0:
        print('waitKey = {}, code = {}'.format(chr(key), key))

    # Stop capture on Space
    if key & 0xFF == ord(' '):
      curr_key = None
      print("Press any key to take photos.")

    # Press q to quit the program
    if key & 0xFF == 27:
        break

    # Continuously save image is curr_key is set
    if curr_key:
        dir_path = os.path.join(data_dir, data_dir_stamp, curr_key)
        if not os.path.exists(dir_path):
          os.makedirs(dir_path)

        if curr_key in nums:
          nums[curr_key] = nums[curr_key] + 1
        else:
          nums[curr_key] = 0

        # Save the image
        # cv2.imwrite('Data/' + set_dir + '/' + name_type + "_" + str(number) + ".png", frame)
        fname = os.path.join(dir_path, data_dir_stamp + '_' + str(nums[curr_key]) + ".png")
        print('fname = {}'.format(fname))
        cv2.imwrite(fname, frame)

        print ("Saving image {} : {} ".format(curr_key, str(nums[curr_key])))
        # print("nums = {}".format(nums))


cap.release()
cv2.destroyAllWindows()
