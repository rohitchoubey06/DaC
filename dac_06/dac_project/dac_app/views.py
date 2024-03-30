from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import UploadedFile  # Import your UploadedFile model
import pandas as pd
from urllib.parse import urljoin
from .cleaner import data_cleaner,convert_object_to_date
from django.http import HttpResponse

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        # file_url = fs.url(filename)
        file_url = urljoin(settings.MEDIA_URL, filename)

        # Create a model instance and save it to the database
        # uploaded_file_obj = UploadedFile.objects.create(file=filename)

        # Process the uploaded file (e.g., read data from Excel or CSV)
        # For example, you can use pandas to read the data



        # Perform further processing on the DataFrame (e.g., data cleaning, analysis)

        # Pass the DataFrame to the success.html template for display
        return render(request, 'success.html', {'file_url': file_url})

    return render(request, 'upload.html')

from datetime import datetime

def upload_success(request):
    if request.method == "POST":
        file = request.FILES['file'] #main error point
        uploaded_at = datetime.now()  # Set 'uploaded_at' to the current date and time
        x = UploadedFile(file=file, uploaded_at=uploaded_at)
        x.save()

    return render(request, "success.html",{'file_url': file.name})

def download(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = urljoin(settings.MEDIA_URL, filename)
        if filename.endswith('.csv'):
            # Use os.path.join() to construct file paths
            file_path = settings.MEDIA_ROOT + '/' + filename
            df = pd.read_csv(file_path)
            data_cleaner(df)
            convert_object_to_date(df)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="modified_data.csv"'
            df.to_csv(response, index=False)
            return response
        elif filename.endswith(('.xls', '.xlsx')):
            file_path = settings.MEDIA_ROOT + '/' + filename
            df = pd.read_excel(file_path)
            data_cleaner(df)
            convert_object_to_date(df)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="modified_data.xlsx"'
            df.to_excel(response, index=False)
            return response
        else:
            return render(request, 'error.html', {'message': 'Unsupported file format'})
    else:
        return render(request, 'download.html')






