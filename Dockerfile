FROM python:3-onbuild
EXPOSE 80
CMD ["python", "./code/api.py"]