# -*- coding: gbk -*-
import pymysql
import traceback
import os
import re
import logging
from pathlib import Path
from functools import wraps
from wtforms import Form, FileField
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_wtf.file import FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.security import generate_password_hash, check_password_hash
from threading import Lock

# ������־
LOG_DIR = Path(__file__).parent / "Algorithm" / "save_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# �̰߳�ȫ��
train_lock = Lock()


def validate_train_params(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        required_params = ['model', 'num_classes', 'epochs', 'train', 'valid', 'test']
        data = request.get_json()

        if not data:
            return jsonify({"code": 400, "message": "���������ΪJSON��ʽ"}), 400

        missing = [p for p in required_params if p not in data]
        if missing:
            return jsonify({"code": 400, "message": f"ȱ�ٱ�Ҫ����: {missing}"}), 400

        if data['model'] not in ['CNN', 'CNN_LSTM']:
            return jsonify({"code": 400, "message": "��Ч��ģ������"}), 400

        return f(*args, **kwargs)

    return wrapper


# �ļ��ϴ�����
ALLOWED_EXTENSIONS = {'mat'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB


def get_db_connection():
    """��ȡ���ݿ�����"""
    return pymysql.connect(
        host="localhost",
        user="root",
        password="weixiyuea",
        database="geerwheel",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )


def allowed_file(filename):
    """����ļ���չ���Ƿ�Ϸ�"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ������־
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# �ļ��ϴ�����
ALLOWED_EXTENSIONS = {'mat'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

# ȫ�ֱ���
save_path = ''


# ���ύ���У��
class fileForm(Form):
    file = FileField(validators=[FileRequired(), FileAllowed(['mat'])])


# �ӿڼ�Ȩ
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = request.headers.get(
        'Origin') or 'http://127.0.0.1:5000' or 'http://localhost:8081/'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE'
    response.headers[
        'Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept, Origin, Referer, User-Agent'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


# ��ʼ��flaskʵ��
app = Flask(__name__)
app.after_request(after_request)

cors = CORS(app, resources={r"/getMsg": {"origins": "*"}})


# ���Է�������ͨ
@app.route('/')
def hello_world():
    print(111)
    return 'Hello World!'


# ����ǰ��˿�ͨ��
@app.route('/getMsg', methods=['GET', 'POST'])
def home():
    response = {
        'msg': 'Hello, Python !'
    }
    return jsonify(response)


# ��ȡע�����󼰴���
@app.route('/register', methods=['POST'])
def getRegisterRequest():
    db = None
    try:
        # �������ݿ�
        db = pymysql.connect(
            user='root',
            password='weixiyuea',
            host='localhost',
            port=3306,
            database='geerwheel',
            charset='utf8'
        )
        cursor = db.cursor()

        # ��ȡ���ݲ�У������ֶ�
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        password2 = data.get('password2', '').strip()
        truename = data.get('truename', '').strip()
        idcardnum = data.get('idcardnum', '').strip()

        # ������֤
        if not all([username, password, password2, truename, idcardnum]):
            return jsonify(success=False, message="�����ֶξ�Ϊ������")

        if password != password2:
            return jsonify(success=False, message="������������벻һ��")

        if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[A-Za-z]', password):
            return jsonify(success=False, message="����������8λ�Ұ�����ĸ������")

        if not re.match(r'^\d{17}[\dX]$', idcardnum):
            return jsonify(success=False, message="���֤�����ʽ����ȷ")

        # �����ϣ����
        hashed_password = generate_password_hash(password)

        # ����û���Ψһ��
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify(success=False, message="�û����Ѵ���")

        # �����û�����
        sql = """
        INSERT INTO users 
            (username, password, truename, idcardnum)
        VALUES 
            (%s, %s, %s, %s)
        """
        cursor.execute(sql, (username, hashed_password, truename, idcardnum))
        db.commit()
        return jsonify(success=True, message="ע��ɹ�")

    except pymysql.IntegrityError:
        db.rollback()
        return jsonify(success=False, message="�û����ѱ�ռ��")
    except Exception as e:
        print(f"Error: {str(e)}")
        if db:
            db.rollback()
        return jsonify(success=False, message="�������ڲ��������Ժ�����")
    finally:
        if db:
            db.close()


# ��ȡ��¼����������
@app.route('/login', methods=['POST'])
def getLoginRequest():
    db = None
    try:
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="weixiyuea",
            database="geerwheel",
            charset="utf8"
        )
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        cursor = db.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result and check_password_hash(result[0], password):
            return jsonify(success=True, message="��¼�ɹ�")
        else:
            return jsonify(success=False, message="�û������������")

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(success=False, message="����������")

    finally:
        if db:
            db.close()


# չʾ���ݼ�
@app.route('/showDataset', methods=['GET'])
def show_dataset():
    try:
        with get_db_connection() as db:
            with db.cursor() as cursor:
                sql = "SELECT id, name, region, contact, description, ischoosed FROM dataset"
                cursor.execute(sql)
                results = cursor.fetchall()

                # ת������ֵ���������ݿ�洢����0/1��
                for item in results:
                    item['ischoosed'] = bool(item['ischoosed'])

                return jsonify(results)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# �������ݼ�ѡ��״̬
@app.route('/updateDataset', methods=['POST'])
def update_dataset():
    try:
        data = request.get_json()
        if not data or 'id' not in data or 'status' not in data:
            return jsonify({"error": "Invalid request data"}), 400

        record_id = data['id']
        new_status = 1 if data['status'] else 0  # ת��Ϊ0/1

        with get_db_connection() as db:
            with db.cursor() as cursor:
                sql = "UPDATE dataset SET ischoosed = %s WHERE id = %s"
                affected_rows = cursor.execute(sql, (new_status, record_id))
                db.commit()

                if affected_rows == 0:
                    return jsonify({"error": "Record not found"}), 404

        return jsonify({"success": True})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ������ݼ�
@app.route('/uploadDataset', methods=['POST'])
def upload_dataset():
    """������ݼ�Ԫ����"""
    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "message": "�������ݸ�ʽ����"}), 400
    # ID������֤
    try:
        dataset_id = int(data['id'])
        if dataset_id <= 0:
            raise ValueError
    except (KeyError, ValueError, TypeError):
        return jsonify({
            "code": 400,
            "message": "ID����Ϊ������"
        }), 400

    required_fields = ['id', 'name', 'region', 'contact', 'description', 'ischoosed']
    if not all(field in data for field in required_fields):
        return jsonify({"code": 400, "message": "ȱ�ٱ�Ҫ�ֶ�"}), 400

    try:
        with get_db_connection() as db:
            with db.cursor() as cursor:
                sql = """INSERT INTO dataset 
                        (id, name, region, contact, description, ischoosed)
                        VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (
                    data['id'],
                    data['name'],
                    data['region'],
                    data['contact'],
                    data['description'],
                    data['ischoosed']
                ))
                db.commit()
                return jsonify({
                    "code": 200,
                    "message": "���ݼ���ӳɹ�",
                    "dataId": data['id']
                })

    except pymysql.IntegrityError as e:
        logger.error(f"���ݿ�Ψһ�Գ�ͻ: {str(e)}")
        return jsonify({
            "code": 409,
            "message": "���ݼ�ID�Ѵ���"
        }), 409
    except Exception as e:
        logger.error(f"���ݿ����ʧ��: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "�������ڲ�����"
        }), 500


