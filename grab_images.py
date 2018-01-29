import cv2
import os
import time
import argparse

def crop_resize_rect(frame, size):
    """
    Resize and crop a square image from the original frame.
    """
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



if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(description="Capture photos from camera")
    parser.add_argument('--data_dir', type=str, default='data', help="Data dir for storing captured images")
    parser.add_argument('--verbose', action='store_true', default=False, help="Verbose mode for debugging")
    parser.add_argument('--gray', action='store_true', default=False, help="Gray image")
    parser.add_argument('--size', type=int, default=256, help="Image size (square)")
    parser.add_argument('--rate', type=float, default=5, help="Capture rate (Hz)")

    args = parser.parse_args()

    data_dir = args.data_dir
    verbose = args.verbose
    img_size = args.size
    rate = args.rate
    is_gray = args.gray

    # Grab your webcam on local machine
    cap = cv2.VideoCapture(0)

    # Initialize photo count per class
    nums = dict()

    # Specify the name of the directory that has been premade and be sure that it's the name of your class
    # Remember this directory name serves as your datas label for that particular class
    data_dir = 'data'
    data_dir_stamp = time.strftime("%G%m%d_%H%M%S")

    print ("Photo capture enabled! Press any key to take photos! Pressed key - is a class.")

    # Latest pressed key (e.g. class)
    curr_key = None

    # Loop until 'esc' key is pressed
    while True:

        # Read in single frame from webcam
        ret, frame = cap.read()

        frame = crop_resize_rect(frame, img_size)

        # If you want them gray
        if is_gray:
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        # Use this line locally to display the current frame
        cv2.imshow('Color Picture', frame)

        # Capture rate is 5 Hz (default)
        key = cv2.waitKey(int(1 / rate * 1000))

        # Use esc to take photos when you're ready
        if (key & 0xFF >= ord('a') and key & 0xFF <= ord('z')) or (key & 0xFF >= ord('0') and key & 0xFF <= ord('9')):
            curr_key = chr(key)

        # Print key for debug
        if key > 0 and verbose:
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
            fname = os.path.join(dir_path, data_dir_stamp + '_' + str(nums[curr_key]) + ".png")
            print('fname = {}'.format(fname))
            cv2.imwrite(fname, frame)

            print ("Saving image {} : {} ".format(curr_key, str(nums[curr_key])))

    # Clean
    cap.release()
    cv2.destroyAllWindows()
