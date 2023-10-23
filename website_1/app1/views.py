from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import finepage,register
from django.views.decorators.csrf import csrf_protect
import difflib
import geocoder
import re,math
from urllib.parse import urlparse, parse_qs
import haversine as hs
from geopy.geocoders import Nominatim

global k 
k= '/media/images/simple.png/'

def home_page(request):
    

    g = geocoder.ip('me')
    lat, lng = g.latlng
    
    items = finepage.objects.all()
    #sorted_items = sorted(items, key=lambda item: haversine(lat, lng, locate(item.ur_rl)[0], locate(item.ur_rl)[1]))
    
    items_with_valid_distances = []

# Calculate the distance for each item and store it in the list, only if locate() doesn't return None
    for item in items:
        location = locate(item.ur_rl)  # Assuming locate is a function to get lat and lng from a URL
    
        if location is not None and len(location) == 2:
            it_lat, it_lng = location
            distance_km = haversine(lat, lng, it_lat, it_lng)
            print(distance_km)
            items_with_valid_distances.append(item)
    sorted_items = sorted(items_with_valid_distances, key=lambda item: haversine(lat, lng, locate(item.ur_rl)[0], locate(item.ur_rl)[1]))

    

        
    
    items=sorted_items
    return render(request, 'homePage.html', {'items': items})

def homePager(request):
    logon = request.POST["uname"]
    mail = request.POST["email"]
    num = request.POST["pno"]
    password = request.POST["password"]
    cpassword = request.POST["copassword"]

    print(logon,mail,num,password,cpassword)
    item=register.objects.all()
    if(password!=cpassword):
        return render(request,'login.html',{'msg':'password should be same'})
    elif(register.objects.filter(mail=mail).exists() or register.objects.filter(username=logon).exists()):
        return render(request,'login.html',{'msg':'email or username exist'})

    else: 
        if(len(str(num))>10 or len(str(num))<10):
            return render(request,'login.html',{'msg':'number must be 10digits'})
        try:
          reg = register.objects.create(username=logon, mail=mail, number=num, password=password)
    
        except Exception as e:
    #
         print(f"An error occurred: {e}")


        print("table created")
        return redirect('/')


def find_page(request, item_id):
    # Your view logic here...
    item = finepage.objects.get(pk=item_id)
    
    return render(request, 'findPage.html', {'item': item,'k':k})

def item_detail(request, item_id):
    
    item = item.objects.get(pk=item_id)
    return render(request, 'findPage.html', {'item': item,'k':k})
def show(request, i):
       # Your view logic here...
    item = finepage.objects.get(pk=i)
    k=item.url_field
    return render(request, 'findPage.html', {'item': item,'k':k})
    

def show_map(request, your_model_id):
    try:
        your_model = finepage.objects.get(pk=your_model_id)
    except finepage.DoesNotExist:
        your_model = None

    return render(request, 'findpage.html', {'your_model': your_model})
def regter(request):
    return render(request,'login.html')
def login(request):
    logon = request.POST.get('username')
    pawword = request.POST.get('password')

    items=finepage.objects.all()
    
    try:
        User=register.objects.get(username=logon,password=pawword)
        return render(request,'homePage.html',{'items':items})
    except register.DoesNotExist:
            return render(request, 'log.html', {'match': False})
        
    except User.DoesNotExist:
        return render(request,'login.html')
    

    
def sort(request):
    items=finepage.objects.all().order_by('price')
    
    return render(request,'homePage.html',{'items':items})
def search(request):
    if request.method == "POST":
        srh = request.POST["search"].lower()  # Convert input to lowercase
        items =finepage.objects.all()  # Use the correct model name
        
        # Extract lowercase names and cities for comparison
        names = [item.name.lower() for item in items]
        cities = [item.address.lower() for item in items]
        
        # Find the closest match for lowercase name and city using difflib
        closest_name = difflib.get_close_matches(srh, names, n=1)
        closest_city = difflib.get_close_matches(srh, cities, n=1)
        
        matched_items = []
        
        if closest_name:
            matched_name = closest_name[0]
            matched_items += items.filter(name__iexact=matched_name)  # Case-insensitive filter
        
        if closest_city:
            matched_city = closest_city[0]
            matched_items += items.filter(address__iexact=matched_city)  # Case-insensitive filter
        
        return render(request, 'homePage.html', {'items': matched_items})
    
    return render(request, 'homePage.html', {'items': [],'k':k})


def emg1(request):
    items=finepage.objects.filter(emg='yes')
    return render(request,'homePage.html',{'items':items,'k':k})
'''def extract_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if 'pb' in query_params:
        pb_param = query_params['pb'][0]  # Extract the 'pb' parameter value
        coordinates_pattern = r"([-+]?\d+\.\d+),\s*([-+]?\d+\.\d+)"
        match = re.search(coordinates_pattern, pb_param)
        
        if match:
            latitude = float(match.group(1))
            longitude = float(match.group(2))
            return latitude, longitude

    return None

def locate(request):
    g = geocoder.ip('me')
    if g.latlng:
        lat, lng = g.latlng
        print(lat,lng)
        iitems = finepage.objects.all()

        def get_distance(item):
            coordinates = item.latitude,item.longitude
            
            if coordinates:
                lat1, lng2 = coordinates
                lat_rad = math.radians(lat)
                lng_rad = math.radians(lng)
                lat1_rad = math.radians(lat1)
                lng2_rad = math.radians(lng2)
                flat = lat1_rad - lat_rad
                flng = lng2_rad - lng_rad
                a = math.sin(flat / 2)**2 + math.cos(lat_rad) * math.cos(lat1_rad) * math.sin(flng / 2)**2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                R = 6371.0
                distance = R * c
                
                return distance
            else:
                return float('inf')  # Placeholder for items with no coordinates
            
        sorted_items = sorted(iitems, key=get_distance)
        for item in sorted_items:
            coordinates = extract_url(item.url_field)
            print(coordinates)
            if coordinates:
                print(f"Coordinates for {item.name}: {coordinates}")
            else:
                print(f"No coordinates found for {item.name}")
        
        return render(request, 'homePage.html', {'items': sorted_items})'''
def locate(google_maps_url):
        match = re.search(r'@([-+]?\d*\.\d+),([-+]?\d*\.\d+)', google_maps_url)

        if match:
            latitude = float(match.group(1))
            longitude = float(match.group(2))
            
            l = [latitude, longitude]  # Create a list with latitude and longitude
            return l
import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the Earth's surface specified in decimal degrees of latitude and longitude.
    """
    # Radius of the Earth in kilometers
    earth_radius = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Calculate the distance
    distance = earth_radius * c

    return distance

def download(request, image_id):
    image = get_object_or_404(finepage, pk=image_id)
    response = HttpResponse(image.img, content_type='image/jpeg') 
    response['Content-Disposition'] = f'attachment; filename="{image.img.name}"'
    return response







           

