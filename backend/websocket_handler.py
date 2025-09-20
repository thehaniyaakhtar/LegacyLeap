"""
WebSocket handler for real-time updates
"""

import json
import asyncio
from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime

class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket connection"""
        try:
            await websocket.send_text(message)
        except Exception as e:
            print(f"Error sending personal message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: str):
        """Broadcast a message to all connected WebSocket clients"""
        if not self.active_connections:
            return
        
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error broadcasting to connection: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection)
    
    async def send_processing_update(self, legacy_id: str, status: str, progress: int = 0):
        """Send processing status update"""
        message = {
            "type": "processing_update",
            "legacy_id": legacy_id,
            "status": status,
            "progress": progress,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(json.dumps(message))
    
    async def send_transformation_complete(self, legacy_id: str, modernized_id: str, api_count: int, microservices_count: int):
        """Send transformation completion notification"""
        message = {
            "type": "transformation_complete",
            "legacy_id": legacy_id,
            "modernized_id": modernized_id,
            "api_count": api_count,
            "microservices_count": microservices_count,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(json.dumps(message))
    
    async def send_dashboard_update(self, dashboard_data: Dict):
        """Send dashboard data update"""
        message = {
            "type": "dashboard_update",
            "data": dashboard_data,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(json.dumps(message))
    
    async def send_error(self, error_message: str, legacy_id: str = None):
        """Send error notification"""
        message = {
            "type": "error",
            "message": error_message,
            "legacy_id": legacy_id,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(json.dumps(message))

# Global connection manager instance
manager = ConnectionManager()
