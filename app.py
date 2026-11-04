from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from models.extraction import *
from models.detection import *
from models.scoring import *
from models.database import *
from models.similarity import *
from models.metadata import *
from models.attribution import *
from models.incident import *

app = Flask(__name__)
CORS(app)

# Upload folder path
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])

def home():

    error = None

    uploaded_filename = None
    entered_text = None
    extracted_text = None
    metadata = None
    findings = []
    total_score = 0
    overall_risk = "SAFE"
    highlighted_text = None
    similarity_results = []
    top_source = None
    final_attribution = None
    incident = None

    metadata_result = {
        "matched": False,
        "score": 0,
        "reason": "No metadata comparison"
    }


    if request.method == 'POST':

        file = request.files.get('file')
        entered_text = request.form.get('prompt_text')


        # Remove leading/trailing whitespace
        if entered_text:
            entered_text = entered_text.strip()
            

        # Empty submission
        if not entered_text and (
            not file or file.filename == ''
        ):

            return render_template(
                'index.html',
                uploaded_filename=None,
                entered_text=None,
                extracted_text=None,
                metadata=None,
                findings=[],
                total_score=0,
                overall_risk="SAFE",
                highlighted_text=None,
                similarity_results=[]
            )

        # ==========================
        # TEXT INPUT ANALYSIS
        # ==========================

        if entered_text:

            findings.extend(
                detect_sensitive_data(
                    entered_text
                )
            )

            highlighted_text = (
                highlight_sensitive_data(
                    entered_text
                )
            )

            similarity_results = (
                analyze_similarity(
                    entered_text
                )
            )

            top_source = get_top_source(
                similarity_results
            )

            if top_source and top_source["document"] != "UNKNOWN":

                metadata_result = {
                    "matched": False,
                    "score": 0,
                    "reason": "Unknown source  "
                }
            
            else:

                metadata_result = {
                    "matched": False,
                    "score": 0,
                    "reason": "Unknown source"
                }

            final_attribution = build_attribution(
                top_source,
                metadata_result
            )


        # ==========================
        # FILE ANALYSIS
        # ==========================

        elif file and file.filename != '':

            # Validate file type
            if not allowed_file(file.filename):
                return render_template(
                    'index.html',
                    error="Unsupported file type. Please upload a PDF, DOCX, or TXT file.",
                    uploaded_filename=None,
                    entered_text=None,
                    extracted_text=None,
                    metadata=None,
                    findings=[],
                    total_score=0,
                    overall_risk="SAFE",
                    highlighted_text=None,
                    similarity_results=[]
                )

            filename = secure_filename(file.filename)

            filename = secure_filename(
                file.filename
            )

            uploaded_filename = filename

            save_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )

            try:
                file.save(save_path)
            except Exception:
                return render_template(
                    'index.html',
                    error="Unable to upload the selected file.",
                    uploaded_filename=None,
                    findings=[],
                    total_score=0,
                    overall_risk="SAFE"
                )

            extension = (
                filename.rsplit(
                    '.',
                    1
                )[1].lower()
            )

            try:

                if extension == 'txt':
                    extracted_text = extract_txt(save_path)
                    metadata = {}

                elif extension == 'pdf':
                    extracted_text, metadata = extract_pdf(save_path)

                elif extension == 'docx':
                    extracted_text, metadata = extract_docx(save_path)

            except Exception:

                return render_template(
                    'index.html',
                    error="Unable to read the uploaded document.",
                    uploaded_filename=None,
                    findings=[],
                    total_score=0,
                    overall_risk="SAFE"
                )

            if not extracted_text or not extracted_text.strip():

                return render_template(
                    'index.html',
                    error="The uploaded document contains no readable text.",
                    uploaded_filename=uploaded_filename,
                    findings=[],
                    total_score=0,
                    overall_risk="SAFE"
                )

            findings.extend(
                detect_sensitive_data(
                    extracted_text
                )
           )

            highlighted_text = (
                highlight_sensitive_data(
                    extracted_text
                )
            )

            similarity_results = analyze_similarity(
                extracted_text,
                metadata
            )

            top_source = get_top_source(
                similarity_results
            )

            if top_source and top_source["document"] != "UNKNOWN":
                metadata_result = compare_metadata(
                    metadata,
                    top_source["document"]
                )

            else:

                metadata_result ={
                    "matched": False,
                    "score": 0,
                    "reason": "Unknown source"
                }

            final_attribution = build_attribution(
                top_source,
                metadata_result
            )

  
        # ==========================
        # RISK SCORING
        # ==========================

        total_score, overall_risk = (
            calculate_risk(
                findings,
                similarity_results
            )
        )

        incident = generate_incident(
            overall_risk,
            findings,
            top_source
        )

        # ==========================
        # DATABASE LOGGING
        # ==========================

        if entered_text or uploaded_filename:

            save_analysis(
                entered_text,
                uploaded_filename,
                findings,
                total_score,
                overall_risk
            )

    return render_template(
        'index.html',
        error=error,
        uploaded_filename=uploaded_filename,
        entered_text=entered_text,
        extracted_text=extracted_text,
        metadata=metadata,
        findings=findings,
        total_score=total_score,
        overall_risk=overall_risk,
        highlighted_text=highlighted_text,
        similarity_results=similarity_results,
        metadata_result=metadata_result,
        top_source=top_source,
        final_attribution=final_attribution,
        incident=incident
    )

@app.route('/analyze_prompt', methods=['POST'])
def analyze_prompt():

    data = request.get_json()

    prompt = data.get(
        'prompt',
        ''
    )

    findings = detect_sensitive_data(
        prompt
    )

    similarity_results = analyze_similarity(
        prompt
    )

    total_score, overall_risk = (
        calculate_risk(
            findings,
            similarity_results
        )
    )

    top_source = get_top_source(
        similarity_results
    )

    incident = generate_incident(
        overall_risk,
        findings,
        top_source
    )

    return jsonify({

        "risk_level":
            overall_risk,

        "risk_score":
            total_score,

        "findings":
            findings,

        "top_source":
            top_source,

        "similarity_results":
            similarity_results[:3],

        "incident":
            incident

    }) 


if __name__ == '__main__':
    app.run(debug=False)