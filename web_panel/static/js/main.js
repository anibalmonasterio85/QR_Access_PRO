const Utils = {
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString('es-CL', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    },
    
    escapeHtml: function(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },
    
    showToast: function(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 
                                 type === 'error' ? 'exclamation-circle' : 
                                 'info-circle'}"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(toast);
        setTimeout(() => toast.classList.add('show'), 10);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
};

const Filters = {
    init: function() {
        document.querySelectorAll('.filter-input, .filter-select').forEach(el => {
            el.addEventListener('input', Utils.debounce(() => {
                this.applyFilters();
            }, 500));
        });
    },
    
    getValues: function() {
        const filters = {};
        document.querySelectorAll('[data-filter]').forEach(el => {
            filters[el.dataset.filter] = el.value;
        });
        return filters;
    },
    
    applyFilters: function() {
        const event = new CustomEvent('filtersChanged', { detail: this.getValues() });
        document.dispatchEvent(event);
    }
};

const LiveUpdates = {
    intervals: {},
    
    start: function(endpoint, callback, intervalMs = 5000) {
        this.stop(endpoint);
        
        const fetchAndUpdate = async () => {
            try {
                // Añadir timestamp para evitar caché de navegador en peticiones GET periódicas
                const separator = endpoint.includes('?') ? '&' : '?';
                const urlWithBuster = `${endpoint}${separator}_t=${new Date().getTime()}`;
                
                const response = await fetch(urlWithBuster, {
                    headers: { 
                        'X-Requested-With': 'XMLHttpRequest',
                        'Cache-Control': 'no-cache, no-store, must-revalidate',
                        'Pragma': 'no-cache',
                        'Expires': '0'
                    }
                });
                const data = await response.json();
                callback(data);
            } catch (error) {
                console.error('Error en live update:', error);
            }
        };
        
        fetchAndUpdate();
        this.intervals[endpoint] = setInterval(fetchAndUpdate, intervalMs);
    },
    
    stop: function(endpoint) {
        if (this.intervals[endpoint]) {
            clearInterval(this.intervals[endpoint]);
            delete this.intervals[endpoint];
        }
    },
    
    stopAll: function() {
        Object.values(this.intervals).forEach(clearInterval);
        this.intervals = {};
    }
};

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.card, .stat-card').forEach((el, index) => {
        el.style.animationDelay = `${index * 0.1}s`;
        el.classList.add('fade-in');
    });
});

window.Utils = Utils;
window.Filters = Filters;
window.LiveUpdates = LiveUpdates;
