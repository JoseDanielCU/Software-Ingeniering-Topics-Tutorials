from django.shortcuts import render, redirect
from .forms import FlightForm
from .models import Flight
from django.db.models import Avg

def home(request):
    return render(request, "home.html")
def register_flight(request):
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_flights")
    else:
        form = FlightForm()
    return render(request, "register.html", {"form": form})

def list_flights(request):
    flights = Flight.objects.all().order_by("price")
    return render(request, "list.html", {"flights": flights})

def flight_stats(request):
    total_national = Flight.objects.filter(type="Nacional").count()
    total_international = Flight.objects.filter(type="Internacional").count()
    avg_national_price = Flight.objects.filter(type="Nacional").aggregate(Avg("price"))["price__avg"]

    context = {
        "total_national": total_national,
        "total_international": total_international,
        "avg_national_price": avg_national_price or 0
    }
    return render(request, "stats.html", context)