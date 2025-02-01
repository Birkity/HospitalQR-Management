from . import create_app
from .models.doctor import Doctor  # Import the Doctor class

app = create_app()

# Initialize dummy doctor data
Doctor.initialize_dummy_data()

if __name__ == '__main__':
    app.run(debug=True)