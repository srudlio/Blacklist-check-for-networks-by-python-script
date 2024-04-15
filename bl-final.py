import csv
import ipaddress
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_ip(ip, organisation, status_codes):
    try:
        reversed_ip = ".".join(reversed(ip.split('.')))  # Reverse the IP address
        result = subprocess.run(["dig", "+short", f"{reversed_ip}.{organisation}"], capture_output=True, text=True, timeout=3) #waiting time for response from spam organisation - by default 10seconds
        result = result.stdout.strip()
        if result in status_codes:
            return "Listed"
        elif result == "":
            return "OK"
        else:
            return "ОК"
    except subprocess.TimeoutExpired:
        print(f"Timeout for IP {ip} while querying {organisation}")
        return "OK"
    except subprocess.CalledProcessError as e:
        print(f"Error for IP {ip} while querying {organisation}: {e}")
        return "OK"

def process_network(network, spam_organisations):
    ips = [str(ip) for ip in ipaddress.IPv4Network(network)]
    results = {ip: {organisation: "OK" for organisation in spam_organisations} for ip in ips}  # Initialize all IPs with "OK" for all organizations

    for organisation, status_codes in spam_organisations.items():
        with ThreadPoolExecutor(max_workers=100) as executor:    #Multythread units
            future_to_ip = {executor.submit(check_ip, ip, organisation, status_codes): ip for ip in ips}
            for future in as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    result = future.result()
                    results[ip][organisation] = result
                except Exception as exc:
                    results[ip][organisation] = "Error"

    return results


def main():
    networks = ["1.0.0.0/24", "2.0.0.0/24"]  # Add more networks as needed
    output_files = ["blacklisted_ips_network1.csv", "blacklisted_ips_network2.csv"]  # Adjust output file names as needed

    spam_organisations = {}
    with open("spam_organisations.csv", mode='r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            try:
                organisation_name = row[0]
                status_codes = row[1].split(",")
                spam_organisations[organisation_name] = status_codes
            except IndexError:
                print(f"Issue with row: {row}")

    for network, output_file in zip(networks, output_files):
        results = process_network(network, spam_organisations)

        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["IP Address"] + list(spam_organisations.keys()))  # Write organisation names as column headers
            writer.writerow([])  # Empty row
            for ip, statuses in results.items():
                row = [ip] + [statuses[organisation] for organisation in spam_organisations]
                writer.writerow(row)

    send_email("*****", "*****", output_files) # replace with email accounts (where to send reports) 


def send_email(to_email, cc_email, attachment_files):
    from_email = "*****"  # Replace with your email
    password = "*****"  # Replace with your email password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Cc'] = cc_email
    msg['Subject'] = "Blacklisted IPs Report"

    for file_path in attachment_files:
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {file_path}",
            )
            msg.attach(part)

    smtp_server = smtplib.SMTP('example.com', 587)  # Replace with other SMTP server details
    smtp_server.starttls()
    smtp_server.login(from_email, password)
    recipients = [to_email] + [cc_email]
    smtp_server.sendmail(from_email, recipients, msg.as_string())
    smtp_server.quit()

  
if __name__ == "__main__":
    main()
