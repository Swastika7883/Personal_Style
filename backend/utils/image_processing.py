import cv2
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from collections import Counter
import logging

logger = logging.getLogger(__name__)

# Define color palettes for each undertone
cool_colors = [
    "#FFFFFF", "#E5E5E5", "#CFCFD3", "#8B8B94",
    "#000000", "#4B1D1D", "#D65A82", "#DBB1C1",
    "#A36B94", "#5D1A48", "#B9AAD3", "#8D99D1",
    "#5E6F9E", "#7189C6", "#A7C7E7", "#3C7D76"
]

neutral_colors = [
    "#D1C8C1", "#A89C94", "#877C78", "#5A4B4B",
    "#FFF9E3", "#F4D882", "#DC979E", "#C27A86",
    "#4C9C6E", "#2E5738", "#3B5E9B", "#A61919",
    "#FDEAE6", "#7A0303", "#A8121A", "#DEDCDC",
    "#9A9A9A", "#6D6D6D", "#454545", "#26262A"
]

warm_colors = [
    "#FFFFF0", "#E6D6B9", "#C1A484", "#A57F5F",
    "#3C1913", "#9E2A2B", "#F15A24", "#FF782A",
    "#DD7870", "#F5A07A", "#FDB147", "#FFC75F",
    "#FFD500", "#88B04B", "#78A67B", "#00A3AD",
    "#4B728F", "#193773", "#02075D", "#70327E"
]

def analyze_image(image_content):
    try:
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_content, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise ValueError("Could not decode image")
        
        # Convert to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Load face detection classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        if len(faces) == 0:
            raise ValueError("No faces detected in the image")
        
        # Extract skin region from the first face
        x, y, w, h = faces[0]
        face_roi = image_rgb[y:y+h, x:x+w]
        
        # Convert to LAB color space
        lab_face = cv2.cvtColor(face_roi, cv2.COLOR_RGB2LAB)
        a_channel = lab_face[:, :, 1].flatten()
        b_channel = lab_face[:, :, 2].flatten()
        
        # Combine features
        features = np.vstack((a_channel, b_channel)).T
        
        # Normalize features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        # Apply K-Means clustering
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        kmeans.fit(features_scaled)
        labels = kmeans.labels_
        
        # Count the number of pixels in each cluster
        cluster_counts = Counter(labels)
        
        # Find the cluster with the highest number of pixels
        dominant_cluster = cluster_counts.most_common(1)[0][0]
        
        # Assign the corresponding undertone label
        if dominant_cluster == 0:
            undertone = "Warm Undertone"
            palette = warm_colors
        elif dominant_cluster == 1:
            undertone = "Neutral Undertone"
            palette = neutral_colors
        else:
            undertone = "Cool Undertone"
            palette = cool_colors
        
        return {"undertone": undertone, "palette": palette}
        
    except Exception as e:
        logger.error(f"Error in image analysis: {str(e)}")
        raise