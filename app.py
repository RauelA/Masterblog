from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_posts():
    with open("posts.json", "r", encoding="utf-8") as file:
        return json.load(file)


def save_posts(posts):
    with open("posts.json", "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4)


def fetch_post_by_id(post_id):
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            return post
    return None

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_posts()

        new_id = max(post["id"] for post in posts) + 1 if posts else 1

        new_post = {
            "id": new_id,
            "author": request.form.get("author"),
            "title": request.form.get("title"),
            "content": request.form.get("content")
        }

        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_posts()

    posts = [post for post in posts if post["id"] != post_id]

    save_posts(posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_posts()

    post_to_update = None

    for post in posts:
        if post["id"] == post_id:
            post_to_update = post
            break

    if post_to_update is None:
        return "Post not found", 404

    if request.method == 'POST':
        for post in posts:
            if post["id"] == post_id:
                post["author"] = request.form.get("author")
                post["title"] = request.form.get("title")
                post["content"] = request.form.get("content")
                break

        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post_to_update)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)