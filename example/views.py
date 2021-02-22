from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from io import BytesIO
import speech_recognition as sr

def index(request):
    return render(request, 'example/index.html', {})

@csrf_exempt
def speech_to_text(request):
    if request.method == 'POST':
        file = request.FILES.get('audio_data', None)
        r = sr.Recognizer()
        audio_file = sr.AudioFile(BytesIO(file.read()))
        with audio_file as source:
            recording = r.record(source)
        try:
            output = r.recognize_google(recording, language="id-ID")
        except sr.UnknownValueError:
            output = "<<could not understand audio>>"
        except sr.RequestError as e:
            output = "Could not request results; {0}".format(e)

        text = output
        return JsonResponse({'error': False, 'result': text})
    return JsonResponse({'error': True, 'result': "null"})
