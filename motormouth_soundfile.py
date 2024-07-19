import librosa
import numpy as np

def analyze_amplitude(file_path):
    # Load the audio file
    y, sr = librosa.load(file_path)

    # Calculate the amplitude envelope
    amplitude_envelope = np.abs(librosa.effects.preemphasis(y))

    # Normalize the amplitude envelope to the range [0, 1]
    normalized_amplitude = (amplitude_envelope - np.min(amplitude_envelope)) / (np.max(amplitude_envelope) - np.min(amplitude_envelope))

    # Map the normalized amplitude to the range [0, 180]
    angles = 180 * normalized_amplitude

    # Generate timestamps with a frequency of 1 per half-second
    timestamps = np.arange(0, len(angles) / sr, 0.5)

    # Find the maximum angle within plus-minus 0.25 seconds for each timestamp
    sampled_angles = [np.max(angles[max(0, int((t - 0.25) * sr)): min(len(angles), int((t + 0.25) * sr))]) for t in timestamps]

    return timestamps, sampled_angles

# Example usage:
file_path = '/home/va55/Code/Antro-Objects/SharedAudio/speech.mp3'  # Replace with the path to your audio file (MP3 or WAV)
timestamps, angles = analyze_amplitude(file_path)

# Print the timestamps and angles
for timestamp, angle in zip(timestamps, angles):
    print(f'Timestamp: {timestamp:.2f} seconds, Angle: {angle:.2f} degrees')

