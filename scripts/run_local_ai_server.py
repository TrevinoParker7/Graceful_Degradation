"""
Local Lightweight OpenAI-Compatible AI Server for Testing
Simulates a real local model runtime (like Ollama / LM Studio) on http://127.0.0.1:11434
"""

import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class LocalAIRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/api/tags", "/v1/models"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "models": [
                    {"name": "qwen2.5-coder:7b", "id": "qwen2.5-coder:7b"},
                    {"name": "llama3.2:3b", "id": "llama3.2:3b"}
                ]
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        req_data = json.loads(body) if body else {}

        # Check prompt for injection
        prompt = req_data.get("prompt", "") or ""
        messages = req_data.get("messages", [])
        if messages:
            prompt = " ".join([m.get("content", "") for m in messages])

        is_suspicious = any(kw in prompt.lower() for kw in ["ignore previous", "override", "dump database", "exfiltrate", "delete all"])
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        if is_suspicious:
            resp_text = "SECURITY_ALERT: Suspicious injection detected in prompt."
        else:
            resp_text = "I am a local AI model assistant. Ready to help with code generation within policy bounds."

        if self.path == "/api/generate":
            response = {
                "model": "qwen2.5-coder:7b",
                "response": resp_text,
                "done": True
            }
        else:
            response = {
                "id": "chatcmpl-local-001",
                "choices": [{
                    "message": {"role": "assistant", "content": resp_text},
                    "finish_reason": "stop"
                }]
            }

        self.wfile.write(json.dumps(response).encode("utf-8"))

    def log_message(self, format, *args):
        pass

def run_local_ai_server(port=11434):
    server = HTTPServer(("127.0.0.1", port), LocalAIRequestHandler)
    print(f"Local AI Server running on http://127.0.0.1:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_local_ai_server()
