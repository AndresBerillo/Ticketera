from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Concert, Ticket, ShoppingCart, User  # Asegúrate de importar el modelo Concert
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, ConcertForm, UserEditForm,UserForm, TicketForm  

# Vista para la página de inicio (home)
def home(request):
    form = LoginForm()  # Crea una instancia del formulario de login
    concerts = Concert.objects.all()  # Obtén todos los conciertos disponibles desde la base de datos
    tickets = Ticket.objects.all()  # Obtén todos los conciertos disponibles desde la base de datos

    return render(request, 'pages/index.html', {'form': form, 'concerts': concerts,'tickets': tickets})  # Pasa el formulario y los conciertos al template

# Vista para la página de conciertos
def concerts(request):
    # Obtiene todos los conciertos
    concerts = Concert.objects.all()  # Cambié Event por Concert
    return render(request, 'pages/concerts.html', {'concerts': concerts})

# Vista para mostrar detalles de un concierto (podría incluir las entradas disponibles)
def concert_detail(request, concert_id):
    concert = Concert.objects.get(id=concert_id)  # Obtén el concierto por ID
    tickets = Ticket.objects.filter(concert=concert)  # Obtén las entradas para ese concierto
    return render(request, 'pages/concert_detail.html', {'concert': concert, 'tickets': tickets})

# Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirige a la página de inicio o donde desees
    else:
        form = AuthenticationForm()
    
    return render(request, 'pages/login.html', {'form': form})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Redirige a la página de inicio
    else:
        form = UserCreationForm()
    
    return render(request, 'pages/register.html', {'form': form})

# Vista para los detalles de un concierto
def concert_detail(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    tickets = concert.tickets.all()

    # Si el usuario está autenticado, obtener su carrito de compras
    if request.user.is_authenticated:
        cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    else:
        cart = None

    if request.method == "POST" and 'add_to_cart' in request.POST:
        ticket_id = request.POST.get('ticket_id')
        ticket = get_object_or_404(Ticket, id=ticket_id)

        # Verificar si el ticket no está vendido y no ha sido agregado ya al carrito
        if not ticket.is_sold and ticket not in cart.tickets.all():
            cart.tickets.add(ticket)  # Añadir el ticket al carrito
            return redirect('concert_detail', concert_id=concert_id)  # Redirigir a la misma página para ver cambios

    return render(request, 'pages/concert_detail.html', {'concert': concert, 'tickets': tickets, 'cart': cart})

#Logica vista carrito
def shopping_cart(request):
    if request.user.is_authenticated:
        cart = ShoppingCart.objects.get(user=request.user)
        tickets = cart.tickets.all()
        return render(request, 'pages/cart.html', {'cart': cart, 'tickets': tickets})
    else:
        return redirect('login')  # Redirigir al login si el usuario no está autenticado
    

@login_required
def checkout(request):
    # Obtener el carrito del usuario
    cart = ShoppingCart.objects.get(user=request.user)
    tickets = cart.tickets.all()

    # Marcar los tickets como vendidos
    for ticket in tickets:
        ticket.is_sold = True
        ticket.save()

    # Vaciar el carrito (eliminar tickets del carrito)
    cart.tickets.clear()

    # Crear una lista de los archivos PDF para mostrar en la página
    pdf_files = [ticket.pdf_file.url for ticket in tickets if ticket.pdf_file]

    return render(request, 'pages/checkout.html', {'pdf_files': pdf_files})

@login_required
def remove_from_cart(request, ticket_id):
    # Obtener el ticket por ID
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Obtener el carrito del usuario
    cart = get_object_or_404(ShoppingCart, user=request.user)
    
    # Eliminar el ticket del carrito
    if ticket in cart.tickets.all():
        cart.tickets.remove(ticket)
    
    # Redirigir al carrito actualizado
    return redirect('shopping_cart')

@login_required
def add_to_cart(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    
    if not ticket.is_sold and ticket not in cart.tickets.all():
        cart.tickets.add(ticket)
    
    return redirect('concert_detail', concert_id=ticket.concert.id)

@login_required
def dashboard(request):
    # Solo los administradores pueden acceder al dashboard
    if not request.user.is_staff:
        return redirect('home')  # Redirigir si no es admin
    
    concerts = Concert.objects.all()  # Obtener todos los conciertos
    users = User.objects.all()  # Obtener todos los usuarios
    tickets = Ticket.objects.all()  # Obtener todos los tickets
    
    return render(request, 'pages/dashboard.html', {'concerts': concerts, 'users': users, 'tickets': tickets})

#Funcionalidad de conciertos

@login_required
def edit_concert(request, concert_id):
    if not request.user.is_staff:
        return redirect('home')

    concert = get_object_or_404(Concert, id=concert_id)

    if request.method == 'POST':
        form = ConcertForm(request.POST, request.FILES, instance=concert)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ConcertForm(instance=concert)

    return render(request, 'pages/edit_concert.html', {'form': form})

@login_required
def delete_concert(request, concert_id):
    if not request.user.is_staff:
        return redirect('home')

    concert = get_object_or_404(Concert, id=concert_id)

    if request.method == 'POST':
        concert.delete()
        return redirect('dashboard')

    return render(request, 'pages/confirm_delete.html', {'concert': concert})

# Vista para crear un nuevo concierto
@login_required
def create_concert(request):
    if request.method == 'POST':
        form = ConcertForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ConcertForm()

    return render(request, 'pages/create_concert.html', {'form': form})

# Funcionalidad de Usuarios
@login_required
def edit_user(request, user_id):
    if not request.user.is_staff:
        return redirect('home')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'pages/edit_user.html', {'form': form, 'user': user})

@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return redirect('home')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        return redirect('dashboard')

    return render(request, 'pages/confirm_delete_user.html', {'user': user})
    
# Vista para crear un nuevo usuario
@login_required
def create_user(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # No guardar aún en la base de datos
            password = form.cleaned_data['password']
            user.set_password(password)  # Establecer la contraseña de forma segura
            user.save()  # Ahora sí guardamos el usuario
            return redirect('dashboard')
    else:
        form = UserForm()

    return render(request, 'pages/create_user.html', {'form': form})

# Vista para editar un ticket
@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)  # Asegúrate de incluir request.FILES
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'pages/edit_ticket.html', {'form': form})

# Vista para eliminar un ticket
@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        ticket.delete()
        return redirect('dashboard')

    return render(request, 'pages/confirm_delete_ticket.html', {'ticket': ticket})

# Vista para crear un nuevo ticket
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TicketForm()

    return render(request, 'pages/create_ticket.html', {'form': form})