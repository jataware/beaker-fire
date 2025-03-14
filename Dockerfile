FROM python:3.10
RUN useradd -m jupyter
RUN useradd -m user
EXPOSE 8888

RUN apt update && apt install -y lsof

# Install Python requirements
RUN pip install --upgrade --no-cache-dir hatch pip

# RUN apt add-repository ppa:ubuntugis/ppa
RUN apt-get update &&\
    apt-get install -y build-essential gcc g++ gdal-bin libgdal-dev python3-all-dev libspatialindex-dev \
            graphviz libgraphviz-dev

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Install project requirements
COPY archytas-1.3.14b1-py3-none-any.whl	beaker_kernel-1.9.2b1-py3-none-any.whl /beaker-fire/
RUN pip install /beaker-fire/archytas-1.3.14b1-py3-none-any.whl /beaker-fire/beaker_kernel-1.9.2b1-py3-none-any.whl

# Copy src code over
COPY . /beaker-fire/
RUN pip install --no-build-isolation --no-cache-dir /beaker-fire

RUN mkdir -m 755 /var/run/beaker
RUN mkdir -m 777 /var/run/beaker/checkpoints

# Set default server env variables
ENV BEAKER_AGENT_USER=jupyter
ENV BEAKER_SUBKERNEL_USER=user
ENV BEAKER_RUN_PATH=/var/run/beaker
ENV BEAKER_APP=beaker_fire.app.BeakerFireApp

COPY --chown=user:user src/beaker_fire/data /home/user/data

# Beaker Server should run as root, but local notebooks should not as Beaker Server sets the UID of running kernels to
# an unprivileged user account when kernel processes are spawned
USER root

# Simple "notebook" service
CMD ["python3.10", "-m", "beaker_kernel.service.server"]
