import gradio as gr

# Sample playlist data
default_songs = [
    {"title": "Blinding Lights", "artist": "The Weeknd", "energy": 90, "duration": 200},
    {"title": "Sunflower", "artist": "Post Malone", "energy": 65, "duration": 158},
    {"title": "Levitating", "artist": "Dua Lipa", "energy": 85, "duration": 203},
    {"title": "Slow Dancing", "artist": "V", "energy": 40, "duration": 230},
    {"title": "Midnight City", "artist": "M83", "energy": 75, "duration": 245},
]

def parse_input(text):
    songs = []
    lines = text.strip().split("\n")

    for line in lines:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 4:
            raise ValueError(
                "Each line must have 4 values: title, artist, energy, duration"
            )

        title, artist, energy, duration = parts

        try:
            energy = int(energy)
            duration = int(duration)
        except ValueError:
            raise ValueError("Energy and duration must be whole numbers.")

        if not (0 <= energy <= 100):
            raise ValueError("Energy must be between 0 and 100.")

        if duration <= 0:
            raise ValueError("Duration must be greater than 0.")

        songs.append({
            "title": title,
            "artist": artist,
            "energy": energy,
            "duration": duration
        })

    return songs

def format_songs(songs):
    output = []
    for song in songs:
        output.append(
            f"{song['title']} by {song['artist']} | Energy: {song['energy']} | Duration: {song['duration']} sec"
        )
    return "\n".join(output)

def merge(left, right, key, steps):
    merged = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        left_value = left[i][key]
        right_value = right[j][key]

        steps.append(
            f"Comparing '{left[i]['title']}' ({key}={left_value}) with '{right[j]['title']}' ({key}={right_value})"
        )

        if left_value <= right_value:
            merged.append(left[i])
            steps.append(f"→ Taking '{left[i]['title']}'")
            i += 1
        else:
            merged.append(right[j])
            steps.append(f"→ Taking '{right[j]['title']}'")
            j += 1

    while i < len(left):
        merged.append(left[i])
        steps.append(f"Adding remaining song '{left[i]['title']}'")
        i += 1

    while j < len(right):
        merged.append(right[j])
        steps.append(f"Adding remaining song '{right[j]['title']}'")
        j += 1

    steps.append("Merged section: " + ", ".join(song["title"] for song in merged))
    return merged

def merge_sort(songs, key, steps):
    if len(songs) <= 1:
        return songs

    mid = len(songs) // 2
    left_half = songs[:mid]
    right_half = songs[mid:]

    steps.append("Splitting: " + ", ".join(song["title"] for song in songs))

    sorted_left = merge_sort(left_half, key, steps)
    sorted_right = merge_sort(right_half, key, steps)

    return merge(sorted_left, sorted_right, key, steps)

def sort_playlist(song_text, sort_key):
    try:
        songs = parse_input(song_text)
    except ValueError as e:
        return f"Error: {str(e)}", ""

    if len(songs) == 0:
        return "Error: Please enter at least one song.", ""

    steps = []
    sorted_songs = merge_sort(songs, sort_key, steps)

    final_output = format_songs(sorted_songs)
    step_output = "\n".join(steps)

    return final_output, step_output

def load_example():
    return "\n".join(
        f"{song['title']}, {song['artist']}, {song['energy']}, {song['duration']}"
        for song in default_songs
    )

with gr.Blocks() as app:
    gr.Markdown("# Playlist Vibe Builder")
    gr.Markdown(
        "Enter songs in this format: title, artist, energy, duration. "
        "Then choose whether to sort by energy or duration."
    )

    song_input = gr.Textbox(
        label="Playlist Input",
        lines=10,
        placeholder="Example:\nBlinding Lights, The Weeknd, 90, 200"
    )

    sort_key = gr.Radio(
        choices=["energy", "duration"],
        value="energy",
        label="Choose sorting key"
    )

    with gr.Row():
        load_button = gr.Button("Load Example Playlist")
        sort_button = gr.Button("Sort Playlist")

    sorted_output = gr.Textbox(label="Sorted Playlist", lines=10)
    step_output = gr.Textbox(label="Merge Sort Steps", lines=18)

    load_button.click(fn=load_example, outputs=song_input)
    sort_button.click(
        fn=sort_playlist,
        inputs=[song_input, sort_key],
        outputs=[sorted_output, step_output]
    )

app.launch()
