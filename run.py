"""
ProjectHub Flask Backend - Entry Point

This script initializes the Flask application with all blueprints (routes)
and starts the development server.

Blueprints Initialized:
  - creation_bp: /creation/... routes (app/creation_manegement/roughts/roughts.py)
  - bank_account_bp: /bank-account/... routes (app/bank_account_manegment/roughts/roughts.py)
  - user_bp: /user/... routes (app/user_manegment/roughts/roughts.py)

Authentication:
  - JWT token validation on all protected routes
  - Public routes: /, /checkLogin

Database:
  - Centralized connection via model/db.py
  - SQLAlchemy models created on startup
"""

from app import create_app
from app.register_blueprint import register_blueprint

# Create Flask app with all configuration
app = create_app()

# Blueprints are already registered in create_app() via register_blueprint()
# But we can verify them here if needed:
print("=" * 60)
print("FLASK APP INITIALIZED")
print("=" * 60)
print(f"Blueprints: {list(app.blueprints.keys())}")
print(f"Total Routes: {len(list(app.url_map.iter_rules()))}")
print("=" * 60)


# Welcome route (public)
@app.route("/")
def welcome():
    """Public welcome endpoint"""
    return "Welcome to projecthub Backend!"


# Optional: Verify all routes on startup (for debugging)
@app.route("/api/routes", methods=['GET'])
def list_routes():
    """List all available routes (debugging endpoint)"""
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes.append({
                'endpoint': rule.endpoint,
                'path': str(rule.rule),
                'methods': list(rule.methods - {'HEAD', 'OPTIONS'})
            })
    return {'total_routes': len(routes), 'routes': sorted(routes, key=lambda x: x['path'])}, 200


if __name__ == '__main__':
    # Start development server
    # All blueprints are already initialized via register_blueprint(app) in app/__init__.py
    print("\n✅ Starting ProjectHub Backend Server")
    print("📍 Server: http://127.0.0.1:5000")
    print("🔐 Authentication: JWT Token Required (except public routes)")
    print("📚 Documentation: See BLUEPRINT_REGISTRATION.md & ROUTES_INITIALIZATION.md")
    print("\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
