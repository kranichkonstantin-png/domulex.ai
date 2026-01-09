"""
Cloud Scheduler Setup for DOMULEX Ingestion
Serverless alternative to Celery - uses GCP Cloud Scheduler + Cloud Tasks
"""

import subprocess
import json

PROJECT_ID = "domulex-ai"
REGION = "europe-west3"
BACKEND_URL = "https://domulex-backend-841507936108.europe-west3.run.app"

# Define all ingestion schedules
SCHEDULES = [
    # ========== DEUTSCHLAND ==========
    {
        "name": "scrape-de-gesetze-im-internet",
        "description": "Deutsche Gesetze (BGB, WEG, MietR) - Wöchentlich",
        "schedule": "0 3 * * 0",  # Sonntags 03:00
        "endpoint": "/ingest/de/gesetze",
        "timezone": "Europe/Berlin"
    },
    {
        "name": "scrape-de-bmf-tax",
        "description": "BMF Steuer-Schreiben (AfA, Grundsteuer) - Täglich",
        "schedule": "30 2 * * *",  # 02:30 täglich
        "endpoint": "/ingest/de/bmf",
        "timezone": "Europe/Berlin"
    },
    {
        "name": "scrape-de-bgh-cases",
        "description": "BGH Rechtsprechung - Alle 6 Stunden",
        "schedule": "0 */6 * * *",  # Alle 6 Stunden
        "endpoint": "/ingest/de/bgh",
        "timezone": "Europe/Berlin"
    },
    
    # ========== USA ==========
    {
        "name": "scrape-us-florida-statutes",
        "description": "Florida Statutes (Landlord-Tenant) - Wöchentlich",
        "schedule": "0 4 * * 1",  # Montags 04:00
        "endpoint": "/ingest/us/florida",
        "timezone": "America/New_York"
    },
    {
        "name": "scrape-us-courtlistener",
        "description": "CourtListener Real Estate Cases - Alle 4 Stunden",
        "schedule": "15 */4 * * *",  # Alle 4 Stunden
        "endpoint": "/ingest/us/courtlistener",
        "timezone": "America/New_York"
    },
    {
        "name": "scrape-us-irs-rulings",
        "description": "IRS Revenue Rulings (1031, Depreciation) - Täglich",
        "schedule": "0 5 * * *",  # 05:00 täglich
        "endpoint": "/ingest/us/irs",
        "timezone": "America/New_York"
    },
    
    # ========== SPANIEN ==========
    {
        "name": "scrape-es-boe-gazette",
        "description": "BOE Amtsblatt - Täglich",
        "schedule": "0 7 * * *",  # 07:00 täglich
        "endpoint": "/ingest/es/boe",
        "timezone": "Europe/Madrid"
    },
    {
        "name": "scrape-es-lau-updates",
        "description": "LAU Mietrecht Updates - Wöchentlich",
        "schedule": "0 8 * * 3",  # Mittwochs 08:00
        "endpoint": "/ingest/es/lau",
        "timezone": "Europe/Madrid"
    },
    
    # ========== MAINTENANCE ==========
    {
        "name": "cleanup-old-embeddings",
        "description": "Lösche veraltete Embeddings - Wöchentlich",
        "schedule": "0 1 * * 0",  # Sonntags 01:00
        "endpoint": "/ingest/maintenance/cleanup",
        "timezone": "UTC"
    },
    {
        "name": "generate-stats-report",
        "description": "Generiere Statistik-Report - Wöchentlich",
        "schedule": "0 9 * * 5",  # Freitags 09:00
        "endpoint": "/ingest/maintenance/stats",
        "timezone": "UTC"
    },
]


def create_scheduler_jobs():
    """Create all Cloud Scheduler jobs"""
    print("🚀 Creating Cloud Scheduler Jobs for DOMULEX Ingestion\n")
    
    for job in SCHEDULES:
        job_name = job["name"]
        
        cmd = [
            "gcloud", "scheduler", "jobs", "create", "http",
            job_name,
            f"--project={PROJECT_ID}",
            f"--location={REGION}",
            f"--schedule={job['schedule']}",
            f"--time-zone={job['timezone']}",
            f"--uri={BACKEND_URL}{job['endpoint']}",
            "--http-method=POST",
            "--headers=Content-Type=application/json",
            f"--description={job['description']}",
            "--attempt-deadline=30m",  # 30 Minuten Timeout
            "--oidc-service-account-email=domulex-scheduler@domulex-ai.iam.gserviceaccount.com",
        ]
        
        print(f"📅 Creating: {job_name}")
        print(f"   Schedule: {job['schedule']} ({job['timezone']})")
        print(f"   Endpoint: {job['endpoint']}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ Created successfully\n")
            else:
                if "already exists" in result.stderr:
                    print(f"   ⚠️  Already exists, updating...\n")
                    # Update existing job
                    update_cmd = cmd.copy()
                    update_cmd[3] = "update"
                    subprocess.run(update_cmd)
                else:
                    print(f"   ❌ Error: {result.stderr}\n")
        except Exception as e:
            print(f"   ❌ Exception: {e}\n")
    
    print("\n✅ All scheduler jobs configured!")
    print(f"📊 Total jobs: {len(SCHEDULES)}")


def list_jobs():
    """List all existing scheduler jobs"""
    cmd = [
        "gcloud", "scheduler", "jobs", "list",
        f"--project={PROJECT_ID}",
        f"--location={REGION}",
        "--format=table(name,schedule,state,lastAttemptTime)"
    ]
    subprocess.run(cmd)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_jobs()
    else:
        create_scheduler_jobs()
