"""
Face Detection Module using MediaPipe Face Mesh
Detects facial expressions using face landmarks
"""

import cv2
import mediapipe as mp
import numpy as np


class FaceDetector:
    def __init__(self, debug_mode=False):
        """Initialize MediaPipe Face Mesh"""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

        # Debug mode
        self.debug_mode = debug_mode
        
        # Store last detection metrics for debugging
        self.last_metrics = {}
        
        # Expression detection parameters
        self.expressions = {
            "happy": False,
            "sad": False,
            "surprised": False,
            "neutral": True,
        }

    def detect_expression(self, frame):
        """
        Detect facial expression from frame
        Returns: detected expression string
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if not results.multi_face_landmarks:
            return "neutral"

        face_landmarks = results.multi_face_landmarks[0]

        # Draw landmarks on frame
        self.mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=face_landmarks,
            connections=self.mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=self.mp_drawing.DrawingSpec(
                color=(0, 255, 0), thickness=1
            ),
        )

        # Analyze landmarks for expressions
        expression = self._analyze_landmarks(face_landmarks, frame.shape)

        return expression

    def _analyze_landmarks(self, landmarks, image_shape):
        """
        Analyze face landmarks to determine expression
        Using face landmark positions to detect:
        - Happy: mouth corners up, slight mouth opening
        - Sad: mouth corners down, eyebrows down
        - Surprised: mouth wide open, eyebrows up, eyes wide
        - Neutral: default state
        """
        h, w = image_shape[:2]

        # Key landmark points (MediaPipe Face Mesh indices)
        # Mouth corners: 61 (left), 291 (right)
        # Upper lip center: 13
        # Lower lip center: 14
        # Mouth top: 0
        # Mouth bottom: 17
        # Left eyebrow inner: 70, outer: 63
        # Right eyebrow inner: 300, outer: 293
        # Left eye top: 159, bottom: 145
        # Right eye top: 386, bottom: 374
        # Nose tip: 4

        # Mouth landmarks
        mouth_left = landmarks.landmark[61]
        mouth_right = landmarks.landmark[291]
        upper_lip = landmarks.landmark[13]
        lower_lip = landmarks.landmark[14]
        mouth_top = landmarks.landmark[0]
        mouth_bottom = landmarks.landmark[17]
        
        # Eyebrow landmarks
        left_eyebrow_inner = landmarks.landmark[70]
        left_eyebrow_outer = landmarks.landmark[63]
        right_eyebrow_inner = landmarks.landmark[300]
        right_eyebrow_outer = landmarks.landmark[293]
        
        # Eye landmarks
        left_eye_top = landmarks.landmark[159]
        left_eye_bottom = landmarks.landmark[145]
        right_eye_top = landmarks.landmark[386]
        right_eye_bottom = landmarks.landmark[374]
        
        # Nose (reference point)
        nose_tip = landmarks.landmark[4]

        # Calculate metrics
        
        # 1. Mouth Aspect Ratio (MAR) - for mouth opening
        mouth_height = abs(lower_lip.y - upper_lip.y) * h
        mouth_width = abs(mouth_right.x - mouth_left.x) * w
        mar = mouth_height / (mouth_width + 1e-6)
        
        # 2. Mouth corner position relative to center
        mouth_center_y = (upper_lip.y + lower_lip.y) / 2
        left_corner_diff = mouth_left.y - mouth_center_y
        right_corner_diff = mouth_right.y - mouth_center_y
        mouth_smile = -(left_corner_diff + right_corner_diff) / 2  # Negative = smile
        
        # 3. Eye Aspect Ratio (EAR) - for eye opening
        left_eye_height = abs(left_eye_top.y - left_eye_bottom.y) * h
        right_eye_height = abs(right_eye_top.y - right_eye_bottom.y) * h
        avg_eye_height = (left_eye_height + right_eye_height) / 2
        
        # 4. Eyebrow position relative to eyes
        left_eyebrow_height = (left_eye_top.y - left_eyebrow_inner.y) * h
        right_eyebrow_height = (right_eye_top.y - right_eyebrow_inner.y) * h
        avg_eyebrow_height = (left_eyebrow_height + right_eyebrow_height) / 2
        
        # Store metrics for debugging/UI display
        self.last_metrics = {
            'mar': mar,
            'smile': mouth_smile,
            'eye_height': avg_eye_height,
            'eyebrow_height': avg_eyebrow_height,
            'mouth_height': mouth_height,
        }
        
        # Debug info
        if self.debug_mode:
            print(f"MAR: {mar:.3f}, Smile: {mouth_smile:.4f}, Eye: {avg_eye_height:.1f}, Brow: {avg_eyebrow_height:.1f}")
        
        # Expression detection with improved thresholds
        
        # SURPRISED: Mouth wide open + eyebrows raised + eyes wide
        if mar > 0.4 and avg_eyebrow_height > 15 and avg_eye_height > 8:
            return "surprised"
        
        # HAPPY: Mouth corners up (smile) + moderate mouth opening
        elif mouth_smile > 0.003 and mar > 0.15:
            return "happy"
        
        # SAD: Mouth corners down + eyebrows slightly down
        elif mouth_smile < -0.002 and avg_eyebrow_height < 12:
            return "sad"
        
        # NEUTRAL: Default state
        else:
            return "neutral"
    
    def get_last_metrics(self):
        """Get last detection metrics for debugging"""
        return self.last_metrics
    
    def get_expression_tips(self, target_expression):
        """Get tips for user on how to make each expression"""
        tips = {
            'happy': "😊 SENYUM LEBAR! Angkat sudut bibir ke atas!",
            'sad': "😢 CEMBERUT! Turunkan sudut bibir & rileks wajah",
            'surprised': "😲 KAGET! Buka mulut lebar & angkat alis!",
            'neutral': "😐 WAJAH DATAR! Rileks & jangan ekspresikan apa-apa"
        }
        return tips.get(target_expression, "Tunjukkan ekspresi yang diminta!")