# �ϴ��ļ�
@app.route("/uploadDatafile", methods=['POST'])
def upload_datafile():
    """�����ļ��ϴ�"""
    # ��֤���ݼ�ID
    dataset_id = request.form.get('datasetId')
    try:
        dataset_id = int(dataset_id)
        if dataset_id <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({
            "code": 400,
            "message": "��Ч�����ݼ�ID��ʽ"
        }), 400

    if 'file' not in request.files:
        return jsonify({"code": 400, "message": "δѡ���ļ�"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"code": 400, "message": "��Ч�ļ���"}), 400

    if not allowed_file(file.filename):
        return jsonify({"code": 400, "message": "��֧��MAT��ʽ�ļ�"}), 400

    try:
        # ��ȡ�ļ���С����Ҫ���÷���������ϴ���С��
        file.seek(0, os.SEEK_END)
        if file.tell() > MAX_FILE_SIZE:
            return jsonify({"code": 413, "message": "�ļ���С����500MB����"}), 413
        file.seek(0)

        # �����������ȡ����·��
        dataset_id = request.form.get('datasetId')
        if not dataset_id:
            return jsonify({"code": 400, "message": "ȱ�����ݼ�ID����"}), 400

        # ��������·��
        base_dir = os.path.abspath(os.path.dirname(__file__))
        save_dir = os.path.join(base_dir, 'static', 'data', dataset_id)

        # ȷ��Ŀ¼����
        os.makedirs(save_dir, exist_ok=True)

        # ��ȫ�����ļ�
        filename = secure_filename(file.filename)
        save_path = os.path.join(save_dir, filename)
        file.save(save_path)

        return jsonify({
            "code": 200,
            "message": "�ļ��ϴ��ɹ�",
            "path": save_path
        })

    except Exception as e:
        logger.error(f"�ļ��ϴ�ʧ��: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "�ļ��ϴ�ʧ��"
        }), 500


