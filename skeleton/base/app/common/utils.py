from flask import current_app

class Utils(object):

    @staticmethod
    def allowed_file_extension(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']