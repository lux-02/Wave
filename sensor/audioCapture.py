### 오디오 캡쳐 (아두이노 연결 필요)


import pyaudio
import serial
import numpy as np

# 오디오 설정
FORMAT = pyaudio.paInt16  # 데이터 형식
CHANNELS = 1
RATE = 44100  # 샘플 레이트
CHUNK = 1024  # 데이터 덩어리 크기

# 시리얼 포트 설정
arduino = serial.Serial('/dev/tty.usbmodem14201', 9600)

# PyAudio 시작
audio = pyaudio.PyAudio()

# 스트림 열기
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

try:
    while True:
        data = stream.read(CHUNK)
        numpydata = np.fromstring(data, dtype=np.int16)
        # 여기서 데이터를 처리하고 필요한 값을 추출하세요
        the_value = int(np.abs(numpydata).mean())  # 예제로 평균 볼륨 수치를 계산

        # 아두이노로 데이터 전송
        arduino.write(str(the_value).encode())

except KeyboardInterrupt:
    # 정리
    stream.stop_stream()
    stream.close()
    audio.terminate()
    arduino.close()
    print("Stopped Recording")

