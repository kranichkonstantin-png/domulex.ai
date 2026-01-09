#!/usr/bin/env python3
"""Setup email configuration in Firestore"""

from google.cloud import firestore

db = firestore.Client(project='domulex-ai')
config_ref = db.collection('settings').document('email_config')

config_ref.set({
    'smtp_host': 'smtp.strato.de',
    'smtp_port': 465,
    'smtp_user': 'kontakt@domulex.ai',
    'smtp_password': '1G5f!akt,hZj5#!nGs',
    'from_email': 'kontakt@domulex.ai',
    'from_name': 'Domulex.ai',
    'use_ssl': True,
})

print('✅ E-Mail-Konfiguration gespeichert!')
print('   SMTP: smtp.strato.de:465')
print('   User: kontakt@domulex.ai')
print('   From: Domulex.ai <kontakt@domulex.ai>')
