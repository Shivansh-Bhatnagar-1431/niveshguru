from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'main/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f"New user created: {user.username}")  # Logging example
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})
# views.py
# from django.shortcuts import render, redirect
# from .forms import CustomUserCreationForm

# def signup_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('dashboard')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        logger.warning("Authenticated user attempted to access login page")
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            logger.info(f"Successful login: {username}")
            messages.success(request, 'Logged in successfully.')
            return redirect('home')
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            messages.error(request, 'Invalid credentials')
    
    response = render(request, 'main/login.html')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    return response
def logout_view(request):
    logger.info(f"User logged out: {request.user.username}")  # Logging example
    logout(request)
    return redirect('home')



@require_http_methods(["POST"])
@login_required
def logout_view(request):
    logger.info(f"User {request.user.username} initiated logout")
    # Clear session data
    request.session.flush()
    # Logout user
    logout(request)
    # Create response with cache control headers
    response = redirect('home')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '-1'
    logger.info(f"User logged out successfully")
    messages.success(request, 'You have been securely logged out.')
    return response

#from nselib import capital_market
#from django.contrib.auth.decorators import login_required



@login_required
def dashboard(request):
    # Get market data using current methods
    index_data = capital_market.market_watch_all_indices()
    top_gainers = capital_market.top_gainers()
    top_losers = capital_market.top_losers()
    
    # Process data for templates
    context = {
        'indices': index_data.to_dict('records'),
        'top_gainers': top_gainers.head(10),
        'top_losers': top_losers.head(10),
        'user': request.user
    }
    return render(request, 'main/dashboard.html', context)
@login_required
def search_stock(request):
    if request.method == 'GET':
        symbol = request.GET.get('symbol', '').upper()
        try:
            # Get current price data
            quote = capital_market.equity_price_volume_data(symbol)
            # Get historical data
            historical = capital_market.price_volume_and_deliverable_position_data(symbol)
            
            context = {
                'symbol': symbol,
                'quote': quote.to_dict(),
                'historical': historical.to_dict('records')
            }
            return render(request, 'main/stock_detail.html', context)
            
        except Exception as e:
            messages.error(request, f"Error fetching data for {symbol}: {str(e)}")
            return redirect('dashboard')