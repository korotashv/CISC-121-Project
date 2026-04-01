# CISC-121 Project – Playlist Vibe Builder

## Chosen Problem
This project solves the Playlist Vibe Builder problem by sorting songs based on either energy or duration. It helps a user organize a playlist depending on the mood or pacing they want.

## Chosen Algorithm
I chose Merge Sort for this project. It is a good fit because it is efficient, works well on lists of records, and its divide-and-merge process is easy to visualize step by step for a user learning how sorting works. The playlist data contains multiple songs, and each song has several componwnwts such likw titles, artists, energys, and duration. Merge Sort works well because it can sort these song records using a selected key while keeping the structure of each song together. It also makes the sorting process clear because the list is repeatedly split into smaller parts and then merged back in sorted order.

## Preconditions and Assumptions
- Each song must have a title, artist, energy value, and duration.
- Energy must be a whole number from 0 to 100.
- Duration must be a positive whole number.
- The app checks for invalid input and shows an error message if the format is incorrect.
- Mutiple artists are allowed, will follow alphabetical order of first listed artist.

## What the User Sees During the Simulation
The user sees:
- the original playlist input
- the final sorted playlist
- the merge sort steps, including splitting, comparisons, selections, and merged sections
This helps the user understand what the algorithm is doing instead of only seeing the final result.

## Demo

## Problem Breakdown & Computational Thinking

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
The app shows the most important parts of the sorting process, such as splitting, comparing, and merging songs. It hides lower-level details like memory handling and Python internals because they are not necessary for the user to understand how the algorithm works. We do not need to show anything except the name of the song and also the title, as the users will probably know its energy and such.

### Algorithm Design
Input → user enters playlist data and chooses a sorting key  
Process → the program validates the data, runs Merge Sort, and records each step  
Output → the app displays the sorted playlist and a step-by-step explanation of the sorting process

## Flowchart
