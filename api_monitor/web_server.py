"""Web server for displaying monitoring in browser."""

import time
import json
import threading
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from .loader import Config
from .checker import check_all_apis, CheckResult
from .reporter import format_html
from .cache import ResultCache


def find_free_port(start_port: int = 8080, max_attempts: int = 100) -> int:
    """
    Finds a free port starting from the specified one.
    
    Args:
        start_port: Starting port for search
        max_attempts: Maximum number of attempts
        
    Returns:
        Free port number
        
    Raises:
        OSError: If failed to find a free port
    """
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise OSError(f"Failed to find free port in range {start_port}-{start_port + max_attempts - 1}")


class MonitoringHandler(BaseHTTPRequestHandler):
    """HTTP request handler for web interface."""
    
    monitoring_data = {
        'results': [],
        'history': [],
        'stats': {
            'total_checks': 0,
            'successful_checks': 0,
            'failed_checks': 0,
            'last_check': None,
            'start_time': datetime.now().isoformat()
        },
        'config': None,
        'config_path': None,
        'server_instance': None
    }
    
    # List of popular APIs for quick addition
    POPULAR_APIS = [
        {'name': 'Google', 'url': 'https://www.google.com', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'GitHub API', 'url': 'https://api.github.com', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'JSONPlaceholder', 'url': 'https://jsonplaceholder.typicode.com/posts/1', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'HTTPBin Status', 'url': 'https://httpbin.org/status/200', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'Stack Overflow API', 'url': 'https://api.stackexchange.com/2.3/info?site=stackoverflow', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'Reddit API', 'url': 'https://www.reddit.com/r/python.json', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'Twitter API', 'url': 'https://api.twitter.com/1.1/help/configuration.json', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'Facebook Graph API', 'url': 'https://graph.facebook.com/v18.0/me', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'OpenWeatherMap', 'url': 'https://api.openweathermap.org/data/2.5/weather?q=London&appid=demo', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'NASA API', 'url': 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'CoinGecko API', 'url': 'https://api.coingecko.com/api/v3/ping', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'REST Countries', 'url': 'https://restcountries.com/v3.1/name/russia', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'Dog API', 'url': 'https://dog.ceo/api/breeds/list/all', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'Cat Facts API', 'url': 'https://catfact.ninja/fact', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'Joke API', 'url': 'https://official-joke-api.appspot.com/random_joke', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'IPify', 'url': 'https://api.ipify.org?format=json', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'JSONPlaceholder Posts', 'url': 'https://jsonplaceholder.typicode.com/posts', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'JSONPlaceholder Users', 'url': 'https://jsonplaceholder.typicode.com/users', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'HTTPBin Get', 'url': 'https://httpbin.org/get', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200},
        {'name': 'HTTPBin JSON', 'url': 'https://httpbin.org/json', 'method': 'GET', 'timeout': 5.0, 'expected_status': 200}
    ]
    
    def do_GET(self):
        """Handles GET requests."""
        if self.path == '/' or self.path == '/index.html':
            self.serve_dashboard()
        elif self.path == '/api/data':
            self.serve_json_data()
        elif self.path == '/api/stats':
            self.serve_stats()
        elif self.path == '/api/project':
            self.serve_project_info()
        elif self.path == '/api/apis':
            self.serve_apis_list()
        elif self.path == '/api/popular':
            self.serve_popular_apis()
        elif self.path == '/api/refresh':
            self.handle_refresh_monitoring()
        elif self.path == '/api/swagger.json' or self.path == '/api/openapi.json':
            self.serve_openapi_spec()
        elif self.path == '/api/docs' or self.path == '/swagger':
            self.serve_swagger_ui()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handles POST requests (adding API)."""
        if self.path == '/api/apis':
            self.handle_add_api()
        else:
            self.send_error(404)
    
    def do_PUT(self):
        """Handles PUT requests (updating API)."""
        if self.path.startswith('/api/apis/'):
            api_name = self.path.split('/')[-1]
            self.handle_update_api(api_name)
        else:
            self.send_error(404)
    
    def do_DELETE(self):
        """Handles DELETE requests (deleting API)."""
        if self.path.startswith('/api/apis/'):
            api_name = self.path.split('/')[-1]
            self.handle_delete_api(api_name)
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        """Serves dashboard main page."""
        html_content = self.get_dashboard_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_json_data(self):
        """Serves monitoring data as JSON."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        data = {
            'results': [self.result_to_dict(r) for r in MonitoringHandler.monitoring_data['results']],
            'stats': MonitoringHandler.monitoring_data['stats'],
            'timestamp': datetime.now().isoformat()
        }
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))
    
    def serve_stats(self):
        """Serves statistics."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(MonitoringHandler.monitoring_data['stats'], ensure_ascii=False).encode('utf-8'))
    
    def serve_project_info(self):
        """Serves project information."""
        project_info = {
            'name': 'API Health Monitor',
            'version': '1.0.0',
            'description': 'Lightweight Python CLI tool for monitoring API availability and performance',
            'features': [
                'HTTP status and latency checks for APIs',
                'Configurable timeouts',
                'Output results in table, JSON, CSV or HTML',
                'Exit codes for CI/CD integration',
                'Result logging',
                'Simple YAML configuration',
                'Periodic monitoring',
                'Web interface for visualization'
            ],
            'tech_stack': [
                'Python 3.8+',
                'requests - HTTP requests',
                'pyyaml - configuration',
                'tabulate - table formatting',
                'pytest - testing'
            ],
            'repository': 'https://github.com/maksim4351/api-health-monitor'
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(project_info, ensure_ascii=False, indent=2).encode('utf-8'))
    
    def result_to_dict(self, result: CheckResult):
        """Converts CheckResult to dictionary."""
        return {
            'name': result.name,
            'url': result.url,
            'status_code': result.status_code,
            'latency_ms': result.latency_ms,
            'success': result.success,
            'error': result.error,
            'timeout': result.timeout,
            'timestamp': datetime.now().isoformat()
        }
    
    def serve_apis_list(self):
        """Serves list of current APIs."""
        from .loader import APIConfig
        server = MonitoringHandler.monitoring_data.get('server_instance')
        if not server:
            self.send_error(500, "Server instance not found")
            return
        
        apis_list = []
        for api in server.config.apis:
            apis_list.append({
                'name': api.name,
                'url': api.url,
                'method': api.method,
                'timeout': api.timeout,
                'expected_status': api.expected_status,
                'headers': api.headers or {}
            })
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(apis_list, ensure_ascii=False, indent=2).encode('utf-8'))
    
    def serve_popular_apis(self):
        """Serves list of popular APIs."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(MonitoringHandler.POPULAR_APIS, ensure_ascii=False, indent=2).encode('utf-8'))
    
    def handle_refresh_monitoring(self):
        """Forces refresh of monitoring for all APIs."""
        from .checker import check_all_apis
        server = MonitoringHandler.monitoring_data.get('server_instance')
        if not server:
            self.send_error(500, "Server instance not found")
            return
        
        try:
            # Perform check for all APIs
            results = check_all_apis(server.config.apis)
            
            # Update data
            MonitoringHandler.monitoring_data['results'] = results
            MonitoringHandler.monitoring_data['history'].append({
                'timestamp': datetime.now().isoformat(),
                'results': [self.result_to_dict(r) for r in results]
            })
            
            # Update statistics
            stats = MonitoringHandler.monitoring_data['stats']
            stats['total_checks'] = stats.get('total_checks', 0) + 1
            stats['last_check'] = datetime.now().isoformat()
            successful = sum(1 for r in results if r.success)
            stats['successful_checks'] = stats.get('successful_checks', 0) + successful
            stats['failed_checks'] = stats.get('failed_checks', 0) + (len(results) - successful)
            
            # Limit history (last 100 checks)
            if len(MonitoringHandler.monitoring_data['history']) > 100:
                MonitoringHandler.monitoring_data['history'].pop(0)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response_data = {
                'success': True,
                'message': 'Monitoring refreshed',
                'results_count': len(results)
            }
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Failed to refresh monitoring: {str(e)}")
    
    def serve_openapi_spec(self):
        """Serves OpenAPI specification."""
        openapi_spec = {
            'openapi': '3.0.0',
            'info': {
                'title': 'API Health Monitor API',
                'version': '1.0.0',
                'description': 'REST API for monitoring API endpoint health',
                'contact': {
                    'name': 'API Support',
                    'url': 'https://github.com/maksim4351/api-health-monitor'
                }
            },
            'servers': [
                {
                    'url': 'http://localhost:8080',
                    'description': 'Local development server'
                }
            ],
            'paths': {
                '/api/data': {
                    'get': {
                        'summary': 'Get monitoring data',
                        'description': 'Returns current check results for all APIs',
                        'responses': {
                            '200': {
                                'description': 'Success response',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'object',
                                            'properties': {
                                                'results': {
                                                    'type': 'array',
                                                    'items': {
                                                        'type': 'object',
                                                        'properties': {
                                                            'name': {'type': 'string'},
                                                            'url': {'type': 'string'},
                                                            'status_code': {'type': 'integer', 'nullable': True},
                                                            'latency_ms': {'type': 'number'},
                                                            'success': {'type': 'boolean'},
                                                            'error': {'type': 'string', 'nullable': True}
                                                        }
                                                    }
                                                },
                                                'stats': {'type': 'object'},
                                                'timestamp': {'type': 'string', 'format': 'date-time'}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                '/api/stats': {
                    'get': {
                        'summary': 'Get statistics',
                        'description': 'Returns overall monitoring statistics',
                        'responses': {
                            '200': {
                                'description': 'Success response',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'object',
                                            'properties': {
                                                'total_checks': {'type': 'integer'},
                                                'successful_checks': {'type': 'integer'},
                                                'failed_checks': {'type': 'integer'},
                                                'last_check': {'type': 'string', 'format': 'date-time'},
                                                'start_time': {'type': 'string', 'format': 'date-time'}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                '/api/apis': {
                    'get': {
                        'summary': 'Get API list',
                        'description': 'Returns list of all configured APIs',
                        'responses': {
                            '200': {
                                'description': 'Success response',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'name': {'type': 'string'},
                                                    'url': {'type': 'string'},
                                                    'method': {'type': 'string'},
                                                    'timeout': {'type': 'number'},
                                                    'expected_status': {'type': 'integer'},
                                                    'headers': {'type': 'object'}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'post': {
                        'summary': 'Add new API',
                        'description': 'Adds new API to monitoring',
                        'requestBody': {
                            'required': True,
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'required': ['name', 'url'],
                                        'properties': {
                                            'name': {'type': 'string', 'description': 'API name'},
                                            'url': {'type': 'string', 'format': 'uri', 'description': 'API URL'},
                                            'method': {'type': 'string', 'enum': ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'], 'default': 'GET'},
                                            'timeout': {'type': 'number', 'default': 5.0, 'description': 'Timeout in seconds'},
                                            'expected_status': {'type': 'integer', 'default': 200, 'minimum': 100, 'maximum': 599},
                                            'headers': {'type': 'object', 'description': 'HTTP headers'}
                                        }
                                    }
                                }
                            }
                        },
                        'responses': {
                            '201': {
                                'description': 'API successfully added',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'object',
                                            'properties': {
                                                'success': {'type': 'boolean'},
                                                'message': {'type': 'string'}
                                            }
                                        }
                                    }
                                }
                            },
                            '400': {'description': 'Bad request'},
                            '409': {'description': 'API already exists'},
                            '500': {'description': 'Server error'}
                        }
                    }
                },
                '/api/apis/{name}': {
                    'put': {
                        'summary': 'Update API',
                        'description': 'Updates existing API',
                        'parameters': [
                            {
                                'name': 'name',
                                'in': 'path',
                                'required': True,
                                'schema': {'type': 'string'},
                                'description': 'API name to update'
                            }
                        ],
                        'requestBody': {
                            'required': True,
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {
                                            'name': {'type': 'string'},
                                            'url': {'type': 'string', 'format': 'uri'},
                                            'method': {'type': 'string'},
                                            'timeout': {'type': 'number'},
                                            'expected_status': {'type': 'integer'},
                                            'headers': {'type': 'object'}
                                        }
                                    }
                                }
                            }
                        },
                        'responses': {
                            '200': {'description': 'API successfully updated'},
                            '404': {'description': 'API not found'},
                            '500': {'description': 'Server error'}
                        }
                    },
                    'delete': {
                        'summary': 'Delete API',
                        'description': 'Removes API from monitoring',
                        'parameters': [
                            {
                                'name': 'name',
                                'in': 'path',
                                'required': True,
                                'schema': {'type': 'string'},
                                'description': 'API name to delete'
                            }
                        ],
                        'responses': {
                            '200': {'description': 'API successfully deleted'},
                            '404': {'description': 'API not found'},
                            '400': {'description': 'Cannot delete last API'},
                            '500': {'description': 'Server error'}
                        }
                    }
                },
                '/api/refresh': {
                    'get': {
                        'summary': 'Refresh monitoring',
                        'description': 'Forces refresh of monitoring results for all APIs',
                        'responses': {
                            '200': {
                                'description': 'Monitoring refreshed',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'object',
                                            'properties': {
                                                'success': {'type': 'boolean'},
                                                'message': {'type': 'string'},
                                                'results_count': {'type': 'integer'}
                                            }
                                        }
                                    }
                                }
                            },
                            '500': {'description': 'Server error'}
                        }
                    }
                },
                '/api/popular': {
                    'get': {
                        'summary': 'Get popular APIs',
                        'description': 'Returns list of popular APIs for quick addition',
                        'responses': {
                            '200': {
                                'description': 'Success response',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'name': {'type': 'string'},
                                                    'url': {'type': 'string'},
                                                    'method': {'type': 'string'},
                                                    'timeout': {'type': 'number'},
                                                    'expected_status': {'type': 'integer'}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(openapi_spec, ensure_ascii=False, indent=2).encode('utf-8'))
    
    def serve_swagger_ui(self):
        """Serves Swagger UI for interactive documentation."""
        swagger_ui_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Health Monitor - API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css" />
    <style>
        body {{
            margin: 0;
            background: #fafafa;
        }}
        .swagger-ui .topbar {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {{
            const ui = SwaggerUIBundle({{
                url: '/api/openapi.json',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout",
                validatorUrl: null
            }});
        }};
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(swagger_ui_html.encode('utf-8'))
    
    def read_json_body(self):
        """Reads JSON request body."""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return None
        body = self.rfile.read(content_length)
        try:
            return json.loads(body.decode('utf-8'))
        except json.JSONDecodeError:
            return None
    
    def handle_add_api(self):
        """Handles adding new API."""
        from .loader import APIConfig, save_config
        try:
            data = self.read_json_body()
            if not data:
                self.send_error(400, "Invalid JSON")
                return
            
            server = MonitoringHandler.monitoring_data.get('server_instance')
            if not server:
                self.send_error(500, "Server instance not found")
                return
            
            # Validation
            if 'name' not in data or 'url' not in data:
                self.send_error(400, "Missing required fields: name, url")
                return
            
            name = data['name'].strip()
            url = data['url'].strip()
            
            if not name or not url:
                self.send_error(400, "Name and URL cannot be empty")
                return
            
            # Check for duplicate by name
            if any(api.name == name for api in server.config.apis):
                self.send_response(409)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_data = {
                    'success': False,
                    'error': 'duplicate',
                    'message': f"API with name '{name}' already exists"
                }
                self.wfile.write(json.dumps(error_data, ensure_ascii=False).encode('utf-8'))
                return
            
            # Check for duplicate by URL
            if any(api.url == url for api in server.config.apis):
                self.send_response(409)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_data = {
                    'success': False,
                    'error': 'duplicate_url',
                    'message': f"API with URL '{url}' already exists"
                }
                self.wfile.write(json.dumps(error_data, ensure_ascii=False).encode('utf-8'))
                return
            
            # Timeout validation
            timeout = float(data.get('timeout', 5.0))
            if timeout <= 0:
                self.send_error(400, "Timeout must be positive")
                return
            
            # Expected status validation
            expected_status = int(data.get('expected_status', 200))
            if expected_status < 100 or expected_status >= 600:
                self.send_error(400, "Expected status must be between 100 and 599")
                return
            
            # Create new API
            new_api = APIConfig(
                name=name,
                url=url,
                method=data.get('method', 'GET'),
                timeout=timeout,
                expected_status=expected_status,
                headers=data.get('headers', {})
            )
            
            server.config.apis.append(new_api)
            
            # Save configuration
            config_path = MonitoringHandler.monitoring_data.get('config_path')
            if config_path:
                try:
                    save_config(server.config, config_path)
                except Exception as e:
                    # Remove API from list if save failed
                    server.config.apis.pop()
                    self.send_error(500, f"Failed to save config: {str(e)}")
                    return
            
            # Update monitoring data
            MonitoringHandler.monitoring_data['config']['apis_count'] = len(server.config.apis)
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response_data = {'success': True, 'message': 'API added successfully', 'api': {'name': name, 'url': url}}
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
        except ValueError as e:
            self.send_error(400, f"Validation error: {str(e)}")
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def handle_update_api(self, api_name: str):
        """Handles updating existing API."""
        from .loader import APIConfig, save_config
        data = self.read_json_body()
        if not data:
            self.send_error(400, "Invalid JSON")
            return
        
        server = MonitoringHandler.monitoring_data.get('server_instance')
        if not server:
            self.send_error(500, "Server instance not found")
            return
        
        # Find API
        api_index = None
        for i, api in enumerate(server.config.apis):
            if api.name == api_name:
                api_index = i
                break
        
        if api_index is None:
            self.send_error(404, f"API '{api_name}' not found")
            return
        
        # Update API
        updated_api = APIConfig(
            name=data.get('name', server.config.apis[api_index].name),
            url=data.get('url', server.config.apis[api_index].url),
            method=data.get('method', server.config.apis[api_index].method),
            timeout=float(data.get('timeout', server.config.apis[api_index].timeout)),
            expected_status=int(data.get('expected_status', server.config.apis[api_index].expected_status)),
            headers=data.get('headers', server.config.apis[api_index].headers)
        )
        
        server.config.apis[api_index] = updated_api
        
        # Save configuration
        config_path = MonitoringHandler.monitoring_data.get('config_path')
        if config_path:
            try:
                save_config(server.config, config_path)
            except Exception as e:
                self.send_error(500, f"Failed to save config: {str(e)}")
                return
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'success': True, 'message': 'API updated successfully'}, ensure_ascii=False).encode('utf-8'))
    
    def handle_delete_api(self, api_name: str):
        """Handles deleting API."""
        from .loader import save_config
        server = MonitoringHandler.monitoring_data.get('server_instance')
        if not server:
            self.send_error(500, "Server instance not found")
            return
        
        # Find and delete API
        api_index = None
        for i, api in enumerate(server.config.apis):
            if api.name == api_name:
                api_index = i
                break
        
        if api_index is None:
            self.send_error(404, f"API '{api_name}' not found")
            return
        
        if len(server.config.apis) <= 1:
            self.send_error(400, "Cannot delete the last API")
            return
        
        server.config.apis.pop(api_index)
        
        # Save configuration
        config_path = MonitoringHandler.monitoring_data.get('config_path')
        if config_path:
            try:
                save_config(server.config, config_path)
            except Exception as e:
                self.send_error(500, f"Failed to save config: {str(e)}")
                return
        
        # Update monitoring data
        MonitoringHandler.monitoring_data['config']['apis_count'] = len(server.config.apis)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'success': True, 'message': 'API deleted successfully'}, ensure_ascii=False).encode('utf-8'))
    
    def handle_refresh_monitoring(self):
        """Forces refresh of monitoring for all APIs."""
        from .checker import check_all_apis
        server = MonitoringHandler.monitoring_data.get('server_instance')
        if not server:
            self.send_error(500, "Server instance not found")
            return
        
        try:
            # Perform check for all APIs
            results = check_all_apis(server.config.apis)
            
            # Update data
            MonitoringHandler.monitoring_data['results'] = results
            MonitoringHandler.monitoring_data['history'].append({
                'timestamp': datetime.now().isoformat(),
                'results': [self.result_to_dict(r) for r in results]
            })
            
            # Update statistics
            stats = MonitoringHandler.monitoring_data['stats']
            stats['total_checks'] = stats.get('total_checks', 0) + 1
            stats['last_check'] = datetime.now().isoformat()
            successful = sum(1 for r in results if r.success)
            stats['successful_checks'] = stats.get('successful_checks', 0) + successful
            stats['failed_checks'] = stats.get('failed_checks', 0) + (len(results) - successful)
            
            # Limit history (last 100 checks)
            if len(MonitoringHandler.monitoring_data['history']) > 100:
                MonitoringHandler.monitoring_data['history'].pop(0)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response_data = {
                'success': True,
                'message': 'Monitoring refreshed',
                'results_count': len(results)
            }
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Failed to refresh monitoring: {str(e)}")
    
    def serve_openapi_spec(self):
        """Serves OpenAPI specification."""
        openapi_spec = {
            'openapi': '3.0.0',
            'info': {
                'title': 'API Health Monitor API',
                'version': '1.0.0',
                'description': 'REST API for monitoring API endpoint health',
                'contact': {
                    'name': 'API Support',
                    'url': 'https://github.com/maksim4351/api-health-monitor'
                }
            },
            'servers': [
                {
                    'url': 'http://localhost:8080',
                    'description': 'Local development server'
                }
            ],
            'paths': {
                '/api/data': {
                    'get': {
                        'summary': 'Get monitoring data',
                        'description': 'Returns current check results for all APIs',
                        'responses': {
                            '200': {
                                'description': 'Success response',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'object',
                                            'properties': {
                                                'results': {
                                                    'type': 'array',
                                                    'items': {
                                                        'type': 'object',
                                                        'properties': {
                                                            'name': {'type': 'string'},
                                                            'url': {'type': 'string'},
                                                            'status_code': {'type': 'integer', 'nullable': True},
                                                            'latency_ms': {'type': 'number'},
                                                            'success': {'type': 'boolean'},
                                                            'error': {'type': 'string', 'nullable': True}
                                                        }
                                                    }
                                                },
                                                'stats': {'type': 'object'},
                                                'timestamp': {'type': 'string', 'format': 'date-time'}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                '/api/stats': {
                    'get': {
                        'summary': 'Get statistics',
                        'description': 'Returns overall monitoring statistics',
                        'responses': {
                            '200': {
                                'description': 'Success response',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'object',
                                            'properties': {
                                                'total_checks': {'type': 'integer'},
                                                'successful_checks': {'type': 'integer'},
                                                'failed_checks': {'type': 'integer'},
                                                'last_check': {'type': 'string', 'format': 'date-time'},
                                                'start_time': {'type': 'string', 'format': 'date-time'}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                '/api/apis': {
                    'get': {
                        'summary': 'Get API list',
                        'description': 'Returns list of all configured APIs',
                        'responses': {
                            '200': {
                                'description': 'Success response',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'name': {'type': 'string'},
                                                    'url': {'type': 'string'},
                                                    'method': {'type': 'string'},
                                                    'timeout': {'type': 'number'},
                                                    'expected_status': {'type': 'integer'},
                                                    'headers': {'type': 'object'}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'post': {
                        'summary': 'Add new API',
                        'description': 'Adds new API to monitoring',
                        'requestBody': {
                            'required': True,
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'required': ['name', 'url'],
                                        'properties': {
                                            'name': {'type': 'string', 'description': 'API name'},
                                            'url': {'type': 'string', 'format': 'uri', 'description': 'API URL'},
                                            'method': {'type': 'string', 'enum': ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'], 'default': 'GET'},
                                            'timeout': {'type': 'number', 'default': 5.0, 'description': 'Timeout in seconds'},
                                            'expected_status': {'type': 'integer', 'default': 200, 'minimum': 100, 'maximum': 599},
                                            'headers': {'type': 'object', 'description': 'HTTP headers'}
                                        }
                                    }
                                }
                            }
                        },
                        'responses': {
                            '201': {
                                'description': 'API successfully added',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'object',
                                            'properties': {
                                                'success': {'type': 'boolean'},
                                                'message': {'type': 'string'}
                                            }
                                        }
                                    }
                                }
                            },
                            '400': {'description': 'Bad request'},
                            '409': {'description': 'API already exists'},
                            '500': {'description': 'Server error'}
                        }
                    }
                },
                '/api/apis/{{name}}': {
                    'put': {
                        'summary': 'Update API',
                        'description': 'Updates existing API',
                        'parameters': [
                            {
                                'name': 'name',
                                'in': 'path',
                                'required': True,
                                'schema': {'type': 'string'},
                                'description': 'API name to update'
                            }
                        ],
                        'requestBody': {
                            'required': True,
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {
                                            'name': {'type': 'string'},
                                            'url': {'type': 'string', 'format': 'uri'},
                                            'method': {'type': 'string'},
                                            'timeout': {'type': 'number'},
                                            'expected_status': {'type': 'integer'},
                                            'headers': {'type': 'object'}
                                        }
                                    }
                                }
                            }
                        },
                        'responses': {
                            '200': {'description': 'API successfully updated'},
                            '404': {'description': 'API not found'},
                            '500': {'description': 'Server error'}
                        }
                    },
                    'delete': {
                        'summary': 'Delete API',
                        'description': 'Removes API from monitoring',
                        'parameters': [
                            {
                                'name': 'name',
                                'in': 'path',
                                'required': True,
                                'schema': {'type': 'string'},
                                'description': 'API name to delete'
                            }
                        ],
                        'responses': {
                            '200': {'description': 'API successfully deleted'},
                            '404': {'description': 'API not found'},
                            '400': {'description': 'Cannot delete last API'},
                            '500': {'description': 'Server error'}
                        }
                    }
                },
                '/api/refresh': {
                    'get': {
                        'summary': 'Refresh monitoring',
                        'description': 'Forces refresh of monitoring results for all APIs',
                        'responses': {
                            '200': {
                                'description': 'Monitoring refreshed',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'object',
                                            'properties': {
                                                'success': {'type': 'boolean'},
                                                'message': {'type': 'string'},
                                                'results_count': {'type': 'integer'}
                                            }
                                        }
                                    }
                                }
                            },
                            '500': {'description': 'Server error'}
                        }
                    }
                },
                '/api/popular': {
                    'get': {
                        'summary': 'Get popular APIs',
                        'description': 'Returns list of popular APIs for quick addition',
                        'responses': {
                            '200': {
                                'description': 'Success response',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'name': {'type': 'string'},
                                                    'url': {'type': 'string'},
                                                    'method': {'type': 'string'},
                                                    'timeout': {'type': 'number'},
                                                    'expected_status': {'type': 'integer'}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(openapi_spec, ensure_ascii=False, indent=2).encode('utf-8'))
    
    def serve_swagger_ui(self):
        """Serves Swagger UI for interactive documentation."""
        swagger_ui_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Health Monitor - API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css" />
    <style>
        body {{
            margin: 0;
            background: #fafafa;
        }}
        .swagger-ui .topbar {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {{
            const ui = SwaggerUIBundle({{
                url: '/api/openapi.json',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout",
                validatorUrl: null
            }});
        }};
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(swagger_ui_html.encode('utf-8'))
    
    def get_dashboard_html(self):
        """Generates HTML dashboard."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Health Monitor - Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .header h1 {{
            font-size: 2.5em;
            color: #667eea;
            margin-bottom: 10px;
        }}
        .header .subtitle {{
            color: #666;
            font-size: 1.1em;
        }}
        .tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .tab {{
            background: white;
            padding: 15px 30px;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .tab.active {{
            background: #667eea;
            color: white;
        }}
        .tab:hover {{
            transform: translateY(-2px);
        }}
        .tab-content {{
            display: none;
            background: white;
            border-radius: 0 10px 10px 10px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            min-height: 500px;
        }}
        .tab-content.active {{
            display: block;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            opacity: 0.9;
            font-size: 0.9em;
        }}
        .status-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        .status-ok {{ background: #28a745; }}
        .status-fail {{ background: #dc3545; }}
        .status-timeout {{ background: #ffc107; }}
        .api-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        .api-table th {{
            background: #f8f9fa;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #dee2e6;
        }}
        .api-table td {{
            padding: 15px;
            border-bottom: 1px solid #dee2e6;
        }}
        .api-table tr:hover {{
            background: #f8f9fa;
        }}
        .badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .badge-success {{
            background: #d4edda;
            color: #155724;
        }}
        .badge-danger {{
            background: #f8d7da;
            color: #721c24;
        }}
        .badge-warning {{
            background: #fff3cd;
            color: #856404;
        }}
        .alert {{
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }}
        .alert-error {{
            background: #f8d7da;
            color: #721c24;
            border-left: 4px solid #dc3545;
        }}
        .alert-success {{
            background: #d4edda;
            color: #155724;
            border-left: 4px solid #28a745;
        }}
        .alert-info {{
            background: #d1ecf1;
            color: #0c5460;
            border-left: 4px solid #17a2b8;
        }}
        .project-info {{
            line-height: 1.8;
        }}
        .project-info h2 {{
            color: #667eea;
            margin: 20px 0 10px 0;
        }}
        .project-info ul {{
            margin-left: 20px;
        }}
        .project-info li {{
            margin: 5px 0;
        }}
        .refresh-indicator {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #28a745;
            margin-left: 10px;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        @keyframes slideIn {{
            from {{
                transform: translateY(-20px);
                opacity: 0;
            }}
            to {{
                transform: translateY(0);
                opacity: 1;
            }}
        }}
        @keyframes slideOut {{
            from {{
                transform: translateY(0);
                opacity: 1;
            }}
            to {{
                transform: translateY(-20px);
                opacity: 0;
            }}
        }}
        .last-update {{
            color: #666;
            font-size: 0.9em;
            margin-top: 20px;
            text-align: center;
        }}
        .manage-container {{
            max-width: 1200px;
        }}
        .manage-section {{
            margin-bottom: 40px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        .manage-section h3 {{
            color: #667eea;
            margin-bottom: 15px;
        }}
        .api-form {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}
        .form-group {{
            display: flex;
            flex-direction: column;
        }}
        .form-group label {{
            font-weight: 600;
            margin-bottom: 5px;
            color: #333;
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .info-icon {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #17a2b8;
            color: white;
            font-size: 12px;
            font-weight: bold;
            cursor: help;
            position: relative;
            flex-shrink: 0;
        }}
        .info-icon:hover {{
            background: #138496;
        }}
        .info-icon[data-tooltip] {{
            position: relative;
        }}
        .info-icon[data-tooltip]:hover::after {{
            content: attr(data-tooltip);
            position: absolute;
            left: 25px;
            top: 50%;
            transform: translateY(-50%);
            background: #333;
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: normal;
            white-space: normal;
            width: 350px;
            max-width: 90vw;
            z-index: 10000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            line-height: 1.6;
            pointer-events: none;
            word-wrap: break-word;
        }}
        .info-icon[data-tooltip]:hover::before {{
            content: '';
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            border: 6px solid transparent;
            border-right-color: #333;
            z-index: 10001;
            pointer-events: none;
        }}
        /* For mobile devices - tooltip at bottom */
        @media (max-width: 768px) {{
            .info-icon[data-tooltip]:hover::after {{
                left: 50%;
                top: auto;
                bottom: 25px;
                transform: translateX(-50%);
                width: 300px;
            }}
            .info-icon[data-tooltip]:hover::before {{
                left: 50%;
                top: auto;
                bottom: 19px;
                transform: translateX(-50%);
                border-right-color: transparent;
                border-top-color: #333;
            }}
        }}
        .form-group input,
        .form-group select {{
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
        }}
        .form-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 5px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        .btn-primary:hover {{
            transform: translateY(-2px);
        }}
        .btn-danger {{
            background: #dc3545;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
        }}
        .btn-edit {{
            background: #ffc107;
            color: #333;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
            margin-right: 5px;
        }}
        .popular-apis-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .popular-api-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 2px solid #667eea;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .popular-api-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}
        .popular-api-card h4 {{
            color: #667eea;
            margin-bottom: 8px;
        }}
        .popular-api-card .url {{
            color: #666;
            font-size: 0.9em;
            word-break: break-all;
        }}
        .current-apis-list {{
            margin-top: 15px;
        }}
        .api-item {{
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .api-item-info {{
            flex: 1;
        }}
        .api-item-info h4 {{
            color: #667eea;
            margin-bottom: 5px;
        }}
        .api-item-info .url {{
            color: #666;
            font-size: 0.9em;
            word-break: break-all;
        }}
        .api-item-info .details {{
            margin-top: 8px;
            font-size: 0.85em;
            color: #999;
        }}
        .api-item-actions {{
            display: flex;
            gap: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 API Health Monitor Dashboard</h1>
            <div class="subtitle">Real-time API Monitoring</div>
            <div class="last-update">
                Last update: <span id="lastUpdate">loading...</span>
                <span class="refresh-indicator"></span>
            </div>
        </div>
        
        <div class="tabs">
            <div class="tab active" onclick="showTab('monitoring')">📊 Monitoring</div>
            <div class="tab" onclick="showTab('manage')">⚙️ API Management</div>
            <div class="tab" onclick="showTab('project')">📖 About</div>
            <div class="tab" onclick="showTab('stats')">📈 Statistics</div>
            <div class="tab" onclick="window.open('/api/docs', '_blank')">📚 API Docs</div>
        </div>
        
        <div id="alertContainer"></div>
        
        <div id="monitoring" class="tab-content active">
            <div class="stats-grid" id="statsGrid">
                <div class="stat-card">
                    <div class="stat-value" id="totalApis">-</div>
                    <div class="stat-label">Total APIs</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="successfulApis">-</div>
                    <div class="stat-label">Successful</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="failedApis">-</div>
                    <div class="stat-label">Failed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="successRate">-</div>
                    <div class="stat-label">Success Rate</div>
                </div>
            </div>
            
            <table class="api-table" id="apiTable">
                <thead>
                    <tr>
                        <th>Status</th>
                        <th>API</th>
                        <th>URL</th>
                        <th>HTTP Code</th>
                        <th>Latency</th>
                        <th>Result</th>
                    </tr>
                </thead>
                <tbody id="apiTableBody">
                    <tr>
                        <td colspan="6" style="text-align: center; padding: 40px;">
                            Loading data...
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div id="project" class="tab-content">
            <div class="project-info" id="projectInfo">
                <h2>About Project</h2>
                <p>Loading information...</p>
            </div>
        </div>
        
        <div id="stats" class="tab-content">
            <div class="project-info" id="statsInfo">
                <h2>Monitoring Statistics</h2>
                <p>Loading statistics...</p>
            </div>
        </div>
        
        <div id="manage" class="tab-content">
            <div class="manage-container">
                <h2>⚙️ API Management</h2>
                
                <div class="manage-section">
                    <h3>➕ Add New API</h3>
                    <form id="addApiForm" class="api-form">
                        <div class="form-group">
                            <label>API Name:</label>
                            <input type="text" id="apiName" required placeholder="e.g., Google">
                        </div>
                        <div class="form-group">
                            <label>URL:</label>
                            <input type="url" id="apiUrl" required placeholder="https://api.example.com">
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label>
                                    Method:
                                    <span class="info-icon" data-tooltip="<strong>HTTP Methods:</strong><br><br><strong>GET</strong> - Get data (read)<br><strong>POST</strong> - Create new resource<br><strong>PUT</strong> - Update existing resource<br><strong>DELETE</strong> - Delete resource<br><strong>PATCH</strong> - Partial resource update">ℹ️</span>
                                </label>
                                <select id="apiMethod">
                                    <option value="GET">GET</option>
                                    <option value="POST">POST</option>
                                    <option value="PUT">PUT</option>
                                    <option value="DELETE">DELETE</option>
                                    <option value="PATCH">PATCH</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>
                                    Timeout (sec):
                                    <span class="info-icon" data-tooltip="<strong>Timeout</strong> - maximum time to wait for API response in seconds.<br><br>If API doesn't respond within this time, request will be aborted and counted as error.<br><br>Recommended: 5-10 seconds for normal APIs, 30+ seconds for slow APIs.">ℹ️</span>
                                </label>
                                <input type="number" id="apiTimeout" value="5.0" min="0.1" step="0.1">
                            </div>
                            <div class="form-group">
                                <label>
                                    Expected Status:
                                    <span class="info-icon" data-tooltip="<strong>Expected HTTP Status</strong> - response code that is considered successful.<br><br><strong>200</strong> - OK (successful request)<br><strong>201</strong> - Created (resource created)<br><strong>204</strong> - No Content (successful but no content)<br><strong>301/302</strong> - Redirect<br><strong>400-499</strong> - Client error<br><strong>500-599</strong> - Server error<br><br>If API returns different status, check will be considered failed.">ℹ️</span>
                                </label>
                                <input type="number" id="apiStatus" value="200" min="100" max="599">
                            </div>
                        </div>
                        <button type="submit" class="btn-primary">Add API</button>
                    </form>
                </div>
                
                <div class="manage-section">
                    <h3>⭐ Popular APIs</h3>
                    <p>Click on API to quickly add it to monitoring:</p>
                    <div id="popularApis" class="popular-apis-grid">
                        <p>Loading popular APIs...</p>
                    </div>
                </div>
                
                <div class="manage-section">
                    <h3>📋 Current APIs</h3>
                    <div id="currentApis" class="current-apis-list">
                        <p>Loading API list...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let lastResults = [];
        let errorNotifications = new Set();
        
        function showTab(tabName) {{
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            document.querySelectorAll('.tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            // Load data for tab
            if (tabName === 'project') {{
                loadProjectInfo();
            }} else if (tabName === 'stats') {{
                loadStats();
            }}
        }}
        
        function loadMonitoringData() {{
            fetch('/api/data')
                .then(response => response.json())
                .then(data => {{
                    updateDashboard(data);
                    checkForErrors(data.results);
                    document.getElementById('lastUpdate').textContent = new Date().toLocaleString('en-US');
                }})
                .catch(error => {{
                    console.error('Error loading data:', error);
                }});
        }}
        
        function updateDashboard(data) {{
            const results = data.results || [];
            lastResults = results;
            
            // Update statistics
            const total = results.length;
            const successful = results.filter(r => r.success).length;
            const failed = total - successful;
            const successRate = total > 0 ? ((successful / total) * 100).toFixed(1) : 0;
            
            document.getElementById('totalApis').textContent = total;
            document.getElementById('successfulApis').textContent = successful;
            document.getElementById('failedApis').textContent = failed;
            document.getElementById('successRate').textContent = successRate + '%';
            
            // Update table
            const tbody = document.getElementById('apiTableBody');
            if (results.length === 0) {{
                tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 40px;">No data to display</td></tr>';
                return;
            }}
            
            tbody.innerHTML = results.map(result => {{
                const statusClass = result.timeout ? 'status-timeout' : 
                                   result.success ? 'status-ok' : 'status-fail';
                const badgeClass = result.timeout ? 'badge-warning' :
                                  result.success ? 'badge-success' : 'badge-danger';
                const statusText = result.timeout ? 'TIMEOUT' :
                                  result.success ? 'OK' : 'FAIL';
                const statusCode = result.status_code || 'N/A';
                const latency = result.latency_ms ? result.latency_ms.toFixed(2) + ' ms' : 'N/A';
                
                return `
                    <tr>
                        <td><span class="status-indicator ${{statusClass}}"></span></td>
                        <td><strong>${{result.name}}</strong></td>
                        <td><a href="${{result.url}}" target="_blank" style="color: #667eea;">${{result.url}}</a></td>
                        <td>${{statusCode}}</td>
                        <td>${{latency}}</td>
                        <td><span class="badge ${{badgeClass}}">${{statusText}}</span></td>
                    </tr>
                `;
            }}).join('');
        }}
        
        function checkForErrors(results) {{
            const container = document.getElementById('alertContainer');
            const hasErrors = results.some(r => !r.success);
            
            if (hasErrors) {{
                const failedApis = results.filter(r => !r.success);
                const errorMsg = failedApis.map(r => `${{r.name}}: ${{r.error || 'Error'}}`).join('<br>');
                
                if (!errorNotifications.has(errorMsg)) {{
                    errorNotifications.add(errorMsg);
                    container.innerHTML = `
                        <div class="alert alert-error">
                            <strong>⚠️ Errors Detected!</strong><br>
                            ${{errorMsg}}
                        </div>
                    `;
                    
                    // Sound notification (if supported)
                    if ('Notification' in window && Notification.permission === 'granted') {{
                        new Notification('API Health Monitor', {{
                            body: 'Errors detected in APIs',
                            icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="red"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>'
                        }});
                    }}
                }}
            }} else {{
                container.innerHTML = `
                    <div class="alert alert-success">
                        <strong>✅ All APIs working normally</strong>
                    </div>
                `;
            }}
        }}
        
        function loadProjectInfo() {{
            fetch('/api/project')
                .then(response => response.json())
                .then(data => {{
                    document.getElementById('projectInfo').innerHTML = `
                        <h2>${{data.name}}</h2>
                        <p><strong>Version:</strong> ${{data.version}}</p>
                        <p><strong>Description:</strong> ${{data.description}}</p>
                        
                        <h2>Features</h2>
                        <ul>
                            ${{data.features.map(f => `<li>${{f}}</li>`).join('')}}
                        </ul>
                        
                        <h2>Technologies</h2>
                        <ul>
                            ${{data.tech_stack.map(t => `<li>${{t}}</li>`).join('')}}
                        </ul>
                        
                        <h2>Repository</h2>
                        <p><a href="${{data.repository}}" target="_blank">${{data.repository}}</a></p>
                    `;
                }})
                .catch(error => {{
                    console.error('Error loading project information:', error);
                }});
        }}
        
        function loadStats() {{
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {{
                    const uptime = new Date() - new Date(data.start_time);
                    const hours = Math.floor(uptime / 3600000);
                    const minutes = Math.floor((uptime % 3600000) / 60000);
                    
                    document.getElementById('statsInfo').innerHTML = `
                        <h2>Monitoring Statistics</h2>
                        <p><strong>Total checks:</strong> ${{data.total_checks}}</p>
                        <p><strong>Successful checks:</strong> ${{data.successful_checks}}</p>
                        <p><strong>Failed checks:</strong> ${{data.failed_checks}}</p>
                        <p><strong>Last check:</strong> ${{data.last_check || 'No data'}}</p>
                        <p><strong>Uptime:</strong> ${{hours}}h ${{minutes}}m</p>
                        <p><strong>Monitoring started:</strong> ${{new Date(data.start_time).toLocaleString('en-US')}}</p>
                    `;
                }})
                .catch(error => {{
                    console.error('Error loading statistics:', error);
                }});
        }}
        
        function showAlert(message, type = 'info') {{
            const alertContainer = document.getElementById('alertContainer');
            if (!alertContainer) {{
                console.error('Alert container not found');
                alert(message); // Fallback
                return;
            }}
            
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${{type}}`;
            
            // Make errors more noticeable
            if (type === 'error') {{
                alertDiv.style.cssText = `
                    padding: 20px 25px;
                    margin-bottom: 15px;
                    border-radius: 5px;
                    animation: slideIn 0.3s ease-out;
                    position: relative;
                    font-size: 1.1em;
                    font-weight: 600;
                    box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
                    z-index: 1000;
                `;
            }} else {{
                alertDiv.style.cssText = `
                    padding: 15px 20px;
                    margin-bottom: 15px;
                    border-radius: 5px;
                    animation: slideIn 0.3s ease-out;
                    position: relative;
                `;
            }}
            
            // Support HTML in message
            if (message.includes('<')) {{
                alertDiv.innerHTML = message;
            }} else {{
                alertDiv.textContent = message;
            }}
            
            // Add close button
            const closeBtn = document.createElement('button');
            closeBtn.textContent = '×';
            closeBtn.style.cssText = `
                position: absolute;
                right: 10px;
                top: 50%;
                transform: translateY(-50%);
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
                color: inherit;
                opacity: 0.7;
                font-weight: bold;
            `;
            closeBtn.onclick = () => alertDiv.remove();
            alertDiv.appendChild(closeBtn);
            
            // Scroll to notification
            alertContainer.appendChild(alertDiv);
            alertDiv.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
            
            // For errors - longer display time
            const timeout = type === 'error' ? 8000 : 5000;
            
            // Auto-remove
            setTimeout(() => {{
                if (alertDiv.parentNode) {{
                    alertDiv.style.animation = 'slideOut 0.3s ease-out';
                    setTimeout(() => alertDiv.remove(), 300);
                }}
            }}, timeout);
        }}
        
        // Request notification permission
        if ('Notification' in window && Notification.permission === 'default') {{
            Notification.requestPermission();
        }}
        
        // API management functions
        async function loadPopularApis() {{
            try {{
                const response = await fetch('/api/popular');
                const apis = await response.json();
                const container = document.getElementById('popularApis');
                container.innerHTML = '';
                apis.forEach(api => {{
                    const card = document.createElement('div');
                    card.className = 'popular-api-card';
                    card.onclick = () => addPopularApi(api);
                    card.innerHTML = `
                        <h4>${{api.name}}</h4>
                        <div class="url">${{api.url}}</div>
                    `;
                    container.appendChild(card);
                }});
            }} catch (error) {{
                console.error('Error loading popular APIs:', error);
            }}
        }}
        
        function addPopularApi(api) {{
            document.getElementById('apiName').value = api.name;
            document.getElementById('apiUrl').value = api.url;
            document.getElementById('apiMethod').value = api.method;
            document.getElementById('apiTimeout').value = api.timeout;
            document.getElementById('apiStatus').value = api.expected_status;
            showAlert('API added to form. Click "Add API" to save.', 'success');
        }}
        
        async function loadCurrentApis() {{
            try {{
                const response = await fetch('/api/apis');
                const apis = await response.json();
                const container = document.getElementById('currentApis');
                container.innerHTML = '';
                if (apis.length === 0) {{
                    container.innerHTML = '<p>No APIs added</p>';
                    return;
                }}
                apis.forEach(api => {{
                    const item = document.createElement('div');
                    item.className = 'api-item';
                    item.innerHTML = `
                        <div class="api-item-info">
                            <h4>${{api.name}}</h4>
                            <div class="url">${{api.url}}</div>
                            <div class="details">
                                Method: ${{api.method}} | Timeout: ${{api.timeout}}s | Status: ${{api.expected_status}}
                            </div>
                        </div>
                        <div class="api-item-actions">
                            <button class="btn-edit" onclick="editApi('${{api.name}}')">✏️ Edit</button>
                            <button class="btn-danger" onclick="deleteApi('${{api.name}}')">🗑️ Delete</button>
                        </div>
                    `;
                    container.appendChild(item);
                }});
            }} catch (error) {{
                console.error('Error loading current APIs:', error);
                document.getElementById('currentApis').innerHTML = '<p style="color: red;">Error loading API list</p>';
            }}
        }}
        
        async function deleteApi(apiName) {{
            if (!confirm(`Are you sure you want to delete API "${{apiName}}"?`)) {{
                return;
            }}
            try {{
                const response = await fetch(`/api/apis/${{encodeURIComponent(apiName)}}`, {{
                    method: 'DELETE'
                }});
                if (response.ok) {{
                    showAlert('API successfully deleted', 'success');
                    loadCurrentApis();
                    // Reload monitoring data
                    setTimeout(loadMonitoringData, 1000);
                }} else {{
                    const error = await response.text();
                    showAlert(`Deletion error: ${{error}}`, 'error');
                }}
            }} catch (error) {{
                showAlert(`Error: ${{error.message}}`, 'error');
            }}
        }}
        
        function editApi(apiName) {{
            // Load API data and fill form
            fetch('/api/apis')
                .then(response => response.json())
                .then(apis => {{
                    const api = apis.find(a => a.name === apiName);
                    if (api) {{
                        document.getElementById('apiName').value = api.name;
                        document.getElementById('apiUrl').value = api.url;
                        document.getElementById('apiMethod').value = api.method;
                        document.getElementById('apiTimeout').value = api.timeout;
                        document.getElementById('apiStatus').value = api.expected_status;
                        // Change form to edit mode
                        const form = document.getElementById('addApiForm');
                        const submitBtn = form.querySelector('button[type="submit"]');
                        submitBtn.textContent = 'Update API';
                        submitBtn.onclick = (e) => {{
                            e.preventDefault();
                            updateApi(apiName);
                        }};
                        showAlert('API data loaded into form. Modify and click "Update API"', 'success');
                    }}
                }})
                .catch(error => {{
                    showAlert(`Error loading data: ${{error.message}}`, 'error');
                }});
        }}
        
        async function updateApi(oldName) {{
            const form = document.getElementById('addApiForm');
            const data = {{
                name: document.getElementById('apiName').value,
                url: document.getElementById('apiUrl').value,
                method: document.getElementById('apiMethod').value,
                timeout: parseFloat(document.getElementById('apiTimeout').value),
                expected_status: parseInt(document.getElementById('apiStatus').value)
            }};
            try {{
                const response = await fetch(`/api/apis/${{encodeURIComponent(oldName)}}`, {{
                    method: 'PUT',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(data)
                }});
                if (response.ok) {{
                    showAlert('API successfully updated', 'success');
                    form.reset();
                    const submitBtn = form.querySelector('button[type="submit"]');
                    submitBtn.textContent = 'Add API';
                    submitBtn.onclick = null;
                    loadCurrentApis();
                    setTimeout(loadMonitoringData, 1000);
                }} else {{
                    const error = await response.text();
                    showAlert(`Update error: ${{error}}`, 'error');
                }}
            }} catch (error) {{
                showAlert(`Error: ${{error.message}}`, 'error');
            }}
        }}
        
        // Handle add API form
        const addApiForm = document.getElementById('addApiForm');
        if (addApiForm) {{
            addApiForm.addEventListener('submit', async (e) => {{
                e.preventDefault();
                e.stopPropagation();
                
                const nameInput = document.getElementById('apiName');
                const urlInput = document.getElementById('apiUrl');
                const methodInput = document.getElementById('apiMethod');
                const timeoutInput = document.getElementById('apiTimeout');
                const statusInput = document.getElementById('apiStatus');
                
                if (!nameInput || !urlInput || !methodInput || !timeoutInput || !statusInput) {{
                    showAlert('Error: Not all form fields found', 'error');
                    console.error('Form fields not found');
                    return;
                }}
                
                const data = {{
                    name: nameInput.value.trim(),
                    url: urlInput.value.trim(),
                    method: methodInput.value,
                    timeout: parseFloat(timeoutInput.value) || 5.0,
                    expected_status: parseInt(statusInput.value) || 200
                }};
                
                // Validation
                if (!data.name || !data.url) {{
                    showAlert('Error: Fill in name and URL', 'error');
                    return;
                }}
                
                if (data.timeout <= 0) {{
                    showAlert('Error: Timeout must be a positive number', 'error');
                    return;
                }}
                
                if (data.expected_status < 100 || data.expected_status >= 600) {{
                    showAlert('Error: HTTP status must be in range 100-599', 'error');
                    return;
                }}
                
                // Show loading indicator
                const submitBtn = addApiForm.querySelector('button[type="submit"]');
                const originalText = submitBtn.textContent;
                submitBtn.disabled = true;
                submitBtn.textContent = '⏳ Adding...';
                
                // Show process notification
                showAlert('⏳ Adding API...', 'info');
                
                try {{
                    console.log('Sending request:', data);
                    const response = await fetch('/api/apis', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify(data)
                    }});
                    
                    console.log('Server response:', response.status, response.statusText);
                    
                    if (response.ok) {{
                        const result = await response.json();
                        showAlert('✅ API successfully added! Updating monitoring...', 'success');
                        
                        // Immediately update monitoring
                        try {{
                            const refreshResponse = await fetch('/api/refresh');
                            if (refreshResponse.ok) {{
                                showAlert('✅ API added and monitoring updated!', 'success');
                                loadMonitoringData(); // Update data on page
                            }} else {{
                                showAlert('⚠️ API added, but monitoring will update automatically in a few seconds', 'info');
                            }}
                        }} catch (refreshError) {{
                            console.error('Error updating monitoring:', refreshError);
                            showAlert('✅ API added! Monitoring will update automatically', 'success');
                        }}
                        
                        addApiForm.reset();
                        loadCurrentApis();
                    }} else {{
                        // Read response as text first
                        const responseText = await response.text();
                        console.log('Server response (text):', responseText);
                        console.log('Response status:', response.status);
                        
                        let errorData = null;
                        try {{
                            // Try to parse as JSON
                            errorData = JSON.parse(responseText);
                            console.log('Parsed JSON:', errorData);
                        }} catch (e) {{
                            // If not JSON, create object with text
                            console.log('Not JSON, using text:', responseText);
                            errorData = {{ message: responseText }};
                        }}
                        
                        console.error('Server error:', response.status, errorData);
                        
                        // Special handling for duplicates
                        if (response.status === 409) {{
                            let duplicateMessage = '';
                            
                            if (errorData) {{
                                console.log('errorData.error:', errorData.error);
                                console.log('errorData.message:', errorData.message);
                                
                                if (errorData.error === 'duplicate') {{
                                    duplicateMessage = `⚠️ API with name "${{data.name}}" already added!`;
                                }} else if (errorData.error === 'duplicate_url') {{
                                    duplicateMessage = `⚠️ API with URL "${{data.url}}" already added!`;
                                }} else if (errorData.message) {{
                                    duplicateMessage = `⚠️ ${{errorData.message}}`;
                                }} else {{
                                    duplicateMessage = `⚠️ This API already exists in the list!`;
                                }}
                            }} else {{
                                duplicateMessage = `⚠️ API "${{data.name}}" already added!`;
                            }}
                            
                            console.log('Showing message:', duplicateMessage);
                            
                            // Show noticeable notification
                            showAlert(duplicateMessage, 'error');
                            
                            // Additionally show browser notification for guarantee
                            if ('Notification' in window) {{
                                if (Notification.permission === 'granted') {{
                                    new Notification('API Health Monitor', {{
                                        body: duplicateMessage,
                                        icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="orange"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>',
                                        tag: 'duplicate-api'
                                    }});
                                }} else if (Notification.permission === 'default') {{
                                    Notification.requestPermission().then(permission => {{
                                        if (permission === 'granted') {{
                                            new Notification('API Health Monitor', {{
                                                body: duplicateMessage,
                                                icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="orange"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>',
                                                tag: 'duplicate-api'
                                            }});
                                        }}
                                    }});
                                }}
                            }}
                            
                            // Scroll to notification
                            setTimeout(() => {{
                                const alertContainer = document.getElementById('alertContainer');
                                if (alertContainer) {{
                                    alertContainer.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                                }}
                            }}, 100);
                        }} else {{
                            showAlert(`❌ Addition error: ${{errorData?.message || responseText || 'Unknown error'}}`, 'error');
                        }}
                    }}
                }} catch (error) {{
                    console.error('Request error:', error);
                    showAlert(`❌ Error: ${{error.message}}`, 'error');
                }} finally {{
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                }}
            }});
        }} else {{
            console.error('Form addApiForm not found');
        }}
        
        // Load data on page load
        loadMonitoringData();
        loadProjectInfo();
        
        // Load API management data when opening tab
        let manageTabLoaded = false;
        const originalShowTab = showTab;
        showTab = function(tabName) {{
            originalShowTab(tabName);
            if (tabName === 'manage' && !manageTabLoaded) {{
                loadPopularApis();
                loadCurrentApis();
                manageTabLoaded = true;
            }}
        }};
        
        // Auto-update every 5 seconds
        setInterval(loadMonitoringData, 5000);
    </script>
</body>
</html>
"""
    
    def log_message(self, format, *args):
        """Disables HTTP request logging."""
        pass


class WebMonitoringServer:
    """Web server for API monitoring."""
    
    def __init__(self, config: Config, port: int = 8080, interval: int = 60, config_path: str = None):
        """
        Initializes web server.
        
        Args:
            config: Monitoring configuration
            port: Port for web server
            interval: API check interval in seconds
            config_path: Path to configuration file for saving changes
        """
        self.config = config
        self.port = port
        self.interval = interval
        self.config_path = config_path
        self.server = None
        self.running = False
        
        # Initialize monitoring data
        MonitoringHandler.monitoring_data['config'] = {
            'apis_count': len(config.apis),
            'interval': interval
        }
        MonitoringHandler.monitoring_data['config_path'] = config_path
        MonitoringHandler.monitoring_data['server_instance'] = self
    
    def start(self):
        """Starts web server and monitoring."""
        import webbrowser
        from .checker import check_all_apis
        
        # Event for server startup synchronization
        server_ready = threading.Event()
        actual_port = [self.port]  # Use list for modification from another thread
        
        def run_server():
            """Starts HTTP server."""
            # Try to use specified port
            current_port = self.port
            max_attempts = 50
            
            for attempt in range(max_attempts):
                try:
                    server_address = ('', current_port)
                    self.server = HTTPServer(server_address, MonitoringHandler)
                    actual_port[0] = current_port  # Save actual port
                    self.port = current_port  # Update port
                    self.running = True
                    print(f"🌐 Web server started: http://localhost:{self.port}")
                    print("📊 Open in browser to view dashboard")
                    server_ready.set()  # Signal that server is ready
                    self.server.serve_forever()
                    break
                except PermissionError:
                    if attempt == 0:
                        print(f"⚠️  Port {current_port} is busy, searching for free port...")
                    # Try to find free port
                    try:
                        current_port = find_free_port(current_port + 1)
                        if attempt == 0:
                            print(f"✅ Found free port: {current_port}")
                    except OSError:
                        print(f"❌ Error: Failed to find free port")
                        print("   Try:")
                        print("   1. Close other programs using ports")
                        print("   2. Specify different port: --port 9000")
                        print("   3. Run as administrator")
                        server_ready.set()  # Unblock even on error
                        raise
                except OSError as e:
                    if attempt == 0:
                        print(f"⚠️  Error starting on port {current_port}: {e}")
                        print(f"   Trying to find free port...")
                    try:
                        current_port = find_free_port(current_port + 1)
                        if attempt == 0:
                            print(f"✅ Found free port: {current_port}")
                    except OSError:
                        print(f"❌ Error: Failed to find free port")
                        server_ready.set()  # Unblock even on error
                        raise
                except Exception as e:
                    print(f"❌ Critical error starting server: {e}")
                    server_ready.set()  # Unblock even on error
                    raise
        
        def run_monitoring():
            """Starts periodic monitoring."""
            from .notifier import create_notifier_from_config
            notifier = create_notifier_from_config(self.config.notifications) if self.config.notifications else None
            
            # Initialize cache
            cache_ttl = self.interval if self.interval else 60.0
            cache = ResultCache(default_ttl=cache_ttl)
            
            check_count = 0
            while self.running:
                try:
                    # Use cache and async requests for optimization
                    use_async = len(self.config.apis) > 5
                    results = check_all_apis(self.config.apis, cache=cache, use_async=use_async)
                    check_count += 1
                    
                    # Cleanup expired cache entries
                    cache.cleanup_expired()
                    
                    # Send notifications
                    if notifier:
                        notifier.notify(results)
                    
                    # Push notifications for web interface
                    failed_apis = [r for r in results if not r.success]
                    if failed_apis and notifier and notifier.config.push_enabled:
                        # Save data for push notifications
                        MonitoringHandler.monitoring_data['pending_push'] = {
                            'failed_apis': [{'name': r.name, 'error': r.error} for r in failed_apis],
                            'timestamp': datetime.now().isoformat()
                        }
                    
                    # Update data
                    MonitoringHandler.monitoring_data['results'] = results
                    MonitoringHandler.monitoring_data['history'].append({
                        'timestamp': datetime.now().isoformat(),
                        'results': [self._result_to_dict(r) for r in results]
                    })
                    
                    # Update statistics
                    stats = MonitoringHandler.monitoring_data['stats']
                    stats['total_checks'] = check_count
                    stats['last_check'] = datetime.now().isoformat()
                    successful = sum(1 for r in results if r.success)
                    stats['successful_checks'] += successful
                    stats['failed_checks'] += len(results) - successful
                    
                    # Limit history (last 100 checks)
                    if len(MonitoringHandler.monitoring_data['history']) > 100:
                        MonitoringHandler.monitoring_data['history'].pop(0)
                    
                    time.sleep(self.interval)
                except Exception as e:
                    print(f"Monitoring error: {e}")
                    time.sleep(self.interval)
        
        # Start server in separate thread
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start (max 5 seconds)
        if server_ready.wait(timeout=5):
            # Server started successfully
            final_port = actual_port[0]
            # Small additional delay for full initialization
            time.sleep(0.5)
            
            # Open browser
            try:
                webbrowser.open(f'http://localhost:{final_port}')
            except Exception as e:
                print(f"⚠️  Failed to open browser automatically: {e}")
                print(f"   Open manually: http://localhost:{final_port}")
        else:
            print("⚠️  Server did not start within 5 seconds")
            print(f"   Try opening manually: http://localhost:{self.port}")
        
        # Start monitoring
        try:
            run_monitoring()
        except KeyboardInterrupt:
            print("\nStopping web server...")
            self.running = False
            if self.server:
                self.server.shutdown()
    
    def _result_to_dict(self, result: CheckResult):
        """Converts CheckResult to dictionary."""
        return {
            'name': result.name,
            'url': result.url,
            'status_code': result.status_code,
            'latency_ms': result.latency_ms,
            'success': result.success,
            'error': result.error,
            'timeout': result.timeout
        }

