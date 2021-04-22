#https://google.github.io/mediapipe/solutions/hands#python-solution-api
#https://gist.github.com/TheJLifeX/74958cc59db477a91837244ff598ef4a
#https://gist.github.com/TheJLifeX/99cdf4823e2b7867c0e94fabc660c58b

#euclidian https://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
#angle https://stackoverflow.com/questions/42258637/how-to-know-the-angle-between-two-points
import numpy as np
import cv2
import mediapipe as mp
import math
import player
import time

class Finger:
    FINGER_THUMB = 1
    FINGER_INDEX = 2
    FINGER_MIDDLE = 3
    FINGER_RING = 4
    FINGER_LITTLE = 5
    
    FINGER_POINTS = {
        1: [1, 2, 3, 4],
        2: [5, 6, 7, 8],
        3: [9, 10, 11, 12],
        4: [13, 14, 15, 16],
        5: [17, 18, 19, 20]
    }

class AudioHands:
    ########################## Variables ##########################
    
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    
    starting_angle = None
    next_prev_starting_point = None
    details_starting_point = None
    starting_depth = None
    show_info = False
    last_time = time.time()
    
    ########################## Methods ##########################
    
    def get_image_shape(self, image):
        return image.shape[0:2]
    
    def between(self, number, min_number, max_number):
        if number < min_number:
            return min_number
        elif number > max_number:
            return max_number
        else:
            return number
    
    def get_angle(self, hand_landmarks):
        fig1 = hand_landmarks.landmark[9].x - hand_landmarks.landmark[0].x;
        fig2 = hand_landmarks.landmark[0].y - hand_landmarks.landmark[9].y;
        radians = math.atan2(fig1, fig2)
        degrees = math.degrees(radians)
        return degrees
    
    def get_point_from_landmark(self, hand_landmarks, landmark_location):
        return np.array((hand_landmarks.landmark[landmark_location].x,
                         hand_landmarks.landmark[landmark_location].y))
    
    def get_image_location(self, point, image):
        height, width = self.get_image_shape(image)
        return (int(point[0] * width), int(point[1] * height))
    
    def compile_point_list(self, hand_landmarks, landmark_locations):
        location_list = []
        for landmark_location in landmark_locations:
            location_list.append(hand_landmarks.landmark[landmark_location])
        return location_list
    
    def monotonic(self, value_list):
        dif_list = np.diff(value_list)
        return np.all(dif_list <= 0) or np.all(dif_list >= 0)
    
    def open_finger(self, hand_landmarks, finger_index):
        finger_points = Finger.FINGER_POINTS.get(finger_index, [])
        
        point_list = self.compile_point_list(hand_landmarks, finger_points)
        list_x = [i.x for i in point_list]
        list_y = [i.y for i in point_list]
        
        if self.monotonic(list_x) and self.monotonic(list_y):
            return True
        else:
            return False
    
    ########################## OpenCV ##########################
    
    def frame(self, image):
        height, width = self.get_image_shape(image)
        color = (0, 0, 255)
        thickness = 10
        
        cv2.rectangle(image, (0,0), (width,height), color, thickness)
    
    def growing_dot(self, image, location, radius):
        color = (66, 245, 200)
        
        cv2.circle(image, location, radius, color, cv2.FILLED)
    
    def show_buttom_text(self, text, image):
        height, width = self.get_image_shape(image)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 1
        color = (0, 255, 0)
        
        cv2.putText(image, str(text), (0, height-10), font, font_scale, color, thickness, cv2.LINE_AA)
    
    def centered_text(self, image, text, location):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 3
        thickness = 10
        color = (245, 132, 66)
        
        textsize = cv2.getTextSize(str(text), font, font_scale, thickness)[0]
        cv2.putText(image, str(text), (location[0]-int(textsize[0]/2),
                                       location[1]+int(textsize[1]/2)),
                    font, font_scale, color, thickness, cv2.LINE_AA)
    
    def draw_volume_circle(self, hand_landmarks, image, angle, volume, location):
        thickness = 10
        radius = 100
        
        color = (164, 235, 52)
        if volume == 0 or volume == 100:
            color = (73, 163, 8)
        
        volume_to_degrees = 2
        
        cv2.ellipse(image, location, (radius, radius),
                    self.starting_angle,
                    -91 -(50*volume_to_degrees),
                    (volume * volume_to_degrees)-90-(50*volume_to_degrees),
                    color, thickness)
    
    def horizontal_line(self, image, location):
        height, width = self.get_image_shape(image)
        color = (63, 13, 117)
        thickness = 3
        
        cv2.line(image, (0,location[1]), (width,location[1]), color, thickness)
    
    ########################## Actions ##########################
    
    def stop_start(self, hand_landmarks, image):
        current_time = time.time()
        if (self.last_time + 1 < current_time and#1 second has passed
            self.open_finger(hand_landmarks, Finger.FINGER_INDEX) and
            self.open_finger(hand_landmarks, Finger.FINGER_MIDDLE) and
            self.open_finger(hand_landmarks, Finger.FINGER_RING) and
            self.open_finger(hand_landmarks, Finger.FINGER_LITTLE)):
            
            depth = abs(hand_landmarks.landmark[9].z)
            
            if depth > 0.3:
                print("play/stop")
                self.last_time = time.time()
                self.player.play_stop()
    
    def next_prev(self, hand_landmarks, image):
        point = self.get_point_from_landmark(hand_landmarks, 8)
        
        if (self.open_finger(hand_landmarks, Finger.FINGER_INDEX) and
            not self.open_finger(hand_landmarks, Finger.FINGER_MIDDLE) and
            not self.open_finger(hand_landmarks, Finger.FINGER_RING) and
            not self.open_finger(hand_landmarks, Finger.FINGER_LITTLE)):
            
            if self.next_prev_starting_point is None:
                self.next_prev_starting_point = point
                
            change = self.next_prev_starting_point[0] - point[0]
            radius = int(abs(change) * 100)
            
            if radius >= 40:
                self.next_prev_starting_point = None
                if change < 0:
                    print("next")
                    self.player.next_song()
                else:
                    print("previous")
                    self.player.previous_song()
            else:
                location = self.get_image_location(point, image)
                self.growing_dot(image, location, radius)
        else:
            self.next_prev_starting_point = None
    
    def set_volume(self, hand_landmarks, image):
        point_thumb = self.get_point_from_landmark(hand_landmarks, 4)
        point = self.get_point_from_landmark(hand_landmarks, 8)
        
        if(np.linalg.norm(point_thumb-point) < 0.1):
            
            angle = self.get_angle(hand_landmarks)
            volume = self.player.get_volume()
            
            if self.starting_angle is None:
                self.starting_angle = angle
            
            change = int(angle - self.starting_angle)
            new_volume = self.between(volume + change//10, 0, 100)
            
            point = self.get_point_from_landmark(hand_landmarks, 9)
            location = self.get_image_location(point, image)
            
            self.centered_text(image, volume, location)
            self.draw_volume_circle(hand_landmarks, image, angle, new_volume, location)
            
            print("change volume")
            self.player.set_volume(new_volume)
        else:
            self.starting_angle = None
    
    def show_details(self, hand_landmarks, image):
        angle = abs(self.get_angle(hand_landmarks))
        
        if (80 < angle < 100):
            
            point = self.get_point_from_landmark(hand_landmarks, 9)
            if self.details_starting_point is None:
                self.details_starting_point = point
            
            location = self.get_image_location(self.details_starting_point, image)
            self.horizontal_line(image, location)
            
            if self.details_starting_point[1] - point[1] > 0.2:
                print("show")
                self.show_info = True
            elif  point[1] - self.details_starting_point[1] > 0.2:
                print("hide")
                self.show_info = False
        else:
            self.details_starting_point = None
    
    ########################## Hands ##########################
    
    def hand_control(self, multi_hand_landmarks, image):
        for hand_landmarks in multi_hand_landmarks:
            self.stop_start(hand_landmarks, image)
            self.next_prev(hand_landmarks, image)
            self.set_volume(hand_landmarks, image)
            self.show_details(hand_landmarks, image)
            
            self.mp_drawing.draw_landmarks(
                image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
    
    def __init__(self):
        # For webcam input:
        cap = cv2.VideoCapture(0)
        self.player = player.Player()
        with self.mp_hands.Hands(
                min_detection_confidence=0.8,
                min_tracking_confidence=0.8,
                max_num_hands=1) as hands:
            
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue
        
                # Flip the image horizontally for a later selfie-view display, and convert
                # the BGR image to RGB.
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                results = hands.process(image)
                
                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                if self.show_info:
                    self.show_buttom_text(self.player.info(), image)
                    
                if not self.player.is_playing():
                    self.frame(image)
                
                if results.multi_hand_landmarks:
                    self.hand_control(results.multi_hand_landmarks, image)

                cv2.imshow('MediaPipe Hands', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        
        cap.release()
    
AudioHands()