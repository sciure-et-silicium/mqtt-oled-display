// Ultra minimal render preview functionality
(function() {
    'use strict';
    
    let debounceTimer;
    const DEBOUNCE_DELAY = 500;
    const PAYLOAD_STORAGE_KEY = 'mqtt_payload_sim';
    const DEFAULT_PAYLOAD = '{"temperature":22,"humidity":40}';
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', init);
    
    function init() {
        const templateInput = document.getElementById('render_template');
        const payloadInput = document.getElementById('payload');
        
        if (!templateInput || !payloadInput) return;
        
        // Load saved payload or use default
        let savedPayload = localStorage.getItem(PAYLOAD_STORAGE_KEY);
        if (!savedPayload) {
            savedPayload = DEFAULT_PAYLOAD;
            localStorage.setItem(PAYLOAD_STORAGE_KEY, savedPayload);
        }
        payloadInput.value = savedPayload;
        
        // Bind events
        templateInput.addEventListener('input', triggerPreview);
        payloadInput.addEventListener('input', onPayloadChange);
        
        // Initial preview
        triggerPreview();
    }
    
    function onPayloadChange() {
        localStorage.setItem(PAYLOAD_STORAGE_KEY, document.getElementById('payload').value);
        triggerPreview();
    }
    
    function triggerPreview() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(previewRender, DEBOUNCE_DELAY);
    }
    
    function previewRender() {
        const template = document.getElementById('render_template').value;
        const payload = document.getElementById('payload').value;
        
        if (!template.trim()) {
            showResult('Template is empty', false);
            return;
        }
        
        fetch('/api/preview-render', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                render_template: template,
                payload: payload
            })
        })
        .then(r => r.json())
        .then(data => {
            showResult(data.success ? data.result : data.error, data.success);
        })
        .catch(err => {
            showResult('Network error: ' + err.message, false);
        });
    }
    
    function showResult(text, isSuccess) {
        const resultDiv = document.getElementById('renderResult');
        resultDiv.textContent = text || 'Empty result';
        resultDiv.className = isSuccess ? 'render-result' : 'render-result render-error';
    }
    
    function reset() {
        document.getElementById('renderResult').innerHTML = '<span class="render-muted">Result will appear here...</span>';
        document.getElementById('renderResult').className = 'render-result';
        
        // Restore saved payload or default
        let savedPayload = localStorage.getItem(PAYLOAD_STORAGE_KEY);
        if (!savedPayload) {
            savedPayload = DEFAULT_PAYLOAD;
            localStorage.setItem(PAYLOAD_STORAGE_KEY, savedPayload);
        }
        document.getElementById('payload').value = savedPayload;
    }
    
    // Global access
    window.RenderPreview = { triggerPreview, reset };
})();
