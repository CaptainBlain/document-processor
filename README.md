# document-processor

2018

I had to regulary update an app from a list of documents, I wrote this document processor to extract all the data that was needed and then pass it back in JSON format.

This is the file structure that had to be processed

![alt text](https://firebasestorage.googleapis.com/v0/b/blain-ellis.appspot.com/o/github-images%2Fprocessor.png?alt=media&token=835ab04e-6fdc-4657-b607-1858cea601f4)

The processor runs through each folder, then runs through each subfolder (if there is one) and gathers all the required data from the word documents.

2022

Add PDF upload and screenshots to images folder

Add Robs Update zip folder (unzipped) to doc folder

Run process_doc with target and actions, this will handle all image uploads

CD to realtime_database_worker

run python3 remote.py --action=publish --target BAIT

or

open "remote.py" if required 
