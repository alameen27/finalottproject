# views.py
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CustomerRegistrationForm, EditProfileForm, PINVerificationForm
# ottapp/views.py
from django.template.loader import render_to_string
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from .models import Customer, CustomerProfile, moviekid, upcoming, waste
from .forms import LoginForm
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, CustomerProfile, KidProfile,movie
from .forms import CustomerProfileForm, KidProfileForm
from django.urls import reverse
from django.core.mail import send_mail


def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                customer = Customer.objects.get(username=username)
                if customer.password == password:
                    # Get the customer ID and redirect to the profile detail page
                    customer_id = customer.id
                    return redirect('profile_detail', customer_id=customer_id)
                else:
                    form.add_error(None, 'Invalid credentials')
            except Customer.DoesNotExist:
                form.add_error(None, 'User not found')

    return render(request, 'user/login.html', {'form': form})






def home_view(request):
    return render(request, 'home.html')



def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Send registration success email
            subject = 'Registration Successful'
            message = f'Thank you for registering on My Website, {user.username}!'
            from_email = 'your_email@example.com'
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('login')  # Redirect to a success page

    else:
        form = CustomerRegistrationForm()

    return render(request, 'registration.html', {'form': form})


def profile_list(request):
    # Assuming the user is logged in and has a related customer object
    if request.user.is_authenticated:
        customer = request.user.customer  # Assuming a one-to-one relationship between User and Customer
        profiles = CustomerProfile.objects.filter(customer=customer)
        return render(request, 'user/profile_list.html', {'profiles': profiles})
    else:
        # Handle the case where the user is not authenticated (e.g., redirect to login)
        return render(request, 'error.html', {'error_message': 'User is not authenticated'})





class ProfileDetailView(View):
    template_name = 'profile_detail.html'

    def get(self, request, customer_id):
        customer = Customer.objects.get(id=customer_id)
        profile = customer.profile.all()  # Assuming there's only one profile per customer
        kid_profiles = customer.kid_profiles.all()
        return render(request, self.template_name, {'customer': customer, 'profile': profile, 'kid_profiles': kid_profiles})
    

