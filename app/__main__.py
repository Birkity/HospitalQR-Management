from . import create_app
from .models.doctor import Doctor 
from .models.patient import Patient  

app = create_app()

# Initialize dummy doctor data
Doctor.initialize_dummy_data()
Patient.initialize_dummy_data()  

if __name__ == '__main__':
    app.run(debug=True)