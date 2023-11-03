from flask import Flask, request, jsonify

from utils import ChatBotSummarizer

app = Flask(__name__)
app.config.from_object("config")

@app.route("/", methods=["POST"])
def home():
    article = request.form.get("article")

    if article == None or article == "":
        return jsonify({"error": "No article provided."}), 400
    
    try:
        summarizer = ChatBotSummarizer(
            openai_api_key         = app.config["OPENAI_API_KEY"], 
            openai_api_base        = app.config["OPENAI_API_BASE"], 
            openai_api_type        = app.config["OPENAI_API_TYPE"], 
            openai_api_version     = app.config["OPENAI_API_VERSION"], 
            openai_deployment_name = app.config["OPENAI_DEPLOYMENT_NAME"]
        )
        gpt_response, langchain_response = summarizer.chat_and_summarize(article)
        return jsonify({"gpt_response": gpt_response, "langchain_response": langchain_response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
