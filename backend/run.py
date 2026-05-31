from app import app

if __name__ == "__main__":
    print("\n====================================")
    print("  Book Rental Management System")
    print("      REST API Server (Flask)")
    print("====================================\n")

    print("Starting Flask API server...")
    print("Base URL: http://localhost:5000/api/v1")
    print("Swagger: http://localhost:5000/api-docs\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
