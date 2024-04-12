# mini-project
This project aim to develop an algorithm which can detect the next word in line based on past detection, it can do the following tasks:
- Load a page image and preprocess it
- Read all contours in the page image
- Detect the writing in an page image
- Can handle an empty page image
- Can detect writing without any past detection from the page image
- Draw rectangle around the detected writing in the page image

How to run the Code + Description:
1 - First download the code using powershell or bash or using ‘git clone url’ or simply download it as a zip file
2 - After downloading it log in to the downloaded file using your powershell or bash and create a python virtual environment by running:  ‘python -m venv venv’
3 - After successfully creating virtual environment named ‘venv’ you should see a folder named ‘venv’
4 - Activate the new ‘venv’ by running: ‘venv\Scripts\activate’, and you should see ‘venv’ written at the left of the prompt line in green
5 - Run the command  ‘pip install -r requirements.txt’ It should not take much time to finish
6 - Run the code by ‘python nextword.py’
7 - The code detects the writing in page images named only ‘writing.jpeg’ so in case you want to test different images rename each image to writing.jpeg
8 - In case you want to test another image, just replace the writing.jpeg and press any key apart from ‘q’
9 - For exiting the run press ‘q’
