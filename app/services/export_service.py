import csv
import io

def generate_applications_csv(applications):
    output = io.StringIO()
    fieldnames = ["company", "status", "last_updated", "created_at"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    writer.writeheader()
    for app in applications:
        writer.writerow({
            "company": app.get("company"),
            "status": app.get("status"),
            "last_updated": app.get("last_updated"),
            "created_at": app.get("created_at")
        })
    
    return output.getvalue()