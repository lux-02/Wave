### 오디오 캡처 시뮬레이션 (No 아두이노)


import pyaudio
import numpy as np

# 오디오 스트림을 설정합니다.
FORMAT = pyaudio.paInt16  # 16비트 포맷
CHANNELS = 1
RATE = 44100  # 샘플 레이트: 44.1kHz
CHUNK = 1024  # 블록 크기

# PyAudio 객체를 생성합니다.
audio = pyaudio.PyAudio()

# 스트림을 열고 마이크로부터 오디오를 캡처하기 시작합니다.
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

try:
    while True:
        data = stream.read(CHUNK)
        # 넘파이 배열로 데이터 변환
        numpydata = np.frombuffer(data, dtype=np.int16)
        # 볼륨 수치 계산: 데이터의 RMS 값
        volume = np.sqrt(np.mean(numpydata**2))
        print("Volume:", volume)

except KeyboardInterrupt:
    # 사용자가 Ctrl+C를 누르면 종료
    print("Stopped by User")

finally:
    # 스트림을 정리합니다.
    stream.stop_stream()
    stream.close()
    audio.terminate()
