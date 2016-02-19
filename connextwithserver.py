from flask import Flask,jsonify

app = Flask(__name__)
language = [{"name" : "english" , "marks" : "100"},{"name" : "digital" , "marks" : "100"},{"name" : "maths" ,  "marks" : "100"},{"name" : "science", "marks" : "100"}]
@app.route('/' , methods=['GET'])
def home():
    return jsonify({"name" : "kshitij"})

@app.route('/firstpage', methods=['GET'])
def page():
    lang = [node for node in language if node["name"] == "maths"]
    return jsonify( lang[0])

if __name__ == "__main__":
 app.run(debug=True)