import boto3
from flask import Flask, request
from pyresparser import ResumeParser
from werkzeug.utils import secure_filename
import io
import uuid
S3_BUCKET = 'wuelev8-resume-bucket'

ALLOWED_EXTENSIONS = {"pdf", "docx"}
app = Flask(__name__)

s3_resource = boto3.resource("s3")
s3_client = boto3.client("s3")


def allowed_file(filename):
    return (
        (True, filename.rsplit(".", 1)[1].lower())
        if "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        else False
    )


@app.route("/parse-resume", methods=["POST"])
def parse_resume():
    if "file" not in request.files:
        return {"ok": False, "msg": "No file part"}
    file = request.files["file"]
    if file.filename == "" or not file:
        return {"ok": False, "msg": "No selected file"}
    if not allowed_file(file.filename):
        return {"ok": False, "msg": "not an allowed format"}

    filename = secure_filename(file.filename)
    id = str(uuid.uuid4()) + "." + allowed_file(filename)[1]
    resume_bucket = s3_resource.Bucket(S3_BUCKET)
    resume_bucket.Object(id).put(Body=file)
    resume_object = s3_resource.Object(S3_BUCKET, id)
    bytes_data = io.BytesIO()
    resume_object.download_fileobj(bytes_data)
    bytes_data.name = id
    data = ResumeParser(resume=bytes_data).get_extracted_data()
    return data


if __name__ == "__main__":
    app.run(debug=True, port=5069)
