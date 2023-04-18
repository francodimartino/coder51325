from django.shortcuts import render
from .models import Curso, Profesor, Estudiante, Avatar
from .forms import ProfesorForm, RegistroUsuarioForm, UserEditForm, AvatarForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate

from django.contrib.auth.decorators import login_required #para vistas basadas en funciones DEF  
from django.contrib.auth.mixins import LoginRequiredMixin #para vistas basadas en clases CLASS   

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


@login_required
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

    avatar= Avatar.objects.filter(user=request.user.id)[0].imagen.url
    
    return render(request, "AppCoder/profesores.html", {"profesores": profesores, "form" : form, "avatar":avatar})

@login_required
def busquedaComision(request):
    
    return render(request, "AppCoder/busquedaComision.html", {"avatar":obtenerAvatar(request)})

def obtenerAvatar(request):

    avatares=Avatar.objects.filter(user=request.user.id)
    if len(avatares)!=0:
        return avatares[0].imagen.url
    else:
        return "/media/avatars/avatarpordefecto.png"



@login_required
def buscar(request):
    
    comision= request.GET["comision"]
    if comision!="":
        cursos= Curso.objects.filter(comision__icontains=comision)#buscar otros filtros en la documentacion de django
        return render(request, "AppCoder/resultadosBusqueda.html", {"cursos": cursos})
    else:
        return render(request, "AppCoder/busquedaComision.html", {"mensaje": "Che Ingresa una comision para buscar!", "avatar":obtenerAvatar(request)})

@login_required
def eliminarProfesor(request, id):
    profesor=Profesor.objects.get(id=id)
    print(profesor)
    profesor.delete()
    profesores=Profesor.objects.all()
    form = ProfesorForm()
    return render(request, "AppCoder/Profesores.html", {"profesores": profesores, "mensaje": "Profesor eliminado correctamente", "form": form})


@login_required
def editarProfesor(request, id):
    profesor=Profesor.objects.get(id=id)
    if request.method=="POST":
        form= ProfesorForm(request.POST)
        if form.is_valid():
            
            info=form.cleaned_data
            
            profesor.nombre=info["nombre"]
            profesor.apellido=info["apellido"]
            profesor.email=info["email"]
            profesor.profesion=info["profesion"]

            profesor.save()
            profesores=Profesor.objects.all()
            form = ProfesorForm()
            return render(request, "AppCoder/Profesores.html" ,{"profesores":profesores, "mensaje": "Profesor editado correctamente", "form": form})
        pass
    else:
        formulario= ProfesorForm(initial={"nombre":profesor.nombre, "apellido":profesor.apellido, "email":profesor.email, "profesion":profesor.profesion})
        return render(request, "AppCoder/editarProfesor.html", {"form": formulario, "profesor": profesor})
@login_required
def estudiantes(request):
    return render(request, "AppCoder/estudiantes.html")

def entregables(request):
    return render(request, "AppCoder/entregables.html")

def inicio(request):
    return HttpResponse("Bienvenido a la pagina principal")


def inicioApp(request):

    return render(request, "AppCoder/inicio.html", {"avatar":obtenerAvatar(request)})


# vistas basadas en clases:

class EstudianteList(LoginRequiredMixin, ListView):#vista usada para LISTAR
    model= Estudiante
    template_name= "AppCoder/estudiantes.html"

class EstudianteCreacion(LoginRequiredMixin, CreateView):#vista usada para CREAR
    model= Estudiante
    success_url= reverse_lazy("estudiante_list")
    fields=['nombre', 'apellido', 'email']

class EstudianteDetalle(LoginRequiredMixin, DetailView): #vista usada para MOSTRAR DATOS
    model=Estudiante
    template_name="Appcoder/estudiante_detalle.html"

class EstudianteDelete(LoginRequiredMixin, DeleteView):#vista usada para ELIMINAR
    model=Estudiante
    success_url= reverse_lazy("estudiante_list")

class EstudianteUpdate(LoginRequiredMixin, UpdateView):#vista usada para EDITAR
    model = Estudiante
    success_url = reverse_lazy('estudiante_list')
    fields=['nombre', 'apellido', 'email']


#login logout register

def login_request(request):
    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            info=form.cleaned_data
            
            usu=info["username"]
            clave=info["password"]
            usuario=authenticate(username=usu, password=clave)#verifica si el usuario existe, si existe, lo devuelve, y si no devuelve None 
            
            if usuario is not None:
                login(request, usuario)
                return render(request, "AppCoder/inicio.html", {"mensaje":f"Usuario {usu} logueado correctamente"})
            else:
                return render(request, "AppCoder/login.html", {"form": form, "mensaje":"Usuario o contraseña incorrectos"})
        else:
            return render(request, "AppCoder/login.html", {"form": form, "mensaje":"Usuario o contraseña incorrectos"})
    else:
        form=AuthenticationForm()
        return render(request, "AppCoder/login.html", {"form": form})




def register(request):
    if request.method=="POST":
        form= RegistroUsuarioForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data.get("username")
            form.save()
            return render(request, "AppCoder/inicio.html", {"mensaje":f"Usuario {username} creado correctamente"})
        else:
            return render(request, "AppCoder/register.html", {"form": form, "mensaje":"Error al crear el usuario"})
    else:
        form= RegistroUsuarioForm()
        return render(request, "AppCoder/register.html", {"form": form})

@login_required
def editarPerfil(request):
    usuario=request.user

    if request.method=="POST":
        form=UserEditForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            usuario.email=info["email"]
            usuario.password1=info["password1"]
            usuario.password2=info["password2"]
            usuario.first_name=info["first_name"]
            usuario.last_name=info["last_name"]
            usuario.save()
            return render(request, "AppCoder/inicio.html", {"mensaje":f"Usuario {usuario.username} editado correctamente"})
        else:
            return render(request, "AppCoder/editarPerfil.html", {"form": form, "nombreusuario":usuario.username})
    else:
        form=UserEditForm(instance=usuario)
        return render(request, "AppCoder/editarPerfil.html", {"form": form, "nombreusuario":usuario.username})

@login_required
def agregarAvatar(request):
    if request.method=="POST":
        form=AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            avatar=Avatar(user=request.user, imagen=request.FILES["imagen"])#antes de guardarlo, tengo q hacer algo
            
            avatarViejo=Avatar.objects.filter(user=request.user)
            if len(avatarViejo)>0:
                avatarViejo[0].delete()
            avatar.save()
            return render(request, "AppCoder/inicio.html", {"mensaje":f"Avatar agregado correctamente", "avatar":obtenerAvatar(request)})
        else:
            return render(request, "AppCoder/agregarAvatar.html", {"form": form, "usuario": request.user, "mensaje":"Error al agregar el avatar"})
    else:
        form=AvatarForm()
        return render(request, "AppCoder/agregarAvatar.html", {"form": form, "usuario": request.user, "avatar":obtenerAvatar(request)})
