import gradio as gr   # Gradio builds the graphical user interface
import random         # Used to generate a random example playlist
import time           # Used to slow down the live simulation for visibility


# -------------------------------------------------
# LARGE SONG DATASET
# -------------------------------------------------
# This built-in dataset gives the user many different songs
# to test sorting with. Each song is stored as:
# (title, artist, energy, duration)
#
# energy: whole number from 0 to 100
# duration: whole number in seconds
SONG_POOL = [
    ("Blinding Lights", "The Weeknd", 90, 200),
    ("Sunflower", "Post Malone", 65, 158),
    ("Levitating", "Dua Lipa", 85, 203),
    ("Stay", "Kid LAROI", 80, 141),
    ("Heat Waves", "Glass Animals", 70, 238),
    ("As It Was", "Harry Styles", 60, 167),
    ("Midnight City", "M83", 75, 245),
    ("Bad Guy", "Billie Eilish", 55, 194),
    ("HUMBLE.", "Kendrick Lamar", 88, 177),
    ("Peaches", "Justin Bieber", 72, 198),
    ("Circles", "Post Malone", 68, 215),
    ("Shape of You", "Ed Sheeran", 78, 233),
    ("Rockstar", "DaBaby", 82, 181),
    ("SICKO MODE", "Travis Scott", 91, 312),
    ("Goosebumps", "Travis Scott", 84, 243),
    ("One Dance", "Drake", 66, 173),
    ("Closer", "The Chainsmokers", 74, 244),
    ("Faded", "Alan Walker", 62, 212),
    ("Memories", "Maroon 5", 50, 189),
    ("Believer", "Imagine Dragons", 87, 204),
    ("Thunder", "Imagine Dragons", 83, 187),
    ("Radioactive", "Imagine Dragons", 86, 186),
    ("Starboy", "The Weeknd", 89, 230),
    ("Save Your Tears", "The Weeknd", 76, 215),
    ("Attention", "Charlie Puth", 71, 211),
    ("Senorita", "Shawn Mendes", 69, 191),
    ("Uptown Funk", "Bruno Mars", 92, 269),
    ("24K Magic", "Bruno Mars", 91, 226),
    ("Rolling in the Deep", "Adele", 73, 228),
    ("Hello", "Adele", 52, 295),
    ("Someone Like You", "Adele", 40, 285),
    ("Counting Stars", "OneRepublic", 79, 257),
    ("Apologize", "OneRepublic", 58, 210),
    ("Sugar", "Maroon 5", 81, 235),
    ("Girls Like You", "Maroon 5", 67, 233),
    ("Titanium", "David Guetta", 85, 245),
    ("Wake Me Up", "Avicii", 88, 247),
    ("Levels", "Avicii", 93, 226),
    ("Lean On", "Major Lazer", 77, 176),
    ("Cheap Thrills", "Sia", 74, 225),
    ("Chandelier", "Sia", 86, 216),
    ("Royals", "Lorde", 48, 190),
    ("Team", "Lorde", 55, 213),
    ("Pompeii", "Bastille", 78, 214),
    ("Habits", "Tove Lo", 61, 208),
    ("Animals", "Martin Garrix", 95, 210),
    ("Don't You Worry Child", "Swedish House Mafia", 89, 212),
    ("Clarity", "Zedd", 82, 248),
    ("Stay High", "Tove Lo", 64, 223),
    ("Bad Habits", "Ed Sheeran", 79, 231),
]


# -------------------------------------------------
# EXAMPLE PLAYLIST
# -------------------------------------------------
def load_example() -> str:
    """Return a randomly generated example playlist in valid input format."""
    sample = random.sample(SONG_POOL, 7)
    return "\n".join(f"{title} | {artist} | {energy} | {duration}" for title, artist, energy, duration in sample)


# -------------------------------------------------
# INPUT PARSING AND VALIDATION
# -------------------------------------------------
def parse_input(text: str):
    """Parse playlist text into valid song dictionaries and collect any input errors."""
    valid_songs = []
    errors = []

    # Split full input into one line per song
    lines = text.split("\n")

    # start=1 makes error messages easier for the user to understand
    for line_number, line in enumerate(lines, start=1):
        # Ignore blank lines
        if not line.strip():
            continue

        # Each line should follow:
        # Title | Artist | Energy | Duration
        parts = [part.strip() for part in line.split("|")]

        if len(parts) != 4:
            errors.append(f"Line {line_number}: wrong format. Use Title | Artist | Energy | Duration")
            continue

        title, artist, energy_text, duration_text = parts

        if not title:
            errors.append(f"Line {line_number}: missing title")
            continue

        if not artist:
            errors.append(f"Line {line_number}: missing artist")
            continue

        # Convert energy to integer
        try:
            energy = int(energy_text)
        except ValueError:
            errors.append(f"Line {line_number}: energy must be a whole number")
            continue

        # Convert duration to integer
        try:
            duration = int(duration_text)
        except ValueError:
            errors.append(f"Line {line_number}: duration must be a whole number")
            continue

        # Check allowed ranges
        if not (0 <= energy <= 100):
            errors.append(f"Line {line_number}: energy must be between 0 and 100")
            continue

        if duration <= 0:
            errors.append(f"Line {line_number}: duration must be greater than 0")
            continue

        # Store valid songs in dictionary form for easier field access
        valid_songs.append({
            "title": title,
            "artist": artist,
            "energy": energy,
            "duration": duration
        })

    return valid_songs, errors


# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------
def get_val(song: dict, key: str):
    """Return the comparison value for a song based on the selected sorting key."""
    # Text values are converted to lowercase so sorting is case-insensitive
    if key in ["title", "artist"]:
        return song[key].lower()
    return song[key]


def format_songs(songs: list) -> str:
    """Format songs into a readable multi-line string for the GUI."""
    if not songs:
        return "No valid songs."
    return "\n".join(
        f"{song['title']} • {song['artist']} | Energy: {song['energy']} | Duration: {song['duration']}s"
        for song in songs
    )


# -------------------------------------------------
# MERGE SORT
# -------------------------------------------------
# This project uses a fully custom Merge Sort implementation.
# Python built-in sorting functions such as sorted() and list.sort()
# are not used for the core algorithm.
def merge(left: list, right: list, key: str, steps: list, reverse: bool) -> list:
    """Merge two already-sorted lists into one sorted list while recording explanation steps."""
    merged = []
    left_index = 0
    right_index = 0

    # Compare front elements from both halves until one side is exhausted
    while left_index < len(left) and right_index < len(right):
        left_val = get_val(left[left_index], key)
        right_val = get_val(right[right_index], key)

        steps.append(
            f"Compare: {left[left_index]['title']} ({left_val}) vs {right[right_index]['title']} ({right_val})"
        )

        # If values are equal, the left item is taken first.
        # This keeps the merge process stable and predictable.
        take_left = (left_val <= right_val and not reverse) or (left_val >= right_val and reverse)

        if take_left:
            merged.append(left[left_index])
            steps.append(f"Place: {left[left_index]['title']}")
            left_index += 1
        else:
            merged.append(right[right_index])
            steps.append(f"Place: {right[right_index]['title']}")
            right_index += 1

    # Append any leftover songs from the left half
    while left_index < len(left):
        merged.append(left[left_index])
        steps.append(f"Add remaining from left: {left[left_index]['title']}")
        left_index += 1

    # Append any leftover songs from the right half
    while right_index < len(right):
        merged.append(right[right_index])
        steps.append(f"Add remaining from right: {right[right_index]['title']}")
        right_index += 1

    steps.append("Merged block complete.")
    return merged


def merge_sort(songs_list: list, key: str, steps: list, reverse: bool) -> list:
    """Recursively split and merge a list of songs using Merge Sort."""
    # Base case: a list with 0 or 1 item is already sorted
    if len(songs_list) <= 1:
        return songs_list

    mid = len(songs_list) // 2

    # Record the split so the user can see the divide-and-conquer process
    steps.append(
        f"Split list of {len(songs_list)} songs into left half ({mid}) and right half ({len(songs_list) - mid})"
    )

    left_half = merge_sort(songs_list[:mid], key, steps, reverse)
    right_half = merge_sort(songs_list[mid:], key, steps, reverse)

    return merge(left_half, right_half, key, steps, reverse)


# -------------------------------------------------
# QUIZ FEATURE
# -------------------------------------------------
def generate_quiz(songs: list, key: str, order: str):
    """Generate a quiz question that checks whether the user understands the chosen sorting rule."""
    if len(songs) < 2:
        return "Not enough songs for quiz.", None

    song_a, song_b = random.sample(songs, 2)
    value_a = get_val(song_a, key)
    value_b = get_val(song_b, key)

    if order == "Ascending":
        correct = "Yes" if value_a > value_b else "No"
    else:
        correct = "Yes" if value_a < value_b else "No"

    question = (
        f"Sorting by {key} in {order.lower()} order:\n\n"
        f"Should '{song_a['title']}' come after '{song_b['title']}'?"
    )

    return question, correct


def answer_yes(correct_answer):
    """Check whether the user's Yes answer matches the stored correct answer."""
    if not correct_answer:
        return "No quiz available."
    return "✅ Correct" if correct_answer == "Yes" else "❌ Incorrect. Correct answer: No"


def answer_no(correct_answer):
    """Check whether the user's No answer matches the stored correct answer."""
    if not correct_answer:
        return "No quiz available."
    return "✅ Correct" if correct_answer == "No" else "❌ Incorrect. Correct answer: Yes"


# -------------------------------------------------
# LIVE SORT SIMULATION
# -------------------------------------------------
def live_sort(text: str, key: str, order: str, speed: float):
    """Run the Merge Sort simulation live and update the GUI step by step."""
    songs, errors = parse_input(text)

    # If there are no valid songs, stop immediately and show errors
    if not songs:
        yield "", "", "", "\n".join(errors) if errors else "No valid songs entered."
        return

    reverse = order == "Descending"
    steps = []

    # Run the custom Merge Sort and collect the explanation steps
    sorted_songs = merge_sort(songs, key, steps, reverse)

    # Add a final summary step so the result is clearly explained to the user
    steps.append(f"Sorting complete. Playlist sorted by {key} in {order.lower()} order.")

    # yield lets Gradio update the GUI gradually, creating a live simulation
    delay = 0.2 + (1 - speed) * 0.8
    current_steps = ""

    for step in steps:
        current_steps += step + "\n"
        yield (
            format_songs(songs),
            "",
            current_steps,
            "\n".join(errors) if errors else "No errors"
        )
        time.sleep(delay)

    yield (
        format_songs(songs),
        format_songs(sorted_songs),
        current_steps,
        "\n".join(errors) if errors else "No errors"
    )


# -------------------------------------------------
# GUIDED EXPLANATION
# -------------------------------------------------
def guided_demo(key: str, order: str):
    """Show a simple teaching explanation of how Merge Sort works."""
    demo_lines = [
        "Step 1: Start with an unsorted playlist.",
        "Step 2: Merge sort splits the playlist into smaller halves.",
        "Step 3: It keeps splitting until each section has only one song.",
        f"Step 4: Now it compares songs using the chosen key: {key}.",
        f"Step 5: Because the order is {order.lower()}, it decides which song should come first.",
        "Step 6: The smaller sorted sections are merged back together.",
        "Step 7: This repeats until the full playlist is rebuilt in sorted order.",
        "Why merge sort is useful: it is efficient and organized, especially for larger lists."
    ]

    output = ""
    for line in demo_lines:
        output += line + "\n\n"
        yield output
        time.sleep(1.1)


# -------------------------------------------------
# RESET FUNCTION
# -------------------------------------------------
def reset_all():
    """Clear all interface components so the user can start over."""
    return "", "", "", "", "", "", ""


# -------------------------------------------------
# QUIZ SETUP
# -------------------------------------------------
def setup_quiz(text: str, key: str, order: str):
    """Prepare the quiz question and store the correct answer before sorting begins."""
    songs, _ = parse_input(text)
    question, correct = generate_quiz(songs, key, order)
    return question, "", correct


# -------------------------------------------------
# USER INTERFACE (GRADIO)
# -------------------------------------------------
with gr.Blocks() as app:
    # Custom CSS for a cleaner and more polished interface
    gr.Markdown("""
    <style>
    body { background:#f5f5f7; font-family:-apple-system, BlinkMacSystemFont, sans-serif; }
    textarea { border-radius:16px; border:1px solid #ddd; }
    .gr-button { background:black !important; color:white !important; border-radius:999px !important; }
    h1 { text-align:center; }
    </style>
    """)

    gr.Markdown("# Playlist Vibe Builder")
    gr.Markdown("Enter one song per line using this format: **Title | Artist | Energy | Duration**")

    # Main input box for the user's playlist
    song_input = gr.Textbox(
        lines=8,
        label="Playlist Input",
        placeholder="Example:\nBlinding Lights | The Weeknd | 90 | 200"
    )

    # Controls for choosing the sorting key and order
    with gr.Row():
        key = gr.Dropdown(
            ["energy", "duration", "title", "artist"],
            value="energy",
            label="Sort by"
        )
        order = gr.Dropdown(
            ["Ascending", "Descending"],
            value="Ascending",
            label="Order"
        )

    # Speed slider controls how fast the live simulation plays
    speed = gr.Slider(0, 1, value=0.35, label="Live Sort Speed")

    # Main action buttons
    with gr.Row():
        load_btn = gr.Button("Random Example")
        sort_btn = gr.Button("Start Live Sort")
        guided_btn = gr.Button("Guided Example")
        reset_btn = gr.Button("Reset")

    # Quiz section
    quiz_question = gr.Markdown(label="Quiz")
    quiz_result = gr.Textbox(label="Quiz Result")
    quiz_answer = gr.State()

    with gr.Row():
        yes_btn = gr.Button("Yes")
        no_btn = gr.Button("No")

    # Main outputs
    before_box = gr.Textbox(label="Original Playlist", lines=8)
    after_box = gr.Textbox(label="Sorted Playlist", lines=8)

    # Accordion sections keep extra details visible but not cluttered
    with gr.Accordion("Sorting Steps", open=False):
        steps_box = gr.Textbox(lines=10, label="Step-by-Step Merge Sort Log")

    with gr.Accordion("Guided Explanation", open=False):
        guided_output = gr.Textbox(lines=10)

    with gr.Accordion("Input Errors", open=False):
        errors_box = gr.Textbox(lines=6)

    # -------------------------------------------------
    # BUTTON LOGIC
    # -------------------------------------------------

    # Load a random valid playlist into the input box
    load_btn.click(load_example, outputs=song_input)

    # First set up the quiz, then run the live sorting simulation
    sort_btn.click(
        setup_quiz,
        inputs=[song_input, key, order],
        outputs=[quiz_question, quiz_result, quiz_answer]
    ).then(
        live_sort,
        inputs=[song_input, key, order, speed],
        outputs=[before_box, after_box, steps_box, errors_box]
    )

    # Quiz answer buttons
    yes_btn.click(answer_yes, inputs=quiz_answer, outputs=quiz_result)
    no_btn.click(answer_no, inputs=quiz_answer, outputs=quiz_result)

    # Guided conceptual explanation
    guided_btn.click(
        guided_demo,
        inputs=[key, order],
        outputs=guided_output
    )

    # Reset all visible outputs, then clear the stored quiz state
    reset_btn.click(
        reset_all,
        outputs=[song_input, before_box, after_box, steps_box, guided_output, errors_box, quiz_result]
    ).then(
        lambda: ("", None),
        outputs=[quiz_question, quiz_answer]
    )

# Launch the Gradio app
app.launch()
