from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def material_list(request):
    """Display a simple list of materials (placeholder)."""
    return HttpResponse('<h1>Materials List</h1><p>Placeholder content.</p>')

@login_required
def material_upload(request):
    """Handle material upload (placeholder)."""
    if request.method == "POST":
        return HttpResponse('Material uploaded successfully.')
    return HttpResponse('<h1>Upload Material</h1><p>Upload form placeholder.</p>')

@login_required
def material_download(request, pk):
    """Download a material file (placeholder)."""
    return HttpResponse(f'Download material with id {pk}.')
