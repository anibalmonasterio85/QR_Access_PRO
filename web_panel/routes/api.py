#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_panel/routes/api.py - API REST
"""

from flask import Blueprint, jsonify, request
from web_panel.models.user import User
from web_panel.models.access_log import AccessLog
from web_panel.utils.decorators import role_required, ajax_required
from web_panel.utils.security import require_api_key

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/accesos/live')
@ajax_required
@role_required('guardia', 'admin')
def accesos_live():
    logs = AccessLog.get_recent(10)
    processed = []
    
    for log in logs:
        detalle = log.qr_texto
        if log.is_permitido():
            user = User.get_by_qr(log.qr_texto)
            if user:
                detalle = f"{user.nombre} ({user.empresa})"
        
        processed.append({
            'detalle': detalle,
            'resultado': log.resultado,
            'fecha_hora': log.fecha_hora.isoformat()
        })
    
    return jsonify(processed)

@api_bp.route('/stats')
@ajax_required
@role_required('guardia', 'admin')
def stats():
    return jsonify(AccessLog.get_stats())

@api_bp.route('/accesos/filter', methods=['POST'])
@ajax_required
@role_required('guardia', 'admin')
def filter_accesos():
    data = request.get_json() or {}
    
    fecha_inicio = data.get('fecha_inicio')
    if not fecha_inicio:
        fecha_inicio = '1970-01-01'
        
    fecha_fin = data.get('fecha_fin')
    if not fecha_fin:
        fecha_fin = '2100-12-31'
        
    resultado = data.get('resultado')
    if not resultado:
        resultado = '%'
        
    busqueda = data.get('busqueda', '')
    
    logs = AccessLog.get_filtered(
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        resultado=resultado,
        busqueda=f"%{busqueda}%"
    )
    
    processed = []
    for log in logs:
        detalle = log.qr_texto
        if log.is_permitido():
            user = User.get_by_qr(log.qr_texto)
            if user:
                detalle = f"{user.nombre} ({user.empresa})"
        
        processed.append({
            'detalle': detalle,
            'resultado': log.resultado,
            'fecha_hora': log.fecha_hora.isoformat()
        })
    
    return jsonify(processed)
