from flask import Flask, render_template, request, jsonify, send_file
import pdfplumber
import os
import re
from pathlib import Path
from PIL import Image, ImageDraw
import io
import json

app = Flask(__name__)

# Configure the PDF folder path - UPDATE THIS TO YOUR FOLDER
PDF_FOLDER = r"C:\Users\223146805.AEROAD\OneDrive - GE Aerospace\Desktop\Sourcing Quotes API"

def get_pdf_files():
    """Get list of all PDF files in the folder"""
    if not os.path.exists(PDF_FOLDER):
        return []
    return [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith('.pdf')]

def search_pdfs(search_term):
    """Search all PDFs for the search term and extract cost data"""
    results = {}
    cost_values = []
    
    pdf_files = get_pdf_files()
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_FOLDER, pdf_file)
        matches = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if not text:
                        continue
                    
                    # Find all instances of search term (case-insensitive)
                    pattern = re.compile(re.escape(search_term), re.IGNORECASE)
                    if pattern.search(text):
                        # Extract lines containing the search term
                        lines = text.split('\n')
                        first_occurrence = True
                        
                        for line in lines:
                            if pattern.search(line):
                                # Try to extract cost value from the line
                                # Look for currency amounts like $100.00
                                cost_pattern = r'\$?\d+(?:,\d{3})*(?:\.\d{2})?'
                                cost_matches = re.findall(cost_pattern, line)
                                
                                if cost_matches and first_occurrence:
                                    # Use only first occurrence for cost average
                                    cost_str = cost_matches[-1]  # Usually last number in line is the cost
                                    cost_str = cost_str.replace('$', '').replace(',', '')
                                    try:
                                        cost_values.append(float(cost_str))
                                    except ValueError:
                                        pass
                                    first_occurrence = False
                                
                                # Add match info
                                if {
                                    'page': page_num,
                                    'text': line.strip()[:100]  # First 100 chars
                                } not in matches:
                                    matches.append({
                                        'page': page_num,
                                        'text': line.strip()[:100]
                                    })
                        
        except Exception as e:
            print(f"Error reading {pdf_file}: {str(e)}")
            continue
        
        if matches:
            results[pdf_file] = matches
    
    # Calculate average cost
    average_cost = sum(cost_values) / len(cost_values) if cost_values else 0
    
    return {
        'results': results,
        'average_cost': f"${average_cost:.2f}" if average_cost > 0 else "No costs found",
        'total_matches': sum(len(v) for v in results.values()),
        'pdfs_with_matches': len(results)
    }

def highlight_pdf(pdf_filename, search_term, page_num=1):
    """Create a highlighted version of the PDF"""
    pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if page_num > len(pdf.pages):
                page_num = len(pdf.pages)
            
            page = pdf.pages[page_num - 1]
            
            # Get page image
            im = page.to_image(resolution=150).original
            draw = ImageDraw.Draw(im, 'RGBA')
            
            # Extract text with locations
            text = page.extract_text()
            
            if not text:
                # Return blank image if no text
                return im
            
            # Highlight search term
            pattern = re.compile(re.escape(search_term), re.IGNORECASE)
            
            # Get word coordinates
            words = page.extract_words()
            
            for word in words:
                if pattern.search(word['text']):
                    # Highlight the word
                    x0, top, x1, bottom = word['x0'], word['top'], word['x1'], word['bottom']
                    # Draw yellow highlight
                    draw.rectangle([x0, top, x1, bottom], fill=(255, 255, 0, 100))
            
            return im
    
    except Exception as e:
        print(f"Error highlighting PDF: {str(e)}")
        return None

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    """API endpoint for searching PDFs"""
    data = request.json
    search_term = data.get('search_term', '').strip()
    
    if not search_term:
        return jsonify({'error': 'Please enter a search term'}), 400
    
    if not os.path.exists(PDF_FOLDER):
        return jsonify({'error': f'PDF folder not found: {PDF_FOLDER}'}), 404
    
    results = search_pdfs(search_term)
    return jsonify(results)

@app.route('/api/pdf/<filename>/<int:page>')
def get_pdf_page(filename, page):
    """Get a highlighted PDF page as image"""
    search_term = request.args.get('search', '')
    
    if not filename or not search_term:
        return jsonify({'error': 'Missing parameters'}), 400
    
    # Security check - prevent directory traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        return jsonify({'error': 'Invalid filename'}), 400
    
    im = highlight_pdf(filename, search_term, page)
    
    if im is None:
        return jsonify({'error': 'Could not process PDF'}), 500
    
    # Convert image to bytes
    img_io = io.BytesIO()
    im.save(img_io, 'PNG', quality=85)
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

@app.route('/api/pdf-info/<filename>')
def get_pdf_info(filename):
    """Get PDF page count"""
    # Security check
    if '..' in filename or '/' in filename or '\\' in filename:
        return jsonify({'error': 'Invalid filename'}), 400
    
    pdf_path = os.path.join(PDF_FOLDER, filename)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return jsonify({
                'page_count': len(pdf.pages),
                'filename': filename
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run on all network interfaces so others can access it
    app.run(debug=True, host='0.0.0.0', port=5000)
