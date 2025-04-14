from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = 'tasks.json'

# 初始化或加载任务数据
def load_tasks():
    if not os.path.exists(DATA_FILE):
        # 初始数据
        data = {
            "数学": [],
            "英语": [],
            "政治": [],
            "408": []
        }
        save_tasks(data)
        return data
    else:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {
                    "数学": [],
                    "英语": [],
                    "政治": [],
                    "408": []
                }

def save_tasks(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

tasks = load_tasks()

@app.route('/')
def index():
    # 默认跳转到“数学”科目，你也可以改成别的
    return redirect(url_for('show_subject', subject='数学'))

@app.route('/subject/<subject>')
def show_subject(subject):
    # 如果科目不存在，就先初始化空列表
    if subject not in tasks:
        tasks[subject] = []
        save_tasks(tasks)
    return render_template('subject.html', subject=subject, task_list=tasks[subject])

@app.route('/add_task/<subject>', methods=['POST'])
def add_task(subject):
    task_name = request.form.get('task_name')
    estimated_time = request.form.get('estimated_time')  # 获取预计用时
    if task_name:
        tasks[subject].append({
            "name": task_name,
            "completed": False,
            "estimated_time": estimated_time  # 保存预计用时
        })
        save_tasks(tasks)
    return redirect(url_for('show_subject', subject=subject))

@app.route('/toggle_task/<subject>/<int:task_index>', methods=['POST'])
def toggle_task(subject, task_index):
    if subject in tasks and 0 <= task_index < len(tasks[subject]):
        tasks[subject][task_index]['completed'] = not tasks[subject][task_index]['completed']
        save_tasks(tasks)
    return redirect(url_for('show_subject', subject=subject))

@app.route('/delete_task/<subject>/<int:task_index>', methods=['POST'])
def delete_task(subject, task_index):
    if subject in tasks and 0 <= task_index < len(tasks[subject]):
        tasks[subject].pop(task_index)
        save_tasks(tasks)
    return redirect(url_for('show_subject', subject=subject))

if __name__ == '__main__':
    app.run(debug=True)
