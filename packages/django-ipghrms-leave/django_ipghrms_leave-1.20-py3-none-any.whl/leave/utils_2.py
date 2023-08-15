from datetime import datetime, timedelta

def calculate_leave_days(start_date, end_date, start_time_status, end_time_status):
    # Check that start_date and end_date are not on weekends
    if start_date.weekday() in [5, 6] or end_date.weekday() in [5, 6]:
        raise ValueError("Data Hahu Ou Data Remata Labele iha Sabado ou Domingo")
    
    hourly_values = {
        "08:00": 8.0,
        "13:00": 4.0,
        "12:00": 4.0,
        "17:00": 8.0,
    }
    
    if start_time_status not in hourly_values or end_time_status not in hourly_values:
        raise ValueError("Wrong input Start Time and End Time")
    
    total_days = 0
    if start_date == end_date:
        # Calculate number of hours based on start_time_status and end_time_status
        if start_time_status == "08:00" and end_time_status == "17:00":
            total_days = 1.0
        elif start_time_status == "13:00" and end_time_status == "17:00":
            total_days = 0.5
        elif start_time_status == "08:00" and end_time_status == "12:00":
            total_days = 0.5
        else:
            raise ValueError("Invalido Horas Hahu no Horas Remata")
    else:
        if end_date < start_date:
            raise ValueError("Data Remata Labele Uluk husi Data Hahu")
    
        current_date = start_date
        while current_date <= end_date:
            # Exclude weekends
            if current_date.weekday() not in [5, 6]:
                # Calculate number of hours on this day based on start_time_status and end_time_status
                if current_date == start_date:
                    if start_time_status == "08:00":
                        hours = 8.0
                    elif start_time_status == "13:00":
                        hours = 4.0
                    else:
                        raise ValueError("Invalid start_time_status")
                elif current_date == end_date:
                    if end_time_status == "17:00":
                        hours = 8.0
                    elif end_time_status == "12:00":
                        hours = 4.0
                    else:
                        raise ValueError("Invalid end_time_status")
                else:
                    hours = 8.0
                
                total_days += hours / 8.0  # Convert hours to days
            
            current_date += timedelta(days=1)
    
    return total_days


def koko2():
    start_date = datetime(2023, 3, 14).date()
    end_date = datetime(2023, 3, 14).date()
    start_time_status = "08:00"
    end_time_status = "12:00"
    days = calculate_leave_days(start_date, end_date, start_time_status, end_time_status)
    print(days)

   
