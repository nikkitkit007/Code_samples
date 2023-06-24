import speech_recognition


def recognise(file) -> str:

    sample = speech_recognition.WavFile(file)

    r = speech_recognition.Recognizer()

    with sample as audio:  # преобразование звукового файла в объект
        # r.adjust_for_ambient_noise(audio, duration=0.5)  # здесь удаление шумов, но оно как-то странно работает. надо разобраться в его настройках
        content = r.record(audio)

    return r.recognize_google(content, language="ru-RU")
