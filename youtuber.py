import os
import subprocess
import time
import base64
import cv2
import random
live_stream_url = os.environ['URL1']
url_2 = os.environ['URL2']
#REPO = os.environ['REPO']

def capture_frame_with_retry(live_stream_url, output_image_path):
    retries = 3
    for i in range(retries):
        try:
            cmd = f'youtube-dl -g "{live_stream_url}"'
            video_url = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

            cmd = f'ffmpeg -y -i "{video_url}" -vf "fps=1" -frames:v 1 {output_image_path}'
            subprocess.run(cmd, shell=True)
            return
        except subprocess.CalledProcessError:
            # If there was an error, wait for 10 seconds before retrying
            time.sleep(10)
    # If all retries have failed, raise an exception
    raise Exception(f"Could not capture frame after {retries} retries")


def capture_frame(live_stream_url, output_image_path):
    cmd = f'youtube-dl -g "{live_stream_url}"'
    video_url = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

    cmd = f'ffmpeg -y -i "{video_url}" -vf "fps=1" -frames:v 1 {output_image_path}'
    subprocess.run(cmd, shell=True)


#live_stream_url = URL1
output_image_path = 'frame.jpg'

#url_2 = URL2
set_url = [live_stream_url,url_2]
live_stream_url = random.choice(set_url)
interval_seconds = 60  # Adjust the interval as needed
capture_frame_with_retry(live_stream_url, output_image_path)
'''
while True:
    capture_frame(live_stream_url, output_image_path)
    os.system('git add ' + output_image_path)
    os.system('git commit -m "Update frame"')
    os.system('git push')
    time.sleep(interval_seconds)
'''

# Name of the QR Code Image file
filename = output_image_path

# read the QRCODE image
image = cv2.imread(filename)

# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()

# detect and decode
data, vertices_array, binary_qrcode = detector.detectAndDecode(image)

# if there is a QR code
# print the data
if vertices_array is not None:
  print("QRCode data:")
  print(data)
else:
  print("There was some error")
  time.sleep(10)
  capture_frame_with_retry(live_stream_url, output_image_path)
  data, vertices_array, binary_qrcode = detector.detectAndDecode(image)


filename = 'temp.txt'

if os.path.isfile(filename) and os.path.getsize(filename) > 0:
    # Read the existing lines from the file
    with open(filename, 'r') as f:
        lines = f.readlines()
else:
    lines = []

# Add the new line to the beginning of the list if there are less than 5 lines
if len(lines) < 10:
    lines.insert(0, data + "\n")
# Otherwise, remove the last line and add the new line to the beginning
else:
    lines.pop()
    lines.insert(0, data + "\n")

# Write the updated lines back to the file
with open(filename, 'w') as f:
    f.writelines(lines)

# Concatenate the lines into a single string
content = ''.join(lines)

#sample_string = "GeeksForGeeks is the best"
sample_string_bytes = content.encode("ascii")

base64_bytes = base64.b64encode(sample_string_bytes)
base64_string = base64_bytes.decode("ascii")

# print(f"Encoded string: {base64_string}")

a=open('readme.txt', 'w')

a.write(base64_string)

a.close()

# Set the repository URL and file path
repo_url = os.environ['REPO']
#os.chdir('/root/youtuber')
os.system('git add readme.txt')
os.system('git commit -m "Update readme"')
os.system('git push origin main')
