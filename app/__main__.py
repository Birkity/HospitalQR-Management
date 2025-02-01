from . import create_app
from .models.doctor import Doctor  # Import the Doctor class
from .models.patient import Patient  # Add this import

app = create_app()

# Initialize dummy doctor data
Doctor.initialize_dummy_data()
Patient.initialize_dummy_data()  # Add this line

if __name__ == '__main__':
    app.run(debug=True)