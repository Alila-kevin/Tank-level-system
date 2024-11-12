from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TankLevel
import pandas as pd
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def upload_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['file']
        try:
            # Determine the file type and read the data accordingly
            if excel_file.name.endswith('.xlsx'):
                df = pd.read_excel(excel_file)
            elif excel_file.name.endswith('.csv'):
                df = pd.read_csv(excel_file)
            else:
                return HttpResponse("Error: Unsupported file format. Please upload an XLSX or CSV file.")

            print(df.columns)  # Add this line to debug

            tank_name = request.POST['tank']
            
            if 'level' not in df.columns or 'time' not in df.columns:
                return HttpResponse("Error: File must contain 'level' and 'time' columns.")

            for _, row in df.iterrows():
                TankLevel.objects.create(
                    tank=tank_name,
                    level=row['level'],
                    time=row['time']
                )
            return HttpResponse("Data uploaded successfully")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")

    return render(request, 'upload.html')


def view_data(request):
    # Get all tank level data
    data = TankLevel.objects.all().values('tank', 'level', 'time')
    
    # Convert to a DataFrame for easier processing
    df = pd.DataFrame(list(data))

    # Convert 'time' column to datetime and UTC timezone handling
    df['time'] = pd.to_datetime(df['time']).dt.tz_convert('UTC')

    # Get the latest date from the 'time' column
    latest_date = df['time'].dt.date.max()

    # Filter the DataFrame to include only rows with the latest date
    df = df[df['time'].dt.date == latest_date]

    # Extract hour from time for grouping
    df['hour'] = df['time'].dt.floor('H')  # Floor to the hour

    # Group by tank and hour, calculating the average level
    average_levels = df.groupby(['tank', 'hour']).agg({'level': 'mean'}).reset_index()

    # Prepare the data for Chart.js
    chart_data = {}
    for tank in average_levels['tank'].unique():
        tank_data = average_levels[average_levels['tank'] == tank]
        # Convert timestamps to strings for JavaScript
        chart_data[tank] = tank_data.to_dict(orient='records')
        for record in chart_data[tank]:
            record['hour'] = record['hour'].isoformat()  # Convert to ISO format

    return render(request, 'view_data.html', {'data': chart_data})
def tank_levels(request):
    # Fetch the latest level for each of the 8 tanks
    tank_names = ['tank1', 'tank2', 'tank3', 'tank4', 'tank5', 'tank6', 'tank7', 'tank8']
    tank_levels = {}

    for tank_name in tank_names:
        latest_level = TankLevel.objects.filter(tank=tank_name).order_by('-time').first()
        if latest_level:
            tank_levels[tank_name] = latest_level.level  # Get the most recent tank level
        else:
            tank_levels[tank_name] = 1  # Default value if no data is found

    return render(request, 'tank.html', {'tank_levels': tank_levels})