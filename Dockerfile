FROM python:3.9

WORKDIR /app

COPY . /app

# 指定容器启动时要执行的命令
CMD ["python", "your_app.py"]
