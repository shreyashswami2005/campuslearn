from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from .models import Material
from .forms import MaterialForm

@login_required
def material_list(request):
    materials = Material.objects.all().order_by('-uploaded_at')
    return render(request, 'study_materials/list.html', {'materials': materials})

@login_required
def material_upload(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.uploaded_by = request.user
            material.save()
            return redirect('study_materials:material_list')
    else:
        form = MaterialForm()
    return render(request, 'study_materials/upload.html', {'form': form})

@login_required
def material_download(request, pk):
    material = get_object_or_404(Material, pk=pk)
    try:
        return FileResponse(material.file.open('rb'), as_attachment=True, filename=material.file.name.split('/')[-1])
    except Exception:
        raise Http404('File not found')

