from flask import Blueprint

def register_routes(app):
    from routes.auth import auth_bp
    from routes.wechat import wechat_bp
    from routes.study import study_bp
    from routes.chat import chat_bp
    from routes.assessment import assessment_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(wechat_bp, url_prefix='/api')
    app.register_blueprint(study_bp, url_prefix='/api')
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(assessment_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
