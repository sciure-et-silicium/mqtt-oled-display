async function killDaemon() {
    const btn = document.getElementById('killBtn');
    const status = document.getElementById('status');
    
    btn.disabled = true;
    btn.textContent = 'Killing...';
    status.textContent = '';
    
    try {
        const response = await fetch('/api/kill-daemon', { method: 'POST' });
        const data = await response.json();
        
        if (response.ok) {
            status.textContent = `✅ Service killed (PID: ${data.pid})`;
        } else {
            status.textContent = `❌ Error: ${data.error}`;
        }
    } catch (error) {
        status.textContent = `❌ Network error: ${error.message}`;
    } finally {
        btn.disabled = false;
        btn.textContent = 'Kill Daemon';
    }
}