@app.route("/train", methods=['POST'])
@validate_train_params
def train():
    data = request.get_json()
    model_type = data['model']

    try:
        # ����ģ��ר����־��
        logger = logging.getLogger(model_type)
        logger.setLevel(logging.INFO)
        log_file = LOG_DIR / f"{model_type}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # �̰߳�ȫ����
        with train_lock:
            logger.info("����ѵ������")

            if model_type == 'CNN':
                from backend.Algorithm import sign_cnn as model
            else:
                from backend.Algorithm import cnn_lstm_model as model

            # ����ģ�Ͳ���
            for param in ['num_classes', 'epochs', 'train', 'valid', 'test']:
                setattr(model, param, data[param])

            # ִ��ѵ��
            model.run_Algorithm(logger)

            logger.info("ѵ�����")

        return jsonify({
            "code": 200,
            "message": "ѵ������������",
            "log_path": str(log_file)
        })

    except Exception as e:
        logger.error(f"ѵ��ʧ��: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "ѵ�����̷�������",
            "error": str(e)
        }), 500
    finally:
        # ������־������
        if 'file_handler' in locals():
            logger.removeHandler(file_handler)
            file_handler.close()


@app.route('/logs/<model_type>', methods=['GET'])
def get_logs(model_type):
    try:
        # ��ȫУ���ļ���
        if not re.match(r'^[A-Za-z0-9_]+$', model_type):
            return jsonify({"status": "error", "message": "��Ч��ģ������"}), 400

        log_file = LOG_DIR / f"{model_type}.log"

        if not log_file.exists():
            return jsonify({"status": "error", "message": "��־�ļ�������"}), 404

        # ֧�ַ�ҳ��ȡ
        page = request.args.get('page', 1, type=int)
        per_page = 100  # ÿҳ100��

        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        total_pages = (len(lines) + per_page - 1) // per_page
        paginated = lines[(page - 1) * per_page: page * per_page]

        return jsonify({
            "status": "success",
            "content": ''.join(paginated),
            "current_page": page,
            "total_pages": total_pages
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# # �鿴ѵ����־
# @app.route('/result', methods=['POST', 'GET'])
# def read_file():
#     file_path = 'D:\WorkSpace\\Undergraduate\\4th_Year\Fault Diagnosis\Code\\fault-diagnosis\\backend\Algorithm\save_logs'
#     model = request.get_json()['model']
#     file_path = file_path + ('\{}.log'.format(model))
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             content = file.read()
#         return jsonify({'content': content, 'status': 'success'})
#     except Exception as e:
#         return jsonify({'error': str(e), 'status': 'error'})


# ��������
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)  # �����ӻ�ֱ�������ڱ��ط�������Ҳ���� localhost:5000
# app.run(host='your_ip_address') # �����ͨ�� host ָ���ڹ���IP������
