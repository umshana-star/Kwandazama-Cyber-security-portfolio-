detect_audit.py (Defensive Python Script)
 """
 detect_audit.py
 Defensive-only Keylogger Detection Tool (starter)
 Collects process, driver, autorun, and network metadata, scores suspicious items,
 and writes a JSON report. DO NOT use on machines you don't own.
 """
 import json, os, sys, datetime, subprocess
 from pathlib import Path
 # Try to import Windows-specific modules
 try:
    import psutil
 except Exception as e:
    print("Missing psutil. Install: pip install psutil")
    raise SystemExit(1)
 # Optional: wmi for richer Windows info
 USE_WMI = False
 try:
    import wmi
    USE_WMI = True
 except:
    pass
 # Helpers
 def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
 def is_path_in_temp(path):
    if not path:
        return False
    p = path.lower()
    return ("\\temp\\" in p) or ("\\appdata\\" in p and "\\local\\" in p)
 # Collect basic host info
 def collect_host_info():
    hostname = os.environ.get("COMPUTERNAME", "unknown")
    addrs = []
    for nic, addrs_list in psutil.net_if_addrs().items():
        for a in addrs_list:
            if a.family.name in ("AF_INET", "IPv4"):
                addrs.append(a.address)
    return {"hostname": hostname, "os": sys.platform, "ip_addresses": addrs}
 # Collect processes
 def collect_processes():
    procs = []
    for p in psutil.process_iter(attrs=['pid','name','exe','create_time','username']):
        info = p.info
        entry = {
            "pid": info.get('pid'),
            "name": info.get('name'),
            "path": info.get('exe'),
            "start_time":
 datetime.datetime.utcfromtimestamp(info.get('create_time')).isoformat()+"Z" if
 info.get('create_time') else None,
            "username": info.get('username'),
            "connections": [],
            "signed": None,
            "signer": None,
            "indicators": []
        }
        try:
            # gather network connections
            for c in p.connections(kind='inet'):
            # gather network connections
            for c in p.connections(kind='inet'):