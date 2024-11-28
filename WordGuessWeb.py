from flask import Flask, render_template, request, redirect, url_for, session
import random
import text

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 用于安全的 session 数据存储

# 假设 text.word_list 在外部模块中
# class texts:
#     word_list = text.word_list
    # word_list = ["hello world", "python flask", "guess the word"]

@app.route("/", methods=["GET", "POST"])
def index():
    # 加载数据
    sheet_url = "https://docs.google.com/spreadsheets/d/1fGC_FzOsUHDt9NsO1LKsIMmcpLq6hZEtohgnBl2kZto/edit"
    word_image_dict = text.get_google_sheet_as_dict(sheet_url)

    # 初始化游戏
    if "chosen_word" not in session or "word_empty" not in session:
        chosen_word = random.choice(list(word_image_dict.keys()))
        session["chosen_word"] = chosen_word
        session["chosen_image"] = word_image_dict[chosen_word]  # 配图 URL
        session["word_empty"] = ["_" if char != " " else "&nbsp;&nbsp;" for char in chosen_word]
        session["attempts_left"] = 50
        session["game_over"] = False
        session["success"] = False
        session["guessed_letters"] = []  # 初始化猜过的字母

    # 如果已经存在 session，则确保 guessed_letters 已初始化
    if "guessed_letters" not in session:
        session["guessed_letters"] = []  # 确保 guessed_letters 存在

    if request.method == "POST" and not session["game_over"]:
        guess_letter = request.form.get("guess", "").lower()

        # 如果猜过的字母未记录，则添加到 guessed_letters
        if guess_letter and guess_letter not in session["guessed_letters"]:
            session["guessed_letters"].append(guess_letter)

        # 更新游戏状态
        chosen_word = session["chosen_word"]
        word_empty = session["word_empty"]

        for i, char in enumerate(chosen_word):
            if char.lower() == guess_letter:
                word_empty[i] = char

        session["word_empty"] = word_empty
        session["attempts_left"] -= 1

        # 检查游戏状态
        if "_" not in word_empty:
            session["game_over"] = True
            session["success"] = True
            session["message"] = f'You win! The words are "{chosen_word}". Congratulations!'
        elif session["attempts_left"] <= 0:
            session["game_over"] = True
            session["success"] = False
            session["message"] = f"You're out of chances. The words are '{chosen_word}'."

    return render_template(
        "index.html",
        word_empty=" ".join(session["word_empty"]),
        guessed_letters=", ".join(session["guessed_letters"]),  # 传递已猜字母列表
        attempts_left=session["attempts_left"],
        game_over=session.get("game_over", False),
        success=session.get("success", False),
        chosen_image=session.get("chosen_image", ""),
        message=session.get("message", ""),
    )

@app.route("/restart")
def restart():
    session.clear()  # 清除所有 session 数据
    return redirect(url_for("index"))

if __name__ == "__main__":
    # app.run()
    app.run(debug=True)