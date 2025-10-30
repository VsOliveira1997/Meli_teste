import requests
from app.database import SessionLocal
from app.models import ExcludedIP

url = "https://check.torproject.org/torbulkexitlist"

def fetch_tor_ips():
    try:
        response = requests.get(url)

        if response.status_code == 200:
            ips = response.text.strip().split("\n")
            return {"tor_ips": ips}
        else:
            return {"tor_ips": []}
    except Exception as e:
        return {"error": f"{str(e)}"}


def get_filtered_ips(session):
    try:
        tor_ips_data = fetch_tor_ips()
        tor_ips_list = tor_ips_data.get("tor_ips", [])

        excluded_ips_from_db = session.query(ExcludedIP).all()

        excluded_ips_list = []
        for ip_record in excluded_ips_from_db:
            excluded_ips_list.append(ip_record.ip)

        final_ips_list = []
        for tor_ip in tor_ips_list:
            if tor_ip not in excluded_ips_list:
                final_ips_list.append(tor_ip)

        return {"filtered_ips": final_ips_list}
    except Exception as e:
        return {"error": f"{str(e)}"}