# Event Driven Serverless Image Processing Pipeline using AWS Lambda and S3
## Project Introduction
This project implements an event-driven image processing pipeline using AWS Lambda and S3, designed to provide automated, scalable, and efficient image manipulation. The system leverages the power of serverless technology to perform tasks such as resizing images into five different resolutions: 8x8, 16x16, 32x32, 48x48, and 64x64.

The solution is ideal for modern applications that demand high scalability and cost-efficiency, such as content management systems, social media platforms, e-commerce websites, or any service requiring robust image processing capabilities. By utilizing AWS Lambda's pay-as-you-go model, the pipeline minimizes operational costs while delivering high performance.

## Project Layout
<img width="745" alt="Screenshot 2025-01-06 at 2 21 06 PM" src="https://github.com/user-attachments/assets/4d28bb4e-0015-48ec-97a0-de4de77a00df" />


## Uses of Pixelation (Objective of the project)
Pixelation can be used in multiple ways, some of them are:

1. Privacy and Anonymity: Obscures sensitive information like faces, license plates, or personal data in images and videos to ensure privacy.
   
2. Content Moderation: Censors explicit, sensitive, or age-restricted content on social media platforms, providing a preview without revealing details.

3. Artistic and Creative Applications: Creates retro-style pixel art, adds creative filters, or applies pixelated effects for abstract art and digital design.
   
4. Low-Resolution Previews: Displays lightweight, pixelated image previews for faster loading in web or mobile applications, reducing bandwidth usage.

5. Gaming and Virtual Reality: Used for retro-style graphics in games or to optimize rendering performance by pixelating distant objects in VR/AR environments.

## Project Solution
### <ins>Step 1: Creating two AWS S3 Buckets( one source and one destination)</ins>
Source: pixelater-source-bucket
Destination: pixelater-destination-bucket
A third bucket to store the code: pixelater-code-bucket

### <ins>Step 2: Create the Lambda Function code(with the necessary libraries)</ins>
Using the CloudShell in the AWS Management Console, 
1. Create a folder "lambda_function". [`mkdir lambda_function`]
2. Navigate to the folder and create another folder "lambda". [`cd lambda_function`] [`mkdir lambda`]
3. Move into that folder and create a python code file "lambda_function.py". [`cd lambda`] [`nano lambda_function.py`]
4. Paste the [python code](https://github.com/Avikaj/Event-Driven-Serverless-Image-Processing-Pipeline-using-AWS-Lambda-and-S3/blob/main/lambda_function.py) .
5. Download this [PIL](https://files.pythonhosted.org/packages/f3/3b/d7bb231b3bc1414252e77463dc63554c1aeccffe0798524467aca7bad089/Pillow-9.0.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl) package into that folder using wget.
6. For the package to include only the required libraries along with the code,
Run [`unzip Pillow-9.0.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`] and then [`rm Pillow-9.0.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`]. 
These are the Pillow module files required for image manipulation in Python 3.9 (which the lambda function will be using).

7. From the same folder, run [`zip -r ../my-deployment-package.zip .`] which will create a lambda function zip, containing all these files in the parent directory.
8. To check this zip file, go one folder back by doing [`cd ..`] and then run [`ls -lrt`] and there will be the zip file in red.

### <ins> Step 3: Creating a Lambda Function</ins>
Name: pixelater-function
Runtime: Python 3.9

To copy the zip file into the third S3 bucket, use the CloudShell command Line, and run [`aws s3 cp name_of_your_zip_file.zip s3://your_third_bucket_name`]
Refresh the objects tab under the third bucket to see the uplaoded zip file. Here, copy the S3 URL.

Now inside the Lambda Function on AWS Management Console, under "upload from", select the [`Amazon S3 location`] and paste the URL.
Under the Confuguration tab, change the timeout to 5 minutes.
To set an environent variable, under the same tab, click on [`Environment variables`] and add the environment variable [`bucket_1`] from the python code and set the value as the name of the destination bucket.

### <ins>Step 4: Adding a trigger</ins>
Adding a trigger, would trigger the lambda function as soon as there is an input image in the S3 bucket.
Hit [`Add trigger`] under the lambda function. Here, select the source S3 bucket.

### <ins>Step 5: Testing and Validating</ins>

