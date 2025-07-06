
#!/usr/bin/env python3
"""
Real-time Performance Monitor for HYBRID Blockchain
"""
import psutil
import time
import json
from datetime import datetime
import streamlit as st

class PerformanceMonitor:
    def __init__(self):
        self.metrics_history = []
        self.start_time = time.time()
    
    def get_system_metrics(self):
        """Get current system performance metrics"""
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "network_io": psutil.net_io_counters()._asdict(),
            "process_count": len(psutil.pids()),
            "uptime": time.time() - self.start_time
        }
    
    def log_metrics(self):
        """Log current metrics to history"""
        metrics = self.get_system_metrics()
        self.metrics_history.append(metrics)
        
        # Keep only last 100 entries
        if len(self.metrics_history) > 100:
            self.metrics_history.pop(0)
        
        return metrics
    
    def get_performance_summary(self):
        """Get performance summary"""
        if not self.metrics_history:
            return None
        
        recent_metrics = self.metrics_history[-10:]  # Last 10 entries
        
        avg_cpu = sum(m['cpu_percent'] for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m['memory_percent'] for m in recent_metrics) / len(recent_metrics)
        
        return {
            "avg_cpu_10s": avg_cpu,
            "avg_memory_10s": avg_memory,
            "total_samples": len(self.metrics_history),
            "monitoring_duration": time.time() - self.start_time
        }

# Global monitor instance
performance_monitor = PerformanceMonitor()

if __name__ == "__main__":
    monitor = PerformanceMonitor()
    
    print("🔍 Starting Performance Monitor...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            metrics = monitor.log_metrics()
            print(f"CPU: {metrics['cpu_percent']:.1f}% | Memory: {metrics['memory_percent']:.1f}% | Processes: {metrics['process_count']}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n✅ Performance monitoring stopped")
        summary = monitor.get_performance_summary()
        if summary:
            print(f"Average CPU (10s): {summary['avg_cpu_10s']:.1f}%")
            print(f"Average Memory (10s): {summary['avg_memory_10s']:.1f}%")
