from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .forms import AddressForm
from PIL import Image
from pdf2image import convert_from_path
from .utils import pdf_to_images, image_to_text

import os
import pyperclip
import pyocr
import pyocr.builders
import numpy as np
import subprocess
import tempfile
import time

# Adobe Acrobat Readerのパス
acr_path = "/Applications/Adobe Acrobat Reader.app/Contents/MacOS/AdobeReader"

# PDFファイルが保存されているディレクトリのパス
td_path = "/Users/itschoolkanazawawest/django/intern/emp_data/media/PDF/"

# 初期値を空のリストにする
td_list = []

def upload_pdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES['pdf']
        images = pdf_to_images(pdf_file)
        coordinates = [(50, 50, 300, 100), (50, 150, 300, 200)]
        data = {}
        for i, coord in enumerate(coordinates):
            text = image_to_text(images[0], coord)
            data[f'field_{i+1}'] = text

        form = AddressForm(initial=data)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            return render(request, 'records/upload.html', {'form': form})
    else:
        form = AddressForm()
        return render(request, 'records/upload.html', {'form': form})

def open_pdf(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        try:
            pdf_file = request.FILES['pdf']

            # ファイルを保存するパスを指定します。ここでは、MEDIA_ROOTディレクトリ内に保存します。
            save_path = os.path.join(settings.MEDIA_ROOT, pdf_file.name)

            # 保存先ディレクトリが存在しない場合は作成
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # ファイルを保存します。
            with open(save_path, 'wb') as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)

            # Adobe Acrobat Readerを起動し、PDFファイルを開く
            subprocess.Popen([acr_path, save_path])

            # 少し待ってから最前面に表示するためのAppleScriptを実行
            applescript = '''
            delay 1
            tell application "Adobe Acrobat Reader"
                activate
            end tell
            '''
            subprocess.Popen(['osascript', '-e', applescript])

            # ファイルの保存が完了したことをメッセージで返します。
            success_message = "PDFファイルが正常にアップロードされ、Adobe Acrobat Reader で開かれました。"
            return JsonResponse({'success_message': success_message})

        except Exception as e:
            error_message = str(e)
            return JsonResponse({'error_message': error_message}, status=500)

    # POSTリクエストでファイルが送信されていない場合は、フォームを再表示します。
    return render(request, 'records/open.html')

def upload_pdf_page(request):
    return render(request, 'records/extract.html')

@csrf_exempt
def extract_text_from_uploaded_pdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf')
        if pdf_file:
            extracted_text = perform_ocr(pdf_file)
            return JsonResponse({'extracted_text': extracted_text})
        else:
            return JsonResponse({'error_message': 'PDFファイルがアップロードされていません。'}, status=400)
    else:
        return JsonResponse({'error_message': 'POSTリクエストのみ受け付けます。'}, status=405)

import tempfile

def perform_ocr(pdf_file):
    tool = pyocr.get_available_tools()[0]  # OCRツールを取得
    lang = 'jpn'  # 使用する言語を指定（日本語の場合）

    # PDFを一時ファイルに保存
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
        for chunk in pdf_file.chunks():
            temp_pdf.write(chunk)

    # 一時ファイルのパスを取得
    pdf_path = temp_pdf.name

    # PDFを画像に変換
    images = convert_from_path(pdf_path)

    # 画像からテキストを抽出
    extracted_text = ""
    for img in images:
        extracted_text += tool.image_to_string(
            Image.fromarray(np.array(img)),  # PIL Imageに変換
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )

    # 一時ファイルを削除
    os.unlink(pdf_path)

    return extracted_text


def process_pdf_and_copy_text(pdf_path):  # PDFファイルを開き、OCRを使用してテキストを抽出し、クリップボードにコピーします
    pdf_pro = subprocess.Popen([acr_path, pdf_path])
    time.sleep(5)  # PDFが開くまでの待機時間を十分に取る

    extracted_text = perform_ocr(pdf_path)
    pyperclip.copy(extracted_text)  # テキストをクリップボードにコピー
    print("テキストをクリップボードにコピーしました:", extracted_text)

    # 以下、PDFを閉じる処理などを追加することも可能です

def my_view(request):
    if request.method == 'POST':
        # アップロードされたファイルにアクセス
        uploaded_file = request.FILES['pdf']

        # ファイルを保存するために一時的なファイルパスを作成
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

            # 一時的なファイルのパスを取得
            uploaded_file_path = temp_file.name

        # td_listにアップロードされたPDFファイルのパスを追加
        td_list.append(uploaded_file_path)  # ここをリストの追加に変更

        # ここで追加の処理を行う

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'POSTリクエストのみ受け付けます。'})

if __name__ == '__main__':
    for idx, file in enumerate(td_list):
        print('open:', file)
        process_pdf_and_copy_text(td_path + file)


