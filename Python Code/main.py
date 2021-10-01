#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import time
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


if not firebase_admin._apps:
    cred_object = credentials.Certificate({
      "type": "service_account",
      "project_id": "traffic-159e8",
      "private_key_id": "",
      "private_key": "",
      "client_email": "",
      "client_id": "112202752645265219203",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-1avzl%40traffic-159e8.iam.gserviceaccount.com"
    })

    default_app = firebase_admin.initialize_app(cred_object, {
         'databaseURL': 'https://traffic-159e8-default-rtdb.firebaseio.com'
        })

ref = db.reference('server/')
#video location
cap1 = cv2.VideoCapture(r"C:\Users\Monish Meher\Downloads\Video\road.mp4")
length1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
print( length1 )
cap2 = cv2.VideoCapture(r"C:\Users\Monish Meher\Downloads\Video\test.mp4")
length2 = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT))
print( length2 )

#varaibles
count = 0
time_skips = float(1000)
success,image = cap1.read()
count1 = 0
time_skips1 = float(200)
success,image1 = cap2.read()

flick = 0
cond1 = 0 
cond2 = 0
carInFeed1 = 0
carInFeed2 = 0


def main():
    global flick
    global cond1
    global cond2
    global count
    global time_skips
    global image
    global length1
    global count1
    global time_skips1
    global image1
    global carInFeed1
    global carInFeed2
    print(count*(3*time_skips/100))
    if flick == 0:
        while(count*(3*time_skips/100)) < length1:
            cv2.imwrite("frame%d.jpg" % count, image) 
            cap1.set(cv2.CAP_PROP_POS_MSEC,(count*time_skips))
            success,image = cap1.read()
            print("Feed 1"+ "frame%d.jpg" % count)
            print(count)
            im = cv2.imread("frame%d.jpg" % count)
            bbox, label, conf = cv.detect_common_objects(im)
            output_image = draw_bbox(im, bbox, label, conf)
            plt.imshow(output_image)
            plt.show()
            print('Feed 1 cars'+ str(label.count('car'))) 
            carInFeed1 = label.count('car')
            count += 1
            flick = 1
            cond1 = 1 
            main()  
        else:
            print("Completed Video 1")

    elif flick == 1:
        while(count1*(3*time_skips1/100)) < length2:
            cv2.imwrite("sec%d.jpg" % count1, image1) 
            cap2.set(cv2.CAP_PROP_POS_MSEC,(count1*time_skips1))
            success,image1 = cap2.read()
            print("Feed 2"+ "sec%d.jpg" % count1)
            im1 = cv2.imread("sec%d.jpg" % count1)
            bbox1, label1, conf1 = cv.detect_common_objects(im1)
            output_image1 = draw_bbox(im1, bbox1, label1, conf1)
            plt.imshow(output_image1)
            plt.show()
            print('Feed 2 cars'+ str(label1.count('car'))) 
            carInFeed2 = label1.count('car')
            count1 += 1
            flick = 0
            cond2 = 1
            compare()    
        else:
            print("Completed Video 2")
            
def compare():   
    if carInFeed1 > carInFeed2:
        print("Feed 1 has more cars")
#         current = "A"
#         firebase.post('/current',current)
        traffic_ref = ref.child('traffic-data')
        traffic_ref.set({
            'roadData': {
                'currentStatus': 'B',
                'carsFeed1': carInFeed1,
                'carsFeed2': carInFeed2,
            }
        })
        main()
    elif carInFeed1 < carInFeed2:
        print("Feed 2 has more cars")
#         current = "B"
#         firebase.post('/current',current)
        traffic_ref = ref.child('traffic-data')
        traffic_ref.set({
            'roadData': {
                'currentStatus': 'A',
                'carsFeed1': carInFeed1,
                'carsFeed2': carInFeed2,
            }
        })
        main()
    elif carInFeed1 == carInFeed2:
        print("Similar Trafiic")
#         current = "B"
#         firebase.post('/current',current)
        traffic_ref = ref.child('traffic-data')
        traffic_ref.set({
            'roadData': {
                'currentStatus': 'Same',
                'carsFeed1': carInFeed1,
                'carsFeed2': carInFeed2,
            }
        })
        main()   

main()        

    


# In[ ]:





# In[ ]:




