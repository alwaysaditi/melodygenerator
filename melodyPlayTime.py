from pydub import AudioSegment
import numpy as np
import simpleaudio as sa



NOTE_FREQUENCIES = {
    'C': 261.63,
    'c': 277.18,  # C#
    'D': 293.66,
    'd': 311.13,  # D#
    'E': 329.63,
    'F': 349.23,
    'f': 369.99,  # F#
    'G': 392.00,
    'g': 415.30,  # G#
    'A': 440.00,
    'a': 466.16,  # A#
    'B': 493.88,
    'R': 0     # Rest
}

# NOTE_FREQUENCIES = {
#     # Octave 3
#     'C3': 130.81, 'c3': 138.59, 'D3': 146.83, 'd3': 155.56,
#     'E3': 164.81, 'F3': 174.61, 'f3': 185.00, 'G3': 196.00,
#     'g3': 207.65, 'A3': 220.00, 'a3': 233.08, 'B3': 246.94,

#     # Octave 4
#     'C4': 261.63, 'c4': 277.18, 'D4': 293.66, 'd4': 311.13,
#     'E4': 329.63, 'F4': 349.23, 'f4': 369.99, 'G4': 392.00,
#     'g4': 415.30, 'A4': 440.00, 'a4': 466.16, 'B4': 493.88,

#     # Octave 5
#     'C5': 523.25, 'c5': 554.37, 'D5': 587.33, 'd5': 622.25,
#     'E5': 659.25, 'F5': 698.46, 'f5': 739.99, 'G5': 783.99,
#     'g5': 830.61, 'A5': 880.00, 'a5': 932.33, 'B5': 987.77,

#     # Rest
#     'R': 0  # Silence
# }

def generate_sine_wave(frequency, duration_ms, sample_rate=44100, amplitude=0.5):
    t = np.linspace(0, duration_ms / 1000, int(sample_rate * duration_ms / 1000), False)
    wave = 0.5 * amplitude * np.sin(2 * np.pi * frequency * t)
    wave = (wave * 32767).astype(np.int16)
    audio_segment = AudioSegment(
        wave.tobytes(), 
        frame_rate=sample_rate, 
        sample_width=wave.dtype.itemsize, 
        channels=1
    )
    return audio_segment




# Define durations for T1 and T2
TIME_TOKENS = {
    'T1': 250,  # 500 ms
    'T2': 450  # 1000 ms
}

# Function to create a sequence of notes with T1 and T2 time tokens
def create_sequence_with_time_tokens(note_sequence, default_duration_ms=500):
    song = AudioSegment.silent(duration=0)
    current_duration_ms = default_duration_ms  # Default duration

    for note in note_sequence:
        if note in TIME_TOKENS:  # Check for T1 or T2
            current_duration_ms = TIME_TOKENS[note]  # Update the duration
        elif note in NOTE_FREQUENCIES:  # If it's a pitch note
            if note == 'R':  # Handle rest
                segment = AudioSegment.silent(duration=current_duration_ms)
            else:
                frequency = NOTE_FREQUENCIES[note]
                segment = generate_sine_wave(frequency, current_duration_ms)
            song += segment
        else:
            print(f"Unknown token: {note}. Skipping.")

    return song

# Example sequence with T1 and T2
sequence = "A T2 A T1 D T2 B T1 D T2 E T1 A T2 B T1 D T2 B T1 D T2 E T1 D T2 B T1 D T2 A T1 A T2 A T1 D T2 R T1 B T2 A T1 D T2 C T1 B T2 A T1 A T2 A T1 A T2 D T1 B T2 D T1 E T2 B T1 A T2 B T1 D T2 E T1 E T2 D T1 A T2 B T1 D T2 B T1 D T2 B T1 D T2 B T1 D T2 B T1 C T2 C T1 B T2 B T1 D T2 E T1 G T2 A T1 G T2 A T1 G T2 A T1 E T2 D T1 A T2 C T1 E T2 E T1 D T2 E T1 D T2 C T1 B T2 B T1 D T2 E T1 E T2 E T1 D T2 D T1 B T2 D T1 B T2 A T1 G T2 E T1 A T2 A T1 B T2 E T1 D T2 B T1 D T2 D T1 D T2 D T1 D T2 B T1 B T2 D T1 D T2 C T1 B T2 D T1 B T2 D T1 A T2 E T1 E T2 D T1 E T2 D T1 E T2 D T1 E T2 E T1 B T2 D T1 E T2 D T1 B T2 D T1 D T2 E T1 E T2 E T1 D T2 B T1 R T2 E T1 B T2 E T1 D T2 B T1 D T2 B T1 B T2 f T1 f T2 G T1 D T2 f T1 f T2 f T1 G T2 B T1 A T2 B T1 D T2 B T1 A T2 E T1 E T2 E T1 D T2 D T1 E T2 E T1 D T2 B T1 D T2 D T1 E T2 f T1 B T2 D T1 D T2 E T1 G T2 E T1 E T2 B T1 E T2 E T1 G T2 E T1 B T2 D T1 D T2 B T1 G T2 B T1 G T2 G T1 G T2 G T1 B T2 D T1 D T2 D T1 E T2 D T1 E T2 E T1 D T2 B T1 E T2 D T1 C T2 E T1 D T2 D T1 D T2 E T1 B T1 D T2 E T1 D T2 B T1 E T2 E T1 E T2 E T1 E T2 E T1 E T2 D T1 D T2 B T1 D T2 D T1 E T2 D T1 E T2 E T1 E T2 D T1 E T2 E T1 E T2 E T1 E T2 B T1 B T2 D T1 D T2 E T1 D T2 D T1 E T2 B T1 D T2 E T1 B T2 D T1 D T2 D T1 E T2 E T1 E T2 E".split()
#sequence1 = "RE T1 D2 g T2 D2 f T1 D2 d T2 D2 c T1 D2 E T2 D2 B T1 D3 R T2 D1 E T1 D2 g T2 D2 f T1 D2 f T2 D2 E T1 D2 R T2 D2 E T1 D2 E T2 D2 E T1 D2 g T2 D2 f T1 D2 f T2 D2 E T1 D2 R T2 D2 E T1 D3 c T2 D2 d T1 D2 E T2 D2 B T1 D2 B T2 D3 B".split()
# Create the sequence
song = create_sequence_with_time_tokens(sequence, default_duration_ms=500)

# Save the song to a .wav file
song.export("TESTING2.wav", format="wav")

# Play the .wav file using simpleaudio
# wave_obj = sa.WaveObject.from_wave_file("melody_with_T1_T2.wav")
# play_obj = wave_obj.play()
# play_obj.wait_done()
