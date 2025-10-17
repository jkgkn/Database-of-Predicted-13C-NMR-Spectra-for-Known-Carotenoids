from flask import Flask, render_template, request, send_from_directory, jsonify
import os
from config import FILES_DIRECTORY
from data_processor import load_and_normalize_csv, CSVProcessingError, validate_filepath

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 允许中文响应

# 安全文件路径检查
def safe_join(base_path, filename):
    safe_path = os.path.abspath(os.path.join(base_path, filename))
    if not safe_path.startswith(base_path):
        raise ValueError("非法路径访问")
    return safe_path

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/search', methods=['GET'])
def search_files():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({})
    
    results = {"pdf": [], "csv": []}
    try:
        for filename in os.listdir(FILES_DIRECTORY):
            if query.lower() in filename.lower():
                # 修复判断逻辑
                _, ext = os.path.splitext(filename)
                ext = ext.lower().replace('.', '')
                if ext in ['pdf', 'csv']:
                    results[ext].append(filename)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/files/<path:filename>')
def serve_file(filename):
    try:
        safe_path = safe_join(FILES_DIRECTORY, filename)
        return send_from_directory(FILES_DIRECTORY, filename)
    except (ValueError, FileNotFoundError):
        return "文件未找到", 404

@app.route('/plot_spectra', methods=['POST'])
def plot_spectra():
    try:
        selected_files = request.json.get('files', [])
        if not isinstance(selected_files, list) or len(selected_files) == 0:
            return jsonify({'error': '无效的文件选择'}), 400
        
        # 验证每个文件名
        for filename in selected_files:
            validate_filepath(filename)
            
        processed_data = load_and_normalize_csv(selected_files)
        return jsonify(processed_data)
    except CSVProcessingError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': '服务器处理错误'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)