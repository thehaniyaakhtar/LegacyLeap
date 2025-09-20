"""
Performance monitoring and metrics collection for AS/400 Legacy Modernization Assistant
"""

import time
import psutil
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass
import logging

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_io_read: int
    disk_io_write: int
    network_sent: int
    network_recv: int
    active_connections: int
    requests_per_second: float
    average_response_time: float
    error_rate: float

class PerformanceMonitor:
    """Performance monitoring system"""
    
    def __init__(self):
        self.metrics_history: List[PerformanceMetrics] = []
        self.request_times: List[float] = []
        self.error_count = 0
        self.request_count = 0
        self.start_time = time.time()
        self.logger = logging.getLogger(__name__)
        
    def record_request(self, response_time: float, is_error: bool = False):
        """Record a request and its performance"""
        self.request_count += 1
        self.request_times.append(response_time)
        
        if is_error:
            self.error_count += 1
        
        # Keep only last 1000 request times for rolling average
        if len(self.request_times) > 1000:
            self.request_times = self.request_times[-1000:]
    
    def collect_system_metrics(self) -> PerformanceMetrics:
        """Collect current system performance metrics"""
        # CPU and Memory
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used_mb = memory.used / (1024 * 1024)
        
        # Disk I/O
        disk_io = psutil.disk_io_counters()
        disk_io_read = disk_io.read_bytes if disk_io else 0
        disk_io_write = disk_io.write_bytes if disk_io else 0
        
        # Network I/O
        network_io = psutil.net_io_counters()
        network_sent = network_io.bytes_sent if network_io else 0
        network_recv = network_io.bytes_recv if network_io else 0
        
        # Application metrics
        uptime = time.time() - self.start_time
        requests_per_second = self.request_count / uptime if uptime > 0 else 0
        average_response_time = sum(self.request_times) / len(self.request_times) if self.request_times else 0
        error_rate = (self.error_count / self.request_count * 100) if self.request_count > 0 else 0
        
        # Active connections (simplified)
        active_connections = len(psutil.net_connections())
        
        metrics = PerformanceMetrics(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            memory_used_mb=memory_used_mb,
            disk_io_read=disk_io_read,
            disk_io_write=disk_io_write,
            network_sent=network_sent,
            network_recv=network_recv,
            active_connections=active_connections,
            requests_per_second=requests_per_second,
            average_response_time=average_response_time,
            error_rate=error_rate
        )
        
        self.metrics_history.append(metrics)
        
        # Keep only last 1000 metrics
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]
        
        return metrics
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for the last hour"""
        now = datetime.now()
        one_hour_ago = now.timestamp() - 3600
        
        recent_metrics = [
            m for m in self.metrics_history 
            if m.timestamp.timestamp() > one_hour_ago
        ]
        
        if not recent_metrics:
            return {"error": "No metrics available"}
        
        # Calculate averages
        avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_percent for m in recent_metrics) / len(recent_metrics)
        avg_response_time = sum(m.average_response_time for m in recent_metrics) / len(recent_metrics)
        avg_rps = sum(m.requests_per_second for m in recent_metrics) / len(recent_metrics)
        avg_error_rate = sum(m.error_rate for m in recent_metrics) / len(recent_metrics)
        
        # Get current values
        current = recent_metrics[-1]
        
        return {
            "timestamp": now.isoformat(),
            "current": {
                "cpu_percent": current.cpu_percent,
                "memory_percent": current.memory_percent,
                "memory_used_mb": current.memory_used_mb,
                "requests_per_second": current.requests_per_second,
                "average_response_time": current.average_response_time,
                "error_rate": current.error_rate,
                "active_connections": current.active_connections
            },
            "averages_last_hour": {
                "cpu_percent": round(avg_cpu, 2),
                "memory_percent": round(avg_memory, 2),
                "average_response_time": round(avg_response_time, 3),
                "requests_per_second": round(avg_rps, 2),
                "error_rate": round(avg_error_rate, 2)
            },
            "totals": {
                "total_requests": self.request_count,
                "total_errors": self.error_count,
                "uptime_seconds": int(time.time() - self.start_time)
            }
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get system health status"""
        current = self.collect_system_metrics()
        
        # Health thresholds
        cpu_threshold = 80.0
        memory_threshold = 85.0
        response_time_threshold = 2.0
        error_rate_threshold = 5.0
        
        # Check health
        health_issues = []
        
        if current.cpu_percent > cpu_threshold:
            health_issues.append(f"High CPU usage: {current.cpu_percent:.1f}%")
        
        if current.memory_percent > memory_threshold:
            health_issues.append(f"High memory usage: {current.memory_percent:.1f}%")
        
        if current.average_response_time > response_time_threshold:
            health_issues.append(f"Slow response time: {current.average_response_time:.3f}s")
        
        if current.error_rate > error_rate_threshold:
            health_issues.append(f"High error rate: {current.error_rate:.1f}%")
        
        status = "healthy" if not health_issues else "unhealthy"
        
        return {
            "status": status,
            "timestamp": current.timestamp.isoformat(),
            "issues": health_issues,
            "metrics": {
                "cpu_percent": current.cpu_percent,
                "memory_percent": current.memory_percent,
                "average_response_time": current.average_response_time,
                "error_rate": current.error_rate
            }
        }
    
    def export_metrics(self, filename: str = None) -> str:
        """Export metrics to JSON file"""
        if not filename:
            filename = f"performance_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "metrics_count": len(self.metrics_history),
            "metrics": [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "cpu_percent": m.cpu_percent,
                    "memory_percent": m.memory_percent,
                    "memory_used_mb": m.memory_used_mb,
                    "disk_io_read": m.disk_io_read,
                    "disk_io_write": m.disk_io_write,
                    "network_sent": m.network_sent,
                    "network_recv": m.network_recv,
                    "active_connections": m.active_connections,
                    "requests_per_second": m.requests_per_second,
                    "average_response_time": m.average_response_time,
                    "error_rate": m.error_rate
                }
                for m in self.metrics_history
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filename

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

def monitor_performance(func):
    """Decorator to monitor function performance"""
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            response_time = time.time() - start_time
            performance_monitor.record_request(response_time, False)
            return result
        except Exception as e:
            response_time = time.time() - start_time
            performance_monitor.record_request(response_time, True)
            raise e
    
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            response_time = time.time() - start_time
            performance_monitor.record_request(response_time, False)
            return result
        except Exception as e:
            response_time = time.time() - start_time
            performance_monitor.record_request(response_time, True)
            raise e
    
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

async def start_performance_monitoring():
    """Start background performance monitoring"""
    while True:
        try:
            performance_monitor.collect_system_metrics()
            await asyncio.sleep(60)  # Collect metrics every minute
        except Exception as e:
            print(f"Error in performance monitoring: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    # Test the performance monitor
    monitor = PerformanceMonitor()
    
    # Simulate some requests
    for i in range(10):
        monitor.record_request(0.1 + i * 0.01, i % 10 == 0)
    
    # Collect metrics
    metrics = monitor.collect_system_metrics()
    print(f"Current CPU: {metrics.cpu_percent}%")
    print(f"Current Memory: {metrics.memory_percent}%")
    
    # Get summary
    summary = monitor.get_performance_summary()
    print(f"Performance Summary: {json.dumps(summary, indent=2)}")
    
    # Get health status
    health = monitor.get_health_status()
    print(f"Health Status: {json.dumps(health, indent=2)}")
