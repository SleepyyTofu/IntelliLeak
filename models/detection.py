import re


# Detect sensitive data
def detect_sensitive_data(text):

    findings = []

    # =========================
    # Malaysia NRIC
    # =========================
    malaysia_nric_pattern = r'\b\d{6}-\d{2}-\d{4}\b'

    malaysia_matches = re.findall(
        malaysia_nric_pattern,
        text
    )

    for match in malaysia_matches:

        findings.append({
            "type": "Identity Number (NRIC)",
            "country": "Malaysia",
            "value": match,
            "risk": "HIGH"
        })



    # =========================
    # Singapore NRIC / FIN
    # =========================
    singapore_pattern = r'\b[STFG]\d{7}[A-Z]\b'

    singapore_matches = re.findall(
        singapore_pattern,
        text
    )

    for match in singapore_matches:

        findings.append({
            "type": "Identity Number (NRIC)",
            "country": "Singapore",
            "value": match,
            "risk": "HIGH"
        })



    # =========================
    # Indonesia NIK
    # =========================
    indonesia_pattern = r'\b\d{16}\b'

    indonesia_matches = re.findall(
        indonesia_pattern,
        text
    )

    for match in indonesia_matches:

        findings.append({
            "type": "Identity Number (NIK)",
            "country": "Indonesia",
            "value": match,
            "risk": "HIGH"
        })



    # =========================
    # Email Detection
    # =========================
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

    email_matches = re.findall(email_pattern, text)

    for match in email_matches:

        findings.append({
            "type": "Email",
            "value": match,
            "risk": "MEDIUM"
        })



    # =========================
    # Phone Number Detection
    # =========================
    phone_pattern = r'\b(?:\+?\d{1,3}[- ]?)?(?:\(?\d{2,4}\)?[- ]?)?\d{3,4}[- ]?\d{4}\b'

    phone_matches = re.findall(phone_pattern, text)

    for match in phone_matches:

        findings.append({
            "type": "Phone Number",
            "value": match,
            "risk": "MEDIUM"
        })



    # =========================
    # IP Address Detection
    # =========================
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

    ip_matches = re.findall(ip_pattern, text)

    for match in ip_matches:

        findings.append({
            "type": "IP Address",
            "value": match,
            "risk": "LOW"
        })



    # =========================
    # API Key Detection
    # =========================
    api_pattern = r'\b(?:sk_live_|sk_test_|sk-)[A-Za-z0-9_-]{16,}\b'

    api_matches = re.findall(api_pattern, text)

    for match in api_matches:

        findings.append({
            "type": "API Key",
            "value": match,
            "risk": "CRITICAL"
        })


    # =========================
    # Password Detection
    # =========================
    password_pattern = (
        r'(?i)\b(?:password|pwd|pass)\b\s*[:=]\s*([^\r\n]+)'
    )

    password_matches = re.finditer(
        password_pattern,
        text
    )

    for match in password_matches:

        findings.append({
            "type": "Password",
            "value": match.group(1),
            "risk": "CRITICAL"
        })

    # =========================
    # Employee ID
    # =========================
    employee_pattern = r'\bEMP-\d{3,6}\b'

    employee_matches = re.findall(
        employee_pattern,
        text
    )

    for match in employee_matches:

        findings.append({
            "type": "Employee ID",
            "value": match,
            "risk": "HIGH"
        })

    # =========================
    # VPN Username
    # =========================
    vpn_pattern = r'(?i)VPN\s*Username\s*:\s*([^\s]+)'

    vpn_matches = re.finditer(
        vpn_pattern,
        text
    )

    for match in vpn_matches:

        findings.append({
            "type": "VPN Username",
            "value": match.group(1),
            "risk": "HIGH"
        })


    # =========================
    # Credit Card Detection
    # =========================
    credit_card_pattern = (
        r'\b(?:4\d{3}|5[1-5]\d{2})'
        r'(?:[ -]?\d{4}){3}\b'
    )

    credit_card_matches = re.finditer(
        credit_card_pattern,
        text
    )

    for match in credit_card_matches:

        findings.append({
            "type": "Credit Card",
            "value": match.group(0),
            "risk": "CRITICAL"
        })


    # =========================
    # AWS Access Key Detection
    # =========================
    aws_pattern = r'\bAKIA[0-9A-Z]{16}\b'

    aws_matches = re.finditer(
        aws_pattern,
        text
    )

    for match in aws_matches:

        findings.append({
            "type": "AWS Access Key",
            "value": match.group(0),
            "risk": "CRITICAL"
        })


    # =========================
    # Private Key Detection
    # =========================
    private_key_pattern = r'-----BEGIN PRIVATE KEY-----'

    private_key_matches = re.findall(
        private_key_pattern,
        text
    )

    for match in private_key_matches:

        findings.append({
            "type": "Private Key",
            "value": match,
            "risk": "CRITICAL"
        })


    # =========================
    # GitHub Token Detection
    # =========================
    github_pattern = r'\bghp_[A-Za-z0-9]{36}\b'

    github_matches = re.finditer(
        github_pattern,
        text
    )

    for match in github_matches:

        findings.append({
            "type": "GitHub Token",
            "value": match.group(0),
            "risk": "CRITICAL"
        })


    # =========================
    # Bank Account Detection
    # =========================
    bank_pattern = r'\b\d{10,12}\b'

    bank_matches = re.finditer(
        bank_pattern,
        text
    )

    for match in bank_matches:

        findings.append({
            "type": "Bank Account",
            "value": match.group(0),
            "risk": "HIGH"
        })


    # =========================
    # AWS Secret Key
    # =========================
    secret_pattern = r'(?i)AWS\s*Secret\s*Access\s*Key\s*:\s*([^\r\n]+)'

    secret_matches = re.finditer(secret_pattern, text)

    for match in secret_matches:

        findings.append({
            "type": "AWS Secret Access Key",
            "value": match.group(1),
            "risk": "CRITICAL"
        })


    return findings



