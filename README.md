1. # CISC-121 Project – Poppy-Playlist-Visualiser

2. ## Chosen Problem
This project solves the Playlist Vibe Builder problem by sorting songs based on either energy or duration. It helps a user organize a playlist depending on the mood or pacing they want.

3. ## Chosen Algorithm
I chose Merge Sort for this project. It is a good fit because it is efficient, works well on lists of records, and its divide-and-merge process is easy to visualize step by step for a user learning how sorting works. The playlist data contains multiple songs, and each song has several components such as titles, artists, energy, and duration. Merge Sort works well because it can sort these song records using a selected key while keeping the structure of each song together. It also makes the sorting process clear because the list is repeatedly split into smaller parts and then merged back in sorted order.

## Preconditions and Assumptions
- Each song must have a title, artist, energy value, and duration.
- Energy must be a whole number from 0 to 100.
- Duration must be a positive whole number.
- The app checks for invalid input and shows an error message if the format is incorrect.
- Multiple artists are allowed; they will follow alphabetical order of the first listed artist.
- working quiz to test users understanding of what they are trying to order.

## What the User Sees During the Simulation
The user sees:
- the original playlist input
- the final sorted playlist
- the merge sort steps, including splitting, comparisons, selections, and merged sections
This helps the user understand what the algorithm is doing instead of only seeing the final result.

4. ## Demo
Click the image below to watch the demo:

[![Watch Demo](cisc-example-video.mov)

5. ## Problem Breakdown & Computational Thinking
### Decomposition
- Read and validate the playlist input
- Convert each line into a song record
- Split the playlist into smaller sublists
- Compare songs using the selected sorting key
- Merge the smaller sorted lists back together
- Display the sorted playlist and all sorting steps

### Pattern Recognition
The same comparison process repeats throughout the algorithm. Merge Sort keeps splitting the list, then repeatedly compares the front elements of two smaller sorted lists until the full list is rebuilt in order.

### Abstraction
The app shows the most important parts of the sorting process, such as splitting, comparing, and merging songs. It hides lower-level details like memory handling and Python internals because they are not necessary for the user to understand how the algorithm works.

### Algorithm Design
Input → user enters playlist data and chooses a sorting key
Process → the program validates the data, runs Merge Sort, and records each step
Output → the app displays the sorted playlist and a step-by-step explanation of the sorting process. quiz is also provided.

## Flowchart
![App Screenshot](CISCFINAL.png)

6. ## Steps to run

    1. Make sure Python is installed on your system
    2. Install required dependencies:
   pip install -r requirements.txt
    3. Run the application:
   python app.py
    4. Open the local Gradio link shown in the terminal
    5. Enter a playlist and start sorting

    
7. ## Hugging face link

8. ## Testing

The application was tested with a variety of inputs to ensure correctness and robustness.

### Normal Cases
- Sorting a playlist of multiple songs by energy (ascending and descending)
- Sorting by duration, title, and artist

### Edge Cases
- Energy values at boundaries (0 and 100)
- Very short and very long durations
- Playlist with only one song

### Error Handling
- Missing fields in input
- Incorrect formatting (not using | separators)
- Non-numeric energy or duration values

### Results
- All valid inputs were sorted correctly
- Invalid inputs displayed clear error messages
- The app did not crash under any tested conditions

10. ## Author & Acknowledgment
 I, Victor korotash made this hugging face link with the help of ChatGPT. I did a lot of brainstorming by hand, then resorted to chatgpt to explain the things i was not able to solve on my own. Moving through this assignment I did not blatantly rely on ai, and always reviewed what it suggested for me to add or improve before commiting the changes.
