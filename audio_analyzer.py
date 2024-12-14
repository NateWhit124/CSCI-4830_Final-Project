import scipy.fft as fft
import scipy.signal
from pydub import AudioSegment
from matplotlib import pyplot as plt
import numpy as np
import os

do_plot = False
spectrogram_data_dir = "spectrogram data"
downsample_factor = 50

sounds_dir = "audio samples"
sounds = [AudioSegment.from_mp3(os.path.join(sounds_dir,file)) for file in os.listdir(sounds_dir)]
sound_names = os.listdir(sounds_dir)

for idx,sound in enumerate(sounds):
    # obtain various sound data
    raw_data = sound.raw_data
    duration = sound.duration_seconds
    sample_rate = sound.frame_rate
    sample_width = sound.sample_width
    channels = sound.channels

    # get audio signal amplitudes from raw data bytes
    signal : np.ndarray = np.frombuffer(raw_data, dtype ="int16") / 32768.0
    signal = signal.reshape(-1,channels) # reshape so that rows represent each channel
    time = np.arange(0,duration,1/sample_rate)
    mono_signal = signal.mean(axis = 1) # convert to mono

    # create spectrogram to show temporal frequency profile
    f,t,Sxx = scipy.signal.spectrogram(mono_signal, sample_rate)
    # Downsample the spectrogram in the time dimension
    Sxx_downsampled = Sxx[:, ::downsample_factor]  # Downsample time columns
    t_downsampled = t[::downsample_factor]  # Downsample time vector
    epsilon = 1e-10 # add a small value to Sxx_downsampled to avoid inf when taking log10
    Sxx_downsampled = 10 * np.log10(Sxx_downsampled + epsilon)

    # plot
    if do_plot:
        plt.figure(figsize=(10, 5))
        plt.pcolormesh(t_downsampled, f, Sxx_downsampled, shading='gouraud')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.title(f"Spectrogram of {sound_names[idx]}")

    # Put the data into CSV
    Sxx_normalized = Sxx_downsampled / np.max(Sxx_downsampled) # normalize data
    rows, cols = Sxx_normalized.shape
    csv_data = np.zeros((rows + 1, cols + 1), dtype=object)  # Add extra row and column for headers
    csv_data[0, 1:] = t_downsampled  # time values in  first row (skip 0,0)
    csv_data[1:, 0] = f  # frequency values in first column
    # Fill in the spectrogram data
    csv_data[1:, 1:] = Sxx_normalized

    # Save to CSV
    file_name = f"{sound_names[idx]} Spectrogram Data.csv"
    file_path = os.path.join(spectrogram_data_dir,file_name)
    np.savetxt(file_path, csv_data, delimiter=",")

if do_plot:
    plt.show()

