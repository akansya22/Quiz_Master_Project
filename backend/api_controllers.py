from flask_restful import Resource, Api
from .models import *

api = Api()

class SubjectApi(Resource):

    def get(self):
        subjects=Subject.query.all()
        subjects_json=[]
        for subject in subjects:
            subjects_json.append({'id':subject.id,'name':subject.subject_name,'code':subject.code,'credit':subject.credit,'description':subject.description})
        return subjects_json

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


api.add_resource(SubjectApi, '/api/get_subject')