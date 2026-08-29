import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random

duration = 5  # segundos de gravação
sample_rate = 44100

linguas = {"Inglês":"en",
           "Espanhol":"es",
           "Russo":"ru",
           "Português":"pt",
           "Indonésio":"id",
           "Polonês":"pl",
           "Italiano":"it",
           "Turco":"tr"}

words_by_level = {
    "fácil": ["gato", "cachorro", "maçã", "leite", "sol"],
    "médio": ["casa", "escola", "amigo", "janela", "amarelo"],
    "difícil": ["tecnologia", "universidade", "informação", "pronúncia", "imaginação"]
}

reconpensa = {
    "fácil": 1,
    "médio": 2,
    "difícil": 3
}
lingua = None
dificuldade = None

pontos = 0
vida = 5

while vida >0:
    while dificuldade not in words_by_level:
        for i in words_by_level:
            print(i)
        dificuldade = input("escolha uma dificuldade").lower().strip()
    
    try:
        while lingua == None:
            for i in linguas:
                print(i)
            try:
                lingua = linguas[input("Qual língua voce deseja praticar").capitalize().strip()]
            except KeyError:
                print("Língua não reconhecida")
    
        palavra = random.choice(words_by_level[dificuldade])
        print(f"Tente traduzir essa palavra: {palavra}, para {lingua}")
        print("Fale agora...")
        recording = sd.rec(
          int(duration * sample_rate), # o número de amostras a serem registradas
          samplerate=sample_rate,      # taxa de amostras
          channels=1,                  # 1 significa gravação mono
          dtype="int16")               # tipo de dados para as amostras registradas
        sd.wait()  # aguardando o término da gravação
        recognizer = sr.Recognizer()
        wav.write("output.wav", sample_rate, recording)
        print("Gravação concluída, estou reconhecendo...")
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)
            
        text = recognizer.recognize_google(audio, language=lingua).lower().strip()
        translator = Translator()
        translated = translator.translate(text, dest="pt")
        print("Você disse:", text)
        if text.lower().strip() == palavra.lower().strip():
            print("Meus parabéns sua pronuncia está correta")
            print(f"você ganhou {reconpensa[dificuldade]*25} pontos")
            pontos += reconpensa[dificuldade] * 25
        else:
            vida -= 1
            print("Sua pronúncia está incorreta")
            print("Você perdeu uma vida")
            print(f"Ainda restam {vida}")
    except sr.UnknownValueError:             # - se o Google não conseguiu entender a fala devido a ruídos ou silêncio
        print("A fala não pôde ser reconhecida.")
    except sr.RequestError as e:             # - se não houver conexão com a Internet ou a API estiver indisponível
        print(f"Service error: {e}")
    dificuldade = None
    lingua = None
print(f"Sua pontuação total foi de {pontos}")
