from flask import Flask, jsonify
from microservice_test import register_user_test, login_user_test, create_entry_test, get_suggestion_test

app = Flask(__name__)
print("Hello from the Testing Service.")
@app.route('/run-tests', methods=['GET'])
def run_tests():
    results = {}

    success, message = register_user_test("test_user", "test_password")
    results["register_user_test"] = message
    if not success:
        return jsonify(results), 601

    token, message = login_user_test("test_user", "test_password")
    results["login_user_test"] = message
    if token is None:
        return jsonify(results), 602

    success, message = create_entry_test(token, "Movie", "Inception", "Test Description")
    results["create_entry_test"] = message
    if not success:
        return jsonify(results), 603

    success, message = get_suggestion_test()
    results["get_suggestion_test"] = message
    if not success:
        return jsonify(results), 604

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True, port=5010)
