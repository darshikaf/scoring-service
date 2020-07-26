FROM darshika/darkf-build-testing:latest

# Copy application source code
COPY . /app

WORKDIR /app

# Copy NGINX configuration and init scripts
# COPY files/post-install /

# Install Python pacakges
RUN pip install -r requirements.txt
RUN pip install dependency/regression_model-0.1.1-py3-none-any.whl

# Expose HTTPS
# EXPOSE 443

# ENTRYPOINT ["tini", "--"]
# CMD ["/init"]

ENTRYPOINT [ "python" ]
CMD ["app.py"]