# Highlight sensitive data
def highlight_sensitive_data(text):

    # Malaysia NRIC
    text = re.sub(
        r'\b\d{6}-\d{2}-\d{4}\b',
        r'<mark style="background-color:#EF5350;color:white;">\g<0></mark>',
        text
    )

    # Singapore NRIC
    text = re.sub(
        r'\b[STFG]\d{7}[A-Z]\b',
        r'<mark style="background-color:#EF5350;color:white;">\g<0></mark>',
        text
    )

    # Indonesia NIK
    text = re.sub(
        r'\b\d{16}\b',
        r'<mark style="background-color:#EF5350;color:white;">\g<0></mark>',
        text
    )

    # Email
    text = re.sub(
        r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
        r'<mark style="background-color:#FFCC80;color:black;">\g<0></mark>',
        text
    )

    # Phone Number
    text = re.sub(
        r'\b(?:\+?\d{1,3}[- ]?)?(?:\(?\d{2,4}\)?[- ]?)?\d{3,4}[- ]?\d{4}\b',
        r'<mark style="background-color:#FFF59D;color:black;">\g<0></mark>',
        text
    )

    # IP Address
    text = re.sub(
        r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        r'<mark style="background-color:#90CAF9;color:black;padding:2px 5px;border-radius:4px;">\g<0></mark>',
        text
    )

    # API Key
    text = re.sub(
        r'\b(?:sk_live_|sk_test_|sk-)[A-Za-z0-9_-]{16,}\b',
        r'<mark style="background-color:#8B0000;color:white;">\g<0></mark>',
        text
    )

    # Password
    text = re.sub(
        r'(?i)\b(?:password|pwd|pass)\b\s*[:=]\s*([^\r\n]+)',
        r'<mark style="background-color:#8B0000;color:white;">\g<0></mark>',
        text
    )

    #Employee ID
    text = re.sub(
        r'\bEMP-\d{3,6}\b',
        r'<mark style="background-color:#EF5350;color:white;">\g<0></mark>',
        text
    )

    # VPN Username 
    text = re.sub(
        r'(?i)VPN\s*Username\s*:\s*([^\s]+)',
        r'<mark style="background-color:#EF5350;color:white;">\g<0></mark>',
        text
    )

    # Credit Card
    text = re.sub(
        r'\b(?:4\d{3}|5[1-5]\d{2})(?:[ -]?\d{4}){3}\b',
        r'<mark style="background-color:#8B0000;color:white;">\g<0></mark>',
        text
    )

    # AWS Access Key
    text = re.sub(
        r'\bAKIA[0-9A-Z]{16}\b',
        r'<mark style="background-color:#8B0000;color:white;">\g<0></mark>',
        text
    )

    # Private Key
    text = re.sub(
        r'-----BEGIN PRIVATE KEY-----',
        r'<mark style="background-color:#8B0000;color:white;">\g<0></mark>',
        text
    )

    # GitHub Token
    text = re.sub(
        r'\bghp_[A-Za-z0-9]{36}\b',
        r'<mark style="background-color:#8B0000;color:white;">\g<0></mark>',
        text
    )

    # Bank Account
    text = re.sub(
        r'\b\d{10,12}\b',
        r'<mark style="background-color:#EF5350;color:white;">\g<0></mark>',
        text
    )

    #AWS Secret Key
    text = re.sub(
        r'(?i)AWS\s*Secret\s*Access\s*Key\s*:\s*([^\r\n]+)',
        r'<mark style="background-color:#8B0000;color:white;">\g<0></mark>',
        text
    )

    return text