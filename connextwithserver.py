from flask import Flask,jsonify

app = Flask(__name__)
language = [{"name" : "maths" , "marks" : "100"},{"name" : "digital" , "marks" : "100"},{"name" : "maths" ,  "marks" : "10"},{"name" : "science", "marks" : "100"}]
@app.route('/' , methods=['GET'])
def home():
    return jsonify({"name" : "hitij"})
lang=[]
@app.route('/firstpage/<string:name>', methods=['GET'])
def page(name):
    lang = [node for node in language if node["name"] == "maths"]
    return jsonify({'data':lang})

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

if __name__ == "__main__":
 app.run(debug=True,port=4000)



