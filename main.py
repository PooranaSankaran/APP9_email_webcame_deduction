import time
from emailing import send_email
import glob
import cv2 # webcame activate and capture
import os
from threading import Thread

video = cv2.VideoCapture(0) #videocapture
time.sleep(1) #giving time to videocapture

first_frame = None

#if no object it will be 0, else 1
status_list = []
count = 1

#after sesnding email dlt all the images captured and start new things
def clean_folder():
    images = glob.glob('images/*.png')
    for image  in images:
        os.remove(image)

while True:
    status = 0
    check, frame = video.read() # frame = matrix out of pixcel
    # to store image
    # cv2.imwrite(f'images/{count}.png',frame)
    # count = count + 1
    #converting frames into gray frames  # we have blue, green and red in frames is complecated so, we converting it into gray
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21,21), 0 ) # to avoid noise
    #cv2.imshow('My video', gray_frame_gau) # it will show's the videocapture

    # we need to see the differnce bettween frames if difference we need to capture
    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame  = cv2.adsdiff(first_frame, gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1] # 255 is full white(differnece from frames)
    dil_frame = cv2.dilate(thresh_frame, None, iterations= 2)
    cv2.imshow('My video', dil_frame)  # it will show's the videocapture

    # find contours with white are to regonize change in frames.
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # if it's fake image continue to loop again the code
        if cv2.contourArea(contour) < 5000:#not real object
            continue
        # if it's original dectation the color frame in the above varibable to capture it
        x, y, w , h = cv2.boundingRect(contour)
        rectangle=cv2.rectangle(frame,(x ,y), (x+w, y +h), (0,255,0),3)  #if object or man dectate it will show the rectangle around face..

        if rectangle.any():
            status = 1 # 1 = object in
            cv2.imwrite(f'images/{count}.png', frame) # save images in images folder
            count = count + 1
            # it will capture all the frames but we need only one frame to send to mail
            all_images = glob.glob('images/*.png')

            # we are extracting the middle number image only we don't need all
            index = int(len(all_images)/2)
            image_with_object = all_images[index]

    # if no object it will be 0, else 1 with 1 we can identify there is boject
    # and we capture that single image and send to out mail

    status_list.append(status)
    status_list = status_list[-2:] # if object enters and exit we can find using last two array
    # if object exit the last two list will be [1,0]

    if status_list[0]==1 and status_list[1]==0:
        email_thread = Thread(target = send_email, args = (image_with_object,))
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        email_thread.start()



    cv2.imshow('Video',frame)
    key = cv2.waitkey(1)  # run constantly # avoid black frames

    if key == ord('q'): # if user press q it will break.
        break
video.release()
clean_thread.start()
