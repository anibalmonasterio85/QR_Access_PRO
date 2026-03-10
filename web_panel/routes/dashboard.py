#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_panel/routes/dashboard.py - Dashboard principal
"""

from flask import Blueprint, render_template
from web_panel.models.access_log import AccessLog
from web_panel.utils.decorators import role_required
from config.settings import config

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@role_required('guardia', 'admin')
def index():
    stats = AccessLog.get_stats()
    weekly = AccessLog.get_weekly_stats()
    
    labels = []
    data_permitidos = []
    data_denegados = []
    
    for day in weekly:
        labels.append(day['fecha'].strftime('%d-%m'))
        data_permitidos.append(day['permitidos'])
        data_denegados.append(day['denegados'])
    
    return render_template(
        'dashboard.html',
        system_name=config.SYSTEM_NAME,
        permitidos=stats['permitidos'],
        denegados=stats['denegados'],
        labels=labels,
        data_permitidos=data_permitidos,
        data_denegados=data_denegados
    )
