
# Hospital Diagnosis Web Application

This project is a Flask-based web application designed to aid in medical diagnosis by classifying lung cancer images into one of three categories. It leverages a deep learning model to analyze medical images uploaded by doctors and provides real-time predictions along with confidence scores.

Key features include:

Image Classification: Detects lung cancer types using a trained model with three output classes.

Doctor & Patient Records: Securely stores and manages information about the submitting doctor and patient for each image.

Confidence-Based Filtering: Automatically rejects images with prediction confidence below 90% to maintain result reliability.

Monitoring Dashboard: Provides visual insights into model performance, including accepted uploads, prediction statistics, and exportable records with timestamps.



---

## Project Overview

This project aims to automate the classification of lung cancer medical images using a deep learning-powered Flask web application. The system provides a seamless pipeline for uploading patient scan images, associating them with doctor and patient details, and generating AI-driven diagnostic predictions.

Key functionalities include:

Medical Image Classification: The application predicts one of three lung cancer classes from a submitted medical image using a trained convolutional neural network.

Integrated Patient Form: Doctors can submit an image alongside essential patient and doctor information using a web form.

Confidence-Based Filtering: Any classification result with a confidence score below 90% is automatically rejected and logged as an invalid input to ensure reliability.

Live Dashboard Monitoring: A powerful dashboard allows real-time tracking of predictions, accepted and rejected cases, visual data analysis via charts, and full CRUD (Create, Read, Update, Delete) operations on each record.

Export & Timestamp Logging: All records are timestamped and can be exported to CSV format for medical review, audits, or reporting.

**Model Training & Selection**
To determine the most accurate model for the task, four state-of-the-art CNN architectures were trained and evaluated:

Model	        Test Accuracy	    Test Loss
InceptionV3	    99.20%	            0.0229
ResNet50	    94.47%	            0.1347
EfficientNetB0	62.60%	            0.8828
DenseNet121	    100.00%	            0.0001

After evaluating all models, DenseNet121 was selected as the final deployment model due to its perfect test accuracy and minimal loss, indicating superior generalization and reliability. This model now powers the backend inference system in the deployed app.
---

## Dataset

This project uses the Lung Cancer Histopathological Images Dataset from Kaggle, which contains labeled histopathological images of lung tissue categorized into three distinct classes:

Benign – Non-cancerous tissue

Adenocarcinoma – A common type of non-small cell lung cancer

Squamous Cell Carcinoma – Another major subtype of non-small cell lung cancer

To ensure reliable evaluation and generalization, the dataset was split as follows:

80% for training, 10% for validation and 10% for testing

Prior to training, the images were resized and normalized. Advanced data augmentation techniques were also applied to improve model robustness and reduce overfitting. These augmentations were implemented using TensorFlow's ImageDataGenerator and included:

rescale = 1./255  
zoom_range = 0.05  
brightness_range = [0.9, 1.1]  
shear_range = 5  
rotation_range = 5  
width_shift_range = 0.05  
height_shift_range = 0.05  
fill_mode = 'nearest'  

These transformations helped simulate real-world variability in medical imaging.

After evaluating multiple models — InceptionV3, ResNet50, EfficientNetB0, and DenseNet121 — the final selected model was **DenseNet121**, which outperformed all others with a 100% test accuracy and minimal loss. This model was integrated into the Flask application for real-time medical image classification.
---

## Pipeline Steps

### 1. **Data Preprocessing**
- The dataset was split into:
  - **80%** for training
  - **10%** for validation
  - **10%** for testing
- All images were:
  - **Resized** to `224x224` pixels
  - **Normalized** by scaling pixel values to the `[0, 1]` range using `rescale=1./255`

### 2. **Feature Engineering**
To enhance the model’s ability to generalize, extensive image augmentation was applied to the training data. Techniques included random zooming, slight changes in brightness, minor rotations, shearing, and horizontal and vertical shifts. All images were also normalized by rescaling pixel values to the [0, 1] range. The validation and test sets, in contrast, were only rescaled without augmentation to preserve their integrity. These engineered features helped the model learn more robust spatial patterns specific to lung cancer tissue morphology.


### 3. **Model Training**
Four deep learning architectures were evaluated: InceptionV3, ResNet50, EfficientNetB0, and DenseNet121. All models were initialized with pretrained ImageNet weights and fine-tuned for the lung cancer classification task.

In the case of DenseNet121 (which was selected for final deployment), the model was partially unfrozen to allow fine-tuning of the top layers while freezing the majority of lower layers. Specifically, all layers except the last 50 were frozen to retain low-level feature representations and adapt the higher-level layers to the new dataset.

