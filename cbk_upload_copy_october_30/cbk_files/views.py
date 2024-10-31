from http.client import responses
import os
from django.http import HttpResponse
from django.shortcuts import render
from .forms import FileUploadForm, BanqueMisrUploadForm
import pandas as pd
from .external_validation import compare_6_7, compare_1A_C2, compare_1A_1B, compare_1B_1B1, compare_4B_7, \
    compare_5A_5B_5C, compare_4A_5A, compare_4B_5B
from .misr_validation import misr_fixes


# Helper function to process city monthly files
def process_file(file):
    return file


# First tab view: City Monthly File Upload
def upload_file(request):
    bm_form = BanqueMisrUploadForm()  # Initialize bm_form in the first tab view

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = [request.FILES['file1A'],
                    request.FILES['file1B'],
                    request.FILES['file1B1'],
                    request.FILES['fileC2'],
                    request.FILES['file4A'],
                    request.FILES['file4B'],
                    request.FILES['file5A'],
                    request.FILES['file5B'],
                    request.FILES['file5C'],
                    request.FILES['file6'],
                    request.FILES['file7']
                    ]
            output_total1 = process_part1(file)

            return render(request, 'upload.html', {'output': output_total1, 'form': form, 'bm_form': BanqueMisrUploadForm()})
    else:
        form = FileUploadForm()
        bm_form = BanqueMisrUploadForm()
    return render(request, 'upload.html', {'form': form, 'bm_form': bm_form})


# Process files for city monthly upload (first tab)
def process_part1(file):
    output1 = compare_1A_1B(file[0], file[1])
    file[0].seek(0)
    file[1].seek(0)

    output2 = compare_1B_1B1(file[1], file[2])
    file[1].seek(0)
    file[2].seek(0)

    output3 = compare_1A_C2(file[0], file[3])
    file[0].seek(0)
    file[3].seek(0)

    output4 = compare_4B_7(file[5], file[10])
    file[5].seek(0)
    file[10].seek(0)

    output5 = compare_4A_5A(file[4], file[6])
    file[4].seek(0)
    file[6].seek(0)

    output6 = compare_4B_5B(file[5], file[7])
    file[5].seek(0)
    file[7].seek(0)

    output7 = compare_6_7(file[9], file[10])
    file[9].seek(0)
    file[10].seek(0)

    output = [output1, output2, output3, output4, output5, output6, output7]
    return output


# Second tab view: Banque Misr File Upload
def banque_misr_upload(request):
    file_form = FileUploadForm()  # Initialize file_form in the second tab view

    if request.method == 'POST':
        bm_form = BanqueMisrUploadForm(request.POST, request.FILES)
        if bm_form.is_valid():
            file = request.FILES['fileBM']
            output_bm = process_part2(file)

            # Generate processed file for download
            processed_file = misr_fixes(file)
            original_filename = os.path.splitext(file.name)[0]

            response = HttpResponse(processed_file, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{original_filename}.txt"'
            return response

    else:
        bm_form = BanqueMisrUploadForm()
        form = FileUploadForm()

    return render(request, 'upload.html', {'bm_form': bm_form, 'form': form})


# Process files for Banque Misr upload (second tab)
def process_part2(file):
    output = misr_fixes(file)
    return output


# Helper function to create downloadable file
def handle_banque_misr_file(file):
    # Process the Banque Misr file and generate a new file for download
    processed_file_path = '/path/to/processed/output_bm.txt'
    # Save or modify the file accordingly
    return processed_file_path