def list_profiles(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    profiles = customer.customerprofile.all()  # Assuming your profile model is named CustomerProfile

    return render(request, 'profile_list.html', {'customer': customer, 'profiles': profiles})


def profile_registration_view(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    template_name = 'profile_registration.html'

    # Check the existing number of profiles for the customer
    total_profiles = CustomerProfile.objects.filter(customer=customer).count()

    if total_profiles >= 4:
        # Return an error message or handle the limit reached scenario
        return render(request,'error.html')

    if request.method == 'POST':
        profile_form = CustomerProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.customer = customer
            profile.save()

            return redirect('profile_detail', customer_id=customer.id)

    else:
        profile_form = CustomerProfileForm()

    return render(request, template_name, {'customer': customer, 'profile_form': profile_form})

def kid_profile_registration_view(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    template_name = 'kid_registration.html'

    # Check the existing number of profiles for the customer
    total_profiles = KidProfile.objects.filter(customer=customer).count()

    if total_profiles >= 2:
        # Return a JSON response with the error message
        return render(request,'error.html')

    if request.method == 'POST':
        profile_form = KidProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            kid_profile = profile_form.save(commit=False)
            kid_profile.customer = customer
            kid_profile.save()

            # Optionally, return a success message or an empty JSON response
            return redirect('profile_detail', customer_id=customer.id)

    else:
        profile_form = KidProfileForm()

    return render(request, template_name, {'customer': customer, 'profile_form': profile_form})



def profile_details(request, customer_id, profile_id):
    customer = get_object_or_404(Customer, id=customer_id)
    profile = get_object_or_404(CustomerProfile, id=profile_id, customer=customer)

    if request.method == 'POST':
        pin_form = PINVerificationForm(request.POST)

        if pin_form.is_valid():
            entered_pin = pin_form.cleaned_data['pin']

            if entered_pin == profile.pin:
                # PIN is correct, redirect to the movie_list function
                movie_list_url = reverse('movie_list', args=[profile_id])
                return redirect(movie_list_url)
            else:
                # PIN is incorrect, show an error message
                pin_form.add_error('pin', 'Incorrect PIN. Please try again.')

    else:
        # If the request is not a POST, initialize an empty form
        pin_form = PINVerificationForm()

    return render(request, 'pin_verification.html', {'customer': customer, 'profile': profile, 'pin_form': pin_form})

def kidprofile_details(request, customer_id, profile_id):
    customer = get_object_or_404(Customer, id=customer_id)
    profile = get_object_or_404(KidProfile, id=profile_id, customer=customer)
    kidmovielist_url = reverse('kidmovielist', args=[profile_id])
    return redirect(kidmovielist_url)

    return render(request, 'hellokids.html', {'customer': customer, 'profile': profile})

class MovieListView(View):
    template_name = 'hello.html'

    def get(self, request, profile_id):
        profile = get_object_or_404(CustomerProfile, id=profile_id)
        customer_movies = movie.objects.filter(customer_profile=profile)
        logo=waste.objects.all()
        upmov = upcoming.objects.all()
        return render(request, self.template_name, {'movies': customer_movies, 'profile': profile,'logo':logo,'upmov':upmov})
    
class Moviedetail(View):
    template_name = 'movie_detail.html'

    def get(self, request, id,):
        # Retrieve the specific movie details
        movie_instance = get_object_or_404(movie, id=id)

        

        # If you want to retrieve all movies related to a specific profile
        # you can use a related field, assuming your Movie model has a ForeignKey
        # field named 'customer_profile'
        customer_movies = movie.objects.filter(customer_profile=movie_instance.customer_profile)

        return render(request, self.template_name, {'movie': movie_instance, 'customer_movies': customer_movies})
    


class KidMovieListView(ListView):
    model = moviekid
    template_name = 'hellokids.html'
    context_object_name = 'movies'

    def get_queryset(self):
        kid_profile_id = self.kwargs.get('id')
        return moviekid.objects.filter(kid_profile_id=kid_profile_id)
    
class MovieKidDetail(View):
    template_name = 'moviekid_detail.html'

    def get(self, request, id):
        # Retrieve the specific movie kid details
        moviekid_instance = get_object_or_404(moviekid, id=id)

        # Retrieve all movie kids related to the same customer profile
        customer_moviekids = moviekid.objects.filter(kid_profile=moviekid_instance.kid_profile_id)

        return render(request, self.template_name, {'moviekid': moviekid_instance, 'customer_moviekids': customer_moviekids})
   


def upcoming_movies(request, movie_id):
    # Retrieve the movie details from the database
    movie = get_object_or_404(upcoming, id=movie_id)

    # You can add any additional logic or processing here if needed

    # Render the movie detail template with the movie object
    return render(request, 'upmoviedetail.html', {'movie': movie})


def movie_list(request):
    query = request.GET.get('q', '')
    move = movie.objects.all()

    if query:
        # Filter movies for each field individually using icontains for partial matching
        move = move.filter(
            Q(name__icontains=query) |
            Q(Genre__icontains=query) |
            Q(Director__icontains=query) |
            Q(year__icontains=query)
        ).distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/_movie_list.html', {'move': move})
        return JsonResponse({'html': html})

    return render(request, 'hello.html', {'move': move})


def kidmovie_list(request):
    query = request.GET.get('q', '')
    kid = moviekid.objects.all()

    if query:

        # Check if the query represents a number (year)
        # Filter movies for each field individually
        kid = kid.filter(
                Q(title__icontains=query) |
                Q(genre__icontains=query)
            ).distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/kidmovie_list.html', {'kid': kid})
        return JsonResponse({'html': html})

    return render(request, 'hellokids.html', {'kid': kid})


def update_profile(request, customer_id, profile_id):
    customer = get_object_or_404(Customer, id=customer_id)
    profile = get_object_or_404(CustomerProfile, id=profile_id)

    form = EditProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('profile_detail', customer_id=customer.id)

    return render(request, 'update_profile.html', {'customer': customer, 'profile': profile, 'form': form})


# views.py


def delete_profile(request, customer_id, profile_id):
    customer = get_object_or_404(Customer, id=customer_id)
    profile = get_object_or_404(CustomerProfile, id=profile_id)

    if request.method == 'POST':
        profile.delete()
        return redirect('profile_detail', customer_id=customer.id)

    return render(request, 'user/delete_profile.html', {'customer': customer, 'profile': profile})

# views.py
from django.shortcuts import get_object_or_404, redirect
from .models import KidProfile

def delete_kid_profile(request, customer_id, kid_profile_id):
    customer = get_object_or_404(Customer, id=customer_id)
    kid_profile = get_object_or_404(KidProfile, id=kid_profile_id)

    if request.method == 'POST':
        kid_profile.delete()
        return redirect('profile_detail', customer_id=customer.id)

    return render(request, 'delete_kid_profile.html', {'customer': customer, 'kid_profile': kid_profile})



def update_kid_profile(request, customer_id, kid_profile_id):
    customer = get_object_or_404(Customer, id=customer_id)
    kid_profile = get_object_or_404(KidProfile, id=kid_profile_id)

    if request.method == 'POST':
        form = KidProfileForm(request.POST, request.FILES, instance=kid_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', customer_id=customer.id)
    else:
        form = KidProfileForm(instance=kid_profile)

    return render(request, 'update_kid_profile.html', {'customer': customer, 'kid_profile': kid_profile, 'form': form})