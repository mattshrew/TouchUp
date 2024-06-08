import cv2
import numpy as np

# Function to detect laptop screen outline
def detect_laptop_screen(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 350, 400)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the contour with the largest area (assuming it's the laptop screen)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Approximate the contour to a polygon
        epsilon = 0.01 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)
        
        # Draw the outline of the laptop screen
        cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
        
        # Calculate the centroid of the contour
        M = cv2.moments(approx)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centroid = (cx, cy)
            cv2.circle(frame, centroid, 5, (255, 0, 0), -1)
            
            # Assume the laptop screen is parallel to the image plane and estimate depth based on size
            # You might need additional calibration for more accurate depth estimation
            depth = 1000  # Arbitrary depth value for demonstration
            # Compute 3D coordinates
            x_3d = (cx - frame.shape[1]/2) * depth / (frame.shape[1]/2)
            y_3d = (cy - frame.shape[0]/2) * depth / (frame.shape[0]/2)
            z_3d = depth
            # Print 3D coordinates
            print("3D Coordinates (x, y, z):", (x_3d, y_3d, z_3d))
        
    return frame

# Main function
def main():
    cap = cv2.VideoCapture(0)  # Use the default camera
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect laptop screen outline
        frame_with_outline = detect_laptop_screen(frame)
        
        # Display the frame
        cv2.imshow('Laptop Screen Detection', frame_with_outline)
        
        # Exit on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
