from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import MeterReading, Bill
from .serializers import MeterReadingSerializer, BillSerializer
from .services import calculate_and_create_bill
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MeterReadingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class MeterReadingCreateAPIView(generics.CreateAPIView):
    serializer_class = MeterReadingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        meter_reading = serializer.instance
        try:
            calculate_and_create_bill(meter_reading)
        except ValueError as e:
            # Handle billing error, maybe log it
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserBillListAPIView(generics.ListAPIView):
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bill.objects.filter(user=self.request.user)

class UserBillDetailAPIView(generics.RetrieveAPIView):
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]
    queryset = Bill.objects.all()  # Important: Start with all Bill objects, then filter in get_object

    def get_object(self):
        # Get the bill, ensuring it belongs to the current user
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'], user=self.request.user)
        return obj

#Web Views
@login_required
def add_reading_web(request):
    if request.method == 'POST':
        form = MeterReadingForm(request.POST)
        if form.is_valid():
            reading = form.save(commit=False)
            reading.user = request.user
            reading.save()
            messages.success(request, "Meter Reading was added successfully")
            return redirect('my-bills')
        else:
            messages.error(request, "There was an error adding your reading")
    else:
        form = MeterReadingForm()
    return render(request, 'billing/add_reading.html', {'form': form})

@login_required
def my_bills_web(request):
    bills = Bill.objects.filter(user=request.user).order_by('-billing_period_end')
    return render(request, 'billing/my_bills.html', {'bills': bills})

@login_required
def bill_detail_web(request, pk):
    bill = get_object_or_404(Bill, pk=pk, user=request.user)
    return render(request, 'billing/bill_detail.html', {'bill': bill})