During training, several callbacks were used to stabilize and optimize learning:
- **EarlyStopping** was applied to halt training if the validation loss did not improve after 5 epochs, restoring the best model weights.
- **ModelCheckpoint** was used to save the best-performing model based on validation loss.
- **ReduceLROnPlateau** monitored the validation loss and reduced the learning rate by a factor of 0.2 if it plateaued for 3 consecutive epochs.

The final DenseNet121 model was saved as a `.h5` file and later converted to ONNX format for deployment.


### 4. **Evaluation**
All four candidate models — InceptionV3, ResNet50, EfficientNetB0, and DenseNet121 — were trained and evaluated using consistent metrics to identify the best-performing architecture.

For each model, training and validation **accuracy** and **loss** were tracked and plotted over epochs to visualize convergence behavior and detect overfitting. In addition to numerical metrics, a **confusion matrix** was generated to assess how well each model distinguished between the three lung cancer classes.

DenseNet121 showed the best balance between high accuracy and low validation loss. Its confusion matrix revealed strong performance across all three classes. Visual inspection of predictions compared to actual labels confirmed the model's robustness and ability to generalize.

This thorough comparison helped justify the selection of DenseNet121 as the final model for deployment.

### 5. **Deployment**
The final DenseNet121 model, after being converted to ONNX format, was deployed in a full-stack Flask application.

The app was modularized using **Flask Blueprints** for clean separation of functionality. It supports multiple routes:
- `/` — Home page for entering doctor and patient information
- `/upload` — Upload page for submitting medical images and triggering ONNX-based classification
- `/monitor` — Monitoring dashboard that displays all classified records, real-time class distribution pie chart (via Matplotlib), and performance statistics
- `/export` — Allows users to download all stored records in CSV format
- `/delete/<id>` — Enables deletion of specific classification records from the database

Uploaded images are stored in the `static/uploads/` directory, and classification results are persisted in an SQLite database (`instance/app.db`) 

Low-confidence predictions (< 90%) are rejected to ensure reliability. The UI was styled using **Bootstrap 5** for a modern, responsive layout, with custom CSS for enhanced readability. Charts and summaries are auto-generated to help visualize model activity and prediction trends in real-time.

This deployment pipeline enables the entire ML workflow to be accessed and utilized through a clean, browser-based medical tool.


---

## Setup Instructions

1. **Clone the Repo**

```bash
git clone https://github.com/yassinahmed01/hospital-diagnosis-app.git
cd hospital-diagnosis-app
```

2. **Create a Virtual Environment**

```bash
python -m venv .venv
```

3. **Activate the Environment**

```bash
# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

4. **Install Requirements**

```bash
pip install -r requirements.txt
```

5. **Run the Application**

```bash
python app.py
```

---

## Usage

- Open your browser and go to `http://localhost:5000`
- Login with dummy credentials or predefined users.
- Use the upload form to:
  - Enter doctor/patient details.
  - Upload an image.
  - Get a prediction and confidence score.
- Rejected predictions (confidence < 90%) are logged separately.
- Visit the **Monitor** page to:
  - View all records.
  - Filter or search.
  - Delete entries.
  - Export records to CSV.
  - View timestamped pie charts and trends.

---

## Folder Structure

```
hospital_app/
├── app.py
├── config.py
├── class_names.json
├── requirements.txt
├── README.md
├── .gitignore
├── densenet121_model.onnx
│
├── instance/
│ └── app.db
│
├── db/
│ └── models.py
│
├── static/
│ ├── css/
│ │ └── style.css
│ └── uploads/
│
├── templates/
│ ├── index.html
│ ├── login.html
│ ├── logout.html
│ ├── monitor.html
│ └── upload.html
│
├── routes/
│ ├── init.py
│ ├── home.py
│ ├── login.py
│ ├── logout.py
│ ├── upload.py
│ ├── monitor.py
│ ├── export.py
│ └── delete_record.py
│
├── utils/
│ └── preprocessing.py
│
└── model/
└── infrence.py
```

---

## 🚀 Technologies Used

- **Python 3.11+** — Core programming language for backend and ML integration
- **Flask** — Lightweight web framework used to build the web application
- **TensorFlow / Keras** — For model training, evaluation, and ONNX conversion
- **ONNX Runtime** — For fast inference with the exported model
- **SQLAlchemy + SQLite** — ORM and lightweight database for storing records
- **Bootstrap 5** — Responsive UI design framework
- **Jinja2** — Template engine for dynamic HTML rendering in Flask
- **Matplotlib** — For generating live pie charts and visual summaries
- **Pandas** — For handling tabular export and filtering of prediction records

---

