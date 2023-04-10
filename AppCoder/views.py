from django.shortcuts import render
from .models import Curso, Profesor
from .forms import ProfesorForm
from django.http import HttpResponse

# Create your views here.

def crear_curso(request):

    nombre_curso="Programacion"
    comision_curso=10010
    print("Creando curso")
    curso=Curso(nombre=nombre_curso, comision=comision_curso)
    curso.save()
    respuesta=f"Curso creado--- {nombre_curso} - {comision_curso}"
    return HttpResponse(respuesta)

    
def cursos(request):
    
    return render(request, "AppCoder/cursos.html")

def profesores(request):

    if request.method == "POST":
        form = ProfesorForm(request.POST)
        if form.is_valid():
            profesor = Profesor()
            profesor.nombre = form.cleaned_data['nombre']
            profesor.apellido = form.cleaned_data['apellido']
            profesor.email = form.cleaned_data['email']
            profesor.profesion = form.cleaned_data['profesion']
            profesor.save()
            form = ProfesorForm()
    else:
        form = ProfesorForm()

    profesores = Profesor.objects.all() #Profesor.objects.filter(nombre__icontains="P").all()
    context = {"profesores": profesores, "form" : form}
    return render(request, "AppCoder/profesores.html", context)

def estudiantes(request):
    return render(request, "AppCoder/estudiantes.html")

def entregables(request):
    return render(request, "AppCoder/entregables.html")

def inicio(request):
    return HttpResponse("Bienvenido a la pagina principal")

def inicioApp(request):
    return render(request, "AppCoder/inicio.html")