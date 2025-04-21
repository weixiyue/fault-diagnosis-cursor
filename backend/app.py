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

# 配置日志
LOG_DIR = Path(__file__).parent / "Algorithm" / "save_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 线程安全锁
train_lock = Lock()


def validate_train_params(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        required_params = ['model', 'num_classes', 'epochs', 'train', 'valid', 'test']
        data = request.get_json()

        if not data:
            return jsonify({"code": 400, "message": "请求体必须为JSON格式"}), 400

        missing = [p for p in required_params if p not in data]
        if missing:
            return jsonify({"code": 400, "message": f"缺少必要参数: {missing}"}), 400

        if data['model'] not in ['CNN', 'CNN_LSTM']:
            return jsonify({"code": 400, "message": "无效的模型类型"}), 400

        return f(*args, **kwargs)

    return wrapper


# 文件上传配置
ALLOWED_EXTENSIONS = {'mat'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB


def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(
        host="localhost",
        user="root",
        password="weixiyuea",
        database="geerwheel",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )


def allowed_file(filename):
    """检查文件扩展名是否合法"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 文件上传配置
ALLOWED_EXTENSIONS = {'mat'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

# 全局变量
save_path = ''


# 表单提交相关校验
class fileForm(Form):
    file = FileField(validators=[FileRequired(), FileAllowed(['mat'])])


# 接口鉴权
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = request.headers.get(
        'Origin') or 'http://127.0.0.1:5000' or 'http://localhost:8081/'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE'
    response.headers[
        'Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept, Origin, Referer, User-Agent'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


# 初始化flask实例
app = Flask(__name__)
app.after_request(after_request)

cors = CORS(app, resources={r"/getMsg": {"origins": "*"}})


# 测试服务器连通
@app.route('/')
def hello_world():
    print(111)
    return 'Hello World!'


# 测试前后端可通信
@app.route('/getMsg', methods=['GET', 'POST'])
def home():
    response = {
        'msg': 'Hello, Python !'
    }
    return jsonify(response)


# 获取注册请求及处理
@app.route('/register', methods=['POST'])
def getRegisterRequest():
    db = None
    try:
        # 连接数据库
        db = pymysql.connect(
            user='root',
            password='weixiyuea',
            host='localhost',
            port=3306,
            database='geerwheel',
            charset='utf8'
        )
        cursor = db.cursor()

        # 获取数据并校验必填字段
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        password2 = data.get('password2', '').strip()
        truename = data.get('truename', '').strip()
        idcardnum = data.get('idcardnum', '').strip()

        # 输入验证
        if not all([username, password, password2, truename, idcardnum]):
            return jsonify(success=False, message="所有字段均为必填项")

        if password != password2:
            return jsonify(success=False, message="两次输入的密码不一致")

        if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[A-Za-z]', password):
            return jsonify(success=False, message="密码需至少8位且包含字母和数字")

        if not re.match(r'^\d{17}[\dX]$', idcardnum):
            return jsonify(success=False, message="身份证号码格式不正确")

        # 密码哈希处理
        hashed_password = generate_password_hash(password)

        # 检查用户名唯一性
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify(success=False, message="用户名已存在")

        # 插入用户数据
        sql = """
        INSERT INTO users 
            (username, password, truename, idcardnum)
        VALUES 
            (%s, %s, %s, %s)
        """
        cursor.execute(sql, (username, hashed_password, truename, idcardnum))
        db.commit()
        return jsonify(success=True, message="注册成功")

    except pymysql.IntegrityError:
        db.rollback()
        return jsonify(success=False, message="用户名已被占用")
    except Exception as e:
        print(f"Error: {str(e)}")
        if db:
            db.rollback()
        return jsonify(success=False, message="服务器内部错误，请稍后重试")
    finally:
        if db:
            db.close()


# 获取登录参数及处理
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
            return jsonify(success=True, message="登录成功")
        else:
            return jsonify(success=False, message="用户名或密码错误")

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(success=False, message="服务器错误")

    finally:
        if db:
            db.close()


# 展示数据集
@app.route('/showDataset', methods=['GET'])
def show_dataset():
    try:
        with get_db_connection() as db:
            with db.cursor() as cursor:
                sql = "SELECT id, name, region, contact, description, ischoosed FROM dataset"
                cursor.execute(sql)
                results = cursor.fetchall()

                # 转换布尔值（假设数据库存储的是0/1）
                for item in results:
                    item['ischoosed'] = bool(item['ischoosed'])

                return jsonify(results)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# 更改数据集选中状态
@app.route('/updateDataset', methods=['POST'])
def update_dataset():
    try:
        data = request.get_json()
        if not data or 'id' not in data or 'status' not in data:
            return jsonify({"error": "Invalid request data"}), 400

        record_id = data['id']
        new_status = 1 if data['status'] else 0  # 转换为0/1

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


# 添加数据集
@app.route('/uploadDataset', methods=['POST'])
def upload_dataset():
    """添加数据集元数据"""
    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "message": "请求数据格式错误"}), 400
    # ID类型验证
    try:
        dataset_id = int(data['id'])
        if dataset_id <= 0:
            raise ValueError
    except (KeyError, ValueError, TypeError):
        return jsonify({
            "code": 400,
            "message": "ID必须为正整数"
        }), 400

    required_fields = ['id', 'name', 'region', 'contact', 'description', 'ischoosed']
    if not all(field in data for field in required_fields):
        return jsonify({"code": 400, "message": "缺少必要字段"}), 400

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
                    "message": "数据集添加成功",
                    "dataId": data['id']
                })

    except pymysql.IntegrityError as e:
        logger.error(f"数据库唯一性冲突: {str(e)}")
        return jsonify({
            "code": 409,
            "message": "数据集ID已存在"
        }), 409
    except Exception as e:
        logger.error(f"数据库操作失败: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "服务器内部错误"
        }), 500


# 上传文件
@app.route("/uploadDatafile", methods=['POST'])
def upload_datafile():
    """处理文件上传"""
    # 验证数据集ID
    dataset_id = request.form.get('datasetId')
    try:
        dataset_id = int(dataset_id)
        if dataset_id <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({
            "code": 400,
            "message": "无效的数据集ID格式"
        }), 400

    if 'file' not in request.files:
        return jsonify({"code": 400, "message": "未选择文件"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"code": 400, "message": "无效文件名"}), 400

    if not allowed_file(file.filename):
        return jsonify({"code": 400, "message": "仅支持MAT格式文件"}), 400

    try:
        # 获取文件大小（需要配置服务器最大上传大小）
        file.seek(0, os.SEEK_END)
        if file.tell() > MAX_FILE_SIZE:
            return jsonify({"code": 413, "message": "文件大小超过500MB限制"}), 413
        file.seek(0)

        # 从请求参数获取保存路径
        dataset_id = request.form.get('datasetId')
        if not dataset_id:
            return jsonify({"code": 400, "message": "缺少数据集ID参数"}), 400

        # 构建保存路径
        base_dir = os.path.abspath(os.path.dirname(__file__))
        save_dir = os.path.join(base_dir, 'static', 'data', dataset_id)

        # 确保目录存在
        os.makedirs(save_dir, exist_ok=True)

        # 安全保存文件
        filename = secure_filename(file.filename)
        save_path = os.path.join(save_dir, filename)
        file.save(save_path)

        return jsonify({
            "code": 200,
            "message": "文件上传成功",
            "path": save_path
        })

    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "文件上传失败"
        }), 500


@app.route("/train", methods=['POST'])
@validate_train_params
def train():
    data = request.get_json()
    model_type = data['model']

    try:
        # 创建模型专属日志器
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

        # 线程安全操作
        with train_lock:
            logger.info("启动训练流程")

            if model_type == 'CNN':
                from backend.Algorithm import sign_cnn as model
            else:
                from backend.Algorithm import cnn_lstm_model as model

            # 设置模型参数
            for param in ['num_classes', 'epochs', 'train', 'valid', 'test']:
                setattr(model, param, data[param])

            # 执行训练
            model.run_Algorithm(logger)

            logger.info("训练完成")

        return jsonify({
            "code": 200,
            "message": "训练任务已启动",
            "log_path": str(log_file)
        })

    except Exception as e:
        logger.error(f"训练失败: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "训练过程发生错误",
            "error": str(e)
        }), 500
    finally:
        # 清理日志处理器
        if 'file_handler' in locals():
            logger.removeHandler(file_handler)
            file_handler.close()


@app.route('/logs/<model_type>', methods=['GET'])
def get_logs(model_type):
    try:
        # 安全校验文件名
        if not re.match(r'^[A-Za-z0-9_]+$', model_type):
            return jsonify({"status": "error", "message": "无效的模型名称"}), 400

        log_file = LOG_DIR / f"{model_type}.log"

        if not log_file.exists():
            return jsonify({"status": "error", "message": "日志文件不存在"}), 404

        # 支持分页读取
        page = request.args.get('page', 1, type=int)
        per_page = 100  # 每页100行

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


# # 查看训练日志
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


# 启动运行
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)  # 这样子会直接运行在本地服务器，也即是 localhost:5000
# app.run(host='your_ip_address') # 这里可通过 host 指定在公网IP上运行
